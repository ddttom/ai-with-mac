#!/bin/bash

# AI with Mac - Jupyter Extensions Setup
# This script installs enhanced Jupyter extensions for a better notebook experience

set -e # Exit on error

# ANSI color codes for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${CYAN}${BOLD}Setting Up Jupyter Extensions${NC}"
echo -e "${CYAN}===========================${NC}"
echo -e "Installing modern Jupyter extensions for code completion and enhanced functionality..."

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${YELLOW}No virtual environment detected. You should run this script from within your AI environment.${NC}"
    echo -e "${YELLOW}Activate it first with the 'go-ai' command or by sourcing your environment activation script.${NC}"
    
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}Setup aborted.${NC}"
        exit 1
    fi
fi

# Remove potentially incompatible old extensions
echo -ne "Removing any incompatible old extensions... "
pip uninstall -y jupyter_contrib_nbextensions jupyter_contrib_core jupyter_nbextensions_configurator 2>/dev/null || true
echo -e "${GREEN}Done!${NC}"

# Install JupyterLab extensions
echo -ne "Installing JupyterLab extensions... "
pip install jupyterlab-lsp python-lsp-server
pip install jupyterlab-git
pip install jupyterlab-code-formatter black isort
pip install ipywidgets
echo -e "${GREEN}Done!${NC}"

# Install language servers
echo -ne "Installing language servers... "
pip install jedi-language-server
echo -e "${GREEN}Done!${NC}"

# Build extensions
echo -ne "Building Jupyter extensions... "
jupyter lab build
echo -e "${GREEN}Done!${NC}"

# Create Jupyter config directory if it doesn't exist
echo -ne "Creating Jupyter configuration... "
jupyter_config_dir=$(jupyter --config-dir)
mkdir -p "$jupyter_config_dir/serverconfig"

# Create config to suppress "skipped server" messages
cat > "$jupyter_config_dir/serverconfig/jupyter_server_config.py" << 'PYCONFIG'
c = get_config()

# Suppress server extension messages
c.ServerApp.log_level = 'WARN'
c.LanguageServerManager.autodetect = False

# Only load language servers we actually installed
c.LanguageServerManager.language_servers = {
    "python-lsp-server": {
        "servercommand": ["pylsp"],
        "languages": ["python"],
        "version": 2
    },
    "jedi-language-server": {
        "servercommand": ["jedi-language-server"],
        "languages": ["python"],
        "version": 2
    }
}
PYCONFIG
echo -e "${GREEN}Done!${NC}"

echo -e "${GREEN}Created Jupyter config to suppress 'skipped server' messages${NC}"

# Explain what was installed
echo -e "\n${CYAN}${BOLD}About Jupyter Extensions:${NC}"
echo -e "These extensions enhance your Jupyter notebook experience with:"
echo -e "- ${GREEN}Code completion and syntax checking (LSP)${NC}"
echo -e "- ${GREEN}Version control integration (Git)${NC}"
echo -e "- ${GREEN}Code formatting (Black and isort for Python)${NC}"
echo -e "- ${GREEN}Interactive widgets${NC}"
echo -e "These tools make coding in notebooks more productive and IDE-like."

echo -e "\n${YELLOW}${BOLD}Note:${NC} You'll need to restart any running Jupyter servers for these changes to take effect."
echo -e "${GREEN}All Jupyter extensions have been successfully installed!${NC}"