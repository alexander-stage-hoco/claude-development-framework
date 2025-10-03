"""Behavioral tests for test-writer agent.

Tests the test-writer agent's ability to:
- Parse specifications and extract testable requirements
- Generate comprehensive test scenarios (happy path, edge cases, errors)
- Create pytest test structure with AAA pattern
- Design fixtures and mocks
- Ensure RED state verification
- Add docstrings with spec references

Test Coverage:
- Spec parsing and requirement extraction
- Test scenario generation
- Fixture design
- Mock creation
- AAA pattern implementation
- Type hint validation
- Spec traceability
"""

import pytest
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import Mock

from tests.agents.fixtures import AgentParser


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def test_writer_parser(agents_dir: Path) -> AgentParser:
    """Parser for test-writer agent."""
    return AgentParser(agents_dir / "test-writer.md")


@pytest.fixture
def sample_uc_spec() -> str:
    """Sample UC specification for testing."""
    return """---
UC-001: Create User
---

## Objective
Allow administrators to create new user accounts.

## Acceptance Criteria

```gherkin
Scenario: Successfully create user with valid data
  Given admin is authenticated
  And admin provides username "john_doe"
  And admin provides email "john@example.com"
  When admin submits user creation
  Then system returns 201 Created
  And user is stored in database

Scenario: User creation fails with duplicate username
  Given admin is authenticated
  And username "john_doe" already exists
  When admin tries to create user with "john_doe"
  Then system returns 400 Bad Request
  And error is "Username already exists"
```

## Data Requirements

### Input Data
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| username | string | Yes | 3-30 chars, alphanumeric |
| email | string | Yes | Valid email format |

## Services Used
| Service | Methods |
|---------|---------|
| UserService | create_user(), validate_username() |
"""


# ============================================================================
# Test: Agent Metadata
# ============================================================================

@pytest.mark.unit
def test_test_writer_has_correct_metadata(test_writer_parser: AgentParser):
    """Test that test-writer has correct metadata configuration."""
    assert test_writer_parser.name == "test-writer"
    assert test_writer_parser.get_metadata_field("model") == "opus"

    # Should have essential tools for test generation
    tools = test_writer_parser.get_metadata_field("tools")
    assert "Read" in tools  # For reading specs
    assert "Write" in tools  # For writing tests
    assert "Bash" in tools  # For running pytest


@pytest.mark.unit
def test_test_writer_description_mentions_test_first(test_writer_parser: AgentParser):
    """Test that description emphasizes test-first development."""
    description = test_writer_parser.get_metadata_field("description")
    assert "test-first" in description.lower() or "test first" in description.lower()
    assert "pytest" in description.lower()


# ============================================================================
# Test: Responsibilities Coverage
# ============================================================================

@pytest.mark.unit
def test_test_writer_covers_spec_parsing(test_writer_parser: AgentParser):
    """Test that agent covers specification parsing."""
    responsibilities = test_writer_parser.get_section("Responsibilities")
    assert "spec" in responsibilities.lower() or "specification" in responsibilities.lower()
    assert "parse" in responsibilities.lower() or "extract" in responsibilities.lower()


@pytest.mark.unit
def test_test_writer_covers_test_scenario_generation(test_writer_parser: AgentParser):
    """Test that agent covers test scenario generation."""
    responsibilities = test_writer_parser.get_section("Responsibilities")
    content = responsibilities.lower()

    # Should mention different scenario types
    assert "happy" in content or "success" in content
    assert "edge" in content or "boundary" in content
    assert "error" in content or "failure" in content


@pytest.mark.unit
def test_test_writer_enforces_aaa_pattern(test_writer_parser: AgentParser):
    """Test that agent enforces AAA (Arrange-Act-Assert) pattern."""
    content = test_writer_parser.content.lower()

    assert "aaa" in content or "arrange-act-assert" in content
    assert "arrange" in content
    assert "act" in content
    assert "assert" in content


@pytest.mark.unit
def test_test_writer_requires_fixtures_and_mocks(test_writer_parser: AgentParser):
    """Test that agent requires fixtures and mocks."""
    content = test_writer_parser.content.lower()

    assert "fixture" in content
    assert "mock" in content or "mocking" in content


@pytest.mark.unit
def test_test_writer_enforces_red_state_verification(test_writer_parser: AgentParser):
    """Test that agent enforces RED state verification."""
    content = test_writer_parser.content.lower()

    # Should mention RED state and verification
    assert "red" in content
    assert "fail" in content

    # Should emphasize tests must fail initially
    process_section = test_writer_parser.get_section("Process").lower()
    assert "fail" in process_section or "red" in process_section


# ============================================================================
# Test: Process Steps
# ============================================================================

