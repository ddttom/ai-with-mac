#!/bin/bash

# AI with Mac - Basic Setup Script
# This script sets up the basic environment for local AI development on Apple Silicon
# Part 1: System checks, virtual environment, and basic structure

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

# Function to create directory if it doesn't exist
ensure_dir() {
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
        echo -e "${GREEN}Created directory: $1${NC}"
    fi
}

# Get project directory input
DEFAULT_PROJECT_DIR="$HOME/play-with-AI"
read -p "Enter new project directory [$DEFAULT_PROJECT_DIR]: " PROJECT_DIR
PROJECT_DIR=${PROJECT_DIR:-$DEFAULT_PROJECT_DIR}

# Check if go-ai already exists and if it points to the correct directory
GO_AI_REPLACE="y"  # Default to yes if script doesn't exist
if [ -f "$HOME/bin/go-ai" ]; then
    CURRENT_PATH=$(grep "PROJECT_DIR=" "$HOME/bin/go-ai" | head -1 | cut -d'"' -f2)
    if [ "$CURRENT_PATH" = "$PROJECT_DIR" ]; then
        echo -e "${GREEN}Found existing go-ai script already pointing to $PROJECT_DIR${NC}"
        echo -e "${YELLOW}Script will be updated with the latest features${NC}"
    else
        echo -e "${YELLOW}A 'go-ai' script already exists but points to a different directory:${NC}"
        echo -e "${BLUE}Current: $CURRENT_PATH${NC}"
        echo -e "${BLUE}New: $PROJECT_DIR${NC}"
        read -p "Do you want to update it to point to the new directory? (y/n) " -n 1 -r
        echo
        GO_AI_REPLACE=$REPLY
    fi
fi

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
    RECOMMENDED_MODELS=("gemma-2b-it-4bit" "phi-3-mini-4bit")
    MAX_MODEL_SIZE="7B"
elif [ "$RAM_GB" -lt 32 ]; then
    echo -e "${BLUE}With 16GB RAM, you can comfortably run medium-sized models.${NC}"
    RECOMMENDED_MODELS=("gemma-7b-it-4bit" "phi-3-mini-4bit")
    MAX_MODEL_SIZE="7-13B"
elif [ "$RAM_GB" -lt 64 ]; then
    echo -e "${BLUE}With 32GB RAM, you can run larger models or multiple smaller models.${NC}"
    RECOMMENDED_MODELS=("gemma-7b-it-4bit" "llama-3-8b-instruct-4bit")
    MAX_MODEL_SIZE="13B"
elif [ "$RAM_GB" -lt 128 ]; then
    echo -e "${BLUE}With 64GB RAM, you can run larger models at higher precision.${NC}"
    RECOMMENDED_MODELS=("gemma-7b-it-8bit" "llama-3-8b-instruct-8bit")
    MAX_MODEL_SIZE="13-30B"
