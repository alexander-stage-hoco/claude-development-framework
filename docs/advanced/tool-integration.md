# Tool Integration Guide

**Purpose**: Set up development tools that enforce framework standards automatically

**Last Updated**: 2025-09-30

---

## Overview

This guide shows how to integrate tools that:
- Enforce code quality standards
- Prevent commits that violate rules
- Automate test execution
- Verify spec-code alignment

**Philosophy**: Automation supports discipline, doesn't replace it.

---

## 1. Git Hooks

### Pre-Commit Hook

Prevents commits that violate framework rules.

**Create**: `.git/hooks/pre-commit`

```bash
#!/bin/bash
# Pre-commit hook for Claude Development Framework
# Enforces quality standards before allowing commit

echo "🔍 Running pre-commit checks..."

# Check 1: No TODO comments in source code
echo "  ├─ Checking for TODO comments..."
if grep -r "TODO" src/ 2>/dev/null; then
    echo "  ❌ ERROR: TODO comments found in src/"
    echo "     Create an issue instead of leaving TODOs"
    exit 1
fi
echo "  ✅ No TODO comments"

# Check 2: All tests must pass
echo "  ├─ Running test suite..."
if ! pytest tests/ -q; then
    echo "  ❌ ERROR: Tests failing"
    echo "     All tests must pass before commit"
    exit 1
fi
echo "  ✅ All tests passing"

# Check 3: Test coverage threshold
echo "  ├─ Checking test coverage..."
if ! pytest --cov=src --cov-fail-under=90 tests/ -q > /dev/null 2>&1; then
    echo "  ❌ ERROR: Test coverage below 90%"
    echo "     Add tests before committing"
    exit 1
fi
echo "  ✅ Coverage threshold met"

# Check 4: Linting
echo "  ├─ Running linter..."
if ! pylint src/ --errors-only; then
    echo "  ❌ ERROR: Linting errors found"
    exit 1
fi
echo "  ✅ No linting errors"

# Check 5: Type checking
echo "  ├─ Running type checker..."
if ! mypy src/ --ignore-missing-imports --no-error-summary 2>/dev/null; then
    echo "  ⚠️  WARNING: Type checking issues (non-blocking)"
fi

echo "✅ All pre-commit checks passed!"
exit 0
```

**Make executable**:
```bash
chmod +x .git/hooks/pre-commit
```

### Commit-Msg Hook

Enforces commit message format.

**Create**: `.git/hooks/commit-msg`

```bash
#!/bin/bash
# Commit message hook
# Enforces descriptive commit messages

commit_msg_file=$1
commit_msg=$(cat "$commit_msg_file")

# Check minimum length
if [ ${#commit_msg} -lt 20 ]; then
    echo "❌ ERROR: Commit message too short (< 20 chars)"
    echo "   Provide descriptive commit message"
    exit 1
fi

# Check for spec references (relaxed check)
if [[ ! $commit_msg =~ (UC-[0-9]|SVC-[0-9]|Iteration [0-9]|ADR-[0-9]) ]]; then
    echo "⚠️  WARNING: No spec reference found in commit message"
    echo "   Consider adding UC-XXX, SVC-XXX, or Iteration XXX"
    # Don't block, just warn
fi

exit 0
```

**Make executable**:
```bash
chmod +x .git/hooks/commit-msg
```

---

## 2. Pre-Commit Framework (Python)

More robust alternative to git hooks.

### Installation

```bash
pip install pre-commit
```

### Configuration

