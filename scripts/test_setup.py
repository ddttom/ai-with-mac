#!/usr/bin/env python3
"""
A simple script to verify our AI development environment is working.

This script demonstrates proper docstring usage while checking that NumPy
and Matplotlib are correctly installed in our environment.
"""
import numpy as np
import matplotlib.pyplot as plt
import platform
import sys
import psutil

def main():
    """
    Main function to test the Python environment setup.
    
    This function checks system information, performs a simple NumPy operation,
    and creates a Matplotlib visualization to verify everything is working.
    
    Returns:
        None
    """
    print(f"Python version: {sys.version}")
    print(f"Running on: {platform.platform()}")
    
    # Check system resources
    memory = psutil.virtual_memory()
    print(f"System memory: {memory.total / (1024**3):.1f} GB total, {memory.available / (1024**3):.1f} GB available")
    cpu_count = psutil.cpu_count(logical=False)
    print(f"CPU cores: {cpu_count} physical cores")
    
    # Simple NumPy operation
    size = 5000  # Larger matrix for higher-end systems
    print(f"Creating {size}x{size} matrices (adjust size based on your system)...")
    array = np.random.rand(size, size)
    print(f"Matrix shape: {array.shape}, Memory usage: {array.nbytes / (1024**3):.2f} GB")
    print(f"NumPy array mean: {array.mean():.4f}")
    
    # Simple Matplotlib plot
    plt.figure(figsize=(10, 6))
    
    # Generate sample data appropriate for visualization
    sample_size = min(1000, size)
    sample = array[:sample_size, :sample_size].mean(axis=1)
    
    plt.hist(sample, bins=30, alpha=0.7)
    plt.title('Random Distribution')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    
    # Save the plot
    plt.savefig('test_plot.png')
    print("Plot saved as 'test_plot.png'")
    
    print("\nSetup verification complete. Your environment is ready for AI development!")

if __name__ == "__main__":
    main()
