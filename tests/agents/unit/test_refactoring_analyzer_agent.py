"""Behavioral tests for refactoring-analyzer agent.

Tests the refactoring-analyzer agent's ability to:
- Detect code duplication (>3 lines repeated, similar patterns)
- Identify complex functions (complexity > 10, length > 30, nesting > 3)
- Find magic numbers and strings
- Detect poor naming patterns
- Identify missing abstractions
- Generate prioritized refactoring recommendations with code examples

Test Coverage:
- Duplication detection
- Complexity analysis
- Code smell detection
- Pattern recognition
- Refactoring recommendations
- Before/after examples
"""

import pytest
from pathlib import Path

from tests.agents.fixtures import AgentParser


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def refactoring_analyzer_parser(agents_dir: Path) -> AgentParser:
    """Parser for refactoring-analyzer agent."""
    return AgentParser(agents_dir / "refactoring-analyzer.md")


# ============================================================================
# Test: Agent Metadata
# ============================================================================

@pytest.mark.unit
def test_refactoring_analyzer_has_correct_metadata(refactoring_analyzer_parser: AgentParser):
    """Test that refactoring-analyzer has correct metadata."""
    assert refactoring_analyzer_parser.name == "refactoring-analyzer"
    assert refactoring_analyzer_parser.get_metadata_field("model") == "opus"

    # Should have tools for reading and analyzing code
    tools = refactoring_analyzer_parser.get_metadata_field("tools")
    assert "Read" in tools
    assert "Bash" in tools  # For running radon
    assert "Glob" in tools
    assert "Grep" in tools


# ============================================================================
# Test: Responsibilities Coverage
# ============================================================================

@pytest.mark.unit
def test_refactoring_analyzer_covers_duplication_detection(refactoring_analyzer_parser: AgentParser):
    """Test that agent covers code duplication detection."""
    responsibilities = refactoring_analyzer_parser.get_section("Responsibilities")
    assert "duplication" in responsibilities.lower() or "duplicate" in responsibilities.lower()


@pytest.mark.unit
def test_refactoring_analyzer_covers_complexity(refactoring_analyzer_parser: AgentParser):
    """Test that agent covers complexity analysis."""
    responsibilities = refactoring_analyzer_parser.get_section("Responsibilities")
    assert "complexity" in responsibilities.lower()


@pytest.mark.unit
def test_refactoring_analyzer_covers_magic_numbers(refactoring_analyzer_parser: AgentParser):
    """Test that agent covers magic number detection."""
    responsibilities = refactoring_analyzer_parser.get_section("Responsibilities")
    assert "magic number" in responsibilities.lower()


@pytest.mark.unit
def test_refactoring_analyzer_covers_naming(refactoring_analyzer_parser: AgentParser):
    """Test that agent covers naming analysis."""
    responsibilities = refactoring_analyzer_parser.get_section("Responsibilities")
    assert "naming" in responsibilities.lower()


@pytest.mark.unit
def test_refactoring_analyzer_covers_missing_abstractions(refactoring_analyzer_parser: AgentParser):
    """Test that agent covers missing abstraction detection."""
    responsibilities = refactoring_analyzer_parser.get_section("Responsibilities")
    assert "abstraction" in responsibilities.lower() or "pattern" in responsibilities.lower()


# ============================================================================
# Test: Analysis Checklist
# ============================================================================

@pytest.mark.unit
def test_refactoring_analyzer_defines_complexity_thresholds(refactoring_analyzer_parser: AgentParser):
    """Test that agent defines complexity thresholds."""
    content = refactoring_analyzer_parser.content

    assert "> 10" in content or ">10" in content  # Complexity threshold
    assert "> 30" in content or ">30" in content  # Length threshold
    assert "> 3" in content or ">3" in content    # Nesting threshold


@pytest.mark.unit
def test_refactoring_analyzer_defines_parameter_count_threshold(refactoring_analyzer_parser: AgentParser):
    """Test that agent defines parameter count threshold."""
    content = refactoring_analyzer_parser.content

    assert "> 4" in content or ">4" in content


# ============================================================================
# Test: Process Steps
# ============================================================================

@pytest.mark.unit
def test_refactoring_analyzer_process_verifies_green_state(refactoring_analyzer_parser: AgentParser):
    """Test that process verifies GREEN state before refactoring."""
    process_steps = refactoring_analyzer_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "green" in process_text or "test" in process_text and "pass" in process_text


