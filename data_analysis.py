import os
from collections import defaultdict

# Count the number of images in train, val, and test sets
def count_image_files(image_path):
    files_count = 0
    for root, dirs, files in os.walk(image_path):
        for file in files:
            if file.endswith((".png", ".jpeg", ".jpg", ".gif", ".tiff", ".bmp")):
                files_count += 1
    return files_count

train_image_path = "D:/Segmentation_City/CityScape/leftImg8bit/train" 
train_files_count = count_image_files(train_image_path)
print(f"Number of train images: {train_files_count}")
print("===========================================")

val_image_path = "D:/Segmentation_City/CityScape/leftImg8bit/val" 
val_files_count = count_image_files(val_image_path)
print(f"Number of validation images: {val_files_count}")
print("===========================================")

test_image_path = "D:/Segmentation_City/CityScape/leftImg8bit/test" 
test_files_count = count_image_files(test_image_path)
print(f"Number of test images: {test_files_count}")
print("===========================================")

#===================================================

annotations_train = "D:/Segmentation_City/CityScape/annotations/train"
annotations_val = "D:/Segmentation_City/CityScape/annotations/val"

# Dictionary to store the total number of objects for each class
class_object_count = defaultdict(int)

# Iterate through all annotation files in the directory
def class_count(annotations_dir):
    for root, _, files in os.walk(annotations_dir):
        for file in files:
            if file.endswith(".txt"):  # Process only annotation files
                file_path = os.path.join(root, file)
                
                # Read the annotation file
                with open(file_path, "r") as f:
                    lines = f.readlines()
                
                # Iterate through each line, where each line represents an object
                for line in lines:
                    label_id = int(line.split()[0])  # Extract class ID of the object
                    class_object_count[label_id] += 1  # Increment the count
    return class_object_count

# Print the statistics
train_class_object_count = class_count(annotations_train)
train_sorted_class_ids = sorted(train_class_object_count.keys())
print("Number of train objects for each class")
for class_id in train_sorted_class_ids:
    print(f"Class {class_id}: {train_class_object_count[class_id]} objects")

print("===========================================") 

val_class_object_count = class_count(annotations_val)  
val_sorted_class_ids = sorted(val_class_object_count.keys())
print("Number of validation objects for each class")
for class_id in val_sorted_class_ids:
    print(f"Class {class_id}: {val_class_object_count[class_id]} objects")
