from ultralytics import YOLO


def train_yolov8():
    # Load the YOLOv8x model
    model = YOLO("yolov8x.pt")  # Replace with 'yolov8x.pt' for the Extra Large version

    # Set up training parameters
    model.train(
        data="./data.yaml",  # Path to the dataset YAML file
        epochs=100,  # Number of epochs
        imgsz=1024,  # Input image size
        batch=4,  # Batch size
        name="yolov8x_training",  # Training session name
        device="0",  # Training device (0 for the first GPU, 'cpu' for CPU)
        project="runs/train",  # Directory to store training results
        save_period=10,  # Checkpoint save interval (in epochs)
        save_dir="runs/train",  # Directory to save results
        cache=True,  # Use dataset caching
        multi_scale=True,  # Enable multi-scale training
        augment=True,  # Enable augmentations
        rect=True,  # Enable rectangular training for non-square images
        resume=False,  # Resume training from checkpoint (False to start fresh)
        verbose=True,  # Display detailed logs
        workers=8,  # Number of DataLoader workers
        iou=0.5,  # IoU threshold for defining positive samples
    )


if __name__ == "__main__":
    train_yolov8()
