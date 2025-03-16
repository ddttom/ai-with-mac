#!/usr/bin/env python3
"""
Batch processing with MLX language models.
"""
import argparse
import time
from mlx_lm import generate, load

def batch_process(model_path, prompts_file, output_file):
    """Process multiple prompts in a batch."""
    # Load prompts
    with open(prompts_file, 'r') as f:
        prompts = [line.strip() for line in f if line.strip()]
    
    print(f"Loaded {len(prompts)} prompts from {prompts_file}")
    
    # Load model
    print(f"Loading model from {model_path}, please wait...")
    model, tokenizer = load(model_path)
    print("Model loaded successfully!")
    
    # Process prompts
    start_time = time.time()
    results = []
    
    for i, prompt in enumerate(prompts):
        print(f"Processing prompt {i+1}/{len(prompts)}...")
        
        # Generation configuration
        gen_config = {
            "max_tokens": 300,
            "temperature": 0.5,
            "top_p": 0.9
        }
        
        # Generate
        tokens = tokenizer.encode(prompt)
        generated_tokens = generate(model, tokenizer, tokens, gen_config)
        response = tokenizer.decode(generated_tokens[len(tokens):])
        
        results.append(f"Prompt: {prompt}\nResponse: {response}\n\n")
    
    # Write results to file
    with open(output_file, 'w') as f:
        f.write("".join(results))
    
    elapsed_time = time.time() - start_time
    print(f"Processed {len(prompts)} prompts in {elapsed_time:.2f} seconds")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process multiple prompts in a batch using an MLX language model")
    parser.add_argument("--model", type=str, default="models/gemma-2b-it-4bit",
                        help="Path to the model directory")
    parser.add_argument("--prompts", type=str, required=True,
                        help="Path to a file containing prompts (one per line)")
    parser.add_argument("--output", type=str, default="batch_results.txt",
                        help="Path to save the results")
    args = parser.parse_args()
    
    batch_process(args.model, args.prompts, args.output)
