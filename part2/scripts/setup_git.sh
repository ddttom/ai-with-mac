#!/bin/bash
# Install Git
brew install git

# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Initialize Git repository
cd ai-with-mac
git init

# Create a .gitignore file for Python projects
curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore

# Add specifics for our AI project
echo "ai-env/" >> .gitignore
echo "*.gguf" >> .gitignore
echo "models/" >> .gitignore
