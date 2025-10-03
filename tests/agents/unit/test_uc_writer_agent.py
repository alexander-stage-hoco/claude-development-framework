"""Behavioral tests for uc-writer agent.

Tests the uc-writer agent's ability to:
- Guide structured UC interview with 16 sections
- Extract requirements, objectives, and user value
- Identify actors and service dependencies
- Document flows (main, alternative, error)
- Generate BDD acceptance criteria in Gherkin format
- Elicit non-functional requirements
- Create complete UC specification files

Test Coverage:
- Interview process coverage
- UC section generation
- Service identification
- BDD criteria generation
- Data requirements specification
- Non-functional requirements
- Completeness validation
"""

import pytest
from pathlib import Path
from typing import List

from tests.agents.fixtures import AgentParser


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def uc_writer_parser(agents_dir: Path) -> AgentParser:
    """Parser for uc-writer agent."""
    return AgentParser(agents_dir / "uc-writer.md")


# ============================================================================
# Test: Agent Metadata
# ============================================================================

@pytest.mark.unit
def test_uc_writer_has_correct_metadata(uc_writer_parser: AgentParser):
    """Test that uc-writer has correct metadata configuration."""
    assert uc_writer_parser.name == "uc-writer"
    assert uc_writer_parser.get_metadata_field("model") == "opus"

    # Should have tools for research and file operations
    tools = uc_writer_parser.get_metadata_field("tools")
    assert "Read" in tools
    assert "Write" in tools
    assert "WebSearch" in tools  # For domain research


@pytest.mark.unit
def test_uc_writer_description_mentions_requirements(uc_writer_parser: AgentParser):
    """Test that description emphasizes requirements analysis."""
    description = uc_writer_parser.get_metadata_field("description")
    assert "requirements" in description.lower() or "use case" in description.lower()


# ============================================================================
# Test: Responsibilities Coverage
# ============================================================================

@pytest.mark.unit
def test_uc_writer_covers_interview_guidance(uc_writer_parser: AgentParser):
    """Test that agent covers structured interview guidance."""
    responsibilities = uc_writer_parser.get_section("Responsibilities")
    assert "interview" in responsibilities.lower()
    assert "16" in responsibilities or "sixteen" in responsibilities.lower()


@pytest.mark.unit
def test_uc_writer_covers_service_identification(uc_writer_parser: AgentParser):
    """Test that agent covers service identification (Rule #1)."""
    responsibilities = uc_writer_parser.get_section("Responsibilities")
    assert "service" in responsibilities.lower()


@pytest.mark.unit
def test_uc_writer_covers_bdd_criteria(uc_writer_parser: AgentParser):
    """Test that agent covers BDD acceptance criteria."""
    responsibilities = uc_writer_parser.get_section("Responsibilities")
    content = responsibilities.lower()

    assert "bdd" in content or "acceptance criteria" in content
    assert "gherkin" in content or "given-when-then" in content


@pytest.mark.unit
def test_uc_writer_covers_actors_identification(uc_writer_parser: AgentParser):
    """Test that agent covers actor identification."""
    responsibilities = uc_writer_parser.get_section("Responsibilities")
    assert "actor" in responsibilities.lower()


@pytest.mark.unit
def test_uc_writer_covers_flows_documentation(uc_writer_parser: AgentParser):
    """Test that agent covers flow documentation."""
    responsibilities = uc_writer_parser.get_section("Responsibilities")
    content = responsibilities.lower()

    assert "flow" in content
    assert "main" in content or "happy" in content or "alternative" in content


@pytest.mark.unit
def test_uc_writer_covers_nfr_elicitation(uc_writer_parser: AgentParser):
    """Test that agent covers non-functional requirements."""
    responsibilities = uc_writer_parser.get_section("Responsibilities")
    content = responsibilities.lower()

    assert (
        "non-functional" in content or
        "performance" in content or
        "security" in content or
        "nfr" in content
    )


# ============================================================================
# Test: Process Steps - 16 Section Interview
# ============================================================================

@pytest.mark.unit
def test_uc_writer_process_determines_uc_id(uc_writer_parser: AgentParser):
    """Test that process includes determining next UC ID."""
    process_steps = uc_writer_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "uc id" in process_text or "uc-" in process_text


@pytest.mark.unit
def test_uc_writer_process_includes_objective_elicitation(uc_writer_parser: AgentParser):
    """Test that process includes eliciting objective."""
    process_steps = uc_writer_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "objective" in process_text


@pytest.mark.unit
def test_uc_writer_process_includes_actor_identification(uc_writer_parser: AgentParser):
    """Test that process includes actor identification."""
    process_steps = uc_writer_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "actor" in process_text


@pytest.mark.unit
def test_uc_writer_process_includes_acceptance_criteria_generation(uc_writer_parser: AgentParser):
    """Test that process includes generating acceptance criteria."""
    process_steps = uc_writer_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "acceptance criteria" in process_text or "gherkin" in process_text


