import torch

# Check PyTorch version
print("PyTorch version:", torch.__version__)

# Check the CUDA version PyTorch is compiled with
print("CUDA version PyTorch is compiled with:", torch.version.cuda)

# Check CUDA availability
print("CUDA available:", torch.cuda.is_available())

# Check the number of available GPUs
print("Number of GPUs available:", torch.cuda.device_count())