**Create**: `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      # Prevent large files
      - id: check-added-large-files
        args: ['--maxkb=1000']

      # Check YAML/JSON syntax
      - id: check-yaml
      - id: check-json

      # Detect private keys
      - id: detect-private-key

      # Trailing whitespace
      - id: trailing-whitespace

      # Mixed line endings
      - id: mixed-line-ending

  - repo: local
    hooks:
      # No TODO comments
      - id: no-todos
        name: No TODO comments
        entry: bash -c 'grep -r "TODO" src/ && exit 1 || exit 0'
        language: system
        pass_filenames: false

      # Tests must pass
      - id: tests-pass
        name: All tests passing
        entry: pytest tests/ -q
        language: system
        pass_filenames: false
        always_run: true

      # Coverage threshold
      - id: coverage
        name: Test coverage >= 90%
        entry: pytest --cov=src --cov-fail-under=90 tests/ -q
        language: system
        pass_filenames: false
        always_run: true

      # Linting
      - id: pylint
        name: Pylint checks
        entry: pylint
        language: system
        types: [python]
        args: [--errors-only]

      # Type checking
      - id: mypy
        name: Type checking
        entry: mypy
        language: system
        types: [python]
        args: [--ignore-missing-imports]
```

**Install hooks**:
```bash
pre-commit install
pre-commit install --hook-type commit-msg
```

---

## 3. Continuous Integration (GitHub Actions)

Automate testing and enforcement in CI/CD pipeline.

**Create**: `.github/workflows/test-enforcement.yml`

```yaml
name: Enforce Development Standards

on: [push, pull_request]

jobs:
  enforce:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov pylint mypy

      - name: Check for TODO comments
        run: |
          if grep -r "TODO" src/; then
            echo "❌ ERROR: TODO comments found"
            exit 1
          fi
          echo "✅ No TODO comments"

      - name: Run tests
        run: pytest tests/ -v

      - name: Check coverage
        run: pytest --cov=src --cov-fail-under=90 --cov-report=term-missing tests/

      - name: Lint with pylint
        run: pylint src/ --errors-only

      - name: Type check with mypy
        run: mypy src/ --ignore-missing-imports
        continue-on-error: true

      - name: Verify spec alignment
        run: python scripts/verify-spec-alignment.py
        if: hashFiles('scripts/verify-spec-alignment.py') != ''

  spec-alignment:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Check specs exist for all use cases
        run: |
          # Verify every UC has a spec file
          for uc_dir in src/services/*/; do
            uc_name=$(basename "$uc_dir")
            if [ ! -f "specs/use-cases/UC-*-${uc_name}.md" ]; then
              echo "⚠️  Missing spec for $uc_name"
            fi
          done
```

---

## 4. IDE Integration

### VS Code

**Create**: `.vscode/settings.json`

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": [
    "tests"
  ],
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.linting.lintOnSave": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": [
    "--line-length=100"
  ],
  "editor.formatOnSave": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/.pytest_cache": true
  },
  "python.analysis.typeCheckingMode": "basic",
  "editor.rulers": [100],
  "files.insertFinalNewline": true,
  "files.trimTrailingWhitespace": true
}
```

**Create**: `.vscode/tasks.json`

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run All Tests",
      "type": "shell",
      "command": "pytest tests/ -v",
      "group": {
        "kind": "test",
        "isDefault": true
      },
      "presentation": {
        "reveal": "always",
        "panel": "dedicated"
      }
    },
    {
      "label": "Run Tests with Coverage",
      "type": "shell",
      "command": "pytest --cov=src --cov-report=html --cov-report=term tests/",
      "group": "test"
    },
    {
      "label": "Run Current Test File",
      "type": "shell",
      "command": "pytest ${file} -v",
      "group": "test"
    },
    {
      "label": "Lint Current File",
      "type": "shell",
      "command": "pylint ${file}",
      "group": "none"
    }
  ]
}
```

**Recommended Extensions** (`.vscode/extensions.json`):

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.pylint",
    "njpwerner.autodocstring",
    "gruntfuggly.todo-tree",
    "eamodio.gitlens",
    "streetsidesoftware.code-spell-checker"
  ]
}
```

### PyCharm

**Settings to Configure**:

1. **Testing**:
   - Preferences → Tools → Python Integrated Tools
   - Default test runner: pytest
   - ✅ Auto-detect test imports

2. **Linting**:
   - Preferences → Tools → External Tools
   - Add pylint as external tool
   - Add to "Before Commit" actions

3. **Type Checking**:
   - Preferences → Editor → Inspections
   - ✅ Enable type checker
   - Set severity to "Error"

4. **File Watchers**:
   - Preferences → Tools → File Watchers
   - Add watcher for Python files
   - Run tests on save

---

## 5. Test Automation

### pytest Configuration

**Create**: `pytest.ini`

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=90

markers =
    unit: Unit tests
    integration: Integration tests
    bdd: BDD scenario tests
    slow: Slow running tests
```

