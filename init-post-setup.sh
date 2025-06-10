#!/bin/bash
set -euo pipefail

# Install uv if not already installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -sSf https://install.ultraviolet.rs | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Navigate to project root
cd /workspaces/medicode

# Create virtual environment with uv
echo "Setting up virtual environment..."
uv venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies from pyproject.toml
echo "Installing dependencies..."
uv sync

# Attempt to install current project in development mode
echo "Attempting to install current project in development mode..."
uv pip install -e . || {
    echo "Warning: Could not install package in editable mode. Continuing without it."
}

# Generate lock file
echo "Generating lock file..."
uv lock

# Test medicode CLI installation if it exists
if command -v medicode &> /dev/null; then
    medicode --help
else
    echo "Warning: medicode CLI not installed or not in PATH."
fi

echo "✨ MediCode development environment setup complete!"