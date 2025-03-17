#!/usr/bin/env python3
"""
Mac Memory Check and Model Recommender

This script checks the available system memory on a Mac and recommends
appropriate ML models based on the detected RAM. It also provides
functionality to download recommended models.
"""

import os
import sys
import argparse
import subprocess
import platform
import psutil
from pathlib import Path
from typing import List, Tuple, Dict, Optional

# ANSI color codes for pretty terminal output
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
BLUE = '\033[0;34m'
MAGENTA = '\033[0;35m'
CYAN = '\033[0;36m'
BOLD = '\033[1m'
NC = '\033[0m'  # No Color

# Model configurations with HuggingFace paths and quantization settings
MODEL_CONFIGS = {
    "gemma-2b-it-4bit": {"hf_path": "google/gemma-2b-it", "quant": 4},
    "gemma-7b-it-4bit": {"hf_path": "google/gemma-7b-it", "quant": 4},
    "gemma-7b-it-8bit": {"hf_path": "google/gemma-7b-it", "quant": 8},
    "mistral-7b-instruct-4bit": {"hf_path": "mistralai/Mistral-7B-Instruct-v0.2", "quant": 4},
    "mistral-7b-instruct-8bit": {"hf_path": "mistralai/Mistral-7B-Instruct-v0.2", "quant": 8},
    "phi-3-mini-4bit": {"hf_path": "microsoft/Phi-3-mini-4k-instruct", "quant": 4},
    "llama-3-8b-instruct-4bit": {"hf_path": "meta-llama/Meta-Llama-3-8B-Instruct", "quant": 4},
    "llama-3-8b-instruct-8bit": {"hf_path": "meta-llama/Meta-Llama-3-8B-Instruct", "quant": 8},
    "llama-3-70b-instruct-4bit": {"hf_path": "meta-llama/Meta-Llama-3-70B-Instruct", "quant": 4}
}

def check_system() -> Tuple[bool, bool, int]:
    """
    Check if the system is a Mac with Apple Silicon and get RAM size.
    
    Returns:
        Tuple[bool, bool, int]: (is_mac, is_apple_silicon, ram_gb)
    """
    # Check if running on macOS
    is_mac = platform.system() == "Darwin"
    
    # Check if running on Apple Silicon
    is_apple_silicon = False
    if is_mac:
        machine = platform.machine()
        is_apple_silicon = machine == "arm64"
    
    # Get RAM size in GB
    ram_bytes = psutil.virtual_memory().total
    ram_gb = ram_bytes // (1024 ** 3)
    
    return is_mac, is_apple_silicon, ram_gb

def get_model_recommendations(ram_gb: int) -> Tuple[List[str], str, str]:
    """
    Get recommended models based on available RAM.
    
    Args:
        ram_gb: Available RAM in GB
        
    Returns:
        Tuple[List[str], str, str]: (recommended_models, max_model_size, message)
    """
    if ram_gb < 8:
        message = f"{YELLOW}{BOLD}Warning: Your system has less than 8GB of RAM.{NC}\n" \
                  f"{YELLOW}You may experience limited performance with AI models.{NC}"
        recommended_models = ["gemma-2b-it-4bit", "phi-3-mini-4bit"]
        max_model_size = "2B"
    elif ram_gb < 16:
        message = f"{BLUE}With 8GB RAM, you can run smaller models efficiently.{NC}"
        recommended_models = ["gemma-2b-it-4bit", "phi-3-mini-4bit"]
        max_model_size = "7B"
    elif ram_gb < 32:
        message = f"{BLUE}With 16GB RAM, you can comfortably run medium-sized models.{NC}"
        recommended_models = ["gemma-7b-it-4bit", "phi-3-mini-4bit"]
        max_model_size = "7-13B"
    elif ram_gb < 64:
        message = f"{BLUE}With 32GB RAM, you can run larger models or multiple smaller models.{NC}"
        recommended_models = ["gemma-7b-it-4bit", "llama-3-8b-instruct-4bit"]
        max_model_size = "13B"
    elif ram_gb < 128:
        message = f"{BLUE}With 64GB RAM, you can run larger models at higher precision.{NC}"
        recommended_models = ["gemma-7b-it-8bit", "llama-3-8b-instruct-8bit"]
        max_model_size = "13-30B"
    else:
        message = f"{GREEN}{BOLD}Excellent! With {ram_gb} GB RAM, you can run very large models.{NC}"
        recommended_models = ["gemma-7b-it-8bit", "llama-3-70b-instruct-4bit"]
        max_model_size = "70B+"
    
    return recommended_models, max_model_size, message

