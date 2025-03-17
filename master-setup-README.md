# Setting Up Your Mac for Local AI Development: The Master Setup

The landscape of artificial intelligence has dramatically shifted. What once required expensive cloud credits or specialized hardware can now run efficiently on your MacBook/Mac Studio or iPad thanks to the incredible capabilities of Apple Silicon. In this guide, I'll walk you through creating a complete AI development environment on your Mac that allows you to run sophisticated machine learning models locally, preserving your privacy and avoiding subscription costs.

## Why Run AI Locally on Your Mac?

Before diving into the technical setup, let's consider why local AI development on Mac has become so compelling:

1. **Privacy**: Your data and prompts never leave your device
2. **No Subscription Costs**: Avoid monthly API fees for model access
3. **Freedom from Internet Dependency**: Work offline anywhere
4. **Lower Latency**: Eliminate network delays
5. **Learning Opportunity**: Gain deeper understanding of AI systems

Apple Silicon's unified memory architecture provides unique advantages for AI workloads - the CPU, GPU, and Neural Engine can all access the same physical memory without costly transfers, dramatically improving performance for these memory-intensive applications.

## The Two-Part Setup System

To streamline the setup process, I've created a comprehensive system using specialized scripts that handle everything you need for a productive AI development environment:

1. **master-setup.sh**: The main script that sets up your project structure and environment
2. **download_models.py**: A utility script for downloading various AI models based on your hardware
3. **jupyter_extensions.py**: A script to enhance your Jupyter experience with IDE-like features

Let's explore how these scripts work together and what they provide.

## The Master Setup Script

The core of our system is the `master-setup.sh` script, which:

1. Verifies it's being run from within the "AI with Mac" repository to access example code
2. Detects your Mac's RAM and recommends appropriate model sizes
3. Creates a clean project environment separate from the original repository
4. Sets up a properly configured Python environment
5. Installs frameworks optimized for Apple Silicon (MLX and PyTorch)
6. Copies relevant examples from the source repository to your project directory
7. Creates a convenient `go-ai` activation script to set up your environment

The script follows several key principles:

- **User-friendly**: Collects all inputs at the beginning to avoid interrupting the installation
- **Informative**: Explains what's happening at each step and why
- **Hardware-aware**: Provides recommendations based on your Mac's capabilities
- **Clean**: Creates a fresh environment isolated from your other projects
- **Flexible**: Offers choices for customization while providing sensible defaults

When you run the master setup script, it will:

1. Present its purpose with a clear banner
2. Verify it's being run from within the "AI with Mac" repository
3. Store the current directory as the source repository for examples
4. Ask where you want to create your AI environment (default: `~/play-with-AI`)
5. Check if you have existing configurations and ask for permission before overwriting them
6. Detect your system's hardware capabilities and RAM
7. Install required dependencies (Homebrew, Python, Git if needed)
8. Create a complete project structure in your specified directory
9. Set up a Python virtual environment with all necessary packages
10. Copy examples, notebooks, and scripts from the source repository to your project
11. Create the `go-ai` activation script for easy environment activation

## Hardware-Aware Model Recommendations

One of the most valuable aspects of the master script is how it detects your Mac's RAM and provides appropriate model recommendations:

| RAM | Recommended Models | Maximum Size |
|-----|-------------------|--------------|
| <8GB | Gemma-2B, Phi-3-mini (4-bit) | 2B parameters |
| 8-16GB | Mistral-7B, Gemma-7B (4-bit) | 7B parameters |
| 16-32GB | Llama-3-8B, Gemma-7B (4-bit) | 7-13B parameters |
| 32-64GB | Llama-3-8B (8-bit), multiple smaller models | 13B parameters |
| 64-128GB | Multiple models at higher precision | 13-30B parameters |
| 128GB+ | Llama-3-70B (4-bit), multiple large models | 70B+ parameters |

This guidance helps you choose models that will run efficiently on your hardware, avoiding out-of-memory errors and performance bottlenecks.

Note that the master script also runs The Jupyter Extensions Script

For data scientists and researchers, this script enhances your Jupyter notebook experience with powerful IDE-like features:

This script installs and configures:

- **Code Completion**: Through integration with language servers
- **Syntax Checking**: Real-time error detection as you type
- **Git Integration**: Version control right from your notebooks
- **Code Formatting**: Automatic formatting with Black and isort
- **Interactive Widgets**: For creating dynamic visualizations

The script also silences those annoying "Skipped non-installed server" messages that typically appear when running Jupyter, providing a cleaner experience.

## The Model Downloader Script

After running the master setup, you'll want to download AI models. The `download_models.py` script makes this process simple:

- Supports various popular models like Gemma, Mistral, Phi-3, and Llama 3
- Handles authentication with Hugging Face
- Handles model conversion for optimal performance on Apple Silicon
- Provides appropriate quantization options (4-bit/8-bit) based on your hardware
- Contains troubleshooting steps if issues arise

The script can be run with a simple command:

```bash
python scripts/download_models.py --model gemma-2b-it-4bit
```

It supports multiple model options:

- `gemma-2b-it-4bit`: Google's small but capable model (good for 8GB RAM)
- `gemma-7b-it-4bit`: Larger Gemma model with 4-bit quantization (16GB+ RAM)
- `mistral-7b-instruct-4bit`: Mistral AI's efficient 7B model (16GB+ RAM)
- `phi-3-mini-4bit`: Microsoft's small but powerful model (8GB RAM)
- `llama-3-8b-instruct-4bit`: Meta's Llama 3 model (16GB+ RAM)
- `llama-3-70b-instruct-4bit`: The massive Llama 3 model (128GB+ RAM)

## The Environment Activation Script: `go-ai`

Perhaps the most convenient feature is the `go-ai` activation script created by the master setup script. This script:

1. Changes to your AI project directory
2. Activates the Python virtual environment
3. Displays helpful information about available models and resources
4. Provides quick command references

**Important**: The `go-ai` script must be sourced, not executed. This means you should run it using:

```bash
source ~/bin/go-ai
```

This is necessary because the script needs to change your current directory and activate the virtual environment in your current shell session, which can only be done when the script is sourced.

The activation script is placed in `~/bin` and made executable, making it accessible from anywhere in your terminal. If `~/bin` isn't already in your PATH, the setup script adds it for you.

## Getting Started With Your AI Environment

After running the setup scripts, getting started is simple:

1. First, clone the repository and run the master setup script from within it:

   ```bash
   git clone https://github.com/ddttom/ai-with-mac.git
   cd ai-with-mac
   bash master-setup.sh
   ```

   Note: The script must be run from within the repository because it copies examples, scripts, and notebooks from the repository to your new project directory.

2. Optionally enhance your Jupyter experience:

   ```bash
   bash scripts/jupyter_extensions.sh
   ```

3. Download your first model:

   ```bash
   python scripts/download_models.py --model gemma-2b-it-4bit
   ```

4. Start using your environment:

   ```bash
   source ~/bin/go-ai
   ```

5. Start chatting with your model:

   ```bash
   python scripts/simple_chat.py --model models/gemma-2b-it-4bit
   ```

6. Or launch Jupyter:

   ```bash
   jupyter notebook
   ```

The environment comes with scripts already prepared for common tasks, copied from the source repository to your project directory. The activation script provides reminders of these commands whenever you start a session and will show you which models you have installed.

## Technical Details

For those interested in the technical aspects, here's what's happening behind the scenes:

### Virtual Environment Setup

The master script creates a proper Python virtual environment with all necessary dependencies:

```bash
# Create virtual environment
python3 -m venv ai-env

# Install core dependencies
pip install numpy pandas matplotlib jupyter

# Install framework-specific packages
pip install mlx mlx-lm torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu

# Install practical utilities
pip install flask pypdf huggingface_hub
```

### Framework Configuration

Both Apple's MLX and PyTorch with Metal support are installed and configured:

- **MLX**: Apple's machine learning framework specifically designed for Apple Silicon
- **PyTorch with Metal**: The popular ML framework optimized to use Apple's Metal API

This dual-framework approach gives you flexibility to use the best tool for each task.

### Jupyter Configuration

The Jupyter extensions script creates a custom Jupyter configuration that provides code completion while eliminating annoying "missing server" messages.

## Customizing Your Environment

The environment is designed to be extended and customized. Here are some ways you might adapt it:

1. **Additional Models**: Download more models based on your hardware capabilities
2. **Custom Scripts**: Add your own scripts to the `scripts` directory
3. **Data Exploration**: Store datasets in the `data` directory for analysis
4. **Framework Extensions**: Install additional packages for specific tasks
5. **New Notebooks**: Create new analysis notebooks in the `notebooks` directory
6. **Additional Repository Examples**: Copy more examples from the source repository as needed

The setup explicitly separates your working environment from the original repository. This means:

1. Your project directory (default: `~/play-with-AI`) is completely independent from the source repository
2. You can update or delete the original repository without affecting your working environment
3. All necessary example files are copied to your project directory during setup
4. The project README includes a reference to the original source repository location

Since everything is contained in a virtual environment within your AI project folder, you can experiment freely without affecting your system Python installation or worrying about changes to the original repository.

## Conclusion

Setting up a productive AI development environment on your Mac doesn't have to be complicated. With these three specialized scripts, you can go from a fresh system to running sophisticated language models in minutes, all configured optimally for your specific hardware.

The ability to run AI models locally on your Mac represents a significant democratization of this technology. No longer do you need expensive cloud credits or specialized hardware - your MacBook can now be a self-contained AI research and development platform.

Whether you're exploring language models for creative writing, analyzing data with machine learning, or developing custom AI applications, this environment provides a solid foundation for your work.

Want to try it yourself? The complete setup scripts are available on GitHub at [AI with Mac](https://github.com/ddttom/ai-with-mac).