@pytest.mark.unit
def test_uc_writer_process_includes_service_identification(uc_writer_parser: AgentParser):
    """Test that process includes identifying services."""
    process_steps = uc_writer_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "service" in process_text


# ============================================================================
# Test: UC Creation Checklist
# ============================================================================

@pytest.mark.unit
def test_uc_writer_has_comprehensive_checklist(uc_writer_parser: AgentParser):
    """Test that agent has comprehensive UC creation checklist."""
    # Look for checklist section
    content = uc_writer_parser.content.lower()

    assert "checklist" in content
    assert "basic information" in content
    assert "core requirements" in content


@pytest.mark.unit
def test_uc_writer_checklist_includes_basic_info(uc_writer_parser: AgentParser):
    """Test that checklist includes basic information items."""
    content = uc_writer_parser.content.lower()

    assert "uc id" in content
    assert "title" in content
    assert "priority" in content
    assert "estimated effort" in content


@pytest.mark.unit
def test_uc_writer_checklist_includes_flows(uc_writer_parser: AgentParser):
    """Test that checklist includes flow requirements."""
    content = uc_writer_parser.content.lower()

    assert "main flow" in content
    assert "alternative flow" in content or "alternative" in content
    assert "error scenario" in content or "error" in content


# ============================================================================
# Test: Quality Checks
# ============================================================================

@pytest.mark.unit
def test_uc_writer_quality_checks_include_uc_id(uc_writer_parser: AgentParser):
    """Test that quality checks verify UC ID assignment."""
    checkboxes = uc_writer_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes).lower()

    assert "uc id" in checkboxes_text or "uc-" in checkboxes_text


@pytest.mark.unit
def test_uc_writer_quality_checks_include_services(uc_writer_parser: AgentParser):
    """Test that quality checks verify Services Used section."""
    checkboxes = uc_writer_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes).lower()

    assert "service" in checkboxes_text


@pytest.mark.unit
def test_uc_writer_quality_checks_reject_placeholders(uc_writer_parser: AgentParser):
    """Test that quality checks reject placeholder text."""
    checkboxes = uc_writer_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes).lower()

    assert "placeholder" in checkboxes_text or "[" in checkboxes_text


@pytest.mark.unit
def test_uc_writer_quality_checks_include_gherkin(uc_writer_parser: AgentParser):
    """Test that quality checks verify Gherkin format."""
    checkboxes = uc_writer_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes).lower()

    assert "gherkin" in checkboxes_text or "given-when-then" in checkboxes_text


@pytest.mark.unit
def test_uc_writer_quality_checks_minimum_flow_steps(uc_writer_parser: AgentParser):
    """Test that quality checks require minimum flow steps."""
    checkboxes = uc_writer_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes)

    # Should require at least 3 steps in main flow
    assert "3" in checkboxes_text or "≥3" in checkboxes_text or "three" in checkboxes_text.lower()


# ============================================================================
# Test: Anti-Patterns
# ============================================================================

@pytest.mark.unit
def test_uc_writer_warns_against_vague_requirements(uc_writer_parser: AgentParser):
    """Test that anti-patterns warn against vague requirements."""
    antipatterns = uc_writer_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert "vague" in antipatterns_text or "generic" in antipatterns_text


@pytest.mark.unit
def test_uc_writer_warns_against_missing_services(uc_writer_parser: AgentParser):
    """Test that anti-patterns warn about missing Services Used section."""
    antipatterns = uc_writer_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert "service" in antipatterns_text


@pytest.mark.unit
def test_uc_writer_warns_against_placeholders(uc_writer_parser: AgentParser):
    """Test that anti-patterns warn about leaving placeholders."""
    antipatterns = uc_writer_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert "placeholder" in antipatterns_text or "[" in antipatterns_text


@pytest.mark.unit
def test_uc_writer_warns_against_generic_acceptance_criteria(uc_writer_parser: AgentParser):
    """Test that anti-patterns warn about generic acceptance criteria."""
    antipatterns = uc_writer_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert (
        "generic" in antipatterns_text and "acceptance" in antipatterns_text or
        "generic acceptance criteria" in antipatterns_text
    )


# ============================================================================
# Test: Interview Question Library
# ============================================================================

@pytest.mark.unit
def test_uc_writer_provides_interview_questions(uc_writer_parser: AgentParser):
    """Test that agent provides interview question library."""
    content = uc_writer_parser.content.lower()

    assert "interview question" in content or "question library" in content


@pytest.mark.unit
def test_uc_writer_questions_cover_objective(uc_writer_parser: AgentParser):
    """Test that questions cover objective and user value."""
    content = uc_writer_parser.content

    # Should have questions about problem, objective, value
    assert "What problem" in content or "what problem" in content
    assert "value" in content.lower()


@pytest.mark.unit
def test_uc_writer_questions_cover_actors(uc_writer_parser: AgentParser):
    """Test that questions cover actors."""
    content = uc_writer_parser.content

    assert "Who initiates" in content or "who initiates" in content or "Who uses" in content


