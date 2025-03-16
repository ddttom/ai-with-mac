#!/bin/bash

# AI with Mac - Setup Script
# This script sets up a fresh environment for the "AI with Mac" series
# It assumes the repo has been cloned and creates a new directory for your work

set -e # Exit on error

# ANSI color codes for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Print logo
echo -e "${BLUE}${BOLD}"
echo "   _   _____   __      _ _   _       __  __            "
echo "  /_\ |_   _|  \ \    / (_) | |_    |  \/  |__ _ __    "
echo " / _ \  | |     \ \/\/ /| | | ' \   | |\/| / _' / _|   "
echo "/_/ \_\ |_|      \_/\_/ |_| |_||_|  |_|  |_\__,_\__|   "
echo -e "${NC}"
echo -e "${CYAN}Setting up a fresh environment for your AI development${NC}"
echo -e "${CYAN}=================================================${NC}\n"

# Check current directory to ensure we're in the cloned repo
if [ ! -f "README.md" ] || ! grep -q "AI with Mac" README.md; then
    echo -e "${RED}${BOLD}Error: This script should be run from the 'AI with Mac' repository.${NC}"
    echo -e "${YELLOW}Please ensure you've cloned the repository and are running this script from its root.${NC}"
    exit 1
fi

REPO_DIR=$(pwd)
echo -e "${GREEN}Source repository: $REPO_DIR${NC}"

# Check if running on macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo -e "${RED}${BOLD}Error: This script is designed for macOS systems only.${NC}"
    exit 1
fi

# Check if running on Apple Silicon
if [[ "$(uname -m)" != "arm64" ]]; then
    echo -e "${YELLOW}${BOLD}Warning: This script is optimized for Apple Silicon Macs.${NC}"
    echo -e "${YELLOW}While it may work on Intel Macs, performance will be significantly reduced.${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}Setup aborted.${NC}"
        exit 1
    fi
fi

# Function to check available RAM
check_ram() {
    # Get physical memory in bytes and convert to GB
    local mem_bytes=$(sysctl -n hw.memsize)
    local mem_gb=$((mem_bytes / 1024 / 1024 / 1024))
    echo $mem_gb
}

# Function to check if command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Function to check if directory exists
dir_exists() {
    [ -d "$1" ]
}

# Function to create directory if it doesn't exist
ensure_dir() {
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
        echo -e "${GREEN}Created directory: $1${NC}"
    fi
}

# Get RAM size
RAM_GB=$(check_ram)
echo -e "${BLUE}Detected ${BOLD}${RAM_GB} GB${NC}${BLUE} of RAM on your system.${NC}"

# Determine which ML models are appropriate
if [ "$RAM_GB" -lt 8 ]; then
    echo -e "${YELLOW}${BOLD}Warning: Your system has less than 8GB of RAM.${NC}"
    echo -e "${YELLOW}You may experience limited performance with AI models.${NC}"
    RECOMMENDED_MODELS=("gemma-2b-it-4bit" "phi-3-mini-4bit")
    MAX_MODEL_SIZE="2B"
elif [ "$RAM_GB" -lt 16 ]; then
    echo -e "${BLUE}With 8GB RAM, you can run smaller models efficiently.${NC}"
    RECOMMENDED_MODELS=("gemma-2b-it-4bit" "phi-3-mini-4bit" "mistral-7b-instruct-4bit")
    MAX_MODEL_SIZE="7B"
elif [ "$RAM_GB" -lt 32 ]; then
    echo -e "${BLUE}With 16GB RAM, you can comfortably run medium-sized models.${NC}"
    RECOMMENDED_MODELS=("gemma-7b-it-4bit" "mistral-7b-instruct-4bit" "phi-3-mini-4bit")
    MAX_MODEL_SIZE="7-13B"
elif [ "$RAM_GB" -lt 64 ]; then
    echo -e "${BLUE}With 32GB RAM, you can run larger models or multiple smaller models.${NC}"
    RECOMMENDED_MODELS=("gemma-7b-it-4bit" "mistral-7b-instruct-4bit" "llama-3-8b-instruct-4bit")
    MAX_MODEL_SIZE="13B"
