# Move images from subdirectories to train/images folder
$sourceDir = "D:\Segmentation_City\CityScape\datasets\images\train"
$destDir = "D:\Segmentation_City\CityScape\datasets\train\images"

# Create the destination directory if it does not exist
if (-not (Test-Path $destDir)) {
    New-Item -ItemType Directory -Path $destDir
}

# Move images
Get-ChildItem -Path $sourceDir -Recurse -Include *.jpg, *.png | Move-Item -Destination $destDir

# Move corresponding labels
$sourceLabelsDir = "D:\Segmentation_City\CityScape\datasets\labels\train"
$destLabelsDir = "D:\Segmentation_City\CityScape\datasets\train\labels"

# Create the destination directory if it does not exist
if (-not (Test-Path $destLabelsDir)) {
    New-Item -ItemType Directory -Path $destLabelsDir
}

# Move label files
Get-ChildItem -Path $sourceLabelsDir -Recurse -Include *.txt | Move-Item -Destination $destLabelsDir

# Repeat for the validation folder
$sourceDirVal = "D:\Segmentation_City\CityScape\datasets\images\val"
$destDirVal = "D:\Segmentation_City\CityScape\datasets\val\images"

if (-not (Test-Path $destDirVal)) {
    New-Item -ItemType Directory -Path $destDirVal
}

Get-ChildItem -Path $sourceDirVal -Recurse -Include *.jpg, *.png | Move-Item -Destination $destDirVal

$sourceLabelsDirVal = "D:\Segmentation_City\CityScape\datasets\labels\val"
$destLabelsDirVal = "D:\Segmentation_City\CityScape\datasets\val\labels"

if (-not (Test-Path $destLabelsDirVal)) {
    New-Item -ItemType Directory -Path $destLabelsDirVal
}

Get-ChildItem -Path $sourceLabelsDirVal -Recurse -Include *.txt | Move-Item -Destination $destLabelsDirVal
