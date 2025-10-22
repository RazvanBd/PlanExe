# PlanExe Installation Guide

This guide provides detailed instructions for installing and running PlanExe.

## Prerequisites

- **Python**: Version 3.10 or higher (3.10, 3.11, 3.12, or 3.13)
  - Check your version: `python --version` or `python3 --version`
- **pip**: Latest version recommended
- **Git**: For cloning the repository

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/neoneye/PlanExe.git
cd PlanExe
```

### 2. Create a Virtual Environment

It's strongly recommended to use a virtual environment to avoid conflicts with other Python packages.

```bash
# Create virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Upgrade pip

Ensure you have the latest version of pip:

```bash
pip install --upgrade pip
```

### 4. Install PlanExe with Gradio UI

To use the web-based Gradio interface (recommended):

```bash
pip install .[gradio-ui]
```

**Alternative**: To install only the core package without UI:

```bash
pip install .
```

**Alternative**: To install with Flask UI:

```bash
pip install .[flask-ui]
```

### 5. Configure API Keys

PlanExe requires an LLM API to function. Follow the configuration instructions:

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Configure your LLM provider (recommended: **Gemini**):
   - See [extra/gemini.md](extra/gemini.md) for Gemini setup instructions
   - Add your API key to the `.env` file

## Running PlanExe

### Start the Gradio Web Interface

```bash
python -m planexe.plan.app_text2plan
```

This will start a local web server at `http://localhost:7860`. Open this URL in your browser to use PlanExe.

### Stop the Server

Press `Ctrl+C` in your terminal to stop the server.

## Troubleshooting

### Dependency Conflicts

The installation should now work without conflicts. The pillow dependency has been configured to work with all required packages:
- `pillow>=10.2.0,<11.0` - Compatible with llama-index-llms-gemini, gradio, and llama-index-core

### Python Version Issues

If you encounter a "Python version not supported" error:
- Ensure you're using Python 3.10 or higher
- Check your Python version: `python --version`
- If you have multiple Python versions, use the specific version: `python3.10`, `python3.11`, etc.

### Network Timeouts During Installation

If you experience network timeouts:
```bash
pip install --default-timeout=300 .[gradio-ui]
```

### Virtual Environment Not Activating

Make sure you're in the PlanExe directory and the virtual environment was created successfully:
```bash
# Check if venv folder exists
ls -la venv/

# Try creating it again if needed
python3 -m venv venv --clear
```

## Verification

### Quick Verification

Run the included verification script to check your installation:

```bash
python verify_installation.py
```

This will check:
- Python version compatibility
- Pillow version and compatibility
- All required dependencies
- PlanExe installation

### Manual Verification

1. Check that PlanExe is installed:
   ```bash
   pip show PlanExe
   ```

2. Start the application (see "Running PlanExe" section above)

3. Open `http://localhost:7860` in your browser

4. Enter a simple test prompt like "Create a plan for a coffee shop"

## Additional Resources

- **Homepage**: https://github.com/neoneye/PlanExe
- **Examples**: https://neoneye.github.io/PlanExe-web/examples/
- **Discord**: https://neoneye.github.io/PlanExe-web/discord.html
- **Configuration**: See [extra/gemini.md](extra/gemini.md) for detailed API configuration

## Common Commands

```bash
# Activate virtual environment (Linux/macOS)
source venv/bin/activate

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install/reinstall PlanExe with Gradio UI
pip install .[gradio-ui]

# Run PlanExe
python -m planexe.plan.app_text2plan

# Deactivate virtual environment
deactivate
```

## Notes

- The first run may take longer as it downloads model weights and dependencies
- Ensure you have a stable internet connection during installation
- Keep your API keys secure and never commit them to version control