elif [ "$RAM_GB" -lt 128 ]; then
    echo -e "${BLUE}With 64GB RAM, you can run larger models at higher precision.${NC}"
    RECOMMENDED_MODELS=("gemma-7b-it-8bit" "mistral-7b-instruct-8bit" "llama-3-8b-instruct-8bit")
    MAX_MODEL_SIZE="13-30B"
else
    echo -e "${GREEN}${BOLD}Excellent! With $RAM_GB GB RAM, you can run very large models.${NC}"
    RECOMMENDED_MODELS=("gemma-7b-it-8bit" "mistral-7b-instruct-8bit" "llama-3-70b-instruct-4bit")
    MAX_MODEL_SIZE="70B+"
fi

echo -e "\n${CYAN}${BOLD}System Check${NC}"
echo -e "${CYAN}===========${NC}"

# Check for Homebrew
echo -ne "Checking for Homebrew... "
if command_exists brew; then
    echo -e "${GREEN}Found!${NC}"
else
    echo -e "${YELLOW}Not found.${NC}"
    echo -ne "Installing Homebrew... "
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo -e "${GREEN}Done!${NC}"
fi

# Check for Python
echo -ne "Checking for Python 3... "
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
        echo -e "${GREEN}Found Python $PYTHON_VERSION!${NC}"
    else
        echo -e "${YELLOW}Found Python $PYTHON_VERSION, but version 3.10+ is recommended.${NC}"
        echo -ne "Installing Python 3.11... "
        brew install python@3.11
        echo -e "${GREEN}Done!${NC}"
    fi
else
    echo -e "${YELLOW}Not found.${NC}"
    echo -ne "Installing Python... "
    brew install python@3.11
    echo -e "${GREEN}Done!${NC}"
fi

# Check for Git
echo -ne "Checking for Git... "
if command_exists git; then
    GIT_VERSION=$(git --version | awk '{print $3}')
    echo -e "${GREEN}Found Git $GIT_VERSION!${NC}"
else
    echo -e "${YELLOW}Not found.${NC}"
    echo -ne "Installing Git... "
    brew install git
    echo -e "${GREEN}Done!${NC}"
fi

echo -e "\n${CYAN}${BOLD}Fresh Project Setup${NC}"
echo -e "${CYAN}===================${NC}"

# Set up a new project directory
DEFAULT_PROJECT_DIR="$HOME/play-with-AI"
read -p "Enter new project directory [$DEFAULT_PROJECT_DIR]: " PROJECT_DIR
PROJECT_DIR=${PROJECT_DIR:-$DEFAULT_PROJECT_DIR}

# Create project directory if it doesn't exist
ensure_dir "$PROJECT_DIR"

# Change to project directory
cd "$PROJECT_DIR"
echo -e "${GREEN}Working in: $(pwd)${NC}"

# Create project structure
echo -ne "Creating fresh project structure... "
ensure_dir "notebooks"
ensure_dir "scripts"
ensure_dir "models"
ensure_dir "data"
ensure_dir "data/processed"
ensure_dir "data/raw"

# Create README.md
cat > README.md << EOF
# AI with Mac - Playground

This is your playground for running AI models locally on Apple Silicon Macs,
based on the "AI with Mac" guide.

## Activate Environment

To activate the environment, simply run:

\`\`\`
source go-ai.sh
\`\`\`

Or use the shortcut command \`go-ai\` if you've set it up.

## Project Structure

- \`notebooks/\`: Jupyter notebooks for exploration
- \`scripts/\`: Python scripts for running models
- \`models/\`: Directory for AI models
- \`data/\`: Data files for testing and demos

## Reference Repository

The original code examples can be found in the source repository.
Feel free to copy over examples as needed.

Source: $REPO_DIR
EOF

echo -e "${GREEN}Done!${NC}"

echo -e "\n${CYAN}${BOLD}Virtual Environment Setup${NC}"
echo -e "${CYAN}=======================${NC}"

# Create and activate virtual environment
echo -ne "Creating virtual environment... "
python3 -m venv ai-env
echo -e "${GREEN}Done!${NC}"

echo -ne "Activating virtual environment... "
source ai-env/bin/activate
echo -e "${GREEN}Done!${NC}"

# Upgrade pip
echo -ne "Upgrading pip... "
pip install --upgrade pip
echo -e "${GREEN}Done!${NC}"

# Install common dependencies
echo -ne "Installing common dependencies... "
pip install numpy pandas matplotlib jupyter

# Install framework-specific packages
echo -e "${GREEN}Done!${NC}"
echo -ne "Installing framework-specific packages... "
pip install mlx mlx-lm huggingface_hub torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu

# Install practical utilities
echo -e "${GREEN}Done!${NC}"
echo -ne "Installing practical utilities... "
pip install flask pypdf
echo -e "${GREEN}Done!${NC}"

# Save requirements.txt
echo -ne "Saving requirements.txt... "
pip freeze > requirements.txt
echo -e "${GREEN}Done!${NC}"

echo -e "\n${CYAN}${BOLD}Creating Model Download Scripts${NC}"
echo -e "${CYAN}=============================${NC}"

# Create scripts directory for model download scripts
ensure_dir "$PROJECT_DIR/scripts"

# Create main download_models.py script
cat > "$PROJECT_DIR/scripts/download_models.py" << EOF
#!/usr/bin/env python3
"""
Download and setup AI models based on your system's capabilities.
"""
import os
import argparse
import sys
from huggingface_hub import login
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
    
    # Check if we need Hugging Face login for this model
    if "llama" in args.model:
        print("Note: You'll need a Hugging Face account with access to Meta's Llama models.")
        login_huggingface()
    
    # Import mlx_lm.convert
    try:
        from mlx_lm.convert import convert
    except ImportError:
        print("Error: mlx_lm package not found. Installing...")
        os.system("pip install mlx-lm")
        from mlx_lm.convert import convert
    
    # Determine model settings
    if args.model == "gemma-2b-it-4bit":
        hf_path = "google/gemma-2b-it"
        quantization = 4
    elif args.model == "gemma-7b-it-4bit":
        hf_path = "google/gemma-7b-it"
        quantization = 4
    elif args.model == "gemma-7b-it-8bit":
        hf_path = "google/gemma-7b-it"
        quantization = 8
    elif args.model == "mistral-7b-instruct-4bit":
        hf_path = "mistralai/Mistral-7B-Instruct-v0.2"
        quantization = 4
    elif args.model == "mistral-7b-instruct-8bit":
        hf_path = "mistralai/Mistral-7B-Instruct-v0.2"
        quantization = 8
    elif args.model == "phi-3-mini-4bit":
        hf_path = "microsoft/Phi-3-mini-4k-instruct"
        quantization = 4
    elif args.model == "llama-3-8b-instruct-4bit":
        hf_path = "meta-llama/Meta-Llama-3-8B-Instruct"
        quantization = 4
    elif args.model == "llama-3-8b-instruct-8bit":
        hf_path = "meta-llama/Meta-Llama-3-8B-Instruct"
        quantization = 8
    elif args.model == "llama-3-70b-instruct-4bit":
        hf_path = "meta-llama/Meta-Llama-3-70B-Instruct"
        quantization = 4
    else:
        print(f"Unknown model: {args.model}")
        return
    
    # Output path
    output_path = f"models/{args.model}"
    
    # Download and convert model
    print(f"Downloading {hf_path}...")
    print(f"This model will be saved to: {output_path}")
    print(f"Using {quantization}-bit quantization")
    
    # Convert model
    convert(hf_path, output_path, quantization=quantization)
    
    print(f"Model downloaded and saved to {output_path}")
    print(f"You can now use this model with scripts from the repository!")

def login_huggingface():
    """Log in to Hugging Face if needed for restricted models."""
    from huggingface_hub import login
    print("Please enter your Hugging Face credentials to access the models")
    login()

if __name__ == "__main__":
    main()
EOF

# Make download script executable
chmod +x "$PROJECT_DIR/scripts/download_models.py"

# Create a simple chat script
cat > "$PROJECT_DIR/scripts/simple_chat.py" << EOF
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
        
        # Check if model exists
        if not os.path.exists(model_path):
            print(f"Model not found at {model_path}.")
            print("Please download a model first using: python scripts/download_models.py")
            return
        
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
            print("\nAssistant: ", end="", flush=True)
            
            # Generation configuration
            gen_config = {
                "max_tokens": 500,
                "temperature": 0.7,
                "top_p": 0.9
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
    args = parser.parse_args()
    chat_with_model(args.model)
EOF

# Make the chat script executable
chmod +x "$PROJECT_DIR/scripts/simple_chat.py"

# Create activation script
cat > "$PROJECT_DIR/go-ai.sh" << EOF
#!/bin/bash
# Activation script for AI with Mac environment

# Activate virtual environment
source "$PROJECT_DIR/ai-env/bin/activate"

# Set project directory
export AI_PROJECT_DIR="$PROJECT_DIR"

# Print welcome message
echo -e "\033[0;32mAI environment activated! You're ready to go.\033[0m"
echo -e "\033[0;34mProject directory: $PROJECT_DIR\033[0m"

# List available models
if [ -d "$PROJECT_DIR/models" ]; then
    echo -e "\033[0;36mAvailable models:\033[0m"
    find "$PROJECT_DIR/models" -maxdepth 1 -type d | grep -v "^$PROJECT_DIR/models\$" | sed 's|.*/||' | sort | sed 's/^/- /'
else
    echo -e "\033[0;33mNo models downloaded yet.\033[0m"
fi

echo ""
echo -e "\033[0;35mQuick commands:\033[0m"
echo "- Download a model:  python scripts/download_models.py --model MODEL_NAME"
echo "- Start chatting:    python scripts/simple_chat.py --model models/MODEL_NAME"
echo "- Launch Jupyter:    jupyter notebook"
echo ""
echo -e "\033[0;32mHappy coding!\033[0m"
EOF

# Make the activation script executable
chmod +x "$PROJECT_DIR/go-ai.sh"

# Create 'go-ai' shell command
echo -e "\n${CYAN}${BOLD}Setting up shell command${NC}"
echo -e "${CYAN}======================${NC}"

# Detect shell
SHELL_NAME=$(basename "$SHELL")
SHELL_CONFIG=""

if [ "$SHELL_NAME" = "bash" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS may use .bash_profile instead
        if [ -f "$HOME/.bash_profile" ]; then
            SHELL_CONFIG="$HOME/.bash_profile"
        fi
    fi
elif [ "$SHELL_NAME" = "zsh" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ "$SHELL_NAME" = "fish" ]; then
    SHELL_CONFIG="$HOME/.config/fish/config.fish"
else
    echo -e "${YELLOW}Unknown shell: $SHELL_NAME. You'll need to manually set up the 'go-ai' command.${NC}"
    SHELL_CONFIG=""
fi

if [ -n "$SHELL_CONFIG" ]; then
    echo -ne "Adding 'go-ai' command to $SHELL_CONFIG... "
    
    if [ "$SHELL_NAME" = "fish" ]; then
        # Fish shell has different syntax
        echo "function go-ai; source $PROJECT_DIR/go-ai.sh; end" >> "$SHELL_CONFIG"
    else
        # Bash/Zsh
        echo "alias go-ai='source $PROJECT_DIR/go-ai.sh'" >> "$SHELL_CONFIG"
    fi
    
    echo -e "${GREEN}Done!${NC}"
    echo -e "${YELLOW}Note: You'll need to restart your terminal or run 'source $SHELL_CONFIG' to use the command.${NC}"
else
    echo -e "${YELLOW}To activate the environment manually, run:${NC}"
    echo -e "${CYAN}source $PROJECT_DIR/go-ai.sh${NC}"
fi

echo -e "\n${GREEN}${BOLD}Setup Complete!${NC}"
echo -e "${GREEN}==================${NC}"
echo -e "${CYAN}Your fresh AI environment has been created at: ${BOLD}$PROJECT_DIR${NC}"
echo -e "\n${YELLOW}Next steps:${NC}"
echo -e "1. ${CYAN}Source your shell config or restart your terminal${NC}"
echo -e "   ${BLUE}source $SHELL_CONFIG${NC}"
echo -e "2. ${CYAN}Activate your environment${NC}"
echo -e "   ${BLUE}go-ai${NC}"
echo -e "3. ${CYAN}Download a model${NC}"
echo -e "   ${BLUE}python scripts/download_models.py --model gemma-2b-it-4bit${NC}"
echo -e "4. ${CYAN}Start chatting with your model${NC}"
echo -e "   ${BLUE}python scripts/simple_chat.py --model models/gemma-2b-it-4bit${NC}"
echo -e "\n${CYAN}Source repository with example code: ${BOLD}$REPO_DIR${NC}"
echo -e "${CYAN}Feel free to copy specific examples as needed.${NC}"
echo -e "\n${GREEN}${BOLD}Happy AI coding on your Mac!${NC}"