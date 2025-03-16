#!/bin/bash
# Download Phi-3 Mini
python -m mlx_lm.convert --hf-path microsoft/Phi-3-mini-4k-instruct -q --out-path models/phi-3-mini-4bit
