from ultralytics import YOLO
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np


def detect_objects(image_path, model_path):
    # Load the trained model (best.pt)
    model = YOLO(model_path)

    # Perform detection on the image
    results = model.predict(
        source=image_path,  # Path to the test image or folder of images
        imgsz=1024,  # Input image size
        conf=0.25,  # Confidence threshold
        save=False,  # Set to False if you do not want to save images with detections
        device="0",  # Use GPU 0, change to 'cpu' if you want to use CPU
    )

    # Iterate through the results to show bounding boxes and labels
    for result in results:
        # Load the image using PIL and convert to numpy array
        image = Image.open(result.path).convert("RGB")
        image_np = np.array(image)

        # Create a plot
        fig, ax = plt.subplots(1, figsize=(12, 9))
        ax.imshow(image_np)

        # Draw bounding boxes and labels
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy.tolist()[0]  # Bounding box coordinates
            confidence = box.conf.tolist()[0]  # Confidence score
            class_id = int(box.cls.tolist()[0])  # Class index
            class_name = result.names[class_id]  # Class label

            # Create a rectangle patch
            rect = patches.Rectangle(
                (x1, y1), x2 - x1, y2 - y1, linewidth=2, edgecolor="r", facecolor="none"
            )
            ax.add_patch(rect)

            # Add label and confidence
            label = f"{class_name} {confidence:.2f}"
            ax.text(
                x1,
                y1,
                label,
                bbox=dict(facecolor="yellow", alpha=0.5),
                fontsize=10,
                color="black",
            )

        # Show the plot
        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    test_image_path = "./CityScape/leftImg8bit/test/bielefeld/bielefeld_000000_021221_leftImg8bit.png"  # Replace with your test image path or folder
    trained_model_path = (
        "runs/train/yolov8x_training/weights/best.pt"  # Replace with your model path
    )
    detect_objects(test_image_path, trained_model_path)
