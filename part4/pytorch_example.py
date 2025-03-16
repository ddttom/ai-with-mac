#!/usr/bin/env python3
"""
Simple PyTorch example to demonstrate syntax and performance with Metal.

This script tests PyTorch performance with Apple's Metal backend for GPU acceleration,
comparing it with CPU-based computation using NumPy.
"""
import time
import torch
import numpy as np

def main():
    """
    Run performance comparison between PyTorch with Metal and NumPy.
    
    Checks for Metal (MPS) availability, creates large matrices and measures
    the time needed to perform matrix multiplication in both frameworks.
    """
    # Check if MPS (Metal) is available
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        print("Using MPS (Metal) device")
    else:
        device = torch.device("cpu")
        print("MPS not available, using CPU")
    
    # Create random matrices
    size = 2000
    print(f"Creating {size}x{size} matrices...")
    
    # PyTorch implementation
    start_time = time.time()
    a = torch.randn((size, size), device=device)
    b = torch.randn((size, size), device=device)
    
    # Matrix multiplication in PyTorch
    print("Performing matrix multiplication with PyTorch...")
    c = torch.matmul(a, b)
    
    # Force computation to complete
    torch.mps.synchronize()
    
    pytorch_time = time.time() - start_time
    print(f"PyTorch time: {pytorch_time:.4f} seconds")
    
    # NumPy implementation for comparison
    start_time = time.time()
    a_np = np.random.normal(0, 1, (size, size))
    b_np = np.random.normal(0, 1, (size, size))
    
    # Matrix multiplication in NumPy
    print("Performing matrix multiplication with NumPy...")
    c_np = np.matmul(a_np, b_np)
    
    numpy_time = time.time() - start_time
    print(f"NumPy time: {numpy_time:.4f} seconds")
    print(f"PyTorch speedup: {numpy_time / pytorch_time:.2f}x")

if __name__ == "__main__":
    main()
