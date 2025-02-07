import os


def rename_images(image_folder):
    """
    Rename image files in the folder to match the label files.
    """
    # Iterate through all files in the image folder
    for filename in os.listdir(image_folder):
        # Check if the file has the correct image format
        if filename.endswith("_leftImg8bit.png"):
            # Create a new filename by removing the "_leftImg8bit" suffix
            new_filename = filename.replace("_leftImg8bit", "")

            # Old and new file paths
            old_path = os.path.join(image_folder, filename)
            new_path = os.path.join(image_folder, new_filename)

            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")


if __name__ == "__main__":
    # Paths to the train and val image folders
    train_image_folder = "D:/Segmentation_City/CityScape/datasets/train/images"
    val_image_folder = "D:/Segmentation_City/CityScape/datasets/val/images"

    # Rename images in the train folder
    print("Renaming images in the train folder...")
    rename_images(train_image_folder)

    # Rename images in the val folder
    print("Renaming images in the val folder...")
    rename_images(val_image_folder)