@pytest.mark.unit
def test_refactoring_analyzer_process_runs_radon(refactoring_analyzer_parser: AgentParser):
    """Test that process includes running radon for complexity."""
    process_steps = refactoring_analyzer_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "radon" in process_text


@pytest.mark.unit
def test_refactoring_analyzer_process_prioritizes_opportunities(refactoring_analyzer_parser: AgentParser):
    """Test that process includes prioritizing opportunities."""
    process_steps = refactoring_analyzer_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "prioritize" in process_text or "priority" in process_text


@pytest.mark.unit
def test_refactoring_analyzer_process_generates_examples(refactoring_analyzer_parser: AgentParser):
    """Test that process includes generating before/after examples."""
    process_steps = refactoring_analyzer_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "example" in process_text or "before/after" in process_text


# ============================================================================
# Test: Quality Checks
# ============================================================================

@pytest.mark.unit
def test_refactoring_analyzer_quality_checks_verify_green(refactoring_analyzer_parser: AgentParser):
    """Test that quality checks verify GREEN state."""
    checkboxes = refactoring_analyzer_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes).lower()

    assert "green" in checkboxes_text or "pass" in checkboxes_text


@pytest.mark.unit
def test_refactoring_analyzer_quality_checks_include_prioritization(refactoring_analyzer_parser: AgentParser):
    """Test that quality checks include prioritization."""
    checkboxes = refactoring_analyzer_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes).lower()

    assert "prioritize" in checkboxes_text or "impact/effort" in checkboxes_text


# ============================================================================
# Test: Anti-Patterns
# ============================================================================

@pytest.mark.unit
def test_refactoring_analyzer_warns_against_refactoring_without_green(refactoring_analyzer_parser: AgentParser):
    """Test that anti-patterns warn against refactoring without GREEN tests."""
    antipatterns = refactoring_analyzer_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert "green" in antipatterns_text or "test" in antipatterns_text


@pytest.mark.unit
def test_refactoring_analyzer_warns_against_generic_suggestions(refactoring_analyzer_parser: AgentParser):
    """Test that anti-patterns warn about generic suggestions without examples."""
    antipatterns = refactoring_analyzer_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert "generic" in antipatterns_text or "example" in antipatterns_text


@pytest.mark.unit
def test_refactoring_analyzer_warns_about_behavior_changes(refactoring_analyzer_parser: AgentParser):
    """Test that anti-patterns warn about suggesting behavior changes."""
    antipatterns = refactoring_analyzer_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert "behavior" in antipatterns_text or "maintain" in antipatterns_text


# ============================================================================
# Test: Refactoring Pattern Library
# ============================================================================

@pytest.mark.unit
def test_refactoring_analyzer_provides_pattern_library(refactoring_analyzer_parser: AgentParser):
    """Test that agent provides refactoring pattern library."""
    content = refactoring_analyzer_parser.content.lower()

    assert "pattern library" in content or "refactoring pattern" in content


@pytest.mark.unit
def test_refactoring_analyzer_pattern_extract_function(refactoring_analyzer_parser: AgentParser):
    """Test that pattern library includes Extract Function."""
    content = refactoring_analyzer_parser.content

    assert "Extract Function" in content


@pytest.mark.unit
def test_refactoring_analyzer_pattern_extract_constant(refactoring_analyzer_parser: AgentParser):
    """Test that pattern library includes Extract Constant."""
    content = refactoring_analyzer_parser.content

    assert "Extract Constant" in content


@pytest.mark.unit
def test_refactoring_analyzer_pattern_split_function(refactoring_analyzer_parser: AgentParser):
    """Test that pattern library includes Split Function (SRP)."""
    content = refactoring_analyzer_parser.content

    assert "Split Function" in content or "SRP" in content


@pytest.mark.unit
def test_refactoring_analyzer_pattern_guard_clauses(refactoring_analyzer_parser: AgentParser):
    """Test that pattern library includes Guard Clauses."""
    content = refactoring_analyzer_parser.content

    assert "Guard Clause" in content or "Flatten Nested" in content


# ============================================================================
# Test: Code Examples
# ============================================================================

@pytest.mark.unit
def test_refactoring_analyzer_provides_before_after_examples(refactoring_analyzer_parser: AgentParser):
    """Test that agent provides before/after code examples."""
    code_blocks = refactoring_analyzer_parser.extract_code_blocks("python")

    assert len(code_blocks) > 0, "Should have Python code examples"

    # Check for before/after pattern in content
    content = refactoring_analyzer_parser.content
    assert "Before" in content or "before" in content
    assert "After" in content or "after" in content


