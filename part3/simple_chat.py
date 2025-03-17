#!/usr/bin/env python3
"""
A simple chat interface for MLX language models.
"""
import os
import argparse
from mlx_lm import generate, load

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def chat_with_model(model_path):
    """Interactive chat with an MLX language model."""
    try:
        # Print header
        clear_screen()
        print("=" * 60)
        print("                 MLX Chat Interface")
        print("=" * 60)
        print("Type 'exit' or 'quit' to end the conversation.")
        print("Type 'clear' to start a new conversation.")
        print()
        
        # Load the model
        print(f"Loading model from {model_path}, please wait...")
        model, tokenizer = load(model_path)
        print("Model loaded successfully!")
        
        # Set up system message for instruction-tuned models
        system_message = "You are a helpful, accurate, and friendly assistant."
        conversation = system_message
        
        while True:
            # Get user input
            try:
                user_input = input("\nYou: ")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
                
            # Handle special commands
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            elif user_input.lower() == 'clear':
                conversation = system_message
                clear_screen()
                print("=" * 60)
                print("                 MLX Chat Interface")
                print("=" * 60)
                print("Type 'exit' or 'quit' to end the conversation.")
                print("Type 'clear' to start a new conversation.")
                print("\nStarted a new conversation.")
                continue
            
            # Update conversation with user input
            if conversation:
                conversation += f"\nHuman: {user_input}\nAssistant: "
            else:
                conversation = f"Human: {user_input}\nAssistant: "
            
            # Generate response
            print("\nA: ", end="", flush=True)
            
            # Generation configuration
            gen_config = {
                "max_tokens": 500,
                "temperature": 0.7,
                "top_p": 0.9
            }
            
            try:
                # Tokenize and generate
                tokens = tokenizer.encode(conversation)
                
                # Ensure tokens is a list/array, not a string
                if isinstance(tokens, str):
                    raise TypeError("Tokenizer returned a string instead of token IDs")
                
                # Generate response tokens
                generated = generate(model, tokenizer, tokens, gen_config)
                
                # Extract and decode the new tokens
                response = tokenizer.decode(generated[len(tokens):])
                
                # Print the response
                print(response)
                
                # Update conversation with assistant's response
                conversation += response
                
            except Exception as e:
                # print(f"\nError during generation: {e}")
                # print("=" * 60)
                # print("Detailed error information:")
                # import traceback
                # traceback.print_exc()
                # print("=" * 60)
                # print("Continuing with a new conversation...")
                conversation = system_message
                continue

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start an interactive chat with an MLX language model")
    parser.add_argument("--model", type=str, default="models/gemma-2b-it-4bit",
                        help="Path to the model directory")
    args = parser.parse_args()
    chat_with_model(args.model)
