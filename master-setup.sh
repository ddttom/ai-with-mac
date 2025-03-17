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
echo " "
echo "  █████  ██      ██     ██ ██ ████████ ██   ██      ███    ███  █████   ██████ "
echo " ██   ██ ██      ██     ██ ██    ██    ██   ██      ████  ████ ██   ██ ██      "
echo " ███████ ██      ██  █  ██ ██    ██    ███████      ██ ████ ██ ███████ ██      "
echo " ██   ██ ██      ██ ███ ██ ██    ██    ██   ██      ██  ██  ██ ██   ██ ██      "
echo " ██   ██ ██       ███ ███  ██    ██    ██   ██      ██      ██ ██   ██  ██████ "
echo " "
echo " =======  A I  W I T H  M A C  ======="
echo " "
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

# Check if go-ai already exists and ask for permission to overwrite
GO_AI_REPLACE="y"  # Default to yes if script doesn't exist
if [ -f "$HOME/bin/go-ai" ]; then
    CURRENT_PATH=$(grep "PROJECT_DIR=" "$HOME/bin/go-ai" | head -1 | cut -d'"' -f2)
    if [ "$CURRENT_PATH" = "$PROJECT_DIR" ]; then
        echo -e "${YELLOW}A 'go-ai' script already exists and points to the same directory: ${BLUE}$PROJECT_DIR${NC}"
    else
        echo -e "${YELLOW}A 'go-ai' script already exists but points to a different directory:${NC}"
        echo -e "${BLUE}Current: $CURRENT_PATH${NC}"
        echo -e "${BLUE}New: $PROJECT_DIR${NC}"
    fi
    read -p "Do you want to overwrite the existing go-ai script? (y/n) " -n 1 -r
    echo
    GO_AI_REPLACE=$REPLY
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
source ~/bin/go-ai
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