@pytest.mark.unit
def test_refactoring_analyzer_examples_show_benefits(refactoring_analyzer_parser: AgentParser):
    """Test that examples explain benefits of refactorings."""
    content = refactoring_analyzer_parser.content

    assert "Benefits:" in content or "benefits" in content.lower()


# ============================================================================
# Test: Output Specification
# ============================================================================

@pytest.mark.unit
def test_refactoring_analyzer_output_includes_executive_summary(refactoring_analyzer_parser: AgentParser):
    """Test that output includes executive summary."""
    output_section = refactoring_analyzer_parser.get_section("Output")

    assert "Executive Summary" in output_section or "executive summary" in output_section.lower()


@pytest.mark.unit
def test_refactoring_analyzer_output_includes_priority_breakdown(refactoring_analyzer_parser: AgentParser):
    """Test that output includes priority breakdown."""
    output_section = refactoring_analyzer_parser.get_section("Output")

    assert "HIGH" in output_section
    assert "MEDIUM" in output_section
    assert "LOW" in output_section


@pytest.mark.unit
def test_refactoring_analyzer_output_includes_examples(refactoring_analyzer_parser: AgentParser):
    """Test that output includes before/after examples."""
    output_section = refactoring_analyzer_parser.get_section("Output")

    assert "Before/After Example" in output_section or "before/after" in output_section.lower()


# ============================================================================
# Test: File Operations
# ============================================================================

@pytest.mark.unit
def test_refactoring_analyzer_reads_recently_modified_files(refactoring_analyzer_parser: AgentParser):
    """Test that agent reads recently modified files."""
    files_section = refactoring_analyzer_parser.get_section("Files")

    assert "recently modified" in files_section.lower() or "Read:" in files_section


@pytest.mark.unit
def test_refactoring_analyzer_excludes_tests(refactoring_analyzer_parser: AgentParser):
    """Test that agent excludes test files."""
    files_section = refactoring_analyzer_parser.get_section("Files")

    assert "Exclude:" in files_section or "exclude" in files_section.lower()
    assert "tests/" in files_section


# ============================================================================
# Test: Framework Compliance
# ============================================================================

@pytest.mark.unit
def test_refactoring_analyzer_enforces_rule_12(refactoring_analyzer_parser: AgentParser):
    """Test that agent enforces Rule #12 (Mandatory Refactoring)."""
    content = refactoring_analyzer_parser.content.lower()

    assert "rule #12" in content or "rule 12" in content or "mandatory refactoring" in content


@pytest.mark.unit
def test_refactoring_analyzer_mentions_tdd_cycle(refactoring_analyzer_parser: AgentParser):
    """Test that agent mentions TDD cycle (RED-GREEN-REFACTOR)."""
    content = refactoring_analyzer_parser.content.lower()

    assert "red-green-refactor" in content or "tdd cycle" in content


# ============================================================================
# Test: Next Steps
# ============================================================================

@pytest.mark.unit
def test_refactoring_analyzer_next_steps_mention_test_verification(refactoring_analyzer_parser: AgentParser):
    """Test that next steps mention running tests after each refactoring."""
    next_steps = refactoring_analyzer_parser.get_section("Next Steps")

    if next_steps:
        next_steps_lower = next_steps.lower()
        assert "test" in next_steps_lower
        assert "each" in next_steps_lower or "after" in next_steps_lower


@pytest.mark.unit
def test_refactoring_analyzer_next_steps_mention_separate_commits(refactoring_analyzer_parser: AgentParser):
    """Test that next steps mention committing each refactoring separately."""
    next_steps = refactoring_analyzer_parser.get_section("Next Steps")

    if next_steps:
        next_steps_lower = next_steps.lower()
        assert "commit" in next_steps_lower
        assert "separate" in next_steps_lower or "each" in next_steps_lower


# ============================================================================
# Test: Content Quality
# ============================================================================

@pytest.mark.unit
def test_refactoring_analyzer_has_comprehensive_report_example(refactoring_analyzer_parser: AgentParser):
    """Test that agent has comprehensive refactoring report example."""
    content = refactoring_analyzer_parser.content.lower()

    assert "example refactoring report" in content or "refactoring analysis report" in content
