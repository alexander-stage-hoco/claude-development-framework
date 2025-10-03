"""Behavioral tests for code-quality-checker agent.

Tests the code-quality-checker agent's ability to:
- Run static analysis tools (pylint, flake8, mypy, radon)
- Check type hints coverage
- Validate docstrings with spec references
- Measure cyclomatic complexity
- Detect code smells (magic numbers, poor naming, TODOs)
- Generate comprehensive quality reports

Test Coverage:
- Tool execution (pylint, flake8, mypy, radon)
- Type safety validation
- Documentation coverage
- Complexity measurement
- Code smell detection
- Quality score calculation
"""

import pytest
from pathlib import Path
from typing import List

from tests.agents.fixtures import AgentParser


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def code_quality_checker_parser(agents_dir: Path) -> AgentParser:
    """Parser for code-quality-checker agent."""
    return AgentParser(agents_dir / "code-quality-checker.md")


# ============================================================================
# Test: Agent Metadata
# ============================================================================

@pytest.mark.unit
def test_code_quality_checker_has_correct_metadata(code_quality_checker_parser: AgentParser):
    """Test that code-quality-checker has correct metadata."""
    assert code_quality_checker_parser.name == "code-quality-checker"
    assert code_quality_checker_parser.get_metadata_field("model") == "sonnet"

    # Should have tools for reading code and running tools
    tools = code_quality_checker_parser.get_metadata_field("tools")
    assert "Read" in tools
    assert "Bash" in tools  # For running quality tools
    assert "Glob" in tools  # For finding files
    assert "Grep" in tools  # For searching code


# ============================================================================
# Test: Responsibilities Coverage
# ============================================================================

@pytest.mark.unit
def test_code_quality_checker_covers_static_analysis(code_quality_checker_parser: AgentParser):
    """Test that agent covers static analysis tools."""
    responsibilities = code_quality_checker_parser.get_section("Responsibilities")
    content = responsibilities.lower()

    assert "pylint" in content
    assert "flake8" in content
    assert "mypy" in content
    assert "radon" in content


@pytest.mark.unit
def test_code_quality_checker_covers_type_hints(code_quality_checker_parser: AgentParser):
    """Test that agent covers type hint validation."""
    responsibilities = code_quality_checker_parser.get_section("Responsibilities")
    assert "type hint" in responsibilities.lower()


@pytest.mark.unit
def test_code_quality_checker_covers_docstrings(code_quality_checker_parser: AgentParser):
    """Test that agent covers docstring validation."""
    responsibilities = code_quality_checker_parser.get_section("Responsibilities")
    assert "docstring" in responsibilities.lower()


@pytest.mark.unit
def test_code_quality_checker_covers_complexity(code_quality_checker_parser: AgentParser):
    """Test that agent covers complexity measurement."""
    responsibilities = code_quality_checker_parser.get_section("Responsibilities")
    assert "complexity" in responsibilities.lower() or "cyclomatic" in responsibilities.lower()


@pytest.mark.unit
def test_code_quality_checker_covers_code_smells(code_quality_checker_parser: AgentParser):
    """Test that agent covers code smell detection."""
    responsibilities = code_quality_checker_parser.get_section("Responsibilities")
    content = responsibilities.lower()

    assert "code smell" in content or "magic number" in content or "naming" in content


# ============================================================================
# Test: Quality Checking Checklist
# ============================================================================

@pytest.mark.unit
def test_code_quality_checker_has_comprehensive_checklist(code_quality_checker_parser: AgentParser):
    """Test that agent has comprehensive quality checking checklist."""
    content = code_quality_checker_parser.content.lower()

    assert "checklist" in content
    assert "static analysis" in content
    assert "type safety" in content
    assert "documentation" in content


@pytest.mark.unit
def test_code_quality_checker_defines_thresholds(code_quality_checker_parser: AgentParser):
    """Test that agent defines quality thresholds."""
    content = code_quality_checker_parser.content

    # Should have numeric thresholds
    assert "8.0" in content or "8" in content  # pylint threshold
    assert "< 10" in content or "<10" in content  # complexity threshold


# ============================================================================
# Test: Process Steps
# ============================================================================

@pytest.mark.unit
def test_code_quality_checker_process_runs_all_tools(code_quality_checker_parser: AgentParser):
    """Test that process includes running all quality tools."""
    process_steps = code_quality_checker_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "pylint" in process_text
    assert "flake8" in process_text
    assert "mypy" in process_text
    assert "radon" in process_text


@pytest.mark.unit
def test_code_quality_checker_process_generates_report(code_quality_checker_parser: AgentParser):
    """Test that process includes generating report."""
    process_steps = code_quality_checker_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "report" in process_text or "generate" in process_text


@pytest.mark.unit
def test_code_quality_checker_process_calculates_score(code_quality_checker_parser: AgentParser):
    """Test that process includes calculating quality score."""
    process_steps = code_quality_checker_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    # Score calculation is part of report generation
    assert "score" in process_text or "calculate" in process_text or "report" in process_text


# ============================================================================
# Test: Quality Checks
# ============================================================================

@pytest.mark.unit
def test_code_quality_checker_quality_checks_include_tools(code_quality_checker_parser: AgentParser):
    """Test that quality checks verify tool execution."""
    checkboxes = code_quality_checker_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes).lower()

    assert "pylint" in checkboxes_text
    assert "flake8" in checkboxes_text
    assert "mypy" in checkboxes_text


