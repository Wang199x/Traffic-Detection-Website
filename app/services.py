import os
import time
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2
import csv


def detect_objects(image_path, save_path):
    model = YOLO("model/best.pt")

    # Start measuring time
    start_time = time.time()

    # Run YOLO model
    results = model(image_path)

    # Calculate time taken
    end_time = time.time()
    total_time = end_time - start_time

    image = Image.open(image_path)
    image_np = np.array(image)
    detected_objects = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy.tolist()[0]
            confidence = box.conf.tolist()[0]
            class_id = int(box.cls.tolist()[0])
            class_name = result.names[class_id]

            # Draw rectangle around detected object
            cv2.rectangle(
                image_np, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2
            )
            label = f"{class_name} {confidence:.2f}"
            cv2.putText(
                image_np,
                label,
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 0, 0),
                2,
            )

            # Save object information into list
            detected_objects.append([class_name, confidence])

    # Save processed image to "processed" folder
    cv2.imwrite(save_path, image_np)

    # Call generate_csv function to create the CSV file
    generate_csv(detected_objects, save_path, image, total_time)

    return os.path.basename(save_path)  # Return only the filename, not the full path


def generate_csv(detected_objects, image_save_path, image, total_time):
    """Function to create CSV file containing information about detected objects"""
    # Get the filename of the processed image (without directory)
    filename = os.path.basename(image_save_path)
    csv_filename = f"{os.path.splitext(filename)[0]}.csv"
    csv_path = os.path.join(os.path.dirname(image_save_path), csv_filename)

    # Get image size
    image_size = image.size  # image.size returns a tuple (width, height)

    # Create and write data to CSV file
    with open(csv_path, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Write image size info
        writer.writerow([f"Image Size: {image_size[0]} x {image_size[1]}"])

        # Write processing time info
        writer.writerow([f"Processing time: {total_time*1000:.1f}ms"])

        # Header for object data
        writer.writerow(["Object #", "Class Name", "Confidence"])  # Header

        # Write detected object data
        for idx, obj in enumerate(detected_objects, start=1):
            writer.writerow([idx, obj[0], obj[1]])

    return csv_path
