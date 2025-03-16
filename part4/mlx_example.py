#!/usr/bin/env python3
"""
Simple MLX example to demonstrate syntax and performance.

This script compares the performance of matrix multiplication operations
between MLX and NumPy to showcase MLX's performance advantages on Apple Silicon.
"""
import time
import mlx.core as mx
import numpy as np

def main():
    """
    Run performance comparison between MLX and NumPy matrix multiplication.
    
    Creates large matrices and measures the time needed to perform
    matrix multiplication operations in both frameworks.
    """
    # Create random matrices
    size = 2000
    print(f"Creating {size}x{size} matrices...")
    
    # MLX implementation
    start_time = time.time()
    a = mx.random.normal((size, size))
    b = mx.random.normal((size, size))
    
    # Matrix multiplication in MLX
    print("Performing matrix multiplication with MLX...")
    c = mx.matmul(a, b)
    
    # Force computation (MLX is lazy by default)
    mx.eval(c)
    
    mlx_time = time.time() - start_time
    print(f"MLX time: {mlx_time:.4f} seconds")
    
    # NumPy implementation for comparison
    start_time = time.time()
    a_np = np.random.normal(0, 1, (size, size))
    b_np = np.random.normal(0, 1, (size, size))
    
    # Matrix multiplication in NumPy
    print("Performing matrix multiplication with NumPy...")
    c_np = np.matmul(a_np, b_np)
    
    numpy_time = time.time() - start_time
    print(f"NumPy time: {numpy_time:.4f} seconds")
    print(f"MLX speedup: {numpy_time / mlx_time:.2f}x")

if __name__ == "__main__":
    main()
