# claude-dev - Claude Development Framework CLI

A command-line interface for the Claude Development Framework that simplifies project initialization, specification generation, testing, planning, and quality checks.

**Version**: 1.0.0
**Part of**: Claude Development Framework v2.2

---

## Features

✅ **Project Initialization** - Create new projects with framework structure
✅ **Specification Generation** - Generate use cases, service specs, and ADRs from templates
✅ **Test Management** - Run tests, check coverage, generate tests from specs
✅ **Planning** - Create and manage iterations and milestones
✅ **Quality Checks** - Verify spec-code alignment, coverage, and code quality
✅ **Session Management** - Track development sessions with state files
✅ **Agent Integration** - Invoke framework agents (placeholder for future implementation)
✅ **Shell Completion** - Bash, Zsh, and Fish completion support

---

## Installation

### From Source (Development)

```bash
cd tools/claude-dev
pip install -e .
```

### From PyPI (Future)

```bash
pip install claude-dev
```

### Verify Installation

```bash
claude-dev --version
```

---

## Quick Start

### 1. Initialize a New Project

```bash
# Create new project
claude-dev init my-project

# Initialize with template
claude-dev init my-api --template api

# Initialize in specific path
claude-dev init my-project --path /path/to/parent
```

### 2. Create Your First Specification

```bash
cd my-project

# Create use case
claude-dev spec new use-case --id UC-001 --title "User Registration"

# Create service spec
claude-dev spec new service --id SVC-001 --title "Auth Service"

# Create ADR
claude-dev spec new adr --id ADR-001 --title "Database Selection"
```

### 3. Work with Tests

```bash
# Run all tests
claude-dev test run

# Run with coverage
claude-dev test run --coverage

# Check coverage threshold
claude-dev test coverage --fail-under 90
```

### 4. Quality Checks

```bash
# Check spec-code alignment
claude-dev check alignment

# Check all quality metrics
claude-dev check all
```

---

## Command Reference

### `claude-dev init`

Initialize a new Claude Development Framework project.

```bash
claude-dev init <project-name> [OPTIONS]

Options:
  --path PATH        Parent directory (default: current directory)
  --template TYPE    Project template (api|cli|data-pipeline|web|ml)
  --no-git           Skip git initialization
```

### `claude-dev spec`

Specification generation and management.

```bash
# Create new specification
claude-dev spec new <type> --id <ID> --title <TITLE> [OPTIONS]

Types: use-case, service, adr

Options:
  --edit    Open in editor after creation

# List specifications
claude-dev spec list [--type TYPE]

# Validate specification
claude-dev spec validate <spec-id>
```

### `claude-dev test`

Test generation and execution.

```bash
# Generate tests from spec (via agent)
claude-dev test generate <spec-id> [--type TYPE]

# Run tests
claude-dev test run [PATH] [OPTIONS]

Options:
  --coverage    Show coverage report
  --watch       Watch mode for TDD
  -v            Verbose output

# Check coverage
claude-dev test coverage [--fail-under THRESHOLD]
```

### `claude-dev plan`

Planning for iterations and milestones.

```bash
# Plan new iteration
claude-dev plan iteration [--milestone ID] [--scope TEXT]

# Plan new milestone
claude-dev plan milestone [--use-cases IDs] [--title TEXT]

# Show current iteration
claude-dev plan current

# List iterations
claude-dev plan list [--status active|completed|all]
```

### `claude-dev check`

Quality checks.

```bash
# Check spec-code alignment
claude-dev check alignment [--report]

# Check test coverage
claude-dev check coverage [--fail-under THRESHOLD]

# Check code quality (lint, format, type check)
claude-dev check quality [--fix]

# Run all checks
claude-dev check all
```

### `claude-dev session`

Session management.

```bash
# Start session
claude-dev session start [--iteration ID]

# End session
claude-dev session end [--summarize]

# Show session status
claude-dev session status
```

### `claude-dev agent`

Agent invocation (placeholder - integration coming soon).

```bash
# Invoke agent
claude-dev agent run <agent-name> [--spec ID] [--output PATH]

# List available agents
claude-dev agent list [--tier 1|2|3|all]

# Show agent info
claude-dev agent info <agent-name>
```

### `claude-dev completion`

Install shell completion.

```bash
# Auto-detect shell
claude-dev completion

# Specific shell
claude-dev completion --shell bash|zsh|fish
```

---

## Configuration

The CLI reads configuration from `.claude/cli-config.yaml`:

```yaml
project:
  name: my-project
  type: api
  version: 1.0.0

paths:
  specs: specs/
  src: src/
  tests: tests/
  planning: planning/
  status: status/
  research: research/

defaults:
  coverage_threshold: 90
  test_runner: pytest
  editor: vim
  auto_open_files: true

agents:
  enabled: true
  api_key: ${CLAUDE_API_KEY}
  default_model: claude-sonnet-4

quality:
  linter: pylint
  formatter: black
  type_checker: mypy
```

