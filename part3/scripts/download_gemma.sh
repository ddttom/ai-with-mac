#!/bin/bash
# Create a models directory if it doesn't exist
mkdir -p models

# Download the model
python -m mlx_lm.convert --hf-path google/gemma-2b-it -q --out-path models/gemma-2b-it-4bit
