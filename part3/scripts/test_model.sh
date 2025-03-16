#!/bin/bash
python -m mlx_lm.generate \
    --model models/gemma-2b-it-4bit \
    --prompt "Explain quantum computing in simple terms" \
    --max-tokens 500