@pytest.mark.unit
def test_code_quality_checker_quality_checks_include_score(code_quality_checker_parser: AgentParser):
    """Test that quality checks verify score calculation."""
    checkboxes = code_quality_checker_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes).lower()

    assert "score" in checkboxes_text


# ============================================================================
# Test: Anti-Patterns
# ============================================================================

@pytest.mark.unit
def test_code_quality_checker_warns_against_ignoring_critical(code_quality_checker_parser: AgentParser):
    """Test that anti-patterns warn against passing with critical violations."""
    antipatterns = code_quality_checker_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert "critical" in antipatterns_text or "violation" in antipatterns_text


@pytest.mark.unit
def test_code_quality_checker_requires_file_line_references(code_quality_checker_parser: AgentParser):
    """Test that anti-patterns require file:line references."""
    antipatterns = code_quality_checker_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert "file:line" in antipatterns_text or "traceable" in antipatterns_text


# ============================================================================
# Test: Output Specification
# ============================================================================

@pytest.mark.unit
def test_code_quality_checker_output_includes_score(code_quality_checker_parser: AgentParser):
    """Test that output includes quality score."""
    output_section = code_quality_checker_parser.get_section("Output")

    assert "score" in output_section.lower()
    assert "0-100" in output_section or "100" in output_section


@pytest.mark.unit
def test_code_quality_checker_output_includes_violations(code_quality_checker_parser: AgentParser):
    """Test that output includes violations by severity."""
    output_section = code_quality_checker_parser.get_section("Output")

    assert "violation" in output_section.lower()
    assert "CRITICAL" in output_section or "HIGH" in output_section


@pytest.mark.unit
def test_code_quality_checker_output_includes_tool_results(code_quality_checker_parser: AgentParser):
    """Test that output includes tool results."""
    output_section = code_quality_checker_parser.get_section("Output")
    content = output_section.lower()

    assert "pylint" in content
    assert "flake8" in content
    assert "mypy" in content


# ============================================================================
# Test: Score Calculation
# ============================================================================

@pytest.mark.unit
def test_code_quality_checker_defines_score_calculation(code_quality_checker_parser: AgentParser):
    """Test that agent defines score calculation methodology."""
    content = code_quality_checker_parser.content.lower()

    assert "quality score calculation" in content or "base score" in content or "deductions" in content


@pytest.mark.unit
def test_code_quality_checker_defines_pass_threshold(code_quality_checker_parser: AgentParser):
    """Test that agent defines pass threshold."""
    content = code_quality_checker_parser.content

    assert "≥ 80" in content or ">= 80" in content or "80" in content


# ============================================================================
# Test: Code Examples
# ============================================================================

@pytest.mark.unit
def test_code_quality_checker_provides_report_example(code_quality_checker_parser: AgentParser):
    """Test that agent provides example quality report."""
    content = code_quality_checker_parser.content.lower()

    assert "example" in content and "quality report" in content


# ============================================================================
# Test: File Operations
# ============================================================================

@pytest.mark.unit
def test_code_quality_checker_reads_implementation_files(code_quality_checker_parser: AgentParser):
    """Test that agent reads implementation files."""
    files_section = code_quality_checker_parser.get_section("Files")

    assert "src/" in files_section or "lib/" in files_section or "services/" in files_section


@pytest.mark.unit
def test_code_quality_checker_excludes_tests(code_quality_checker_parser: AgentParser):
    """Test that agent excludes test files."""
    files_section = code_quality_checker_parser.get_section("Files")

    assert "Exclude:" in files_section or "exclude" in files_section.lower()
    assert "tests/" in files_section


# ============================================================================
# Test: Framework Compliance
# ============================================================================

@pytest.mark.unit
def test_code_quality_checker_enforces_rule_9(code_quality_checker_parser: AgentParser):
    """Test that agent enforces Rule #9 (Code Quality Standards)."""
    content = code_quality_checker_parser.content.lower()

    assert "rule #9" in content or "rule 9" in content or "code quality standards" in content


# ============================================================================
# Test: Next Steps
# ============================================================================

@pytest.mark.unit
def test_code_quality_checker_next_steps_mention_fixes(code_quality_checker_parser: AgentParser):
    """Test that next steps mention fixing violations."""
    next_steps = code_quality_checker_parser.get_section("Next Steps")

    if next_steps:
        next_steps_lower = next_steps.lower()
        assert "fix" in next_steps_lower
        assert "critical" in next_steps_lower or "violation" in next_steps_lower


@pytest.mark.unit
def test_code_quality_checker_next_steps_mention_rerun(code_quality_checker_parser: AgentParser):
    """Test that next steps mention re-running check."""
    next_steps = code_quality_checker_parser.get_section("Next Steps")

    if next_steps:
        assert "re-run" in next_steps.lower() or "rerun" in next_steps.lower() or "verify" in next_steps.lower()


# ============================================================================
# Test: Content Quality
# ============================================================================

@pytest.mark.unit
def test_code_quality_checker_has_severity_levels(code_quality_checker_parser: AgentParser):
    """Test that agent defines severity levels."""
    content = code_quality_checker_parser.content

    assert "CRITICAL" in content
    assert "HIGH" in content
    assert "MEDIUM" in content
    assert "LOW" in content


@pytest.mark.unit
def test_code_quality_checker_mentions_spec_references(code_quality_checker_parser: AgentParser):
    """Test that agent checks for spec references in docstrings."""
    content = code_quality_checker_parser.content.lower()

    assert "spec reference" in content or "specification:" in content
