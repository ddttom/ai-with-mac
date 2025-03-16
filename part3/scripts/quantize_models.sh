#!/bin/bash
# 4-bit quantization (smallest, fastest)
python -m mlx_lm.convert --hf-path google/gemma-7b-it -q --out-path models/gemma-7b-it-4bit

# 8-bit quantization (better quality, larger size)
python -m mlx_lm.convert --hf-path google/gemma-7b-it -q8 --out-path models/gemma-7b-it-8bit
