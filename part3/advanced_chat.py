#!/usr/bin/env python3
"""
An advanced chat interface for MLX language models with parameter control.
"""
import os
import argparse
from mlx_lm import generate, load

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def chat_with_model(model_path, temperature=0.7, max_tokens=500, top_p=0.9):
    """Interactive chat with an MLX language model."""
    try:
        # Print header
        clear_screen()
        print("=" * 60)
        print("             Advanced MLX Chat Interface")
        print("=" * 60)
        print("Type 'exit' or 'quit' to end the conversation.")
        print("Type 'clear' to start a new conversation.")
        print("Type '/temp 0.5' to change temperature.")
        print("Type '/max 300' to change max tokens.")
        print("Type '/top_p 0.8' to change top_p.")
        print(f"Current settings: temp={temperature}, max_tokens={max_tokens}, top_p={top_p}")
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
                print("             Advanced MLX Chat Interface")
                print("=" * 60)
                print("Type 'exit' or 'quit' to end the conversation.")
                print("Type 'clear' to start a new conversation.")
                print("Type '/temp 0.5' to change temperature.")
                print("Type '/max 300' to change max tokens.")
                print("Type '/top_p 0.8' to change top_p.")
                print(f"Current settings: temp={temperature}, max_tokens={max_tokens}, top_p={top_p}")
                print("\nStarted a new conversation.")
                continue
            elif user_input.startswith('/temp '):
                try:
                    temperature = float(user_input.split(' ')[1])
                    print(f"Temperature set to {temperature}")
                    continue
                except:
                    print("Invalid temperature value. Please use a number between 0.0 and 1.0")
                    continue
            elif user_input.startswith('/max '):
                try:
                    max_tokens = int(user_input.split(' ')[1])
                    print(f"Max tokens set to {max_tokens}")
                    continue
                except:
                    print("Invalid max tokens value. Please use a positive integer.")
                    continue
            elif user_input.startswith('/top_p '):
                try:
                    top_p = float(user_input.split(' ')[1])
                    print(f"Top-p set to {top_p}")
                    continue
                except:
                    print("Invalid top_p value. Please use a number between 0.0 and 1.0")
                    continue
            
            # Update conversation with user input
            if conversation:
                conversation += f"\nHuman: {user_input}\nAssistant: "
            else:
                conversation = f"Human: {user_input}\nAssistant: "
            
            # Generate response
            print("\nAssistant: ", end="", flush=True)
            
            # Generation configuration with current parameters
            gen_config = {
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p
            }
            
            # Tokenize and generate
            tokens = tokenizer.encode(conversation)
            generated_tokens = generate(model, tokenizer, tokens, gen_config)
            response = tokenizer.decode(generated_tokens[len(tokens):])
            
            # Print the response
            print(response)
            
            # Update conversation with assistant's response
            conversation += response

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start an interactive chat with an MLX language model")
    parser.add_argument("--model", type=str, default="models/gemma-2b-it-4bit",
                        help="Path to the model directory")
    parser.add_argument("--temperature", type=float, default=0.7,
                        help="Initial temperature for generation")
    parser.add_argument("--max-tokens", type=int, default=500,
                        help="Initial maximum tokens to generate")
    parser.add_argument("--top-p", type=float, default=0.9,
                        help="Initial top-p value for nucleus sampling")
    args = parser.parse_args()
    chat_with_model(args.model, args.temperature, args.max_tokens, args.top_p)
