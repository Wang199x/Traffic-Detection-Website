import cv2
import numpy as np
import os
from label_define import labels


def process_image(mask_path, output_path):
    # Read mask
    mask = cv2.imread(mask_path)
    annotated_image = mask.copy()

    # Elimminate class if `ignoreInEval = True` or Train ID = -1
    valid_labels = [
        label for label in labels if not label.ignoreInEval and label.trainId != -1
    ]

    for label in valid_labels:
        # RGB to BGR
        bgr_color = (label.color[2], label.color[1], label.color[0])

        # Create mask for fixed color
        color_mask = cv2.inRange(mask, np.array(bgr_color), np.array(bgr_color))

        # Find contours in mask color
        contours, _ = cv2.findContours(
            color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:
            # Calculate bounding box for each contour
            x, y, w, h = cv2.boundingRect(contour)

            # Create bounding box
            cv2.rectangle(
                annotated_image,
                (x, y),
                (x + w, y + h),
                (label.color[0], label.color[1], label.color[2]),
                2,
            )

            # Label
            label_text = label.name
            cv2.putText(
                annotated_image,
                label_text,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 0),
                2,
            )

    # Save result
    cv2.imwrite(output_path, annotated_image)


def process_directory(input_dir, output_dir):
    # Create directory if not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Search through all input files
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith("_color.png"):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, relative_path)

                # Create output directory
                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)

                output_path = os.path.join(output_subdir, file)
                process_image(input_path, output_path)
                print(f"Processed {input_path} -> {output_path}")


input_dir = "./CityScape/masks"

output_dir = "./CityScape/masks_with_bbox"

process_directory(input_dir, output_dir)
