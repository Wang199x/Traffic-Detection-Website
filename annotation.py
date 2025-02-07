import cv2
import numpy as np
import os
import torch
from label_define import labels
from torchvision.ops import nms


def create_yolo_annotation(x_center, y_center, width, height, label_id):
    return f"{label_id} {x_center} {y_center} {width} {height}"


def process_image_to_yolo(
    mask_path, annotation_path, label_to_id_map, nms_iou_threshold
):
    mask = cv2.imread(mask_path)
    image_height, image_width, _ = mask.shape
    annotations = []

    valid_labels = [label for label in labels if not label.ignoreInEval]

    for label in valid_labels:
        bgr_color = (label.color[2], label.color[1], label.color[0])
        color_mask = cv2.inRange(mask, np.array(bgr_color), np.array(bgr_color))
        contours, _ = cv2.findContours(
            color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        all_boxes = []
        all_scores = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            x_center = (x + w / 2) / image_width
            y_center = (y + h / 2) / image_height
            # norm_width = w / image_width
            # norm_height = h / image_height

            # Add box to the list
            all_boxes.append(
                [
                    x / image_width,
                    y / image_height,
                    (x + w) / image_width,
                    (y + h) / image_height,
                ]
            )
            all_scores.append(1.0)  # Assume score

        # Transform box into numpy array
        if len(all_boxes) > 0:
            boxes = np.array(all_boxes)
            scores = np.array(all_scores)
            boxes = torch.tensor(boxes, dtype=torch.float32)
            scores = torch.tensor(scores, dtype=torch.float32)

            # NMS for boxes with the same labels
            keep = nms(boxes, scores, nms_iou_threshold)
            keep = keep.numpy()

            # Creat and save annotations after NMS
            for idx in keep:
                x1, y1, x2, y2 = boxes[idx]
                x_center = (x1 + x2) / 2
                y_center = (y1 + y2) / 2
                width = x2 - x1
                height = y2 - y1
                annotation = create_yolo_annotation(
                    x_center, y_center, width, height, label_to_id_map[label.name]
                )
                annotations.append(annotation)

    # Save annotations
    with open(annotation_path, "w") as f:
        f.write("\n".join(annotations))


def process_directory_to_yolo(
    input_dir, output_dir, label_to_id_map, nms_iou_threshold
):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith("_color.png"):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, relative_path)

                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)

                annotation_path = os.path.join(
                    output_subdir, file.replace("_color.png", ".txt")
                )
                process_image_to_yolo(
                    input_path, annotation_path, label_to_id_map, nms_iou_threshold
                )
                print(f"Processed {input_path} -> {annotation_path}")


# Label ID
label_to_id_map = {
    label.name: label.trainId for label in labels if not label.ignoreInEval
}

# IoU threshold for NMS (can be changed)
nms_iou_threshold = 0.6

# Prepare annotations for all images data
input_dir = "./CityScape/masks"
output_dir = "./CityScape/annotations"
process_directory_to_yolo(input_dir, output_dir, label_to_id_map, nms_iou_threshold)
