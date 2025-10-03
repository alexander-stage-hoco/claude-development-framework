"""Behavioral tests for bdd-scenario-writer agent.

Tests the bdd-scenario-writer agent's ability to:
- Extract acceptance criteria from UC specifications
- Convert criteria to Given-When-Then Gherkin scenarios
- Identify parameterization opportunities (Scenario Outline)
- Generate complete .feature files with metadata
- Validate 100% coverage of acceptance criteria
- Add spec references for traceability

Test Coverage:
- UC analysis and criteria extraction
- Gherkin scenario generation
- Scenario Outline with Examples tables
- Feature file structure
- Coverage validation
- Spec traceability
"""

import pytest
from pathlib import Path

from tests.agents.fixtures import AgentParser


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def bdd_scenario_writer_parser(agents_dir: Path) -> AgentParser:
    """Parser for bdd-scenario-writer agent."""
    return AgentParser(agents_dir / "bdd-scenario-writer.md")


# ============================================================================
# Test: Agent Metadata
# ============================================================================

@pytest.mark.unit
def test_bdd_scenario_writer_has_correct_metadata(bdd_scenario_writer_parser: AgentParser):
    """Test that bdd-scenario-writer has correct metadata."""
    assert bdd_scenario_writer_parser.name == "bdd-scenario-writer"
    assert bdd_scenario_writer_parser.get_metadata_field("model") == "sonnet"

    # Should have tools for reading and writing
    tools = bdd_scenario_writer_parser.get_metadata_field("tools")
    assert "Read" in tools
    assert "Write" in tools


# ============================================================================
# Test: Responsibilities Coverage
# ============================================================================

@pytest.mark.unit
def test_bdd_scenario_writer_covers_acceptance_criteria(bdd_scenario_writer_parser: AgentParser):
    """Test that agent covers acceptance criteria extraction."""
    responsibilities = bdd_scenario_writer_parser.get_section("Responsibilities")
    assert "acceptance criteria" in responsibilities.lower()


@pytest.mark.unit
def test_bdd_scenario_writer_covers_gherkin_conversion(bdd_scenario_writer_parser: AgentParser):
    """Test that agent covers Gherkin conversion."""
    responsibilities = bdd_scenario_writer_parser.get_section("Responsibilities")
    content = responsibilities.lower()

    assert "gherkin" in content or "given-when-then" in content


@pytest.mark.unit
def test_bdd_scenario_writer_covers_parameterization(bdd_scenario_writer_parser: AgentParser):
    """Test that agent covers parameterization (Scenario Outline)."""
    responsibilities = bdd_scenario_writer_parser.get_section("Responsibilities")
    assert "scenario outline" in responsibilities.lower() or "parameterization" in responsibilities.lower()


@pytest.mark.unit
def test_bdd_scenario_writer_covers_coverage_validation(bdd_scenario_writer_parser: AgentParser):
    """Test that agent covers 100% coverage validation."""
    responsibilities = bdd_scenario_writer_parser.get_section("Responsibilities")
    assert "100%" in responsibilities or "coverage" in responsibilities.lower()


# ============================================================================
# Test: Process Steps
# ============================================================================

@pytest.mark.unit
def test_bdd_scenario_writer_process_reads_uc(bdd_scenario_writer_parser: AgentParser):
    """Test that process includes reading UC specification."""
    process_steps = bdd_scenario_writer_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "read" in process_text and "uc" in process_text


@pytest.mark.unit
def test_bdd_scenario_writer_process_generates_feature_file(bdd_scenario_writer_parser: AgentParser):
    """Test that process includes generating .feature file."""
    process_steps = bdd_scenario_writer_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "feature" in process_text or "gherkin" in process_text


@pytest.mark.unit
def test_bdd_scenario_writer_process_validates_coverage(bdd_scenario_writer_parser: AgentParser):
    """Test that process includes validating coverage."""
    process_steps = bdd_scenario_writer_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "coverage" in process_text or "validate" in process_text


# ============================================================================
# Test: Quality Checks
# ============================================================================

@pytest.mark.unit
def test_bdd_scenario_writer_quality_checks_include_coverage(bdd_scenario_writer_parser: AgentParser):
    """Test that quality checks verify 100% coverage."""
    checkboxes = bdd_scenario_writer_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes)

    assert "100%" in checkboxes_text or "coverage" in checkboxes_text.lower()


@pytest.mark.unit
def test_bdd_scenario_writer_quality_checks_include_gherkin_syntax(bdd_scenario_writer_parser: AgentParser):
    """Test that quality checks verify Gherkin syntax."""
    checkboxes = bdd_scenario_writer_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes).lower()

    assert "gherkin" in checkboxes_text or "syntax" in checkboxes_text


@pytest.mark.unit
def test_bdd_scenario_writer_quality_checks_include_spec_references(bdd_scenario_writer_parser: AgentParser):
    """Test that quality checks verify spec references."""
    checkboxes = bdd_scenario_writer_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes).lower()

    assert "spec" in checkboxes_text or "uc" in checkboxes_text or "reference" in checkboxes_text


# ============================================================================
# Test: Anti-Patterns
# ============================================================================

@pytest.mark.unit
def test_bdd_scenario_writer_warns_against_missing_coverage(bdd_scenario_writer_parser: AgentParser):
    """Test that anti-patterns warn about missing acceptance criteria coverage."""
    antipatterns = bdd_scenario_writer_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert "coverage" in antipatterns_text or "missing" in antipatterns_text


