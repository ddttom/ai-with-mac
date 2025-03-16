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

# Create a README for the models directory
cat > models/README.md << 'README'
# Model Directory

This directory contains versioned ML models.

## Structure

- `checkpoints/`: Training checkpoints
- `production/`: Production-ready models
- `quantized/`: Quantized versions of models

## Versioning

Models are versioned using semantic versioning:

- Major version: Architectural changes
- Minor version: Training improvements
- Patch version: Bug fixes or small adjustments

Example: `chatbot-v1.2.3` represents:

- Version 1 architecture
- Training improvement iteration 2
- Bug fix or adjustment 3

## Usage

Each model directory contains:

- Model weights
- `config.json` with hyperparameters
- `metadata.json` with version info
- `metrics.json` with performance metrics
README

git add models/README.md
git commit -m "Add model directory structure and documentation"

echo "Git LFS setup complete for model versioning!"