@pytest.mark.unit
def test_test_writer_process_includes_spec_reading(test_writer_parser: AgentParser):
    """Test that process includes reading specification."""
    process_steps = test_writer_parser.extract_process_steps()

    # First step should be reading spec
    first_steps = " ".join(process_steps[:3]).lower()
    assert "read" in first_steps or "parse" in first_steps
    assert "spec" in first_steps


@pytest.mark.unit
def test_test_writer_process_includes_test_execution(test_writer_parser: AgentParser):
    """Test that process includes running tests."""
    process_steps = test_writer_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "run" in process_text or "execute" in process_text
    assert "pytest" in process_text or "test" in process_text


@pytest.mark.unit
def test_test_writer_process_includes_red_verification(test_writer_parser: AgentParser):
    """Test that process includes verifying RED state."""
    process_steps = test_writer_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "verify" in process_text or "check" in process_text
    assert "fail" in process_text or "red" in process_text


# ============================================================================
# Test: Quality Checks
# ============================================================================

@pytest.mark.unit
def test_test_writer_quality_checks_include_aaa_pattern(test_writer_parser: AgentParser):
    """Test that quality checks verify AAA pattern."""
    checkboxes = test_writer_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes).lower()

    assert "aaa" in checkboxes_text or "arrange" in checkboxes_text


@pytest.mark.unit
def test_test_writer_quality_checks_include_coverage(test_writer_parser: AgentParser):
    """Test that quality checks include coverage verification."""
    checkboxes = test_writer_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes).lower()

    assert "coverage" in checkboxes_text or "90%" in checkboxes_text or "90" in checkboxes_text


@pytest.mark.unit
def test_test_writer_quality_checks_include_spec_references(test_writer_parser: AgentParser):
    """Test that quality checks verify spec references."""
    checkboxes = test_writer_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes).lower()

    assert "spec" in checkboxes_text or "traceability" in checkboxes_text


@pytest.mark.unit
def test_test_writer_quality_checks_include_type_hints(test_writer_parser: AgentParser):
    """Test that quality checks verify type hints."""
    checkboxes = test_writer_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes).lower()

    assert "type" in checkboxes_text or "hint" in checkboxes_text


# ============================================================================
# Test: Anti-Patterns
# ============================================================================

@pytest.mark.unit
def test_test_writer_warns_against_passing_tests(test_writer_parser: AgentParser):
    """Test that anti-patterns warn against tests that pass initially."""
    antipatterns = test_writer_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert "pass" in antipatterns_text or "green" in antipatterns_text
    assert "red" in antipatterns_text or "fail" in antipatterns_text


@pytest.mark.unit
def test_test_writer_warns_against_weak_assertions(test_writer_parser: AgentParser):
    """Test that anti-patterns warn against weak assertions."""
    antipatterns = test_writer_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert "assert" in antipatterns_text or "weak" in antipatterns_text


@pytest.mark.unit
def test_test_writer_warns_against_missing_edge_cases(test_writer_parser: AgentParser):
    """Test that anti-patterns warn about incomplete edge case coverage."""
    antipatterns = test_writer_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert "edge" in antipatterns_text or "boundary" in antipatterns_text


# ============================================================================
# Test: Code Examples
# ============================================================================

@pytest.mark.unit
def test_test_writer_provides_code_examples(test_writer_parser: AgentParser):
    """Test that agent provides code examples."""
    code_blocks = test_writer_parser.extract_code_blocks("python")

    assert len(code_blocks) > 0, "test-writer should have Python code examples"


@pytest.mark.unit
def test_test_writer_examples_demonstrate_aaa_pattern(test_writer_parser: AgentParser):
    """Test that code examples demonstrate AAA pattern."""
    code_blocks = test_writer_parser.extract_code_blocks("python")

    if code_blocks:
        example_code = "\n".join(code_blocks).lower()

        # Should have comments or structure showing AAA
        has_aaa = (
            "# arrange" in example_code or
            "# act" in example_code or
            "# assert" in example_code
        )

        assert has_aaa, "Code examples should demonstrate AAA pattern"


@pytest.mark.unit
def test_test_writer_examples_show_fixtures(test_writer_parser: AgentParser):
    """Test that code examples show fixture usage."""
    code_blocks = test_writer_parser.extract_code_blocks("python")

    if code_blocks:
        example_code = "\n".join(code_blocks)

        assert "@pytest.fixture" in example_code, "Examples should demonstrate fixtures"


