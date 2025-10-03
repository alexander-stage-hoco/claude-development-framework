# Claude Development Framework Pre-commit Hooks

Automated enforcement of the 12 Non-Negotiable Development Rules via Git pre-commit hooks.

## Overview

This package provides 5 custom pre-commit hooks that enforce framework discipline:

| Hook | Rule Enforced | What It Checks |
|------|---------------|----------------|
| `no-todos` | #6: No Shortcuts | Blocks TODO comments in source code |
| `spec-alignment` | #1: Specifications Are Law | Verifies UC references have corresponding spec files |
| `test-first` | #2: Tests Define Correctness | Ensures source files have tests |
| `adr-references` | #7: Technical Decisions Are Binding | Validates ADR references point to real files |
| `coverage-threshold` | #2: Tests Define Correctness | Enforces minimum test coverage (default: 90%) |

These hooks run automatically on `git commit` and block commits that violate framework rules.

## Quick Start

```bash
# Install (from project root)
./tools/pre-commit-hooks/install-hooks.sh

# Choose configuration level when prompted:
#   1) Relaxed  - For learning (70% coverage, warnings only)
#   2) Normal   - Recommended (90% coverage, balanced enforcement)
#   3) Strict   - Production (95% coverage, maximum enforcement)
```

That's it! Hooks now run automatically on every commit.

## Configuration Levels

### Relaxed Mode (Learning)
- **Coverage threshold**: 70%
- **Enforcement**: Warnings only for most checks
- **Auto-fix**: Enabled (black, trailing whitespace)
- **Use when**: Learning the framework, early-stage projects

### Normal Mode (Recommended)
- **Coverage threshold**: 90%
- **Enforcement**: Most checks enforced, some allow ≤1-2 violations
- **Auto-fix**: Enabled for formatting
- **Use when**: Active development, most projects

### Strict Mode (Production)
- **Coverage threshold**: 95%
- **Enforcement**: All checks enforced strictly
- **Auto-fix**: Disabled (check mode only)
- **Additional checks**: Bandit security, no print() statements
- **Use when**: Production code, mature projects

## Hook Details

### 1. No TODO Comments (`no-todos`)

**Enforces**: Rule #6 (No Shortcuts)

```python
# ❌ BLOCKED
def process_user(user):
    # TODO: Add validation
    return user

# ✅ ALLOWED
def process_user(user):
    """Process user data.

    Validation: See UC-003-validate-user-input.md
    """
    return user
```

**Rationale**: TODOs accumulate technical debt. Create specs or tickets instead.

### 2. Spec Alignment (`spec-alignment`)

**Enforces**: Rule #1 (Specifications Are Law)

```python
# ❌ BLOCKED (no specs/use-cases/UC-042-*.md exists)
def create_user(data):
    """Create user (UC-042)."""
    pass

# ✅ ALLOWED (specs/use-cases/UC-042-create-user.md exists)
def create_user(data):
    """Create user (UC-042)."""
    pass
```

**Modes**:
- Normal: Warns if ≤2 missing specs
- Strict: Blocks any missing specs

### 3. Test-First Development (`test-first`)

**Enforces**: Rule #2 (Tests Define Correctness)

```bash
# ❌ BLOCKED
git add src/services/user_service.py
git commit -m "Add user service"
# Error: No test file found for src/services/user_service.py

# ✅ ALLOWED
git add tests/unit/test_user_service.py  # Write test first!
git add src/services/user_service.py
git commit -m "Add user service with tests"
```

**Skips**: `__init__.py`, `config.py`, files <10 lines

**Modes**:
- Normal: Allows ≤1 untested file
- Strict: Blocks any untested files

### 4. ADR References (`adr-references`)

**Enforces**: Rule #7 (Technical Decisions Are Binding)

```python
# ❌ BLOCKED (no specs/adrs/ADR-015-*.md exists)
# Architecture decision: Use Redis for caching (ADR-015)

# ✅ ALLOWED (specs/adrs/ADR-015-caching-strategy.md exists)
# Architecture decision: Use Redis for caching (ADR-015)
```

### 5. Coverage Threshold (`coverage-threshold`)

**Enforces**: Rule #2 (Tests Define Correctness)

