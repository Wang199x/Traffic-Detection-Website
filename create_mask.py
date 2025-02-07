import json
import numpy as np
import cv2
import os
from label_define import labels, create_label_to_color_map, create_label_to_id_map

# Path to data folder
cityscapes_path = "CityScape/gtFine"
output_path = "CityScape/masks"  # Save mask folder

os.makedirs(output_path, exist_ok=True)


# Read data from JSON
def read_json(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    return data


def create_output_folders(base_path, splits):
    for split in splits:
        split_path = os.path.join(base_path, split)
        os.makedirs(split_path, exist_ok=True)


# Transform polygon into masks with labelIds value
def polygons_to_labelIds_mask(image_shape, objects, label_to_id):
    mask = np.zeros(image_shape, dtype=np.uint8)
    for obj in objects:
        polygons = obj.get("polygon", [])
        label = obj.get("label", "unknown")
        label_id = label_to_id.get(label, 0)  # Get id for each label

        if len(polygons) > 0:
            # Change list points [[x, y], [x, y], ...] into numpy array
            points = np.array(polygons, dtype=np.int32)
            # Ensure the OpenCV form
            if points.shape[0] > 0:
                points = points.reshape((-1, 1, 2))
                cv2.fillPoly(mask, [points], color=label_id)
    return mask


# Transform polygon into color masks with fixed color
def polygons_to_color_mask(image_shape, objects, label_to_color):
    # Create mask with image size and 3 color channels
    mask = np.zeros((image_shape[0], image_shape[1], 3), dtype=np.uint8)

    for obj in objects:
        label = obj.get("label", "unknown")

        # Skip label "license plate"
        if label == "license plate":
            continue

        polygons = obj.get("polygon", [])
        color = label_to_color.get(label, (0, 0, 0))  # Get color for each label

        # Turn RGB into BGR for OpenCV
        color = (color[2], color[1], color[0])

        if len(polygons) > 0:
            points = np.array(polygons, dtype=np.int32)
            if points.shape[0] > 0:
                points = points.reshape((-1, 1, 2))  # Ensure the OpenCV form
                cv2.fillPoly(mask, [points], color=color)

    return mask


# Save masks into file
def save_mask(mask, output_path):
    if mask.size == 0:
        print(f"Empty mask can not be saved at {output_path}")
    else:
        cv2.imwrite(output_path, mask)  # Save grayscale images
        print(f"Saved mask {output_path}")


# Browse `train`, `val`, `test` and city folders
def process_data(splits, cityscapes_path, output_path):
    for split in splits:
        split_folder_path = os.path.join(cityscapes_path, split)
        split_output_path = os.path.join(output_path, split)
        create_output_folders(output_path, [split])  # Create split folder if not exist

        for city_folder in os.listdir(split_folder_path):
            city_folder_path = os.path.join(split_folder_path, city_folder)
            city_output_path = os.path.join(split_output_path, city_folder)
            create_output_folders(split_output_path, [city_folder])

            # Browse files in split and city folders
            for file_name in os.listdir(city_folder_path):
                if file_name.endswith("_gtFine_polygons.json"):
                    # Search JSON path
                    json_path = os.path.join(city_folder_path, file_name)
                    data = read_json(json_path)

                    # Read image size from JSON
                    image_height = data.get("imgHeight", 0)
                    image_width = data.get("imgWidth", 0)

                    if image_height == 0 or image_width == 0:
                        print(f"Invalid image size in JSON file: {json_path}")
                        continue

                    # Create mask from JSON
                    objects = data.get("objects", [])
                    label_to_id = create_label_to_id_map()
                    label_to_color = create_label_to_color_map()
                    mask = polygons_to_labelIds_mask(
                        (image_height, image_width), objects, label_to_id
                    )
                    color_mask = polygons_to_color_mask(
                        (image_height, image_width), objects, label_to_color
                    )

                    if np.all(mask == 0):
                        print(f"Empty mask is created from JSON file: {json_path}")
                    else:
                        print(
                            f"Mask has already been created from JSON file: {json_path}"
                        )

                    # Save masks into file
                    mask_file_name = file_name.replace(
                        "_gtFine_polygons.json", "_labelIds.png"
                    )
                    color_mask_file_name = file_name.replace(
                        "_gtFine_polygons.json", "_color.png"
                    )
                    mask_output_path = os.path.join(city_output_path, mask_file_name)
                    color_mask_output_path = os.path.join(
                        city_output_path, color_mask_file_name
                    )
                    save_mask(mask, mask_output_path)
                    save_mask(color_mask, color_mask_output_path)


splits = ["train", "val"]
process_data(splits, cityscapes_path, output_path)