This file is created automatically when you run `claude-dev init`.

---

## Examples

### Complete Workflow Example

```bash
# 1. Initialize project
claude-dev init todo-api --template api
cd todo-api

# 2. Create first use case
claude-dev spec new use-case --id UC-001 --title "Create TODO Item" --edit

# 3. Start development session
claude-dev session start --iteration iteration-01

# 4. Generate tests (placeholder - currently manual)
# claude-dev test generate UC-001

# 5. Run tests
claude-dev test run --coverage

# 6. Check quality
claude-dev check all

# 7. End session
claude-dev session end
```

### Quality Gate in CI/CD

```bash
#!/bin/bash
# ci-quality-check.sh

set -e

echo "Running quality checks..."

# Check spec alignment
claude-dev check alignment

# Check coverage
claude-dev check coverage --fail-under 90

# Check code quality
claude-dev check quality

echo "✓ All quality checks passed!"
```

---

## Project Structure

The CLI creates the following project structure:

```
my-project/
├── .claude/
│   ├── cli-config.yaml      # CLI configuration
│   ├── CLAUDE.md             # Framework overview
│   ├── development-rules.md  # 12 Non-Negotiable Rules
│   ├── templates/            # Spec templates
│   ├── guides/               # Development guides
│   ├── quick-ref/            # Quick reference cards
│   └── agents/               # Agent definitions
├── specs/
│   ├── use-cases/            # Use case specifications
│   ├── services/             # Service specifications
│   └── adrs/                 # Architecture Decision Records
├── src/                      # Source code
├── tests/                    # Test files
├── planning/                 # Iteration and milestone plans
├── status/                   # Session state
├── research/                 # Research notes
└── README.md
```

---

## Requirements

### Runtime Dependencies

- Python >= 3.8
- click >= 8.0.0
- pyyaml >= 6.0
- jinja2 >= 3.0
- rich >= 13.0
- pytest >= 7.0
- coverage >= 7.0

### Optional Dependencies

For agent integration (coming soon):
- anthropic >= 0.18.0

### System Dependencies

For quality checks:
- pytest (test running)
- pytest-cov (coverage)
- pylint or flake8 (linting)
- black (formatting)
- mypy (type checking)

---

## Development

### Setup Development Environment

```bash
cd tools/claude-dev

# Install in editable mode
pip install -e .

# Install dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run tests (when implemented)
pytest tests/

# With coverage
pytest --cov=claude_dev tests/
```

### Code Quality

```bash
# Format code
black claude_dev/

# Lint
pylint claude_dev/

# Type check
mypy claude_dev/
```

---

## Roadmap

### Completed ✅

- [x] Core CLI framework
- [x] Project initialization
- [x] Specification commands
- [x] Test commands
- [x] Planning commands
- [x] Quality check commands
- [x] Session management
- [x] Shell completion

### In Progress 🚧

- [ ] Agent integration (via Claude API)
- [ ] Test suite for CLI (90%+ coverage)
- [ ] Integration with init-project.sh

### Future 📋

- [ ] Interactive project wizard
- [ ] Git workflow integration
- [ ] Template customization
- [ ] Plugin system
- [ ] Web UI dashboard

---

## Troubleshooting

### "Command not found: claude-dev"

Make sure the package is installed and your PATH includes Python's bin directory:

```bash
pip install -e .
# or
pip install claude-dev
```

### "Template directory not found"

The CLI looks for `.claude/templates/` by walking up from the current directory. Make sure you're in a Claude framework project or initialize a new one with `claude-dev init`.

### "Config file not found"

The CLI will use defaults if no config file is found. To create one:

```bash
claude-dev init my-project
# This creates .claude/cli-config.yaml
```

### Agent commands not working

Agent integration requires Claude API access and is not yet fully implemented. For now, invoke agents manually from a Claude session:

```
@agent-name perform task
```

---

## Contributing

This CLI is part of the Claude Development Framework. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## License

Part of the Claude Development Framework. Use freely, adapt as needed.

---

## Support

For issues, questions, or suggestions:

- **Documentation**: See `../docs/` for framework docs
- **Examples**: See `../docs/examples/` for usage examples
- **Issues**: Create an issue in the repository

---

## Version History

### v1.0.0 (2025-10-03)

- Initial release
- 7 command groups (init, spec, test, plan, check, session, agent)
- Shell completion support
- Configuration management
- Template rendering
- Quality checks

---

**Built with ❤️ for disciplined, spec-driven development with Claude**
