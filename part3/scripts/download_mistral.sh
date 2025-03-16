#!/bin/bash
# Download Mistral 7B Instruct
python -m mlx_lm.convert --hf-path mistralai/Mistral-7B-Instruct-v0.2 -q --out-path models/mistral-7b-instruct-4bit
