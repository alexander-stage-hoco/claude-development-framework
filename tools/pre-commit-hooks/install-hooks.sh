#!/bin/bash
# Installation script for Claude Development Framework pre-commit hooks

set -e

echo "🔧 Installing Claude Development Framework Pre-commit Hooks"
echo

# Check if pre-commit is installed
if ! command -v pre-commit &> /dev/null; then
    echo "❌ pre-commit not found!"
    echo
    echo "Please install pre-commit first:"
    echo "  pip install pre-commit"
    echo
    echo "Or with homebrew:"
    echo "  brew install pre-commit"
    exit 1
fi

echo "✓ pre-commit is installed"

# Ask for strictness level
echo
echo "Choose configuration level:"
echo "  1) Relaxed  - For learning and early-stage projects"
echo "  2) Normal   - Recommended for most projects (default)"
echo "  3) Strict   - Maximum enforcement for production"
echo

read -p "Select [1/2/3] (default: 2): " choice
choice=${choice:-2}

# Determine config file
case $choice in
    1)
        config_file=".claude/templates/pre-commit-config-relaxed.yaml"
        config_name="relaxed"
        ;;
    3)
        config_file=".claude/templates/pre-commit-config-strict.yaml"
        config_name="strict"
        ;;
    *)
        config_file=".claude/templates/pre-commit-config.yaml"
        config_name="normal"
        ;;
esac

echo
echo "Selected: $config_name configuration"

# Check if config source exists
if [ ! -f "$config_file" ]; then
    echo "❌ Configuration file not found: $config_file"
    echo "Are you in a Claude Development Framework project?"
    exit 1
fi

# Copy config file
if [ -f ".pre-commit-config.yaml" ]; then
    echo
    echo "⚠️  .pre-commit-config.yaml already exists"
    read -p "Overwrite? [y/N]: " overwrite
    if [ "$overwrite" != "y" ] && [ "$overwrite" != "Y" ]; then
        echo "Installation cancelled"
        exit 0
    fi
    # Backup existing file
    cp .pre-commit-config.yaml .pre-commit-config.yaml.bak
    echo "✓ Backed up existing config to .pre-commit-config.yaml.bak"
fi

cp "$config_file" .pre-commit-config.yaml
echo "✓ Copied $config_name configuration"

# Make hook scripts executable
echo
echo "Setting up hook scripts..."
chmod +x tools/pre-commit-hooks/*.py
echo "✓ Hook scripts are executable"

# Install pre-commit hooks
echo
echo "Installing pre-commit hooks..."
pre-commit install
echo "✓ Pre-commit hooks installed"

# Optionally run on all files
echo
read -p "Run hooks on all files now? [y/N]: " run_all
if [ "$run_all" == "y" ] || [ "$run_all" == "Y" ]; then
    echo
    pre-commit run --all-files
fi

echo
echo "✅ Installation complete!"
echo
echo "Pre-commit hooks are now active. They will run automatically on:"
echo "  - git commit"
echo
echo "To bypass hooks (emergency only):"
echo "  git commit --no-verify"
echo
echo "To run manually:"
echo "  pre-commit run --all-files"
echo
