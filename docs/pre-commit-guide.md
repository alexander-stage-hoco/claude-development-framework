# Pre-commit Hooks Guide
## Automated Framework Discipline

**Version**: 1.0.0
**Last Updated**: 2025-10-03
**Applies to**: Claude Development Framework v2.1+

---

## Table of Contents

1. [Introduction](#introduction)
2. [Why Pre-commit Hooks?](#why-pre-commit-hooks)
3. [Installation](#installation)
4. [Configuration Levels](#configuration-levels)
5. [Hook Reference](#hook-reference)
6. [Workflow Integration](#workflow-integration)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Usage](#advanced-usage)
9. [FAQ](#faq)

---

## Introduction

Pre-commit hooks are automated checks that run before each Git commit. The Claude Development Framework provides custom hooks that enforce the [12 Non-Negotiable Rules](../.claude/12-rules.md), preventing violations from entering your codebase.

### What Gets Checked

Every commit is automatically validated for:

- **Specification Alignment** (Rule #1) - UC references must have spec files
- **Test Coverage** (Rule #2) - Minimum coverage thresholds enforced
- **Test-First Development** (Rule #2) - Source files must have tests
- **No Shortcuts** (Rule #6) - TODO comments are blocked
- **Technical Decisions** (Rule #7) - ADR references must be valid

### Benefits

✅ **Catch violations early** - Before they enter version control
✅ **Consistent discipline** - Automated enforcement across team
✅ **Faster reviews** - Less time checking basic compliance
✅ **Learning aid** - Immediate feedback on framework rules
✅ **Quality gates** - Progressive strictness as projects mature

---

## Why Pre-commit Hooks?

### The Problem: Discipline Drift

Even with the best intentions, developers skip steps under pressure:

```python
# 😰 Under deadline pressure...
def process_payment(amount):
    # TODO: Add validation later
    # TODO: Add error handling
    # TODO: Write tests
    charge_card(amount)
    return True  # Hope for the best!
```

Without enforcement, "later" never comes. Technical debt accumulates.

### The Solution: Automation

Pre-commit hooks enforce discipline **before** code enters version control:

```bash
$ git commit -m "Add payment processing"

❌ TODO comments found!
  src/billing/payment.py:
    Line 3: # TODO: Add validation later
    Line 4: # TODO: Add error handling

❌ Source files without tests!
  src/billing/payment.py
    Create: tests/unit/test_payment.py

❌ Test coverage below 90%!
  TOTAL: 45%

Commit blocked. Please fix violations.
```

### Framework Alignment

Pre-commit hooks operationalize the framework's core principles:

| Framework Rule | How Hooks Enforce It |
|----------------|----------------------|
| #1: Specifications Are Law | Block commits with UC references but no spec files |
| #2: Tests Define Correctness | Require tests for all source files, enforce coverage |
| #6: No Shortcuts | Block TODO comments, force proper planning |
| #7: Technical Decisions Are Binding | Validate ADR references point to real files |

### Progressive Enforcement

Three strictness levels support learning → mastery:

1. **Relaxed** - Learn framework rules with gentle warnings
2. **Normal** - Balanced enforcement for active development
3. **Strict** - Maximum discipline for production code

---

## Installation

### Prerequisites

```bash
# Install pre-commit framework
pip install pre-commit

# Verify installation
pre-commit --version
# Output: pre-commit 3.x.x
```

### Install Framework Hooks

From your project root:

```bash
./tools/pre-commit-hooks/install-hooks.sh
```

You'll be prompted to choose a configuration level:

```
Choose configuration level:
  1) Relaxed  - For learning and early-stage projects
  2) Normal   - Recommended for most projects (default)
  3) Strict   - Maximum enforcement for production

Select [1/2/3] (default: 2): 2
```

The installer will:

1. ✅ Check pre-commit is installed
2. ✅ Copy configuration to `.pre-commit-config.yaml`
3. ✅ Make hook scripts executable
4. ✅ Install Git hooks
5. ✅ Optionally run on all files

### Verify Installation

```bash
# Check hooks are installed
ls -la .git/hooks/pre-commit

# Run hooks manually
pre-commit run --all-files
```

---

## Configuration Levels

### Relaxed Mode

**Use when**: Learning the framework, early-stage projects, prototyping

**Characteristics**:
- Coverage threshold: **70%**
- Most checks in **warning mode** (don't block)
- Auto-fix enabled for formatting
- Skips strict linting and type checking

**Sample output**:
```bash
$ git commit -m "WIP feature"

⚠️  Warning: Test coverage below 70% (68%)
⚠️  Warning: Missing tests for src/utils.py
✓ No TODO comments
✓ Spec alignment OK

[main abc1234] WIP feature  # Commit succeeds with warnings
```

**Configuration file**: `.claude/templates/pre-commit-config-relaxed.yaml`

### Normal Mode (Recommended)

**Use when**: Active development on most projects

**Characteristics**:
- Coverage threshold: **90%**
- Most checks enforced, some allow **≤1-2 violations**
- Auto-fix for formatting
- Standard linting and type checking

**Sample output**:
```bash
$ git commit -m "Add user service"

❌ Test coverage below 90%! (87%)
  src/services/user_service.py: 45% coverage

Please:
  1. Add tests to increase coverage
  2. Ensure coverage ≥ 90%
  3. Commit again

Commit blocked.  # Must fix to proceed
```

**Configuration file**: `.claude/templates/pre-commit-config.yaml`

### Strict Mode

**Use when**: Production-ready code, mature projects, main/master branch

**Characteristics**:
- Coverage threshold: **95%**
- **All checks strictly enforced** (zero violations)
- Formatting in check mode (fails if not formatted)
- Full pylint (not just errors)
- Bandit security scanning
- No `print()` statements in source code

**Sample output**:
```bash
$ git commit -m "Release v1.0"

❌ Code not formatted!
  Run: black src/

❌ Test coverage below 95%! (93%)
❌ Print statement found!
  src/debug/logger.py:42: print(f"Debug: {data}")

Commit blocked.  # Zero tolerance for violations
```

**Configuration file**: `.claude/templates/pre-commit-config-strict.yaml`

### Switching Levels

```bash
# Copy desired configuration
cp .claude/templates/pre-commit-config-strict.yaml .pre-commit-config.yaml

# Reinstall hooks
pre-commit install

# Run to verify
pre-commit run --all-files
```

---

## Hook Reference

### 1. No TODO Comments (`no-todos`)

**Purpose**: Enforce Rule #6 (No Shortcuts) by blocking TODO comments

**Rationale**: TODO comments become technical debt. The framework requires proper planning through specs or tickets.

**What it checks**:
```python
# ❌ BLOCKED
def process_data(data):
    # TODO: Add validation
    # TODO: Handle edge cases
    return transform(data)

# ✅ ALLOWED - Use specs instead
def process_data(data):
    """Process data according to UC-042.

    Validation: See UC-043-validate-input.md
    Edge cases: See specs/use-cases/UC-042-*.md § Edge Cases
    """
    return transform(data)
```

**Configuration**:
```yaml
- id: no-todos
  entry: python tools/pre-commit-hooks/check-no-todos.py
  language: system
  types: [python]
  exclude: '^(tests/|docs/)'  # Allowed in tests/docs
```

**Bypass patterns** (when absolutely necessary):
```python
# HACK: Quick fix for production issue (ticket: PROJ-123)
# NOTE: This is a known limitation, see ADR-015
# FIXME: Will be addressed in refactor (milestone: v2.0)
```

### 2. Spec Alignment (`spec-alignment`)

**Purpose**: Enforce Rule #1 (Specifications Are Law) by validating UC references

**Rationale**: Every UC reference in code must have a corresponding specification file. This ensures traceability and prevents orphaned references.

**What it checks**:
```python
# ❌ BLOCKED - No specs/use-cases/UC-042-*.md exists
def create_user(data):
    """Create new user (UC-042)."""
    pass

# ✅ ALLOWED - specs/use-cases/UC-042-create-user.md exists
def create_user(data):
    """Create new user (UC-042)."""
    pass
```

**Modes**:
- **Normal**: Warns if ≤2 missing specs (doesn't block)
- **Strict**: Blocks any missing specs

**Configuration**:
```yaml
- id: spec-alignment
  entry: python tools/pre-commit-hooks/check-spec-alignment.py
  args: ['--strict']  # Optional: strict mode
  pass_filenames: false
  always_run: true
```

### 3. Test-First Development (`test-first`)

**Purpose**: Enforce Rule #2 (Tests Define Correctness) via TDD

**Rationale**: Tests must be written before implementation. This hook ensures every source file has a corresponding test file.

**What it checks**:
```bash
# ❌ BLOCKED - No tests/unit/test_user_service.py
git add src/services/user_service.py
git commit -m "Add user service"

# ✅ ALLOWED - Test file exists
git add tests/unit/test_user_service.py
git add src/services/user_service.py
git commit -m "Add user service with tests"
```

**Skipped files**:
- `__init__.py` (typically just imports)
- `__main__.py` (entry point)
- `config.py` (configuration only)
- Files with <10 non-comment lines

**Modes**:
- **Normal**: Allows ≤1 untested file
- **Strict**: Blocks any untested files

**Configuration**:
```yaml
- id: test-first
  entry: python tools/pre-commit-hooks/check-test-first.py
  types: [python]
  exclude: '^(tests/|docs/|scripts/)'
```

### 4. ADR References (`adr-references`)

**Purpose**: Enforce Rule #7 (Technical Decisions Are Binding) by validating ADRs

**Rationale**: Architecture Decision Records must exist for all references in code. This ensures decisions are documented and traceable.

**What it checks**:
```python
# ❌ BLOCKED - No specs/adrs/ADR-015-*.md exists
# Uses Redis for caching (ADR-015)

# ✅ ALLOWED - specs/adrs/ADR-015-caching-strategy.md exists
# Uses Redis for caching (ADR-015)
```

**Modes**:
- **Normal**: Warns if ≤2 missing ADRs
- **Strict**: Blocks any missing ADRs

**Configuration**:
```yaml
- id: adr-references
  entry: python tools/pre-commit-hooks/check-adr-references.py
  types: [python]
```

### 5. Coverage Threshold (`coverage-threshold`)

**Purpose**: Enforce Rule #2 (Tests Define Correctness) via coverage metrics

**Rationale**: High test coverage ensures correctness. This hook blocks commits that drop coverage below the threshold.

**What it checks**:
```bash
$ pytest --cov=src --cov-report=term-missing

----------- coverage: platform darwin, python 3.11 -----------
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
src/services/user.py        45      5    89%   23-27
------------------------------------------------------
TOTAL                      234     12    95%

❌ Coverage below threshold (95%)
```

**Thresholds**:
- Relaxed: **70%**
- Normal: **90%**
- Strict: **95%**

**Configuration**:
```yaml
- id: coverage-threshold
  entry: python tools/pre-commit-hooks/check-coverage-threshold.py
  args: ['--threshold=90']  # Override default
  pass_filenames: false
  always_run: true
```

**Warning mode** (for gradual adoption):
```yaml
args: ['--threshold=90', '--warn-only']  # Warn but don't block
```

---

## Workflow Integration

### Daily Development

```bash
# 1. Write failing test (TDD)
vim tests/unit/test_user_service.py

# 2. Implement to make test pass
vim src/services/user_service.py

# 3. Commit (hooks run automatically)
git add tests/unit/test_user_service.py
git add src/services/user_service.py
git commit -m "Add user creation (UC-042)"

# Hooks run:
# ✓ No TODO comments
# ✓ Spec alignment (UC-042)
# ✓ Test file exists
# ✓ Coverage ≥ 90%
# ✓ Black formatting
# ✓ Pylint checks

[main abc1234] Add user creation (UC-042)
```

### Handling Failures

**Scenario 1: Coverage too low**

```bash
$ git commit -m "Add feature"

❌ Test coverage below 90%! (87%)
  src/services/payment.py: 45% coverage
    Missing: Lines 23-27, 34-39

Please:
  1. Add tests to increase coverage
  2. Ensure coverage ≥ 90%
  3. Commit again
```

**Fix**:
```bash
# Add more tests
vim tests/unit/test_payment.py

# Run coverage to verify
pytest --cov=src/services/payment.py --cov-report=term-missing

# Commit again
git add tests/unit/test_payment.py
git commit -m "Add feature with tests"
# ✓ Coverage now 92%
```

**Scenario 2: Missing spec**

```bash
$ git commit -m "Add payment processing"

❌ Missing spec files!
  src/billing/payment.py: UC-050
    Expected: specs/use-cases/UC-050-*.md
```

**Fix**:
```bash
# Create spec first
claude-dev spec uc 50 "Process Payment"

# Update code reference if needed
git add specs/use-cases/UC-050-process-payment.md
git commit -m "Add payment processing (UC-050)"
```

### Feature Branch Workflow

```bash
# Create feature branch
git checkout -b feature/user-management

# Work with relaxed enforcement during development
cp .claude/templates/pre-commit-config-relaxed.yaml .pre-commit-config.yaml
pre-commit install

# Develop iteratively (warnings OK)
git commit -m "WIP: User service skeleton"
git commit -m "WIP: Add user tests"
git commit -m "WIP: Implement user creation"

# Before merging: Switch to strict mode
cp .claude/templates/pre-commit-config-strict.yaml .pre-commit-config.yaml

# Ensure all checks pass
pre-commit run --all-files

# ✓ All checks pass - ready for PR
git push origin feature/user-management
```

### CI/CD Integration

Run hooks in CI to enforce compliance:

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - name: Install dependencies
        run: pip install pre-commit
      - name: Run pre-commit
        run: pre-commit run --all-files
```

---

## Troubleshooting

### Problem: Hooks not running

**Symptoms**:
```bash
$ git commit -m "Test"
[main abc1234] Test  # No hooks ran!
```

**Diagnosis**:
```bash
# Check if hooks installed
ls -la .git/hooks/pre-commit
# Should show: -rwxr-xr-x  ... pre-commit

# Check pre-commit version
pre-commit --version
```

**Fix**:
```bash
# Reinstall hooks
pre-commit install

# Verify
pre-commit run --all-files
```

### Problem: "pytest not found"

**Symptoms**:
```bash
❌ pytest not found (skipping coverage check)
```

**Fix**:
```bash
pip install pytest pytest-cov
```

### Problem: "Configuration file not found"

**Symptoms**:
```bash
❌ Configuration file not found: .claude/templates/pre-commit-config.yaml
Are you in a Claude Development Framework project?
```

**Diagnosis**: Not in project root or framework not initialized

**Fix**:
```bash
# Ensure you're in project root
cd /path/to/project

# Initialize framework if needed
claude-dev init

# Install hooks from root
./tools/pre-commit-hooks/install-hooks.sh
```

### Problem: Hook fails but no clear error

**Diagnosis**: Run hook directly for detailed output

```bash
# Run specific hook with verbose output
python tools/pre-commit-hooks/check-spec-alignment.py --verbose

# Or use pre-commit's verbose mode
pre-commit run spec-alignment --verbose --all-files
```

### Problem: Too slow on large repos

**Symptoms**: Commits take >10 seconds

**Optimization**:

1. **Limit file scope**:
```yaml
# Only run coverage on changed files, not all
- id: coverage-threshold
  files: '^src/.*\.py$'  # Only src/ changes
```

2. **Skip expensive checks in normal commits**:
```yaml
- id: coverage-threshold
  stages: [push]  # Only run on push, not commit
```

3. **Use relaxed mode for local development**:
```bash
cp .claude/templates/pre-commit-config-relaxed.yaml .pre-commit-config.yaml
```

### Problem: Want to bypass one hook but not all

**Use `SKIP` environment variable**:

```bash
# Skip coverage check for this commit only
SKIP=coverage-threshold git commit -m "WIP: Refactoring"

# Skip multiple hooks
SKIP=coverage-threshold,test-first git commit -m "WIP"
```

---

## Advanced Usage

### Custom Threshold per Project

Create project-specific override:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: coverage-threshold
        entry: python tools/pre-commit-hooks/check-coverage-threshold.py
        args: ['--threshold=85']  # Custom for this project
```

### Different Configs per Branch

```bash
# main branch: strict mode
git checkout main
cp .claude/templates/pre-commit-config-strict.yaml .pre-commit-config.yaml
pre-commit install

# feature branches: normal mode
git checkout -b feature/new-thing
cp .claude/templates/pre-commit-config.yaml .pre-commit-config.yaml
pre-commit install
```

### Auto-update Hooks

```bash
# Update to latest versions of dependencies
pre-commit autoupdate

# Review changes
git diff .pre-commit-config.yaml

# Test updated hooks
pre-commit run --all-files
```

### Custom Hooks

Add project-specific hooks:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: no-debug-imports
        name: Block debug imports
        entry: python tools/custom-hooks/check-no-debug.py
        language: system
        types: [python]
```

```python
# tools/custom-hooks/check-no-debug.py
#!/usr/bin/env python3
import sys
import re

for filepath in sys.argv[1:]:
    with open(filepath) as f:
        if re.search(r'^import (pdb|ipdb)', f.read(), re.M):
            print(f"❌ Debug import found in {filepath}")
            sys.exit(1)

sys.exit(0)
```

---

## FAQ

### Q: Can I use these hooks without the full framework?

**A**: Yes, but they assume framework structure:
- `specs/use-cases/` for UC references
- `specs/adrs/` for ADR references
- `src/` for source code
- `tests/` for tests

Without this structure, some hooks will skip checks.

### Q: Do hooks slow down my workflow?

**A**: Minimal impact for most projects:
- TODO check: <100ms
- Spec alignment: <500ms
- Test-first: <200ms
- Coverage: 2-5s (runs full test suite)

Use relaxed mode or `SKIP` for WIP commits if needed.

### Q: Can I commit without tests during prototyping?

**A**: Yes, two options:

1. **Use relaxed mode** (recommended):
   ```bash
   cp .claude/templates/pre-commit-config-relaxed.yaml .pre-commit-config.yaml
   ```

2. **Bypass for specific commits** (use sparingly):
   ```bash
   git commit --no-verify -m "WIP: Prototype"
   ```

### Q: What if a spec doesn't exist yet?

**A**: Create spec first (framework principle):

```bash
# Create spec
claude-dev spec uc 42 "Create User"

# Then implement
vim src/services/user_service.py

# Commit both
git add specs/use-cases/UC-042-create-user.md src/services/user_service.py
git commit -m "Add user creation (UC-042)"
```

### Q: Can I disable specific hooks?

**A**: Yes, comment out in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      # - id: coverage-threshold  # Disabled
      - id: no-todos
      - id: spec-alignment
```

### Q: Do hooks work with other languages?

**A**: Framework hooks are Python-specific, but pre-commit supports many languages:

```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.50.0
    hooks:
      - id: eslint
        files: \.[jt]sx?$  # JavaScript/TypeScript
```

### Q: How do I share configuration across team?

**A**: Commit `.pre-commit-config.yaml` to version control:

```bash
git add .pre-commit-config.yaml
git commit -m "Add pre-commit configuration"
git push

# Team members install
git pull
pre-commit install
```

---

## Summary

Pre-commit hooks automate framework discipline, catching violations before they enter version control. They're a force multiplier for team quality:

✅ **Automatic enforcement** - No manual review needed for basic compliance
✅ **Immediate feedback** - Learn framework rules through practice
✅ **Progressive adoption** - Start relaxed, ramp to strict
✅ **Team consistency** - Same standards for everyone
✅ **Faster reviews** - Focus on logic, not formatting/coverage

**Quick Start**:
```bash
./tools/pre-commit-hooks/install-hooks.sh
```

**Learn More**:
- [Hook Package README](../tools/pre-commit-hooks/README.md)
- [12 Non-Negotiable Rules](../.claude/12-rules.md)
- [Pre-commit Framework Docs](https://pre-commit.com/)

**Next Steps**:
1. Install hooks with normal mode
2. Commit something (experience automatic checks)
3. Switch to strict mode before merging to main
4. Share configuration with team

---

**Questions or Issues?**
See [Enhancement Roadmap](../ENHANCEMENT-ROADMAP.md) or create a ticket.
