#!/bin/bash
# Install Git LFS
brew install git-lfs

# Initialize Git LFS
git lfs install

# Track specific file patterns
git lfs track "*.gguf"
git lfs track "*.bin"
git lfs track "models/**/*.pth"

# Make sure .gitattributes is tracked
git add .gitattributes

# Now commit and push as usual
git add models/my-large-model.gguf
git commit -m "Add model file using LFS"
git push