@pytest.mark.unit
def test_uc_writer_questions_cover_errors(uc_writer_parser: AgentParser):
    """Test that questions cover error scenarios."""
    content = uc_writer_parser.content

    assert "What can go wrong" in content or "what can go wrong" in content


# ============================================================================
# Test: Code Examples
# ============================================================================

@pytest.mark.unit
def test_uc_writer_provides_interview_flow_example(uc_writer_parser: AgentParser):
    """Test that agent provides example interview flow."""
    content = uc_writer_parser.content.lower()

    assert "example interview" in content or "example flow" in content


@pytest.mark.unit
def test_uc_writer_example_shows_complete_uc(uc_writer_parser: AgentParser):
    """Test that example shows complete UC structure."""
    content = uc_writer_parser.content

    # Example should show UC structure
    has_uc_structure = (
        "UC-" in content and
        "Objective" in content and
        "Actors" in content and
        "Main Flow" in content
    )

    assert has_uc_structure, "Should provide complete UC example"


# ============================================================================
# Test: File Operations
# ============================================================================

@pytest.mark.unit
def test_uc_writer_reads_template(uc_writer_parser: AgentParser):
    """Test that agent reads UC template."""
    files_section = uc_writer_parser.get_section("Files")

    assert "use-case-template" in files_section.lower()


@pytest.mark.unit
def test_uc_writer_reads_service_registry(uc_writer_parser: AgentParser):
    """Test that agent reads service registry."""
    files_section = uc_writer_parser.get_section("Files")

    assert "service-registry" in files_section.lower() or "service" in files_section.lower()


@pytest.mark.unit
def test_uc_writer_writes_to_specs_directory(uc_writer_parser: AgentParser):
    """Test that agent writes to specs/use-cases/ directory."""
    files_section = uc_writer_parser.get_section("Files")

    assert "specs/use-cases" in files_section or "UC-" in files_section


# ============================================================================
# Test: Framework Compliance
# ============================================================================

@pytest.mark.unit
def test_uc_writer_enforces_rule_1(uc_writer_parser: AgentParser):
    """Test that agent enforces Rule #1 (Specifications Are Law)."""
    content = uc_writer_parser.content.lower()

    assert "rule #1" in content or "rule 1" in content or "specifications are law" in content


@pytest.mark.unit
def test_uc_writer_mentions_service_oriented_architecture(uc_writer_parser: AgentParser):
    """Test that agent mentions service-oriented architecture."""
    content = uc_writer_parser.content.lower()

    assert "service-oriented" in content or "service oriented" in content


# ============================================================================
# Test: Output Specification
# ============================================================================

@pytest.mark.unit
def test_uc_writer_output_lists_16_sections(uc_writer_parser: AgentParser):
    """Test that output section describes all UC sections."""
    output_section = uc_writer_parser.get_section("Output")

    # Should mention key sections
    assert "Objective" in output_section
    assert "Actors" in output_section
    assert "Main Flow" in output_section
    assert "Acceptance Criteria" in output_section
    assert "Services Used" in output_section


@pytest.mark.unit
def test_uc_writer_output_requires_gherkin_scenarios(uc_writer_parser: AgentParser):
    """Test that output requires Gherkin scenarios."""
    output_section = uc_writer_parser.get_section("Output")

    assert "Gherkin" in output_section or "Given-When-Then" in output_section


# ============================================================================
# Test: Next Steps
# ============================================================================

@pytest.mark.unit
def test_uc_writer_next_steps_mention_bdd_scenario_writer(uc_writer_parser: AgentParser):
    """Test that next steps mention bdd-scenario-writer agent."""
    next_steps = uc_writer_parser.get_section("Next Steps")

    if next_steps:
        assert "bdd-scenario-writer" in next_steps.lower()


@pytest.mark.unit
def test_uc_writer_next_steps_mention_test_writer(uc_writer_parser: AgentParser):
    """Test that next steps mention test-writer agent."""
    next_steps = uc_writer_parser.get_section("Next Steps")

    if next_steps:
        assert "test-writer" in next_steps.lower()


# ============================================================================
# Test: Content Quality
# ============================================================================

@pytest.mark.unit
def test_uc_writer_has_comprehensive_process(uc_writer_parser: AgentParser):
    """Test that process is comprehensive (16+ steps for 16 sections)."""
    process_steps = uc_writer_parser.extract_process_steps()

    assert len(process_steps) >= 15, (
        f"uc-writer should have ≥15 process steps for 16-section interview, "
        f"found {len(process_steps)}"
    )


@pytest.mark.unit
def test_uc_writer_mentions_data_requirements(uc_writer_parser: AgentParser):
    """Test that agent covers data requirements section."""
    content = uc_writer_parser.content.lower()

    assert "data requirement" in content or "input data" in content
    assert "validation" in content


@pytest.mark.unit
def test_uc_writer_mentions_implementation_plan(uc_writer_parser: AgentParser):
    """Test that agent covers implementation planning."""
    content = uc_writer_parser.content.lower()

    assert "implementation plan" in content or "iteration" in content
