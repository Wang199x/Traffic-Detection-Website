import os
import csv
import re
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    jsonify,
    session,
    url_for,
    send_from_directory,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from app.services import detect_objects, generate_csv

# Initialize Flask app
app = Flask(__name__)

# Configure PostgreSQL database
POSTGRES_URL = "postgresql://postgres:admin_198@localhost/traffic_db"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", POSTGRES_URL)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Configure session
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_SQLALCHEMY"] = db
app.config["SECRET_KEY"] = "supersecretkey"
migrate = Migrate(app, db)
session_db = Session(app)

# Directories for storing uploaded and processed images
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER


# User model
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)


@app.route("/api/check-session")
def check_session():
    username = session.get("user")
    if username:
        return jsonify({"logged_in": True, "username": username}), 200
    return jsonify({"logged_in": False}), 200


@app.route("/")
def home():
    username = session.get("user")
    return render_template("homepage.html", username=username)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        # Check username
        if len(username) < 6 or len(username) > 15:
            return (
                jsonify({"message": "Username must be between 6 and 15 characters"}),
                400,
            )

        # Check password
        if len(password) < 6 or len(password) > 15:
            return (
                jsonify({"message": "Password must be between 6 and 15 characters"}),
                400,
            )

        if not re.search(r"[A-Z]", password):
            return (
                jsonify(
                    {"message": "Password must contain at least one uppercase letter"}
                ),
                400,
            )
        if not re.search(r"[a-z]", password):
            return (
                jsonify(
                    {"message": "Password must contain at least one lowercase letter"}
                ),
                400,
            )
        if not re.search(r"\d", password):
            return (
                jsonify({"message": "Password must contain at least one number"}),
                400,
            )

        if User.query.filter_by(username=username).first():
            return jsonify({"message": "Username already exists"}), 400

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Signup successful", "redirect": "/login"}), 200

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({"message": "Invalid username or password"}), 401

        session["user"] = username
        return jsonify({"message": "Login successful", "redirect": "/"}), 200

    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


@app.route("/process", methods=["GET", "POST"])
def process():
    """Page to process the image and run YOLO"""
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        # Receive the image from frontend
        file = request.files.get("image")
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            # Define save_path to store processed image
            processed_filename = f"processed_{filename}"
            save_path = os.path.join(app.config["PROCESSED_FOLDER"], processed_filename)

            # Call detect_objects function and save the image
            processed_filename = detect_objects(file_path, save_path)

            # Create URL for processed image
            processed_image_url = f"/processed/{processed_filename}"

            return jsonify({"processed_image": processed_image_url})

    return render_template("process.html")


@app.route("/upload", methods=["POST"])
def upload_image():
    """Handle image upload"""
    if "user" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    if "image" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    return (
        jsonify(
            {
                "message": "File uploaded",
                "filename": filename,
                "file_url": f"/uploads/{filename}",
            }
        ),
        200,
    )


@app.route("/detect", methods=["POST"])
def detect():
    """Process object detection in the image and return processed image"""
    if "user" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()
    filename = data.get("filename")

    if not filename:
        return jsonify({"message": "Filename is required"}), 400

    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    processed_filename = f"processed_{filename}"
    save_path = os.path.join(app.config["PROCESSED_FOLDER"], processed_filename)

    # Call YOLO to process the image
    processed_filename = detect_objects(image_path, save_path)

    if processed_filename:
        return (
            jsonify(
                {
                    "message": "Detection completed",
                    "processed_image": f"/processed/{processed_filename}",
                }
            ),
            200,
        )
    else:
        return jsonify({"message": "File not found"}), 404


@app.route("/processed/<filename>")
def processed_file(filename):
    """Allow downloading the processed image"""
    return send_from_directory(app.config["PROCESSED_FOLDER"], filename)


@app.route("/download_detected_info", methods=["GET"])
def download_detected_info():
    """Generate CSV file containing information about detected objects"""
    filename = request.args.get("filename")
    if not filename:
        return jsonify({"message": "Filename is required"}), 400

    # Split the filename and extension
    base_filename, _ = os.path.splitext(filename)

    # Create CSV filename from image name
    csv_filename = f"{base_filename}.csv"
    csv_path = os.path.join(app.config["PROCESSED_FOLDER"], csv_filename)

    if not os.path.exists(csv_path):
        return jsonify({"message": "CSV file not found"}), 404

    return send_from_directory(app.config["PROCESSED_FOLDER"], csv_filename)


if __name__ == "__main__":
    app.run(debug=True)