### Makefile for Common Commands

**Create**: `Makefile`

```makefile
.PHONY: test test-unit test-integration test-bdd coverage lint typecheck format clean help

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

test:  ## Run all tests
	pytest tests/ -v

test-unit:  ## Run unit tests only
	pytest tests/unit/ -v -m unit

test-integration:  ## Run integration tests only
	pytest tests/integration/ -v -m integration

test-bdd:  ## Run BDD tests only
	pytest tests/bdd/ -v -m bdd

coverage:  ## Run tests with coverage report
	pytest --cov=src --cov-report=html --cov-report=term-missing tests/
	@echo "Coverage report: file://$(PWD)/htmlcov/index.html"

lint:  ## Run linting
	pylint src/ tests/

typecheck:  ## Run type checking
	mypy src/ --ignore-missing-imports

format:  ## Format code with black
	black src/ tests/ --line-length=100

verify:  ## Run all quality checks
	@echo "Running verification suite..."
	@make test
	@make lint
	@make typecheck
	@echo "✅ All checks passed!"

clean:  ## Clean generated files
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache .coverage htmlcov/ .mypy_cache/
```

---

## 6. Spec Alignment Verification

**Create**: `scripts/verify-spec-alignment.py`

```python
#!/usr/bin/env python3
"""
Verify spec-code alignment.

Checks:
1. Every use case has a specification
2. Every BDD feature matches a use case
3. Every service has a specification
4. No orphaned test files
"""
import sys
from pathlib import Path

def verify_alignment():
    """Run all alignment checks."""
    errors = []

    # Check 1: UC specs exist for implementations
    src_services = Path("src/services").glob("*/")
    for service_dir in src_services:
        service_name = service_dir.name
        uc_spec = list(Path("specs/use-cases").glob(f"UC-*-{service_name}.md"))
        if not uc_spec:
            errors.append(f"Missing UC spec for service: {service_name}")

    # Check 2: BDD features match UC specs
    uc_specs = Path("specs/use-cases").glob("UC-*.md")
    for uc_spec in uc_specs:
        uc_number = uc_spec.stem.split("-")[1]
        bdd_feature = Path(f"tests/bdd/features/UC-{uc_number}*.feature")
        if not list(Path("tests/bdd/features").glob(f"UC-{uc_number}*.feature")):
            errors.append(f"Missing BDD feature for {uc_spec.name}")

    # Check 3: Report results
    if errors:
        print("❌ Spec-Code Alignment Errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("✅ All specs aligned with code")
        sys.exit(0)

if __name__ == "__main__":
    verify_alignment()
```

**Make executable**:
```bash
chmod +x scripts/verify-spec-alignment.py
```

---

## 7. Documentation Generation

### API Documentation with Sphinx

```bash
pip install sphinx sphinx-rtd-theme
sphinx-quickstart docs/
```

**Configure** `docs/conf.py` to autodoc from docstrings.

### OpenAPI/Swagger (FastAPI)

FastAPI auto-generates docs:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

No additional setup needed!

---

## Summary: Tool Setup Checklist

- [ ] Git hooks installed (pre-commit, commit-msg)
- [ ] Pre-commit framework configured
- [ ] GitHub Actions workflow added
- [ ] IDE configured (VS Code or PyCharm)
- [ ] pytest.ini created
- [ ] Makefile for common commands
- [ ] Spec alignment script created
- [ ] Documentation generation setup (optional)

---

## Quick Start Commands

After setup:

```bash
# Run all tests
make test

# Check coverage
make coverage

# Run quality checks
make verify

# Format code
make format

# Clean artifacts
make clean
```

---

**Document Version**: 1.0
**Part of**: Claude Development Framework
**See also**: `.claude/CLAUDE.md`, `.claude/development-rules.md`
