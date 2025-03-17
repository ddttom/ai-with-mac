#!/usr/bin/env python3
"""
Download and setup AI models based on your system's capabilities.
"""
import os
import argparse
import sys
import subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Download AI models for local use")
    parser.add_argument("--model", type=str, choices=[
        "gemma-2b-it-4bit",
        "gemma-7b-it-4bit",
        "gemma-7b-it-8bit", 
        "mistral-7b-instruct-4bit",
        "mistral-7b-instruct-8bit",
        "phi-3-mini-4bit",
        "llama-3-8b-instruct-4bit",
        "llama-3-8b-instruct-8bit",
        "llama-3-70b-instruct-4bit"
    ], default="gemma-2b-it-4bit", help="Model to download")
    
    args = parser.parse_args()
    
    print(f"Setting up model: {args.model}")
    
    # Create models directory if it doesn't exist
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Ensure user is logged in to Hugging Face
    print("Most models require Hugging Face authentication.")
    print("You'll need to accept the model license terms on the Hugging Face website.")
    login_huggingface()
    
    # Determine model settings
    if args.model == "gemma-2b-it-4bit":
        hf_path = "google/gemma-2b-it"
        quant = 4
    elif args.model == "gemma-7b-it-4bit":
        hf_path = "google/gemma-7b-it"
        quant = 4
    elif args.model == "gemma-7b-it-8bit":
        hf_path = "google/gemma-7b-it"
        quant = 8
    elif args.model == "mistral-7b-instruct-4bit":
        hf_path = "mistralai/Mistral-7B-Instruct-v0.2"
        quant = 4
    elif args.model == "mistral-7b-instruct-8bit":
        hf_path = "mistralai/Mistral-7B-Instruct-v0.2"
        quant = 8
    elif args.model == "phi-3-mini-4bit":
        hf_path = "microsoft/Phi-3-mini-4k-instruct"
        quant = 4
    elif args.model == "llama-3-8b-instruct-4bit":
        hf_path = "meta-llama/Meta-Llama-3-8B-Instruct"
        quant = 4
    elif args.model == "llama-3-8b-instruct-8bit":
        hf_path = "meta-llama/Meta-Llama-3-8B-Instruct"
        quant = 8
    elif args.model == "llama-3-70b-instruct-4bit":
        hf_path = "meta-llama/Meta-Llama-3-70B-Instruct"
        quant = 4
    else:
        print(f"Unknown model: {args.model}")
        return
    
    # Output path
    output_path = f"models/{args.model}"
    
    # Download and convert model
    print(f"Downloading {hf_path}...")
    print(f"This model will be saved to: {output_path}")
    print(f"Using {quant}-bit quantization")
    
    # Try the direct command line approach using the mlx_lm.convert module
    cmd = ["python", "-m", "mlx_lm.convert", "--hf-path", hf_path]
    
    # Add the output path parameter - try both naming conventions
    if quant == 4:
        cmd.append("-q")
    elif quant == 8:
        cmd.append("-q8")
        
    # Try the latest format (--mlx-path)
    out_cmd = cmd.copy()
    out_cmd.extend(["--mlx-path", output_path])
    
    print("Running command:", " ".join(out_cmd))
    result = subprocess.run(out_cmd)
    
    # If that fails, try the older format (--out-path)
    if result.returncode != 0:
        print("First attempt failed. Trying older command format...")
        out_cmd = cmd.copy()
        out_cmd.extend(["--out-path", output_path])
        print("Running command:", " ".join(out_cmd))
        result = subprocess.run(out_cmd)
    
    # If still not working, try using huggingface_hub directly
    if result.returncode != 0:
        print("Command line approaches failed. Trying direct download...")
        try:
            print("Installing huggingface_hub if needed...")
            subprocess.run(["pip", "install", "--upgrade", "huggingface_hub"])
            
            print(f"Downloading {hf_path} directly...")
            download_cmd = [
                "python", "-c", 
                f"from huggingface_hub import snapshot_download; "
                f"print('Downloaded to:', snapshot_download(repo_id='{hf_path}'))"
            ]
            subprocess.run(download_cmd)
            
            print("Model downloaded but needs conversion. Please check the documentation for your specific mlx_lm version.")
            print("You may need to run a command like:")
            print(f"python -m mlx_lm.convert --hf-path {hf_path} --mlx-path {output_path} -q")
            result.returncode = 1  # Still mark as failure since manual steps are needed
        except Exception as e:
            print(f"Error during direct download: {e}")
    
    if result.returncode == 0:
        print(f"Model downloaded and saved to {output_path}")
        print(f"You can now use this model with scripts from the repository!")
    else:
        print("Model download failed. Please check the error messages above.")
        print("\nTroubleshooting steps:")
        print("1. Make sure you've accepted the model license on the Hugging Face website:")
        print(f"   https://huggingface.co/{hf_path}")
        print("2. Try updating mlx and mlx-lm packages:")
        print("   pip install --upgrade mlx mlx-lm")

def login_huggingface():
    """Log in to Hugging Face if needed for restricted models."""
    try:
        # Check if already logged in
        import huggingface_hub
        try:
            if huggingface_hub.whoami():
                print("Already logged in to Hugging Face")
                return
        except:
            pass
    except:
        pass
        
    print("Logging in to Hugging Face...")
    print("If prompted, enter your Hugging Face credentials.")
    print("If you don't have an account, create one at https://huggingface.co/join")
    
    # Run the login command
    subprocess.run(["huggingface-cli", "login"])
    
    print("Please also make sure you've accepted the model license on the Hugging Face website.")

if __name__ == "__main__":
    main()