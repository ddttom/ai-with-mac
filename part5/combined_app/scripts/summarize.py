#!/usr/bin/env python3

"""
Text summarization using MLX.
"""

import os
import mlx.core as mx
from mlx_lm import generate, load

class Summarizer:
    """Text summarizer using MLX."""
    def __init__(self, model_path="models/gemma-2b-it-4bit"):
        """Initialize the summarizer."""
        # Ensure model directory exists
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Check if model exists, download if needed
        if not os.path.exists(model_path):
            print(f"Model not found at {model_path}. Please download it first using:")
            print(f"python -m mlx_lm.convert --hf-path google/gemma-2b-it -q --out-path {model_path}")
            return
        
        print(f"Loading summarization model from {model_path}...")
        self.model, self.tokenizer = load(model_path)
        print("Summarization model loaded successfully!")
    
    def summarize(self, text, max_length=200, temperature=0.3):
        """Summarize the given text."""
        prompt = f"""Please summarize the following text concisely:

Text: {text}

Summary:"""
        
        # Generate summary
        gen_config = {
            "max_tokens": max_length,
            "temperature": temperature,
            "top_p": 0.9
        }
        
        tokens = self.tokenizer.encode(prompt)
        generated_tokens = generate(self.model, self.tokenizer, tokens, gen_config)
        summary = self.tokenizer.decode(generated_tokens[len(tokens):])
        
        return summary.strip()

# Example usage
if __name__ == "__main__":
    summarizer = Summarizer()
    
    # Example text
    text = """
    Apple Silicon has fundamentally changed what's possible for machine learning on
    consumer-grade hardware. With the M1, M2, M3, and now M4 chips, Mac users can run
    sophisticated AI models locally with impressive performance. This unified memory
    architecture eliminates the traditional bottleneck of data transfers between CPU and
    GPU memory, allowing both processors to access the same physical memory seamlessly.
    Whether you're a data scientist, AI researcher, app developer, or just an enthusiast
    exploring machine learning, understanding your options on Apple Silicon is crucial for
    maximizing performance and efficiency.
    """
    
    summary = summarizer.summarize(text)
    print("\nSummary:")
    print(summary)
