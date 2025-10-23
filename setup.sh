#!/bin/bash
# Setup script for blog post image automation

echo "Setting up Blog Post Image Automation..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✓ Python 3 found"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✓ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To generate a single image, run:"
echo "  python src/cli.py \"Your Title\" -s \"Your Subtitle\""
echo ""
echo "To batch process images, run:"
echo "  python src/batch_generator.py examples/blog_posts.json"
echo ""