```bash
# ❌ BLOCKED
$ git commit -m "Add feature"
❌ Test coverage below 90%!

TOTAL    87%

Please:
  1. Add tests to increase coverage
  2. Ensure coverage ≥ 90%
  3. Commit again

# ✅ ALLOWED
$ git commit -m "Add feature"
✓ Test coverage meets threshold (90%)
```

**Thresholds**:
- Relaxed: 70%
- Normal: 90%
- Strict: 95%

## Bypass Mechanisms

### Emergency Bypass (Use Sparingly!)

```bash
git commit --no-verify
```

**When to use**:
- Emergency hotfixes
- Work-in-progress commits on feature branches
- Exceptional circumstances documented in commit message

**Never bypass**:
- Main/master branch commits
- Release commits
- Merge commits

### Configuration Override

Edit `.pre-commit-config.yaml` to customize:

```yaml
repos:
  - repo: local
    hooks:
      - id: coverage-threshold
        entry: python tools/pre-commit-hooks/check-coverage-threshold.py
        args: ['--threshold=85', '--warn-only']  # Custom threshold
```

## Manual Execution

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run no-todos --all-files

# Run on staged files only
pre-commit run
```

## Integration with Standard Hooks

The framework configurations also include standard pre-commit hooks:

- **check-added-large-files**: Blocks files >500KB
- **check-yaml**: Validates YAML syntax
- **trailing-whitespace**: Removes trailing whitespace
- **black**: Python code formatting (line length: 100)
- **pylint**: Python linting
- **mypy**: Python type checking

See `.pre-commit-config.yaml` for full list.

## Troubleshooting

### Hook fails with "pytest not found"

```bash
pip install pytest pytest-cov
```

Coverage hook requires pytest with coverage plugin.

### Hook fails with "pre-commit not found"

```bash
pip install pre-commit
# or
brew install pre-commit
```

### "Configuration file not found" error

Run `install-hooks.sh` from project root, not from `tools/` directory:

```bash
# ❌ Wrong
cd tools/pre-commit-hooks
./install-hooks.sh

# ✅ Correct
./tools/pre-commit-hooks/install-hooks.sh
```

### Hooks not running on commit

```bash
# Reinstall hooks
pre-commit install

# Verify installation
pre-commit --version
ls -la .git/hooks/pre-commit
```

## Uninstallation

```bash
# Remove hooks
pre-commit uninstall

# Remove configuration
rm .pre-commit-config.yaml

# Optional: Remove backup
rm .pre-commit-config.yaml.bak
```

## Development

### Testing Hooks Locally

```bash
# Make hook executable
chmod +x tools/pre-commit-hooks/check-no-todos.py

# Run directly
python tools/pre-commit-hooks/check-no-todos.py src/main.py

# Test with pre-commit
pre-commit try-repo . no-todos --verbose --all-files
```

### Adding New Hooks

1. Create hook script in `tools/pre-commit-hooks/`
2. Make executable: `chmod +x <script>.py`
3. Add entry to `.pre-commit-hooks.yaml`:

```yaml
- id: my-custom-hook
  name: My Custom Hook
  description: What it checks
  entry: python tools/pre-commit-hooks/my-custom-hook.py
  language: system
  types: [python]
```

4. Add to configuration templates in `.claude/templates/`

## Best Practices

1. **Start with Relaxed mode** when learning the framework
2. **Progress to Normal mode** for active development
3. **Use Strict mode** for production-ready code
4. **Never bypass on main/master** - use feature branches for WIP
5. **Run manually before push** to catch issues early: `pre-commit run --all-files`
6. **Keep hooks fast** - they run on every commit
7. **Document bypass reasons** in commit message if absolutely necessary

## See Also

- [Pre-commit Framework Documentation](https://pre-commit.com/)
- [Claude Development Framework Rules](../../.claude/12-rules.md)
- [Framework Validation Guide](../../docs/FRAMEWORK-VALIDATION-GUIDE.md)
- [Enhancement Roadmap](../../ENHANCEMENT-ROADMAP.md)

## Version

**Version**: 1.0.0
**Last Updated**: 2025-10-03
**Compatible with**: Claude Development Framework v2.2+
