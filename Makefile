# Makefile for Claude Development Framework
# Version: 2.2
# Provides convenient targets for testing, quality checks, and development

.PHONY: help install install-dev install-hooks install-cli setup \
		test test-unit test-integration test-e2e test-performance test-fast test-watch test-coverage test-html test-markers \
		check check-alignment check-quality check-coverage check-todos check-adrs pre-commit \
		hooks-install hooks-run hooks-test-first hooks-no-todos hooks-alignment \
		cli-init cli-spec-uc cli-spec-service cli-spec-adr cli-plan cli-status \
		validate estimate-context init-project \
		clean clean-pyc clean-test clean-build clean-all \
		dev quick-test docs readme test-docs

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Python
PYTHON := python3
PIP := pip3

# Pytest
PYTEST := pytest
PYTEST_ARGS := -v
PYTEST_COV_ARGS := --cov=tests --cov-report=html --cov-report=term-missing

# Paths
TESTS_DIR := tests/agents
TOOLS_DIR := tools
SCRIPTS_DIR := scripts
HOOKS_DIR := tools/pre-commit-hooks

#=============================================================================
# Default Target
#=============================================================================

.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "$(BLUE)================================================================================================$(NC)"
	@echo "$(BLUE)  Claude Development Framework v2.2 - Make Targets$(NC)"
	@echo "$(BLUE)================================================================================================$(NC)"
	@echo ""
	@echo "$(GREEN)Setup & Installation:$(NC)"
	@awk '/^[a-zA-Z\-\_0-9]+:.*?##/ { if ($$0 ~ /^(install|setup)/) printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, substr($$0, index($$0, "##")+3) }' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)Testing (794 tests):$(NC)"
	@awk '/^[a-zA-Z\-\_0-9]+:.*?##/ { if ($$0 ~ /^test/) printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, substr($$0, index($$0, "##")+3) }' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)Quality Checks:$(NC)"
	@awk '/^[a-zA-Z\-\_0-9]+:.*?##/ { if ($$0 ~ /^(check|pre-commit|lint|format)/) printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, substr($$0, index($$0, "##")+3) }' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)Pre-commit Hooks:$(NC)"
	@awk '/^[a-zA-Z\-\_0-9]+:.*?##/ { if ($$0 ~ /^hooks/) printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, substr($$0, index($$0, "##")+3) }' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)Claude-dev CLI:$(NC)"
	@awk '/^[a-zA-Z\-\_0-9]+:.*?##/ { if ($$0 ~ /^cli/) printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, substr($$0, index($$0, "##")+3) }' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)Scripts & Utilities:$(NC)"
	@awk '/^[a-zA-Z\-\_0-9]+:.*?##/ { if ($$0 ~ /^(validate|estimate|init-project)/) printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, substr($$0, index($$0, "##")+3) }' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)Cleanup:$(NC)"
	@awk '/^[a-zA-Z\-\_0-9]+:.*?##/ { if ($$0 ~ /^clean/) printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, substr($$0, index($$0, "##")+3) }' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@awk '/^[a-zA-Z\-\_0-9]+:.*?##/ { if ($$0 ~ /^(dev|quick|docs|readme)/) printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, substr($$0, index($$0, "##")+3) }' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(BLUE)Examples:$(NC)"
	@echo "  make setup                    # Complete project setup"
	@echo "  make test                     # Run all 794 tests"
	@echo "  make test-fast                # Quick test run"
	@echo "  make check                    # Run quality checks"
	@echo "  make cli-spec-uc ID=UC-001 TITLE=\"User Login\"  # Create use case"
	@echo ""

#=============================================================================
# Setup & Installation
#=============================================================================

install: ## Install all dependencies (test + CLI)
	@echo "$(GREEN)Installing test dependencies...$(NC)"
	$(PIP) install -r requirements-test.txt
	@echo "$(GREEN)Installing claude-dev CLI...$(NC)"
	cd $(TOOLS_DIR)/claude-dev && $(PIP) install -e .
	@echo "$(GREEN)✓ Installation complete$(NC)"

install-dev: ## Install in development mode
	@echo "$(GREEN)Installing in development mode...$(NC)"
	$(PIP) install -e .
	$(PIP) install -r requirements-test.txt
	@echo "$(GREEN)✓ Development installation complete$(NC)"

install-hooks: ## Install pre-commit hooks
	@echo "$(GREEN)Installing pre-commit hooks...$(NC)"
	cd $(HOOKS_DIR) && bash install-hooks.sh
	@echo "$(GREEN)✓ Pre-commit hooks installed$(NC)"

install-cli: ## Install claude-dev CLI tool
	@echo "$(GREEN)Installing claude-dev CLI...$(NC)"
	cd $(TOOLS_DIR)/claude-dev && $(PIP) install -e .
	claude-dev --version
	@echo "$(GREEN)✓ CLI installed$(NC)"

setup: install install-hooks ## Complete project setup (install + hooks)
	@echo "$(GREEN)================================$(NC)"
	@echo "$(GREEN)✓ Setup complete!$(NC)"
	@echo "$(GREEN)================================$(NC)"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Run tests: make test"
	@echo "  2. See all commands: make help"

