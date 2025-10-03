#!/bin/bash
# Installation script for Claude Development Framework pre-commit hooks

set -e

echo "🔧 Installing Claude Development Framework Pre-commit Hooks"
echo

# Detect pre-commit location (venv first, then system)
if [ -f "../../.venv/bin/pre-commit" ]; then
    PRE_COMMIT="../../.venv/bin/pre-commit"
elif command -v pre-commit &> /dev/null; then
    PRE_COMMIT="pre-commit"
else
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

# Determine configuration level
# Accept from: 1) command-line arg, 2) interactive prompt, 3) default (non-interactive)
if [ -n "$1" ]; then
    # Use command-line argument
    choice="$1"
elif [ -t 0 ]; then
    # Interactive mode - prompt user
    echo
    echo "Choose configuration level:"
    echo "  1) Relaxed  - For learning and early-stage projects"
    echo "  2) Normal   - Recommended for most projects (default)"
    echo "  3) Strict   - Maximum enforcement for production"
    echo
    read -p "Select [1/2/3] (default: 2): " choice
    choice=${choice:-2}
else
    # Non-interactive mode - use default
    choice=2
    echo "Using default configuration: Normal (2)"
fi

# Determine config file (relative to project root)
case $choice in
    1)
        config_file="../../.claude/templates/pre-commit-config-relaxed.yaml"
        config_name="relaxed"
        ;;
    3)
        config_file="../../.claude/templates/pre-commit-config-strict.yaml"
        config_name="strict"
        ;;
    *)
        config_file="../../.claude/templates/pre-commit-config.yaml"
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

# Copy config file to project root
PROJECT_ROOT="../.."
if [ -f "$PROJECT_ROOT/.pre-commit-config.yaml" ]; then
    if [ -t 0 ]; then
        # Interactive mode - ask for confirmation
        echo
        echo "⚠️  .pre-commit-config.yaml already exists"
        read -p "Overwrite? [y/N]: " overwrite
        if [ "$overwrite" != "y" ] && [ "$overwrite" != "Y" ]; then
            echo "Installation cancelled"
            exit 0
        fi
    else
        # Non-interactive mode - backup and overwrite
        echo "⚠️  .pre-commit-config.yaml exists, backing up and overwriting"
    fi
    # Backup existing file
    cp "$PROJECT_ROOT/.pre-commit-config.yaml" "$PROJECT_ROOT/.pre-commit-config.yaml.bak"
    echo "✓ Backed up existing config to .pre-commit-config.yaml.bak"
fi

cp "$config_file" "$PROJECT_ROOT/.pre-commit-config.yaml"
echo "✓ Copied $config_name configuration"

# Make hook scripts executable
echo
echo "Setting up hook scripts..."
chmod +x *.py
echo "✓ Hook scripts are executable"

# Install pre-commit hooks
echo
echo "Installing pre-commit hooks..."
$PRE_COMMIT install
echo "✓ Pre-commit hooks installed"

# Optionally run on all files
if [ -t 0 ]; then
    # Interactive mode - ask user
    echo
    read -p "Run hooks on all files now? [y/N]: " run_all
    if [ "$run_all" == "y" ] || [ "$run_all" == "Y" ]; then
        echo
        $PRE_COMMIT run --all-files
    fi
else
    # Non-interactive mode - skip running on all files
    echo
    echo "Skipping 'run on all files' (non-interactive mode)"
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
