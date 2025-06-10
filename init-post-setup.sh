#!/bin/bash
set -euo pipefail

# Navigate to project root (codespace_files)
cd /workspaces/codespace_files

# Create virtual environment with Python's built-in venv
echo "Setting up virtual environment with Python venv..."
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip to latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# Install current project in development mode
echo "Installing MediCode CLI in development mode..."
pip install -e . || {
    echo "Warning: Could not install package in editable mode. Continuing without it."
}

# Test medicode CLI installation if it exists
if command -v medicode &> /dev/null; then
    echo "Testing MediCode CLI..."
    medicode --help
else
    echo "Warning: medicode CLI not installed or not in PATH."
fi

echo "✨ MediCode student environment setup complete!"
echo "Virtual environment created at: /workspaces/codespace_files/.venv"
echo "To activate manually, run: source /workspaces/codespace_files/.venv/bin/activate"