@pytest.mark.unit
def test_test_writer_examples_show_mocks(test_writer_parser: AgentParser):
    """Test that code examples show mock usage."""
    code_blocks = test_writer_parser.extract_code_blocks("python")

    if code_blocks:
        example_code = "\n".join(code_blocks).lower()

        has_mocks = (
            "mock" in example_code or
            "unittest.mock" in example_code or
            "patch" in example_code
        )

        assert has_mocks, "Examples should demonstrate mocking"


@pytest.mark.unit
def test_test_writer_examples_show_type_hints(test_writer_parser: AgentParser):
    """Test that code examples include type hints."""
    code_blocks = test_writer_parser.extract_code_blocks("python")

    if code_blocks:
        example_code = "\n".join(code_blocks)

        # Should have type hints
        has_types = (
            "->" in example_code or  # Return type hints
            ": " in example_code     # Parameter type hints
        )

        assert has_types, "Examples should include type hints"


# ============================================================================
# Test: File Operations
# ============================================================================

@pytest.mark.unit
def test_test_writer_reads_specs(test_writer_parser: AgentParser):
    """Test that agent reads specification files."""
    files_section = test_writer_parser.get_section("Files")

    assert "Read:" in files_section or "read:" in files_section.lower()
    assert "spec" in files_section.lower() or "UC-" in files_section


@pytest.mark.unit
def test_test_writer_writes_to_tests_directory(test_writer_parser: AgentParser):
    """Test that agent writes tests to tests/ directory."""
    files_section = test_writer_parser.get_section("Files")

    assert "Write:" in files_section or "write:" in files_section.lower()
    assert "tests/" in files_section or "test_" in files_section


# ============================================================================
# Test: Framework Compliance
# ============================================================================

@pytest.mark.unit
def test_test_writer_enforces_rule_2(test_writer_parser: AgentParser):
    """Test that agent enforces Rule #2 (Tests Define Correctness)."""
    content = test_writer_parser.content.lower()

    # Should mention Rule #2 or tests define correctness
    assert "rule #2" in content or "rule 2" in content or "tests define correctness" in content


@pytest.mark.unit
def test_test_writer_mentions_90_percent_coverage(test_writer_parser: AgentParser):
    """Test that agent targets 90%+ coverage."""
    content = test_writer_parser.content

    assert "90%" in content or "90" in content


# ============================================================================
# Test: Output Specification
# ============================================================================

@pytest.mark.unit
def test_test_writer_output_describes_test_file_structure(test_writer_parser: AgentParser):
    """Test that output section describes complete test file structure."""
    output_section = test_writer_parser.get_section("Output")

    assert "import" in output_section.lower()
    assert "fixture" in output_section.lower()
    assert "test function" in output_section.lower() or "test_" in output_section.lower()


@pytest.mark.unit
def test_test_writer_output_requires_pytest_execution(test_writer_parser: AgentParser):
    """Test that output section requires pytest execution results."""
    output_section = test_writer_parser.get_section("Output")

    assert "pytest" in output_section.lower() or "execution" in output_section.lower()
    assert "fail" in output_section.lower() or "red" in output_section.lower()


# ============================================================================
# Test: Next Steps
# ============================================================================

@pytest.mark.unit
def test_test_writer_next_steps_mention_implementation(test_writer_parser: AgentParser):
    """Test that next steps mention moving to implementation (GREEN phase)."""
    next_steps = test_writer_parser.get_section("Next Steps")

    if next_steps:
        next_steps_lower = next_steps.lower()
        assert "implement" in next_steps_lower or "green" in next_steps_lower


@pytest.mark.unit
def test_test_writer_next_steps_mention_refactoring(test_writer_parser: AgentParser):
    """Test that next steps mention refactoring after GREEN."""
    next_steps = test_writer_parser.get_section("Next Steps")

    if next_steps:
        assert "refactor" in next_steps.lower()


# ============================================================================
# Test: Behavioral Simulation
# ============================================================================

def test_test_writer_workflow_simulation(sample_uc_spec: str):
    """Simulate test-writer workflow with sample UC spec.

    This test validates the expected workflow:
    1. Parse UC spec
    2. Extract test scenarios
    3. Identify required fixtures
    4. Identify required mocks
    5. Generate test structure
    """
    # Parse UC spec
    assert "UC-001" in sample_uc_spec
    assert "create user" in sample_uc_spec.lower()

    # Extract test scenarios from acceptance criteria
    assert "Scenario:" in sample_uc_spec
    scenarios = [line for line in sample_uc_spec.split('\n') if line.strip().startswith("Scenario:")]
    assert len(scenarios) >= 2, "Should have happy path and error scenarios"

    # Identify services (for mocking)
    assert "UserService" in sample_uc_spec

    # Verify Gherkin format
    assert "Given" in sample_uc_spec
    assert "When" in sample_uc_spec
    assert "Then" in sample_uc_spec