else
    echo -e "${GREEN}${BOLD}Excellent! With $RAM_GB GB RAM, you can run very large models.${NC}"
    RECOMMENDED_MODELS=("gemma-7b-it-8bit" "llama-3-70b-instruct-4bit")
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
go-ai
\`\`\`

## What's Included

This environment includes:

- Ready-to-use examples from the original repository
- Scripts for downloading and running AI models
- A properly configured Python environment with all dependencies
- Convenient activation command

## Project Structure

- \`notebooks/\`: Jupyter notebooks for exploration (copied from source repository)
- \`scripts/\`: Python scripts for running models (copied from source repository)
- \`models/\`: Directory for AI models (will be populated when you download models)
- \`data/\`: Data files for testing and demos (small examples copied from source repository)

## Reference Repository

The original code examples can be found in the source repository.
Additional examples can be copied over as needed.

Source: $REPO_DIR

## Getting Started

1. Activate the environment: \`go-ai\`
2. Download a model: \`python scripts/download_models.py --model ${RECOMMENDED_MODELS[0]}\`
3. Start chatting: \`python scripts/simple_chat.py --model models/${RECOMMENDED_MODELS[0]}\`
4. Explore notebooks: \`jupyter notebook\`
EOF
echo -e "${GREEN}Done!${NC}"

echo -e "\n${CYAN}${BOLD}Setting Up Virtual Environment${NC}"
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

echo -e "\n${CYAN}${BOLD}Copying Examples from Repository${NC}"
echo -e "${CYAN}==============================${NC}"

# Copy examples from repository
echo -e "Copying useful examples from the repository to your new environment..."

# Copy notebook examples
echo -ne "Copying notebook examples... "
if [ -d "$REPO_DIR/notebooks" ] && [ "$(ls -A "$REPO_DIR/notebooks" 2>/dev/null)" ]; then
    cp -r "$REPO_DIR/notebooks"/* "$PROJECT_DIR/notebooks"/ 2>/dev/null
    echo -e "${GREEN}Done!${NC}"
else
    echo -e "${YELLOW}No notebooks found in repository.${NC}"
fi

# Copy script examples
echo -ne "Copying script examples... "
if [ -d "$REPO_DIR/scripts" ] && [ "$(ls -A "$REPO_DIR/scripts" 2>/dev/null)" ]; then
    cp -r "$REPO_DIR/scripts"/* "$PROJECT_DIR/scripts"/ 2>/dev/null
    echo -e "${GREEN}Done!${NC}"
else
    echo -e "${YELLOW}No scripts found in repository.${NC}"
fi

# Copy data examples (if they aren't too large)
echo -ne "Copying small data examples... "
if [ -d "$REPO_DIR/data" ]; then
    # Find and copy only small data files (< 5MB)
    find "$REPO_DIR/data" -type f -size -5M -exec cp {} "$PROJECT_DIR/data/" \; 2>/dev/null
    echo -e "${GREEN}Done!${NC}"
else
    echo -e "${YELLOW}No data directory found in repository.${NC}"
fi

# Explain what was copied
echo -e "${GREEN}Examples successfully copied to your new environment!${NC}"
echo -e "${YELLOW}Note:${NC} Only smaller data files were copied. Larger files should be downloaded as needed."
echo -e "You can always reference the original repository at ${BLUE}$REPO_DIR${NC} for more examples."

echo -e "\n${CYAN}${BOLD}Creating Standalone Launcher Script${NC}"
echo -e "${CYAN}================================${NC}"

# Create bin directory in home if it doesn't exist
ensure_dir "$HOME/bin"

# Create standalone go-ai executable script based on user's earlier choice
if [[ "$GO_AI_REPLACE" =~ ^[Yy]$ ]]; then
    echo -ne "Creating standalone go-ai launcher script... "
    cat > "$HOME/bin/go-ai" << EOF
#!/bin/bash

# Path to your AI project
PROJECT_DIR="$PROJECT_DIR"

# Change to the project directory
cd "\$PROJECT_DIR" || { echo "Error: Could not change to \$PROJECT_DIR"; exit 1; }

# Activate the virtual environment
source "\$PROJECT_DIR/ai-env/bin/activate"

# Print welcome message
echo -e "\033[0;32mAI environment activated! You're now in your AI project directory.\033[0m"
echo -e "\033[0;34mProject directory: \$PROJECT_DIR\033[0m"

# Display the helpful information
if [ -d "\$PROJECT_DIR/models" ]; then
    MODEL_COUNT=\$(find "\$PROJECT_DIR/models" -maxdepth 1 -type d | grep -v "^\$PROJECT_DIR/models\\\$" | wc -l | tr -d ' ')
    if [ "\$MODEL_COUNT" -gt 0 ]; then
        echo -e "\033[0;36mAvailable models:\033[0m"
        find "\$PROJECT_DIR/models" -maxdepth 1 -type d | grep -v "^\$PROJECT_DIR/models\\\$" | sed 's|.*/||' | sort | sed 's/^/- /'
    else
        echo -e "\033[0;33mNo models downloaded yet. You can download one with the commands below.\033[0m"
    fi
else
    echo -e "\033[0;33mNo models downloaded yet. You can download one with the commands below.\033[0m"
fi

# Check what examples are available
NOTEBOOK_COUNT=\$(find "\$PROJECT_DIR/notebooks" -name "*.ipynb" | wc -l | tr -d ' ')
SCRIPT_COUNT=\$(find "\$PROJECT_DIR/scripts" -name "*.py" | wc -l | tr -d ' ')

echo ""
echo -e "\033[0;35mAvailable resources:\033[0m"
echo -e "- \033[0;36mNotebooks:\033[0m \$NOTEBOOK_COUNT Jupyter notebooks in the 'notebooks' directory"
echo -e "- \033[0;36mScripts:\033[0m \$SCRIPT_COUNT Python scripts in the 'scripts' directory"

echo ""
echo -e "\033[0;35mQuick commands:\033[0m"
echo "- Download a model:  python scripts/download_models.py --model ${RECOMMENDED_MODELS[0]}"
echo "- Start chatting:    python scripts/simple_chat.py --model models/MODEL_NAME"
echo "- Launch Jupyter:    jupyter notebook"
echo ""

echo -e "\033[1;33mTo exit this environment:\033[0m"
echo -e "   \033[0;36mtype 'exit' or press Ctrl+D\033[0m"
echo ""

echo -e "\033[0;32mHappy coding!\033[0m"

# Start a new shell with the virtual environment active
\$SHELL
EOF

    # Make the script executable
    chmod +x "$HOME/bin/go-ai" || { 
        echo -e "${RED}Error: Could not make script executable. Trying with sudo...${NC}"
        sudo chmod +x "$HOME/bin/go-ai" || {
            echo -e "${RED}Error: Could not make script executable even with sudo.${NC}"
            echo -e "${YELLOW}Please manually make it executable with: chmod +x $HOME/bin/go-ai${NC}"
        }
    }
    echo -e "${GREEN}Done!${NC}"
else
    echo -e "${YELLOW}Skipping launcher script creation.${NC}"
    echo -e "${YELLOW}Note: You can still run 'source $PROJECT_DIR/ai-env/bin/activate' to activate the environment.${NC}"
    echo -e "${YELLOW}Then 'cd $PROJECT_DIR' to change to the project directory.${NC}"
fi

# Update PATH if needed
echo -ne "Checking if ~/bin is in your PATH... "
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    # Add ~/bin to PATH in shell config
    if [ "$SHELL_NAME" = "bash" ]; then
        echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
    elif [ "$SHELL_NAME" = "zsh" ]; then
        echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.zshrc"
    elif [ "$SHELL_NAME" = "fish" ]; then
        echo 'set -gx PATH $HOME/bin $PATH' >> "$HOME/.config/fish/config.fish"
    fi
    echo -e "${YELLOW}Added ~/bin to your PATH in your shell config file${NC}"
else
    echo -e "${GREEN}Already in PATH!${NC}"
fi

# Call other setup scripts with instructions
echo -e "\n${GREEN}${BOLD}Basic setup complete!${NC}"
echo -e "${CYAN}You can now run these additional setup scripts:${NC}"
echo -e "1. ${BLUE}setup_jupyter_extensions.sh${NC} - Install enhanced Jupyter extensions"
echo -e "2. ${BLUE}setup_download_models.py${NC} - Create model download script"

echo -e "\n${GREEN}${BOLD}Next Steps:${NC}"
echo -e "1. Source your shell config: ${BLUE}source ~/.zshrc${NC} (or your shell's config file)"
echo -e "2. Launch your AI environment: ${BLUE}go-ai${NC}"

echo -e "\n${GREEN}${BOLD}Happy AI coding on your Mac!${NC}"
