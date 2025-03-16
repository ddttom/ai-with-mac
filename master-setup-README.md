# Setting Up Your Mac for Local AI Development: The Master File

Over the past year, the landscape of artificial intelligence has dramatically shifted. What once required expensive cloud credits or specialized hardware can now run efficiently on your MacBook, thanks to the incredible capabilities of Apple Silicon. In this guide, I'll walk you through creating a complete AI development environment on your Mac that allows you to run sophisticated machine learning models locally, preserving your privacy and avoiding subscription costs.

Why Run AI Locally on Your Mac?
Before diving into the technical setup, let's consider why local AI development on Mac has become so compelling:

Privacy: Your data and prompts never leave your device
No Subscription Costs: Avoid monthly API fees for model access
Freedom from Internet Dependency: Work offline anywhere
Lower Latency: Eliminate network delays
Learning Opportunity: Gain deeper understanding of AI systems

Apple Silicon's unified memory architecture provides unique advantages for AI workloads - the CPU, GPU, and Neural Engine can all access the same physical memory without costly transfers, dramatically improving performance for these memory-intensive applications.
The Master Setup Script
To simplify the setup process, I've created a comprehensive script that handles everything you need for a productive AI development environment on your Mac. This script:

Detects your Mac's RAM and recommends appropriate model sizes
Creates a clean project environment separate from any repositories
Sets up a properly configured Python environment
Installs frameworks optimized for Apple Silicon (MLX and PyTorch)
Creates helpful utilities for downloading and using AI models
Configures enhanced Jupyter notebook extensions
Sets up a convenient command to activate everything

Let's explore how it works and what it provides.
How the Setup Script Works
The script follows several key principles to ensure a smooth experience:

User-friendly: Collects all inputs at the beginning to avoid interrupting the installation
Informative: Explains what's happening at each step and why
Hardware-aware: Provides recommendations based on your Mac's capabilities
Clean: Creates a fresh environment isolated from your other projects
Flexible: Offers choices for customization while providing sensible defaults

When you run the setup script, it will:

Present its purpose with a clear banner
Ask where you want to create your AI environment (default: ~/play-with-AI)
Check if you have existing configurations to avoid overwriting them
Detect your system's hardware capabilities
Install required dependencies
Create a complete project structure
Set up activation commands for easy access

All of this happens with minimal interaction after the initial prompts, allowing you to focus on your work while the environment takes shape.
Hardware-Aware Model Recommendations
One of the most valuable aspects of the script is how it detects your Mac's RAM and provides appropriate model recommendations. Here's a breakdown of what it suggests:

| Table (striped,bordered,first-line) |                                             |                   |
| :---------------------------------- | :------------------------------------------ | :---------------- |
| **RAM**                             | **Recommended Models**                      | **Maximum Size**  |
| \<8GB                               | Gemma-2B, Phi-3-mini (4-bit)                | 2B parameters     |
| 8-16GB                              | Mistral-7B, Gemma-7B (4-bit)                | 7B parameters     |
| 16-32GB                             | Llama-3-8B, Gemma-7B (4-bit)                | 7-13B parameters  |
| 32-64GB                             | Llama-3-8B (8-bit), multiple smaller models | 13B parameters    |
| 64-128GB                            | Multiple models at higher precision         | 13-30B parameters |
| 128GB+                              | Llama-3-70B (4-bit), multiple large models  | 70B+ parameters   |

This guidance helps you choose models that will run efficiently on your hardware, avoiding out-of-memory errors and performance bottlenecks.
The Standalone Launcher: go-ai
Perhaps the most convenient feature is the go-ai command the script creates. This standalone launcher does several things:

Changes to your AI project directory
Activates the Python virtual environment
Displays helpful information about available models and resources
Provides quick command references
Starts a new shell session for your AI work

To exit this environment, you simply type exit or press Ctrl+D, and you'll return to your previous shell session.

The launcher script is placed in ~/bin and made executable, making it accessible from anywhere in your terminal. If ~/bin isn't already in your PATH, the setup script adds it for you.
Enhanced Jupyter Notebook Experience
For data scientists and ML researchers, Jupyter notebooks are an essential tool. The setup script includes a special section that creates a Jupyter environment with powerful IDE-like features:

Code Completion: Through integration with language servers
Syntax Checking: Real-time error detection as you type
Git Integration: Version control right from your notebooks
Code Formatting: Automatic formatting with Black and isort
Interactive Widgets: For creating dynamic visualizations

The script also silences those annoying "Skipped non-installed server" messages that typically appear when running Jupyter, providing a cleaner experience.
Getting Started with Your AI Environment
After running the setup script, getting started is simple:

Open a terminal and type go-ai
Download your first model with python scripts/download_models.py --model gemma-2b-it-4bit
Start chatting with your model using python scripts/simple_chat.py --model models/gemma-2b-it-4bit
Or launch Jupyter with jupyter notebook to explore the included example notebooks

The environment comes with scripts already prepared for common tasks, and the launcher provides reminders of these commands whenever you start a session.
Technical Details
For those interested in the technical aspects, here's what's happening behind the scenes:
Virtual Environment Setup
The script creates a proper Python virtual environment with all necessary dependencies:

## Create virtual environment

python3 -m venv ai-env

## Install core dependencies

pip install numpy pandas matplotlib jupyter

## Install framework-specific packages

pip install mlx mlx-lm torch torchvision --extra-index-url <https://download.pytorch.org/whl/cpu>

## Install practical utilities

pip install flask pypdf huggingface_hub
Framework Configuration
Both Apple's MLX and PyTorch with Metal support are installed and configured:

MLX: Apple's machine learning framework specifically designed for Apple Silicon
PyTorch with Metal: The popular ML framework optimized to use Apple's Metal API

This dual-framework approach gives you flexibility to use the best tool for each task.
Jupyter Configuration
For a better notebook experience, the script creates a custom Jupyter configuration:

c = get_config()

## Suppress server extension messages

c.ServerApp.log_level = 'WARN'

c.LanguageServerManager.autodetect = False

## Only load language servers we actually installed

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

This configuration provides code completion while eliminating those annoying "missing server" messages.
Customizing Your Environment
The environment is designed to be extended and customized. Here are some ways you might adapt it:

Additional Models: Download more models based on your hardware capabilities
Custom Scripts: Add your own scripts to the scripts directory
Data Exploration: Store datasets in the data directory for analysis
Framework Extensions: Install additional packages for specific tasks
New Notebooks: Create new analysis notebooks in the notebooks directory

Since everything is contained in a virtual environment within your AI project folder, you can experiment freely without affecting your system Python installation.
Conclusion
Setting up a productive AI development environment on your Mac doesn't have to be complicated. With this comprehensive setup script, you can go from a fresh system to running sophisticated language models in minutes, all configured optimally for your specific hardware.

The ability to run AI models locally on your Mac represents a significant democratization of this technology. No longer do you need expensive cloud credits or specialized hardware - your MacBook can now be a self-contained AI research and development platform.

Whether you're exploring language models for creative writing, analyzing data with machine learning, or developing custom AI applications, this environment provides a solid foundation for your work.

Want to try it yourself? The complete script is available on GitHub at AI with Mac.
