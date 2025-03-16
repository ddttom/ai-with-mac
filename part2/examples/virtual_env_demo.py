#!/usr/bin/env python3
"""
Demo script to show the benefit of virtual environments.

This script demonstrates how to detect and report information about the
current Python environment, helping users verify they're running in a
virtual environment.
"""
import sys
import os
import subprocess
import platform

def detect_virtualenv():
    """
    Detect if running inside a virtual environment.
    
    Returns:
        tuple: (is_in_venv, venv_name, venv_path)
    """
    # Check for virtual environment
    is_in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    # Get venv name (directory name of the virtual environment)
    venv_path = sys.prefix
    venv_name = os.path.basename(venv_path)
    
    return is_in_venv, venv_name, venv_path

def get_installed_packages():
    """
    Get a list of installed packages in the current environment.
    
    Returns:
        list: List of installed packages and their versions
    """
    try:
        # Use pip list to get installed packages
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'list'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip().split('\n')[2:]  # Skip header rows
    except subprocess.CalledProcessError:
        return ["Failed to retrieve package list"]

def main():
    """Display information about the current Python environment."""
    print("=" * 60)
    print("Python Environment Information")
    print("=" * 60)
    
    # Check Python version and platform
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    
    # Check virtual environment
    is_in_venv, venv_name, venv_path = detect_virtualenv()
    
    if is_in_venv:
        print(f"\n✅ Running in a virtual environment!")
        print(f"Virtual environment name: {venv_name}")
        print(f"Virtual environment path: {venv_path}")
    else:
        print("\n❌ Not running in a virtual environment!")
        print("It's recommended to use a virtual environment for ML projects.")
        print("Create one with: python -m venv ai-env")
        print("Activate with: source ai-env/bin/activate (Linux/Mac)")
        print("             : ai-env\\Scripts\\activate (Windows)")
    
    # Show Python executable path
    print(f"\nPython executable: {sys.executable}")
    
    # Show installed packages
    packages = get_installed_packages()
    print(f"\nInstalled packages ({len(packages)}):")
    for pkg in packages[:10]:  # Show first 10 packages
        print(f"  {pkg}")
    
    if len(packages) > 10:
        print(f"  ...and {len(packages) - 10} more")
    
    print("\nEnvironment Variables:")
    python_path = os.environ.get('PYTHONPATH', 'Not set')
    print(f"  PYTHONPATH: {python_path}")
    
    print("\nThis information can help you verify your environment setup is correct.")
    print("=" * 60)

if __name__ == "__main__":
    main()
