#!/usr/bin/env python3
"""
Example script to demonstrate working with requirements.txt.

This script checks for required packages and generates a simple
requirements.txt file based on currently installed packages.
"""
import sys
import subprocess
import os
import importlib.util
from datetime import datetime

def check_package_installed(package_name):
    """
    Check if a package is installed in the current environment.
    
    Args:
        package_name (str): Name of the package to check
        
    Returns:
        bool: True if installed, False otherwise
    """
    return importlib.util.find_spec(package_name) is not None

def generate_requirements_file(filename="requirements.txt", include_versions=True):
    """
    Generate a requirements.txt file from installed packages.
    
    Args:
        filename (str): Output filename
        include_versions (bool): Whether to include version numbers
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Use pip freeze to get installed packages with versions
        if include_versions:
            cmd = [sys.executable, '-m', 'pip', 'freeze']
        else:
            # Get package names without versions
            cmd = [sys.executable, '-m', 'pip', 'list', '--format=freeze']
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # For the no-versions case, strip version info
        if not include_versions:
            packages = []
            for line in result.stdout.strip().split('\n'):
                if '==' in line:
                    package_name = line.split('==')[0]
                    packages.append(package_name)
            package_list = '\n'.join(packages)
        else:
            package_list = result.stdout.strip()
        
        # Add header comment with timestamp
        header = f"# Requirements generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += "# For AI with Mac project\n\n"
        
        # Write to file
        with open(filename, 'w') as f:
            f.write(header + package_list)
        
        return True
    except Exception as e:
        print(f"Error generating requirements file: {e}")
        return False

def check_essential_packages():
    """
    Check if essential packages for ML development are installed.
    
    Returns:
        dict: Dictionary with package name as key and installed status as value
    """
    essential_packages = [
        "numpy",
        "pandas",
        "matplotlib",
        "scipy",
        "scikit-learn",
        "torch",
        "mlx",  # Apple's ML framework
        "jupyter",
        "requests",
        "tqdm"
    ]
    
    status = {}
    for package in essential_packages:
        status[package] = check_package_installed(package)
    
    return status

def main():
    """Main function to demonstrate requirements management."""
    print("=" * 60)
    print("Requirements Management Demo")
    print("=" * 60)
    
    # Check for essential packages
    print("Checking for essential ML packages:")
    package_status = check_essential_packages()
    
    installed = []
    missing = []
    
    for package, is_installed in package_status.items():
        status = "✅ Installed" if is_installed else "❌ Missing"
        print(f"  {package}: {status}")
        
        if is_installed:
            installed.append(package)
        else:
            missing.append(package)
    
    print(f"\nInstalled: {len(installed)}/{len(package_status)} essential packages")
    
    # Give instructions for missing packages
    if missing:
        print("\nTo install missing packages, run:")
        print(f"pip install {' '.join(missing)}")
    
    # Generate requirements.txt
    print("\nGenerating requirements.txt file...")
    success = generate_requirements_file()
    
    if success:
        print("✅ Requirements file created successfully!")
        
        # Show content preview
        with open("requirements.txt", 'r') as f:
            content = f.readlines()
        
        print("\nPreview of requirements.txt:")
        for line in content[:10]:
            print(f"  {line.strip()}")
        
        if len(content) > 10:
            print(f"  ...and {len(content) - 10} more lines")
    else:
        print("❌ Failed to create requirements.txt")
    
    print("\nTip: Share requirements.txt with collaborators to ensure")
    print("everyone has the same environment setup!")
    print("=" * 60)

if __name__ == "__main__":
    main()
