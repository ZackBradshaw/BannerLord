#!/bin/bash

# BannerLord Setup Script
# Installs dependencies and sets up the environment

set -e

echo "=========================================="
echo "BannerLord Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check if Python 3.8+ using a more robust method
if ! python3 -c 'import sys; exit(0 if sys.version_info >= (3,8) else 1)'; then
    echo "❌ Error: Python 3.8 or higher is required"
    exit 1
fi

echo "✅ Python version OK"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo ""
echo "Installing dependencies..."
echo "This may take several minutes..."
pip install -r requirements.txt

echo ""
echo "✅ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your OpenAI API key"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Create outputs directory
mkdir -p outputs
echo "✅ Created outputs directory"
echo ""

# Run tests
echo "Running tests..."
python test_bannerlord.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Setup Complete!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "  1. Edit .env and add your OpenAI API key"
    echo "  2. Activate the virtual environment: source venv/bin/activate"
    echo "  3. Run the tool: python bannerlord.py --prompt 'your prompt' --text 'YOUR TEXT'"
    echo ""
    echo "Examples:"
    echo "  python bannerlord.py --prompt 'modern tech' --text 'INNOVATE'"
    echo "  python examples.py"
    echo ""
else
    echo ""
    echo "⚠️  Some tests failed, but setup is complete."
    echo "The tool should still work if you have a valid OpenAI API key."
    echo ""
fi
