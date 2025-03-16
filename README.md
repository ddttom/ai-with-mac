# AI with Mac


A comprehensive guide and code repository for running AI models locally on Apple Silicon Macs.

## Overview

This repository contains all the code examples, utilities, and guides from the "AI with Mac" series. It demonstrates how to leverage Apple Silicon's capabilities for various machine learning tasks, from running large language models to computer vision and time series forecasting.

The focus is on two main frameworks:

- **MLX**: Apple's new machine learning framework optimized for Apple Silicon
- **PyTorch**: A popular ML framework with Metal support for Apple GPUs

## Repository Structure

```terminal
ai-with-mac/
├── .gitattributes
├── .gitignore
├── README.md
├── data/                # Example datasets and data files
├── docs/
│   └── the essential gitignore file for apple AI projects.md
├── master-setup-README.md
├── master-setup.sh
├── models/              # Directory for storing ML models
├── notebooks/
│   └── 01_Environment_Test.ipynb
├── part1/               # Introduction to AI on Mac
│   └── examples/
│       └── hardware_check.py
├── part2/               # Getting Started with Python and Git
│   ├── examples/
│   │   ├── docstring_example.py
│   │   ├── requirements_example.py
│   │   ├── test_setup.py
│   │   └── virtual_env_demo.py
│   ├── notebooks/
│   │   └── 01_Environment_Test.ipynb
│   └── scripts/
│       ├── alternative_python_install.sh
│       ├── alternative_venv.sh
│       ├── create_project_structure.sh
│       ├── fix_permissions.sh
│       ├── install_homebrew.sh
│       ├── install_python.sh
│       ├── memory_issues.sh
│       ├── setup_git.sh
│       └── setup_venv.sh
├── part3/               # Running LLMs on Apple Silicon
│   ├── scripts/
│   │   ├── download_gemma.sh
│   │   ├── download_mistral.sh
│   │   ├── download_phi.sh
│   │   ├── huggingface_login.sh
│   │   ├── install_mlx.sh
│   │   ├── quantize_models.sh
│   │   └── test_model.sh
│   ├── advanced_chat.py
│   ├── batch_process.py
│   ├── document_qa.py
│   └── simple_chat.py
├── part4/               # Comparing MLX and PyTorch
│   ├── convert_model.py
│   ├── mlx_example.py
│   └── pytorch_example.py
├── part5/               # Choosing the Right Method
│   ├── combined_app/    # Web app combining MLX and PyTorch
│   │   ├── data/
│   │   ├── models/
│   │   ├── scripts/
│   │   │   ├── caption.py
│   │   │   ├── server.py
│   │   │   └── summarize.py
│   │   ├── static/
│   │   │   └── css/
│   │   │       └── style.css
│   │   └── templates/
│   │       ├── index.html
│   │       └── result.html
│   ├── images/          # Diagrams and screenshots
│   ├── scripts/
│   │   ├── lfs_track_model.sh
│   │   └── setup_git_lfs.sh
│   ├── document_qa_mlx.py
│   ├── image_classifier_torch.py
│   ├── ml_versioning.py
│   ├── model_registry.py
│   ├── setup_git_lfs.sh
│   └── timeseries_mlx.py
├── part6/               # Glossary of terms
├── requirements.txt
└── scripts/
    └── test_setup.py
```

## Getting Started

### Prerequisites

- A Mac with Apple Silicon (M1, M2, M3, or M4 chip)
- macOS Sonoma or newer (recommended)
- Xcode Command Line Tools

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ddttom/ai-with-mac.git
   cd ai-with-mac
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv ai-env
   source ai-env/bin/activate  # On Windows: ai-env\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Verify your setup:**

   ```bash
   python scripts/test_setup.py
   ```

### Model Setup

Most examples require downloading models. You can either:

1. **Use the built-in download scripts:**

   ```bash
   # For Gemma 2B Instruct model
   python -m mlx_lm.convert --hf-path google/gemma-2b-it -q --out-path models/gemma-2b-it-4bit
   ```

2. **Download from Hugging Face directly:**
   Visit [Hugging Face](https://huggingface.co/models) and download supported models.

## Key Examples

### Simple Chat Interface with MLX

Run a local chatbot using MLX:

```bash
python part3/simple_chat.py --model models/gemma-2b-it-4bit
```

### Document Q&A System

Ask questions about PDF documents:

```bash
python part3/document_qa.py --model models/gemma-2b-it-4bit --pdf your_document.pdf
```

### Comparing MLX and PyTorch Performance

Run a benchmark to compare performance:

```bash
python part4/mlx_example.py
python part4/pytorch_example.py
```

### Image Classification with PyTorch

Classify images using PyTorch with Metal acceleration:

```bash
python part5/image_classifier_torch.py --image your_image.jpg
```

### Time Series Forecasting with MLX

Forecast stock prices or other time series data:

```bash
python part5/timeseries_mlx.py --csv your_stock_data.csv
```

### Combined Web Application

Run a web app that demonstrates both frameworks:

```bash
cd part5/combined_app/scripts
python server.py
```

Then visit <http://localhost:5000> in your browser.

## Performance Considerations

Performance varies significantly based on your specific Mac hardware:

| Memory | Typical Use Cases |
|------------------|--------|------------------|
| 8GB RAM | Small models (2-4B parameters), 4-bit quantization |
| 16GB RAM | Medium models (up to 7B parameters), mixed precision |
| 32GB RAM | Larger models (up to 13B parameters), multiple tasks |
| 64GB RAM | Multiple models simultaneously, higher precision |
| 128GB+ RAM (Mac Studio/Pro) | Largest open models (70B+), model training |

## Model Management

This repository includes tools for model versioning and registry:

```bash
# Register a model
python part5/model_registry.py register-model --name "gemma-2b" --path "models/gemma-2b-it-4bit"

# List all registered models
python part5/model_registry.py list-models
```

## Git LFS Support

For large model files, we recommend using Git LFS:

```bash
# Set up Git LFS
bash part5/setup_git_lfs.sh
```

## Articles in the Series

1. [Introduction to AI on Mac](https://yourblog.com/ai-with-mac-part1)
2. [Getting Started with Python and Git](https://yourblog.com/ai-with-mac-part2)
3. [Running LLMs on Apple Silicon](https://yourblog.com/ai-with-mac-part3)
4. [Comparing MLX and PyTorch](https://yourblog.com/ai-with-mac-part4)
5. [Choosing the Right Method](https://yourblog.com/ai-with-mac-part5)
6. [Glossary](https://yourblog.com/ai-with-mac-part6)
7. [The Essential .gitignore Guide](https://yourblog.com/ai-with-mac-gitignore)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Apple for the MLX framework
- PyTorch team for Metal support
- All model creators (Google, Meta, Mistral AI, etc.)
- The open-source ML community

---

Happy coding with AI on your Mac!