#=============================================================================
# Testing Targets
#=============================================================================

test: ## Run all agent tests (794 tests)
	@echo "$(GREEN)Running all agent tests (794 tests)...$(NC)"
	$(PYTEST) $(TESTS_DIR)/ $(PYTEST_ARGS)

test-unit: ## Run unit tests (Phases 1-4: 649 tests)
	@echo "$(GREEN)Running unit tests...$(NC)"
	$(PYTEST) $(TESTS_DIR)/unit/ $(PYTEST_ARGS)

test-integration: ## Run integration tests (Phase 5: 48 tests)
	@echo "$(GREEN)Running integration tests...$(NC)"
	$(PYTEST) $(TESTS_DIR)/integration/ $(PYTEST_ARGS)

test-e2e: ## Run e2e workflow tests (Phase 6: 35 tests)
	@echo "$(GREEN)Running e2e tests...$(NC)"
	$(PYTEST) $(TESTS_DIR)/e2e/ $(PYTEST_ARGS)

test-performance: ## Run performance tests (Phase 7: 62 tests)
	@echo "$(GREEN)Running performance tests...$(NC)"
	$(PYTEST) $(TESTS_DIR)/performance/ $(PYTEST_ARGS)

test-fast: ## Quick test run (quiet mode, no coverage)
	@echo "$(GREEN)Running quick test...$(NC)"
	$(PYTEST) $(TESTS_DIR)/ -q --tb=no

test-watch: ## Run tests in watch mode (TDD)
	@echo "$(GREEN)Starting watch mode (press Ctrl+C to exit)...$(NC)"
	$(PYTEST) $(TESTS_DIR)/ --looponfail

test-coverage: ## Run tests with coverage report
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	$(PYTEST) $(TESTS_DIR)/ $(PYTEST_ARGS) $(PYTEST_COV_ARGS)

test-html: ## Generate HTML coverage report
	@echo "$(GREEN)Generating HTML coverage report...$(NC)"
	$(PYTEST) $(TESTS_DIR)/ $(PYTEST_COV_ARGS)
	@echo "$(GREEN)✓ Coverage report: htmlcov/index.html$(NC)"

test-markers: ## Run tests by marker (usage: make test-markers MARKER=unit)
	@echo "$(GREEN)Running tests with marker: $(MARKER)$(NC)"
	$(PYTEST) $(TESTS_DIR)/ -m $(MARKER) $(PYTEST_ARGS)

#=============================================================================
# Quality Check Targets
#=============================================================================

check: check-todos check-alignment ## Run all quality checks
	@echo "$(GREEN)✓ All quality checks passed$(NC)"

check-alignment: ## Check spec-code alignment
	@echo "$(GREEN)Checking spec-code alignment...$(NC)"
	$(PYTHON) $(HOOKS_DIR)/check-spec-alignment.py

check-quality: ## Check code quality (placeholder for linters)
	@echo "$(YELLOW)Code quality check (configure linters if needed)$(NC)"

check-coverage: ## Check coverage threshold
	@echo "$(GREEN)Checking coverage threshold...$(NC)"
	$(PYTHON) $(HOOKS_DIR)/check-coverage-threshold.py

check-todos: ## Check for TODO comments
	@echo "$(GREEN)Checking for TODO comments...$(NC)"
	$(PYTHON) $(HOOKS_DIR)/check-no-todos.py

check-adrs: ## Check ADR references
	@echo "$(GREEN)Checking ADR references...$(NC)"
	$(PYTHON) $(HOOKS_DIR)/check-adr-references.py

pre-commit: check-todos ## Run pre-commit validation
	@echo "$(GREEN)Running pre-commit checks...$(NC)"
	@echo "$(GREEN)✓ Pre-commit checks passed$(NC)"

#=============================================================================
# Pre-commit Hook Targets
#=============================================================================

hooks-install: install-hooks ## Install pre-commit hooks

hooks-run: ## Run all pre-commit hooks
	@echo "$(GREEN)Running all pre-commit hooks...$(NC)"
	cd $(HOOKS_DIR) && pre-commit run --all-files || true

hooks-test-first: ## Run test-first enforcement hook
	@echo "$(GREEN)Running test-first hook...$(NC)"
	$(PYTHON) $(HOOKS_DIR)/check-test-first.py

hooks-no-todos: ## Run no-todos hook
	@echo "$(GREEN)Running no-todos hook...$(NC)"
	$(PYTHON) $(HOOKS_DIR)/check-no-todos.py

hooks-alignment: ## Run spec-alignment hook
	@echo "$(GREEN)Running spec-alignment hook...$(NC)"
	$(PYTHON) $(HOOKS_DIR)/check-spec-alignment.py

#=============================================================================
# Claude-dev CLI Targets
#=============================================================================

cli-init: ## Initialize new project (usage: make cli-init PROJECT=myapp)
	@if [ -z "$(PROJECT)" ]; then \
		echo "$(RED)Error: PROJECT not set. Usage: make cli-init PROJECT=myapp$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Initializing project: $(PROJECT)$(NC)"
	claude-dev init $(PROJECT)