def login_huggingface() -> bool:
    """
    Log in to Hugging Face if needed for restricted models.
    
    Returns:
        bool: True if login successful or already logged in
    """
    try:
        # Check if already logged in
        try:
            import huggingface_hub
            try:
                if huggingface_hub.whoami():
                    print(f"{GREEN}Already logged in to Hugging Face{NC}")
                    return True
            except Exception:
                pass
        except ImportError:
            # Install huggingface_hub if not present
            print("Installing huggingface_hub...")
            subprocess.run([sys.executable, "-m", "pip", "install", "huggingface_hub"])
            import huggingface_hub
        
        print(f"{CYAN}Logging in to Hugging Face...{NC}")
        print("If prompted, enter your Hugging Face credentials.")
        print("If you don't have an account, create one at https://huggingface.co/join")
        
        # Run the login command
        result = subprocess.run(["huggingface-cli", "login"])
        
        if result.returncode == 0:
            print(f"{GREEN}Successfully logged in to Hugging Face{NC}")
            return True
        else:
            print(f"{YELLOW}Please also make sure you've accepted the model license on the Hugging Face website.{NC}")
            return False
    
    except Exception as e:
        print(f"{RED}Error during Hugging Face login: {e}{NC}")
        return False

def download_model(model_name: str) -> bool:
    """
    Download and convert an ML model.
    
    Args:
        model_name: Name of the model to download
        
    Returns:
        bool: True if download successful
    """
    if model_name not in MODEL_CONFIGS:
        print(f"{RED}Unknown model: {model_name}{NC}")
        return False
    
    # Create models directory if it doesn't exist
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Get model settings
    config = MODEL_CONFIGS[model_name]
    hf_path = config["hf_path"]
    quant = config["quant"]
    
    # Output path
    output_path = f"models/{model_name}"
    
    # Download and convert model
    print(f"{CYAN}Downloading {hf_path}...{NC}")
    print(f"This model will be saved to: {output_path}")
    print(f"Using {quant}-bit quantization")
    
    # Try the direct command line approach using the mlx_lm.convert module
    cmd = [sys.executable, "-m", "mlx_lm.convert", "--hf-path", hf_path]
    
    # Add the quantization parameter
    if quant == 4:
        cmd.append("-q")
    elif quant == 8:
        cmd.append("-q8")
    
    # Try the latest format (--mlx-path)
    out_cmd = cmd.copy()
    out_cmd.extend(["--mlx-path", output_path])
    
    print(f"{BLUE}Running command:{NC} {' '.join(out_cmd)}")
    result = subprocess.run(out_cmd)
    
    # If that fails, try the older format (--out-path)
    if result.returncode != 0:
        print(f"{YELLOW}First attempt failed. Trying older command format...{NC}")
        out_cmd = cmd.copy()
        out_cmd.extend(["--out-path", output_path])
        print(f"{BLUE}Running command:{NC} {' '.join(out_cmd)}")
        result = subprocess.run(out_cmd)
    
    # If still not working, try using huggingface_hub directly
    if result.returncode != 0:
        print(f"{YELLOW}Command line approaches failed. Trying direct download...{NC}")
        try:
            print("Installing huggingface_hub if needed...")
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "huggingface_hub"])
            
            print(f"Downloading {hf_path} directly...")
            download_cmd = [
                sys.executable, "-c", 
                f"from huggingface_hub import snapshot_download; "
                f"print('Downloaded to:', snapshot_download(repo_id='{hf_path}'))"
            ]
            subprocess.run(download_cmd)
            
            print(f"{YELLOW}Model downloaded but needs conversion. Please check the documentation for your specific mlx_lm version.{NC}")
            print("You may need to run a command like:")
            print(f"{BLUE}python -m mlx_lm.convert --hf-path {hf_path} --mlx-path {output_path} -q{NC}")
            return False
        except Exception as e:
            print(f"{RED}Error during direct download: {e}{NC}")
            return False
    
    if result.returncode == 0:
        print(f"{GREEN}Model downloaded and saved to {output_path}{NC}")
        print(f"{GREEN}You can now use this model with scripts from the repository!{NC}")
        return True
    else:
        print(f"{RED}Model download failed. Please check the error messages above.{NC}")
        print(f"\n{YELLOW}Troubleshooting steps:{NC}")
        print(f"1. Make sure you've accepted the model license on the Hugging Face website:")
        print(f"   {BLUE}https://huggingface.co/{hf_path}{NC}")
        print(f"2. Try updating mlx and mlx-lm packages:")
        print(f"   {BLUE}pip install --upgrade mlx mlx-lm{NC}")
        return False

