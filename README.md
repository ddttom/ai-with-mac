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
│   ├── prd.md           # Product Requirements Document
│   ├── web/             # Web documentation files
│   │   ├── Part 1 - AI with Mac - Running AI Locally on a mac
│   │   ├── Part 2 - Getting Started with Python and Git for AI Development on Mac
│   │   └── ...
│   └── images/          # Documentation images
│       ├── part1/
│       │   ├── apple-silicon-ai-hero.svg
│       │   ├── mac-hardware-comparison.svg
│       │   ├── unified-memory-architecture.svg
│       │   └── llm-performance-comparison.svg
│       ├── part2/
│       └── ...
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
    ├── download_models.py
    ├── jupyter_extensions.sh
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

| Memory                      | Typical Use Cases                                    |
| --------------------------- | ---------------------------------------------------- |  |
| 8GB RAM                     | Small models (2-4B parameters), 4-bit quantization   |
| 16GB RAM                    | Medium models (up to 7B parameters), mixed precision |
| 32GB RAM                    | Larger models (up to 13B parameters), multiple tasks |
| 64GB RAM                    | Multiple models simultaneously, higher precision     |
| 128GB+ RAM (Mac Studio/Pro) | Largest open models (70B+), model training           |

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

## Documentation and Images

This repository includes comprehensive documentation with instructional articles and diagrams:

- **Documentation**: Located in the `docs/web/` directory
- **Images**: Located in the `docs/images/` directory, organized by part

### Image Guidelines

When contributing to the documentation:

1. Store all images in the appropriate subdirectory under `docs/images/part[X]/`
2. Use SVG format for diagrams and charts for better scalability
3. Reference images in documentation using relative paths: `../images/part[X]/filename.svg`
4. Include descriptive alt text and figure captions

Example image reference in Markdown:

```markdown
![Performance Comparison](../images/part3/performance-chart.svg)
*Figure 4: Comparison of token generation speeds across different models.*
```

## Articles in the Series

1. [Introduction to AI on Mac](docs/web/Part%201%20-%20AI%20with%20Mac%20-%20Running%20AI%20Locally%20on%20a%20mac)
2. [Getting Started with Python and Git](docs/web/Part%202%20-%20Getting%20Started%20with%20Python%20and%20Git%20for%20AI%20Development%20on%20Mac)
3. [Running LLMs on Apple Silicon](docs/web/Part%203%20-%20Running%20LLMs%20on%20Apple%20Silicon%20-%20A%20Step-by-Step%20Guide)
4. [Comparing MLX and PyTorch](docs/web/Part%204%20-%20Comparing%20MLX%20and%20PyTorch%20for%20Machine%20Learning%20on%20Apple%20Silicon)
5. [Choosing the Right Method](docs/web/Part%205%20-%20Machine%20Learning%20on%20Apple%20Silicon%3A%20Choosing%20the%20Right%20Method)
6. [Glossary](docs/web/Part%206%20-%20Glossary)
7. [The Essential .gitignore Guide](docs/web/Part%207%20-%20The%20essential%20gitignore%20file%20for%20mac%20AI%20projects)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

When contributing:

- Follow the established directory structure
- Use descriptive commit messages
- Update documentation as needed
- Add appropriate images for new features or concepts
- Ensure code examples are tested

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Apple for the MLX framework
- PyTorch team for Metal support
- All model creators (Google, Meta, Mistral AI, etc.)
- The open-source ML community

---

Happy coding with AI on your Mac!