1. Activate the environment: \`source ~/bin/go-ai\`
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

# Modify the virtual environment's activate script to use a simple prompt
echo -ne "Customizing virtual environment... "
ACTIVATE_SCRIPT="$PROJECT_DIR/ai-env/bin/activate"
if [ -f "$ACTIVATE_SCRIPT" ]; then
    # Backup the original activate script
    cp "$ACTIVATE_SCRIPT" "${ACTIVATE_SCRIPT}.bak"
    
    # Replace the PS1 setting in the activate script
    sed -i '' 's/PS1="(ai-env) \$PS1"/PS1="(ai-env) $ "/' "$ACTIVATE_SCRIPT"
    echo -e "${GREEN}Done!${NC}"
else
    echo -e "${YELLOW}Could not find activate script. Prompt customization skipped.${NC}"
fi

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
echo -e "${GREEN}Done!${NC}"

# Install framework-specific packages
echo -ne "Installing framework-specific packages... "
pip install mlx mlx-lm huggingface_hub torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu
echo -e "${GREEN}Done!${NC}"

# Install practical utilities
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

# Copy .gitignore
echo -ne "Copying .gitignore... "
if [ -f "$REPO_DIR/.gitignore" ]; then
    cp "$REPO_DIR/.gitignore" "$PROJECT_DIR/" 2>/dev/null
    echo -e "${GREEN}Done!${NC}"
else
    echo -e "${YELLOW}No .gitignore found in repository.${NC}"
fi

# Copy notebook examples
echo -ne "Copying notebook examples... "
if [ -d "$REPO_DIR/notebooks" ] && [ "$(ls -A "$REPO_DIR/notebooks" 2>/dev/null)" ]; then
    cp -r "$REPO_DIR/notebooks/"* "$PROJECT_DIR/notebooks/" 2>/dev/null
    echo -e "${GREEN}Done!${NC}"
else
    echo -e "${YELLOW}No notebook examples found in repository.${NC}"
fi

# Copy script examples
echo -ne "Copying script examples... "
if [ -d "$REPO_DIR/scripts" ] && [ "$(ls -A "$REPO_DIR/scripts" 2>/dev/null)" ]; then
    cp -r "$REPO_DIR/scripts/"* "$PROJECT_DIR/scripts/" 2>/dev/null
    echo -e "${GREEN}Done!${NC}"
else
    echo -e "${YELLOW}No script examples found in repository.${NC}"
fi

# Copy part3 examples if they exist
echo -ne "Copying chat examples... "
if [ -d "$REPO_DIR/part3" ] && [ "$(ls -A "$REPO_DIR/part3" 2>/dev/null)" ]; then
    # Copy Python files from part3 to scripts
    find "$REPO_DIR/part3" -maxdepth 1 -name "*.py" -exec cp {} "$PROJECT_DIR/scripts/" \; 2>/dev/null
    # Copy scripts from part3/scripts to scripts
    if [ -d "$REPO_DIR/part3/scripts" ]; then
        cp -r "$REPO_DIR/part3/scripts/"* "$PROJECT_DIR/scripts/" 2>/dev/null
    fi
    echo -e "${GREEN}Done!${NC}"
else
    echo -e "${YELLOW}No chat examples found in repository.${NC}"
fi

# Copy small data examples if they exist
echo -ne "Copying data examples... "
if [ -d "$REPO_DIR/data" ] && [ "$(ls -A "$REPO_DIR/data" 2>/dev/null)" ]; then
    # Only copy small files (< 5MB)
    find "$REPO_DIR/data" -type f -size -5M -exec cp --parents {} "$PROJECT_DIR/" \; 2>/dev/null
    echo -e "${GREEN}Done!${NC}"
else
    echo -e "${YELLOW}No data examples found in repository.${NC}"
fi

echo -e "\n${CYAN}${BOLD}Creating Activation Script${NC}"
echo -e "${CYAN}========================${NC}"

# Create bin directory if it doesn't exist
ensure_dir "$HOME/bin"

# Create go-ai script
if [[ "$GO_AI_REPLACE" =~ ^[Yy]$ ]]; then
    echo -ne "Creating go-ai activation script... "
    cat > "$HOME/bin/go-ai" << EOF
#!/bin/bash

# AI with Mac - Environment Activation Script
# This script activates the AI development environment
# IMPORTANT: This script must be sourced, not executed
# Usage: source ~/bin/go-ai

# Exit if the script is executed instead of sourced
if [[ "\${BASH_SOURCE[0]}" == "\${0}" ]]; then
    echo "Error: This script must be sourced, not executed."
    echo "Please use: source ~/bin/go-ai"
    exit 1
fi

# Configuration
PROJECT_DIR="$PROJECT_DIR"
VENV_DIR="\$PROJECT_DIR/ai-env"

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "\$VENV_DIR" ]; then
    echo -e "\${RED}Error: Virtual environment not found at \$VENV_DIR\${NC}"
    echo "Please run the setup script first."
    return 1
fi

# Change to project directory and activate virtual environment
echo -e "\${CYAN}Activating AI environment...\${NC}"
cd "\$PROJECT_DIR"
source "\$VENV_DIR/bin/activate"

# Print success message
echo -e "\${GREEN}\${BOLD}AI environment activated!\${NC}"
echo -e "\${CYAN}Working directory: \${BOLD}\$PROJECT_DIR\${NC}"
echo -e "\${CYAN}Python: \${BOLD}\$(python --version)\${NC}"
echo -e "\${CYAN}Available models: \${BOLD}\$(ls -1 \$PROJECT_DIR/models 2>/dev/null | wc -l)\${NC} models found in models/ directory"
echo ""
echo -e "\${BLUE}Quick commands:\${NC}"
echo -e "  \${GREEN}python scripts/download_models.py --help\${NC} # Download AI models"
echo -e "  \${GREEN}python scripts/simple_chat.py --help\${NC} # Start chatting with a model"
echo -e "  \${GREEN}jupyter notebook\${NC} # Launch Jupyter Notebook"
echo ""
echo -e "Enjoy your AI development session!"
EOF
    chmod +x "$HOME/bin/go-ai"
    echo -e "${GREEN}Done!${NC}"
    
    # Check if ~/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
        echo -e "${YELLOW}Adding ~/bin to your PATH...${NC}"
        
        # Determine shell configuration file
        SHELL_CONFIG=""
        if [[ "$SHELL" == *"zsh"* ]]; then
            SHELL_CONFIG="$HOME/.zshrc"
        elif [[ "$SHELL" == *"bash"* ]]; then
            SHELL_CONFIG="$HOME/.bash_profile"
            if [ ! -f "$SHELL_CONFIG" ]; then
                SHELL_CONFIG="$HOME/.bashrc"
            fi
        fi
        
        if [ -n "$SHELL_CONFIG" ]; then
            echo 'export PATH="$HOME/bin:$PATH"' >> "$SHELL_CONFIG"
            echo -e "${GREEN}Added ~/bin to $SHELL_CONFIG${NC}"
            echo -e "${YELLOW}Please restart your terminal or run 'source $SHELL_CONFIG' to apply changes.${NC}"
        else
            echo -e "${YELLOW}Could not determine shell configuration file. Please add ~/bin to your PATH manually.${NC}"
        fi
    fi
else
    echo -e "${YELLOW}Skipping go-ai script creation as requested.${NC}"
fi

echo -e "\n${CYAN}Installing Jupyter extensions...${NC}"
bash scripts/jupyter_extensions.sh
echo -e "\n${CYAN}Installing gemma-2b-it-4bit model...${NC}"
python scripts/download_models.py --model gemma-2b-it-4bit

echo -e "\n${GREEN}${BOLD}Setup Complete!${NC}"
echo -e "${GREEN}===================${NC}"
echo -e "\n${CYAN}Your AI development environment is ready to use.${NC}"
echo -e "${CYAN}To activate it, run: ${BOLD}source ~/bin/go-ai${NC}"
echo -e "${CYAN}(You may need to restart your terminal first)${NC}"
echo -e "\n${CYAN}Recommended next steps:${NC}"
echo -e "1. ${YELLOW}Activate the environment:${NC} source ~/bin/go-ai
echo -e "2. ${YELLOW}Download a model:${NC} python scripts/download_models.py --model ${RECOMMENDED_MODELS[0]}"
echo -e "3. ${YELLOW}Start chatting:${NC} python scripts/simple_chat.py --model models/${RECOMMENDED_MODELS[0]}"
echo -e "4. ${YELLOW}Explore notebooks:${NC} jupyter notebook"

echo -e "\n${CYAN}We've included a specialized .gitignore file:${NC}"
echo -e "${YELLOW}This .gitignore is specifically configured for AI development work,${NC}"
echo -e "${YELLOW}preventing large model files, datasets, and sensitive information from being committed.${NC}"

echo -e "\n${CYAN}Version control with GitHub:${NC}"
echo -e "5. ${YELLOW}Initialize Git repository:${NC} git init"
echo -e "6. ${YELLOW}Add your files:${NC} git add ."
echo -e "7. ${YELLOW}Create first commit:${NC} git commit -m \"Initial commit\""
echo -e "8. ${YELLOW}Create GitHub repository:${NC} Visit github.com/new"
echo -e "9. ${YELLOW}Connect and push:${NC} git remote add origin YOUR_REPO_URL && git push -u origin main"
echo -e "\n${CYAN}To preserve your versions and track changes, commit regularly with descriptive messages:${NC}"
echo -e "    ${YELLOW}git add [files]${NC}"
echo -e "    ${YELLOW}git commit -m \"Description of changes\"${NC}"
echo -e "    ${YELLOW}git push${NC}"
echo -e "\n${CYAN}Happy AI development!${NC}"