def list_available_models() -> None:
    """List all available models that can be downloaded."""
    print(f"{CYAN}{BOLD}Available Models for Download:{NC}")
    print(f"{CYAN}============================{NC}")
    
    # Calculate the longest model name for formatting
    max_len = max(len(model) for model in MODEL_CONFIGS.keys())
    
    # Group models by size category
    small_models = [m for m in MODEL_CONFIGS.keys() if "2b" in m or "3-mini" in m]
    medium_models = [m for m in MODEL_CONFIGS.keys() if "7b" in m or "8b" in m]
    large_models = [m for m in MODEL_CONFIGS.keys() if "70b" in m]
    
    print(f"{BOLD}Small Models (2-4B parameters):{NC}")
    for model in small_models:
        config = MODEL_CONFIGS[model]
        print(f"  {model.ljust(max_len)} - {BLUE}{config['hf_path']}{NC} ({config['quant']}-bit)")
    
    print(f"\n{BOLD}Medium Models (7-8B parameters):{NC}")
    for model in medium_models:
        config = MODEL_CONFIGS[model]
        print(f"  {model.ljust(max_len)} - {BLUE}{config['hf_path']}{NC} ({config['quant']}-bit)")
    
    print(f"\n{BOLD}Large Models (70B+ parameters):{NC}")
    for model in large_models:
        config = MODEL_CONFIGS[model]
        print(f"  {model.ljust(max_len)} - {BLUE}{config['hf_path']}{NC} ({config['quant']}-bit)")

def list_downloaded_models() -> None:
    """List all models that have been downloaded."""
    models_dir = Path("models")
    if not models_dir.exists():
        print(f"{YELLOW}No models directory found.{NC}")
        return
    
    # Get all subdirectories in the models directory
    model_dirs = [d for d in models_dir.iterdir() if d.is_dir()]
    
    if not model_dirs:
        print(f"{YELLOW}No models have been downloaded yet.{NC}")
        return
    
    print(f"{GREEN}{BOLD}Downloaded Models:{NC}")
    for model_dir in model_dirs:
        model_name = model_dir.name
        if model_name in MODEL_CONFIGS:
            config = MODEL_CONFIGS[model_name]
            print(f"  {model_name} - {BLUE}{config['hf_path']}{NC} ({config['quant']}-bit)")
        else:
            print(f"  {model_name} - Custom or unknown model")

def main() -> None:
    """Main function for memory checking and model recommendations."""
    parser = argparse.ArgumentParser(
        description="Check Mac memory and download appropriate ML models"
    )
    parser.add_argument(
        "--list", action="store_true", 
        help="List all available models for download"
    )
    parser.add_argument(
        "--downloaded", action="store_true", 
        help="List all downloaded models"
    )
    parser.add_argument(
        "--model", type=str, 
        help="Download a specific model"
    )
    parser.add_argument(
        "--skip-check", action="store_true", 
        help="Skip system compatibility and memory checks"
    )
    
    args = parser.parse_args()
    
    # If just listing models, do that and exit
    if args.list:
        list_available_models()
        return
    
    # If just listing downloaded models, do that and exit
    if args.downloaded:
        list_downloaded_models()
        return
    
    
    print(f"{CYAN}================================================={NC}\n")
    print(f"{CYAN}System Memory Checker and Model Recommendation Tool{NC}")
    print(f"{CYAN}================================================={NC}\n")
    
    if not args.skip_check:
        # Check system compatibility
        is_mac, is_apple_silicon, ram_gb = check_system()
        
        if not is_mac:
            print(f"{RED}{BOLD}Error: This script is designed for macOS systems only.{NC}")
            sys.exit(1)
        
        if not is_apple_silicon:
            print(f"{YELLOW}{BOLD}Warning: This script is optimized for Apple Silicon Macs.{NC}")
            print(f"{YELLOW}While it may work on Intel Macs, performance will be significantly reduced.{NC}")
        
        # Get recommended models based on memory
        recommended_models, max_model_size, message = get_model_recommendations(ram_gb)
        
        # Print system info and recommendations
        print(f"{BLUE}Detected {BOLD}{ram_gb} GB{NC}{BLUE} of RAM on your system.{NC}")
        print(message)
        print(f"\n{CYAN}{BOLD}Maximum recommended model size:{NC} {max_model_size} parameters")
        print(f"{CYAN}{BOLD}Recommended models for your system:{NC}")
        for model in recommended_models:
            config = MODEL_CONFIGS[model]
            print(f"  - {GREEN}{model}{NC} ({config['hf_path']}, {config['quant']}-bit quantization)")
        
        print(f"\n{CYAN}To download one of these models, run:{NC}")
        print(f"  {BLUE}python {sys.argv[0]} --model {recommended_models[0]}{NC}")
        print(f"\n{CYAN}To see all available models:{NC}")
        print(f"  {BLUE}python {sys.argv[0]} --list{NC}")
    
    # If a specific model is requested for download
    if args.model:
        if args.model not in MODEL_CONFIGS:
            print(f"{RED}Error: Unknown model '{args.model}'.{NC}")
            print(f"Run {BLUE}python {sys.argv[0]} --list{NC} to see available models.")
            sys.exit(1)
            
        # Check if we need to log in to Hugging Face
        if not login_huggingface():
            print(f"{YELLOW}Warning: Not logged in to Hugging Face. Some models may not be accessible.{NC}")
        
        # Download the model
        success = download_model(args.model)
        if not success:
            sys.exit(1)
    
if __name__ == "__main__":
    main()
