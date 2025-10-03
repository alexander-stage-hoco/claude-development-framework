# Agent Test Suite - Documentation

**Version**: 1.0
**Last Updated**: 2025-10-03
**Framework Version**: v2.2 (includes Agent Test Suite)

---

## Overview

Comprehensive test suite validating the Claude Development Framework's 18 agents across metadata, structure, behavior, integration, workflows, and performance.

**Total Tests**: 794
**Coverage**: Metadata (131) + Structure (309) + Behavioral (209) + Integration (48) + E2E (35) + Performance (62)
**Runtime**: <1 second for full suite

---

## Test Organization

### Phase 1-2: Metadata & Structure Validation (440 tests)
**Location**: `tests/agents/unit/`

- `test_agent_metadata.py` (131 tests) - YAML front matter validation
- `test_agent_structure.py` (309 tests) - Markdown structure & content quality

**What**: Validates all 18 agents have correct metadata and required sections

**Run**: `pytest tests/agents/unit/test_agent_metadata.py tests/agents/unit/test_agent_structure.py -v`

---

### Phase 4: Behavioral Tests - Tier 1 Agents (209 tests)
**Location**: `tests/agents/unit/`

6 test files for critical agents:
- `test_test_writer_agent.py` (31 tests)
- `test_uc_writer_agent.py` (40 tests)
- `test_bdd_scenario_writer_agent.py` (30 tests)
- `test_code_quality_checker_agent.py` (40 tests)
- `test_refactoring_analyzer_agent.py` (36 tests)
- `test_adr_manager_agent.py` (52 tests)

**What**: Validates agent-specific behaviors, quality checks, examples

**Run**: `pytest tests/agents/unit/test_*_agent.py -v`

---

### Phase 5: Integration Tests - Agent Chains (48 tests)
**Location**: `tests/agents/integration/`

3 integration test files:
- `test_uc_to_bdd_to_test_chain.py` (27 tests) - Complete UC → BDD → Test workflow
- `test_tdd_cycle_chain.py` (16 tests) - RED → GREEN → REFACTOR validation
- `test_adr_compliance_chain.py` (15 tests) - ADR creation & enforcement

**What**: Validates multi-agent workflows and handoffs

**Run**: `pytest tests/agents/integration/ -v`

---

### Phase 6: E2E Workflow Tests (35 tests)
**Location**: `tests/agents/e2e/`

3 end-to-end workflow files:
- `test_feature_development_workflow.py` (9 tests) - Complete feature workflows
- `test_iteration_workflow.py` (14 tests) - Iteration planning & MVP delivery
- `test_service_creation_workflow.py` (12 tests) - Service-oriented architecture

**What**: Validates complete development workflows from idea to commit

**Run**: `pytest tests/agents/e2e/ -v`

---

### Phase 7: Performance Tests (62 tests)
**Location**: `tests/agents/performance/`

3 performance/consistency files:
- `test_agent_context_usage.py` (14 tests) - Context efficiency validation
- `test_agent_consistency.py` (21 tests) - Cross-agent consistency
- `test_coverage_analysis.py` (27 tests) - Test suite completeness

**What**: Validates agent efficiency, consistency, and test coverage

**Run**: `pytest tests/agents/performance/ -v`

---

## Running Tests

### Quick Start
```bash
# Run all tests
pytest tests/agents/ -v

# Run specific phase
pytest tests/agents/unit/ -v           # Phases 1-4
pytest tests/agents/integration/ -v    # Phase 5
pytest tests/agents/e2e/ -v            # Phase 6
pytest tests/agents/performance/ -v    # Phase 7

# Run with coverage
pytest tests/agents/ --cov=tests --cov-report=html

# Quiet mode (summary only)
pytest tests/agents/ -q
```

### Test Markers
Tests use pytest markers for organization:
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.performance` - Performance tests

Run specific marker:
```bash
pytest tests/agents/ -m "unit" -v
pytest tests/agents/ -m "e2e" -v
```

---

## Test Fixtures

### Core Fixtures
**Location**: `tests/agents/fixtures/`

- **AgentParser** - Parse agent markdown files, extract sections
- **MockFileSystem** - Mock file operations for testing
- **MockGitRepo** - Mock git operations
- **get_all_agent_paths()** - Get paths to all agent files

**Usage**:
```python
from tests.agents.fixtures import AgentParser, MockFileSystem

def test_example(tmp_path):
    parser = AgentParser(Path(".claude/subagents/test-writer.md"))
    mock_fs = MockFileSystem(tmp_path)
```

---

## Notes

### Agent-Agnostic Design
Performance tests gracefully skip when no agent files are present (this is a template repository, not an agent-based project).

3 tests skip with message: "No agent files found (not an agent-based project)"

### Test Philosophy
- **Fast**: All 794 tests run in <1 second
- **Isolated**: Each test is independent
- **Realistic**: Uses actual agent files when present
- **Graceful**: Skips appropriately for template repos

---

## CI/CD Integration

### GitHub Actions (Recommended)
Add to `.github/workflows/test-agents.yml`:

```yaml
name: Agent Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: pip install pytest pytest-cov pyyaml
      - run: pytest tests/agents/ -v --cov=tests --cov-report=xml
      - uses: codecov/codecov-action@v3
```

### Pre-commit Hook
Add to `.pre-commit-config.yaml`:

```yaml
  - repo: local
    hooks:
      - id: agent-tests
        name: Run agent test suite
        entry: pytest tests/agents/ -q
        language: system
        pass_filenames: false
```

---

## Maintenance

### Adding New Tests
1. Choose appropriate phase/directory
2. Follow existing naming convention (`test_*.py`)
3. Use appropriate pytest marker
4. Add docstrings to all test functions
5. Use fixtures from `tests/agents/fixtures/`

### Extending Fixtures
Edit `tests/agents/fixtures/agent_parser.py` or `mock_helpers.py`

Export new fixtures in `tests/agents/fixtures/__init__.py`

---

**Last Updated**: 2025-10-03
**Test Count**: 794
**Phases**: 1-7 (Complete)
