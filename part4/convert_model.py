#!/usr/bin/env python3
"""
Convert a PyTorch model to MLX.

This script demonstrates how to convert a simple PyTorch model
to MLX format for optimized inference on Apple Silicon.
"""
import torch
import mlx.core as mx
import mlx.nn as nn
import numpy as np

# Define a simple PyTorch model
class SimplePyTorchModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = torch.nn.Linear(784, 128)
        self.linear2 = torch.nn.Linear(128, 10)
        
    def forward(self, x):
        x = torch.relu(self.linear1(x))
        x = self.linear2(x)
        return x

# Define the same model architecture in MLX
class SimpleMLXModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = nn.Linear(784, 128)
        self.linear2 = nn.Linear(128, 10)
        
    def __call__(self, x):
        x = nn.relu(self.linear1(x))
        x = self.linear2(x)
        return x

def convert_pytorch_to_mlx():
    """Convert PyTorch model weights to MLX."""
    # Create and initialize the PyTorch model
    pytorch_model = SimplePyTorchModel()
    
    # Create the MLX model
    mlx_model = SimpleMLXModel()
    
    # Convert weights from PyTorch to MLX
    mlx_params = {}
    for name, param in pytorch_model.named_parameters():
        # Convert to numpy, then to MLX array
        mlx_params[name.replace('.', '_')] = mx.array(param.detach().numpy())
    
    # Set the MLX model parameters
    mlx_model.update(mlx_params)
    
    return mlx_model

def test_models():
    """Test and compare both models."""
    # Convert model
    mlx_model = convert_pytorch_to_mlx()
    
    # Create test input
    test_input_np = np.random.randn(1, 784).astype(np.float32)
    
    # PyTorch forward pass
    pytorch_model = SimplePyTorchModel()
    pytorch_input = torch.tensor(test_input_np)
    with torch.no_grad():
        pytorch_output = pytorch_model(pytorch_input).numpy()
    
    # MLX forward pass
    mlx_input = mx.array(test_input_np)
    mlx_output = mlx_model(mlx_input)
    
    # Convert MLX output to numpy for comparison
    mlx_output_np = mlx_output.tolist()
    
    # Compare outputs
    print("PyTorch output shape:", pytorch_output.shape)
    print("MLX output shape:", mlx_output.shape)
    
    # Calculate maximum absolute difference
    max_diff = np.max(np.abs(pytorch_output - np.array(mlx_output_np)))
    print(f"Maximum absolute difference: {max_diff:.6f}")
    
    print("Conversion successful!" if max_diff < 1e-5 else "Conversion results differ significantly")

if __name__ == "__main__":
    convert_pytorch_to_mlx()
    test_models()
