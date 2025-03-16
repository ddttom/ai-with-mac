#!/bin/bash
# Script to set up Git LFS for model versioning

# Check if Git LFS is installed
if ! command -v git-lfs &> /dev/null; then
    echo "Git LFS is not installed. Installing..."
    brew install git-lfs
fi

# Initialize Git LFS
git lfs install

# Track model files
git lfs track "*.bin"
git lfs track "*.gguf"
git lfs track "*.pt"
git lfs track "*.pth"
git lfs track "*.onnx"
git lfs track "*.mlpackage"
git lfs track "models/**/*"

# Add .gitattributes
git add .gitattributes
git commit -m "Initialize Git LFS for model versioning"

# Create directory structure
mkdir -p models/checkpoints datasets/processed datasets/raw