@pytest.mark.unit
def test_bdd_scenario_writer_warns_against_ambiguous_steps(bdd_scenario_writer_parser: AgentParser):
    """Test that anti-patterns warn about ambiguous steps."""
    antipatterns = bdd_scenario_writer_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert "ambiguous" in antipatterns_text or "clear" in antipatterns_text


@pytest.mark.unit
def test_bdd_scenario_writer_warns_against_implementation_details(bdd_scenario_writer_parser: AgentParser):
    """Test that anti-patterns warn about implementation details."""
    antipatterns = bdd_scenario_writer_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert "implementation" in antipatterns_text or "behavior" in antipatterns_text


# ============================================================================
# Test: Code Examples
# ============================================================================

@pytest.mark.unit
def test_bdd_scenario_writer_provides_feature_example(bdd_scenario_writer_parser: AgentParser):
    """Test that agent provides example feature file."""
    code_blocks = bdd_scenario_writer_parser.extract_code_blocks("gherkin")

    assert len(code_blocks) > 0, "Should have Gherkin code examples"


@pytest.mark.unit
def test_bdd_scenario_writer_example_shows_background(bdd_scenario_writer_parser: AgentParser):
    """Test that example shows Background usage."""
    code_blocks = bdd_scenario_writer_parser.extract_code_blocks("gherkin")

    if code_blocks:
        example_code = "\n".join(code_blocks)
        assert "Background:" in example_code, "Example should demonstrate Background"


@pytest.mark.unit
def test_bdd_scenario_writer_example_shows_scenario_outline(bdd_scenario_writer_parser: AgentParser):
    """Test that example shows Scenario Outline with Examples."""
    code_blocks = bdd_scenario_writer_parser.extract_code_blocks("gherkin")

    if code_blocks:
        example_code = "\n".join(code_blocks)
        assert "Scenario Outline:" in example_code, "Example should demonstrate Scenario Outline"
        assert "Examples:" in example_code, "Example should demonstrate Examples table"


@pytest.mark.unit
def test_bdd_scenario_writer_example_shows_spec_references(bdd_scenario_writer_parser: AgentParser):
    """Test that example shows spec references in comments."""
    code_blocks = bdd_scenario_writer_parser.extract_code_blocks("gherkin")

    if code_blocks:
        example_code = "\n".join(code_blocks)
        assert "# Specification:" in example_code or "UC-" in example_code, "Example should show spec references"


# ============================================================================
# Test: Output Specification
# ============================================================================

@pytest.mark.unit
def test_bdd_scenario_writer_output_describes_feature_structure(bdd_scenario_writer_parser: AgentParser):
    """Test that output section describes complete feature file structure."""
    output_section = bdd_scenario_writer_parser.get_section("Output")

    assert "Feature" in output_section
    assert "Scenario" in output_section
    assert "Given-When-Then" in output_section or "Given" in output_section


@pytest.mark.unit
def test_bdd_scenario_writer_output_requires_coverage_report(bdd_scenario_writer_parser: AgentParser):
    """Test that output requires coverage report."""
    output_section = bdd_scenario_writer_parser.get_section("Output")

    assert "coverage" in output_section.lower()


# ============================================================================
# Test: File Operations
# ============================================================================

@pytest.mark.unit
def test_bdd_scenario_writer_reads_uc_specs(bdd_scenario_writer_parser: AgentParser):
    """Test that agent reads UC specifications."""
    files_section = bdd_scenario_writer_parser.get_section("Files")

    assert "Read:" in files_section or "read:" in files_section.lower()
    assert "UC-" in files_section or "use-cases" in files_section.lower()


@pytest.mark.unit
def test_bdd_scenario_writer_writes_feature_files(bdd_scenario_writer_parser: AgentParser):
    """Test that agent writes .feature files."""
    files_section = bdd_scenario_writer_parser.get_section("Files")

    assert "Write:" in files_section or "write:" in files_section.lower()
    assert ".feature" in files_section


# ============================================================================
# Test: Framework Compliance
# ============================================================================

@pytest.mark.unit
def test_bdd_scenario_writer_enforces_rule_8(bdd_scenario_writer_parser: AgentParser):
    """Test that agent enforces Rule #8 (BDD for User-Facing Features)."""
    content = bdd_scenario_writer_parser.content.lower()

    assert "rule #8" in content or "rule 8" in content or "bdd for user-facing" in content


# ============================================================================
# Test: Gherkin Best Practices
# ============================================================================

@pytest.mark.unit
def test_bdd_scenario_writer_documents_best_practices(bdd_scenario_writer_parser: AgentParser):
    """Test that agent documents Gherkin best practices."""
    content = bdd_scenario_writer_parser.content.lower()

    assert "best practices" in content or "given steps" in content


@pytest.mark.unit
def test_bdd_scenario_writer_explains_when_to_use_scenario_outline(bdd_scenario_writer_parser: AgentParser):
    """Test that agent explains when to use Scenario Outline."""
    content = bdd_scenario_writer_parser.content

    # Should explain Scenario vs Scenario Outline
    assert "Scenario Outline" in content
    assert "Examples" in content


# ============================================================================
# Test: Next Steps
# ============================================================================

@pytest.mark.unit
def test_bdd_scenario_writer_next_steps_mention_step_definitions(bdd_scenario_writer_parser: AgentParser):
    """Test that next steps mention implementing step definitions."""
    next_steps = bdd_scenario_writer_parser.get_section("Next Steps")

    if next_steps:
        next_steps_lower = next_steps.lower()
        assert "step definition" in next_steps_lower or "implement" in next_steps_lower