cli-spec-uc: ## Create use case (usage: make cli-spec-uc ID=UC-001 TITLE="User Login")
	@if [ -z "$(ID)" ] || [ -z "$(TITLE)" ]; then \
		echo "$(RED)Error: ID or TITLE not set. Usage: make cli-spec-uc ID=UC-001 TITLE=\"User Login\"$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Creating use case: $(ID) - $(TITLE)$(NC)"
	claude-dev spec new use-case --id $(ID) --title "$(TITLE)"

cli-spec-service: ## Create service spec (usage: make cli-spec-service ID=SVC-001 TITLE="Auth Service")
	@if [ -z "$(ID)" ] || [ -z "$(TITLE)" ]; then \
		echo "$(RED)Error: ID or TITLE not set. Usage: make cli-spec-service ID=SVC-001 TITLE=\"Auth Service\"$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Creating service spec: $(ID) - $(TITLE)$(NC)"
	claude-dev spec new service --id $(ID) --title "$(TITLE)"

cli-spec-adr: ## Create ADR (usage: make cli-spec-adr ID=ADR-001 TITLE="Database Choice")
	@if [ -z "$(ID)" ] || [ -z "$(TITLE)" ]; then \
		echo "$(RED)Error: ID or TITLE not set. Usage: make cli-spec-adr ID=ADR-001 TITLE=\"Database Choice\"$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Creating ADR: $(ID) - $(TITLE)$(NC)"
	claude-dev spec new adr --id $(ID) --title "$(TITLE)"

cli-plan: ## Show current iteration plan
	@echo "$(GREEN)Current iteration plan:$(NC)"
	claude-dev plan current || echo "$(YELLOW)No active iteration$(NC)"

cli-status: ## Show session status
	@echo "$(GREEN)Session status:$(NC)"
	claude-dev session status || echo "$(YELLOW)No active session$(NC)"

#=============================================================================
# Scripts & Utilities
#=============================================================================

validate: ## Run template validation
	@echo "$(GREEN)Validating template...$(NC)"
	bash validate-template.sh

estimate-context: ## Estimate context window usage
	@echo "$(GREEN)Estimating context usage...$(NC)"
	bash $(SCRIPTS_DIR)/estimate-context.sh

init-project: ## Initialize new project from template (usage: make init-project PROJECT=myapp)
	@if [ -z "$(PROJECT)" ]; then \
		echo "$(RED)Error: PROJECT not set. Usage: make init-project PROJECT=myapp$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Initializing project: $(PROJECT)$(NC)"
	bash init-project.sh $(PROJECT)

#=============================================================================
# Cleanup Targets
#=============================================================================

clean: clean-pyc clean-test ## Clean all artifacts

clean-pyc: ## Remove Python artifacts
	@echo "$(GREEN)Cleaning Python artifacts...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name "*.pyo" -delete 2>/dev/null || true
	find . -name "*~" -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Python artifacts cleaned$(NC)"

clean-test: ## Remove test artifacts
	@echo "$(GREEN)Cleaning test artifacts...$(NC)"
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf coverage.xml
	@echo "$(GREEN)✓ Test artifacts cleaned$(NC)"

clean-build: ## Remove build artifacts
	@echo "$(GREEN)Cleaning build artifacts...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	@echo "$(GREEN)✓ Build artifacts cleaned$(NC)"

clean-all: clean clean-build ## Deep clean (all artifacts)
	@echo "$(GREEN)✓ Deep clean complete$(NC)"

#=============================================================================
# Development Targets
#=============================================================================

dev: ## Start development mode (watch tests)
	@echo "$(GREEN)Starting development mode...$(NC)"
	@echo "$(YELLOW)Running tests in watch mode. Press Ctrl+C to exit.$(NC)"
	$(PYTEST) $(TESTS_DIR)/ --looponfail

quick-test: test-fast ## Quick smoke test (alias for test-fast)

docs: ## Open documentation
	@echo "$(GREEN)Opening documentation...$(NC)"
	@if command -v open &> /dev/null; then \
		open README.md; \
	elif command -v xdg-open &> /dev/null; then \
		xdg-open README.md; \
	else \
		echo "$(YELLOW)Please open README.md manually$(NC)"; \
	fi

readme: docs ## Open README.md (alias for docs)

test-docs: ## Open test suite documentation
	@echo "$(GREEN)Opening test documentation...$(NC)"
	@if command -v open &> /dev/null; then \
		open tests/README.md; \
	elif command -v xdg-open &> /dev/null; then \
		xdg-open tests/README.md; \
	else \
		echo "$(YELLOW)Please open tests/README.md manually$(NC)"; \
	fi

#=============================================================================
# Version Info
#=============================================================================

version: ## Show framework version
	@echo "$(BLUE)Claude Development Framework$(NC)"
	@echo "Version: 2.2 (Agent Ecosystem + Comprehensive Test Suite)"
	@echo "Last Updated: 2025-10-03"
	@echo ""
	@echo "Test Suite: 794 tests"
	@echo "Agent Library: 18 agents"
	@if command -v claude-dev &> /dev/null; then \
		echo ""; \
		claude-dev --version; \
	fi
