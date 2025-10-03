"""Behavioral tests for adr-manager agent.

Tests the adr-manager agent's ability to:
- Interview user for technical decision details
- Determine if decision qualifies as ADR (decision tree)
- Generate ADR with proper format and sequential numbering
- Check implementation compliance against existing ADRs
- Detect architectural violations with evidence
- Guide ADR lifecycle (deprecation, superseding, status updates)

Test Coverage:
- ADR creation mode
- Compliance checking mode
- Decision qualification
- Format validation
- Violation detection
- Lifecycle management
"""

import pytest
from pathlib import Path

from tests.agents.fixtures import AgentParser


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def adr_manager_parser(agents_dir: Path) -> AgentParser:
    """Parser for adr-manager agent."""
    return AgentParser(agents_dir / "adr-manager.md")


# ============================================================================
# Test: Agent Metadata
# ============================================================================


@pytest.mark.unit
def test_adr_manager_has_correct_metadata(adr_manager_parser: AgentParser):
    """Test that adr-manager has correct metadata."""
    assert adr_manager_parser.name == "adr-manager"
    assert adr_manager_parser.get_metadata_field("model") == "opus"

    # Should have tools for reading, writing, and searching
    tools = adr_manager_parser.get_metadata_field("tools")
    assert "Read" in tools
    assert "Write" in tools
    assert "Grep" in tools
    assert "Glob" in tools


# ============================================================================
# Test: Responsibilities Coverage
# ============================================================================


@pytest.mark.unit
def test_adr_manager_covers_decision_interviewing(adr_manager_parser: AgentParser):
    """Test that agent covers decision interviewing."""
    responsibilities = adr_manager_parser.get_section("Responsibilities")
    assert "interview" in responsibilities.lower()


@pytest.mark.unit
def test_adr_manager_covers_decision_qualification(adr_manager_parser: AgentParser):
    """Test that agent covers decision qualification."""
    responsibilities = adr_manager_parser.get_section("Responsibilities")
    assert "qualif" in responsibilities.lower() or "decision tree" in responsibilities.lower()


@pytest.mark.unit
def test_adr_manager_covers_adr_generation(adr_manager_parser: AgentParser):
    """Test that agent covers ADR generation."""
    responsibilities = adr_manager_parser.get_section("Responsibilities")
    assert "generate" in responsibilities.lower() or "create" in responsibilities.lower()


@pytest.mark.unit
def test_adr_manager_covers_compliance_checking(adr_manager_parser: AgentParser):
    """Test that agent covers compliance checking."""
    responsibilities = adr_manager_parser.get_section("Responsibilities")
    assert "compliance" in responsibilities.lower()


@pytest.mark.unit
def test_adr_manager_covers_violation_detection(adr_manager_parser: AgentParser):
    """Test that agent covers violation detection."""
    responsibilities = adr_manager_parser.get_section("Responsibilities")
    assert "violation" in responsibilities.lower()


@pytest.mark.unit
def test_adr_manager_covers_lifecycle_management(adr_manager_parser: AgentParser):
    """Test that agent covers lifecycle management."""
    responsibilities = adr_manager_parser.get_section("Responsibilities")
    content = responsibilities.lower()

    assert "lifecycle" in content or "deprecat" in content or "supersed" in content


# ============================================================================
# Test: ADR Management Checklist
# ============================================================================


@pytest.mark.unit
def test_adr_manager_defines_adr_format(adr_manager_parser: AgentParser):
    """Test that agent defines ADR format requirements."""
    content = adr_manager_parser.content

    # Should define all required sections
    assert "Context" in content
    assert "Decision" in content
    assert "Consequences" in content
    assert "Alternatives" in content


@pytest.mark.unit
def test_adr_manager_requires_minimum_alternatives(adr_manager_parser: AgentParser):
    """Test that agent requires minimum 2 alternatives."""
    content = adr_manager_parser.content.lower()

    assert "at least 2" in content or "minimum 2" in content or "≥2" in content


# ============================================================================
# Test: Decision Tree
# ============================================================================


@pytest.mark.unit
def test_adr_manager_has_decision_tree(adr_manager_parser: AgentParser):
    """Test that agent has ADR qualification decision tree."""
    content = adr_manager_parser.content.lower()

    assert "decision tree" in content


@pytest.mark.unit
def test_adr_manager_decision_tree_questions(adr_manager_parser: AgentParser):
    """Test that decision tree includes qualification questions."""
    content = adr_manager_parser.content.lower()

    # Should have questions about impact, options, change difficulty
    assert "multiple parts" in content or "impact" in content
    assert "multiple options" in content or "choice" in content
    assert "hard to change" in content


# ============================================================================
# Test: Process Steps - Creation Mode
# ============================================================================


@pytest.mark.unit
def test_adr_manager_process_determines_qualification(adr_manager_parser: AgentParser):
    """Test that process includes determining ADR qualification."""
    process_steps = adr_manager_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "qualification" in process_text or "decision tree" in process_text


@pytest.mark.unit
def test_adr_manager_process_finds_next_number(adr_manager_parser: AgentParser):
    """Test that process includes finding next ADR number."""
    process_steps = adr_manager_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "adr number" in process_text or "next" in process_text and "number" in process_text


@pytest.mark.unit
def test_adr_manager_process_interviews_for_context(adr_manager_parser: AgentParser):
    """Test that process includes interviewing for context."""
    process_steps = adr_manager_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "context" in process_text


@pytest.mark.unit
def test_adr_manager_process_interviews_for_alternatives(adr_manager_parser: AgentParser):
    """Test that process includes interviewing for alternatives."""
    process_steps = adr_manager_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "alternative" in process_text


@pytest.mark.unit
def test_adr_manager_process_interviews_for_consequences(adr_manager_parser: AgentParser):
    """Test that process includes interviewing for consequences."""
    process_steps = adr_manager_parser.extract_process_steps()
    process_text = " ".join(process_steps).lower()

    assert "consequence" in process_text


# ============================================================================
# Test: Process Steps - Compliance Mode
# ============================================================================


@pytest.mark.unit
def test_adr_manager_compliance_reads_all_adrs(adr_manager_parser: AgentParser):
    """Test that compliance process reads all ADRs."""
    content = adr_manager_parser.content.lower()

    assert "read all adrs" in content or "parse" in content and "adr" in content


@pytest.mark.unit
def test_adr_manager_compliance_scans_implementation(adr_manager_parser: AgentParser):
    """Test that compliance process scans implementation files."""
    content = adr_manager_parser.content.lower()

    assert "scan implementation" in content or "implementation files" in content


@pytest.mark.unit
def test_adr_manager_compliance_detects_violations(adr_manager_parser: AgentParser):
    """Test that compliance process detects violations."""
    content = adr_manager_parser.content.lower()

    assert "detect violation" in content or "detect technology violations" in content


# ============================================================================
# Test: Interview Question Library
# ============================================================================


@pytest.mark.unit
def test_adr_manager_provides_question_library(adr_manager_parser: AgentParser):
    """Test that agent provides interview question library."""
    content = adr_manager_parser.content.lower()

    assert "interview question" in content or "question library" in content


@pytest.mark.unit
def test_adr_manager_questions_cover_context(adr_manager_parser: AgentParser):
    """Test that questions cover context."""
    content = adr_manager_parser.content

    assert "What problem" in content or "what problem" in content


@pytest.mark.unit
def test_adr_manager_questions_cover_alternatives(adr_manager_parser: AgentParser):
    """Test that questions cover alternatives."""
    content = adr_manager_parser.content

    assert "What other options" in content or "what other options" in content


@pytest.mark.unit
def test_adr_manager_questions_cover_consequences(adr_manager_parser: AgentParser):
    """Test that questions cover consequences."""
    content = adr_manager_parser.content

    assert "becomes EASIER" in content or "becomes HARDER" in content


# ============================================================================
# Test: Quality Checks
# ============================================================================


@pytest.mark.unit
def test_adr_manager_quality_checks_include_qualification(adr_manager_parser: AgentParser):
    """Test that quality checks verify ADR qualification."""
    checkboxes = adr_manager_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes).lower()

    assert "qualification" in checkboxes_text or "decision tree" in checkboxes_text


@pytest.mark.unit
def test_adr_manager_quality_checks_require_alternatives(adr_manager_parser: AgentParser):
    """Test that quality checks verify minimum alternatives."""
    checkboxes = adr_manager_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes).lower()

    assert "alternative" in checkboxes_text


@pytest.mark.unit
def test_adr_manager_quality_checks_require_consequences(adr_manager_parser: AgentParser):
    """Test that quality checks verify pros and cons."""
    checkboxes = adr_manager_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes).lower()

    assert "consequence" in checkboxes_text or "pros and cons" in checkboxes_text


@pytest.mark.unit
def test_adr_manager_quality_checks_verify_format(adr_manager_parser: AgentParser):
    """Test that quality checks verify ADR format."""
    checkboxes = adr_manager_parser.get_section_checkboxes("Quality Checks")
    checkboxes_text = " ".join(checkboxes).lower()

    assert "format" in checkboxes_text or "section" in checkboxes_text


# ============================================================================
# Test: Anti-Patterns
# ============================================================================


@pytest.mark.unit
def test_adr_manager_warns_against_trivial_decisions(adr_manager_parser: AgentParser):
    """Test that anti-patterns warn about ADRs for trivial decisions."""
    antipatterns = adr_manager_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert "trivial" in antipatterns_text or "decision tree" in antipatterns_text


@pytest.mark.unit
def test_adr_manager_warns_against_missing_alternatives(adr_manager_parser: AgentParser):
    """Test that anti-patterns warn about missing alternatives."""
    antipatterns = adr_manager_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert "alternative" in antipatterns_text


@pytest.mark.unit
def test_adr_manager_warns_against_vague_content(adr_manager_parser: AgentParser):
    """Test that anti-patterns warn about vague context or consequences."""
    antipatterns = adr_manager_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert "vague" in antipatterns_text or "specific" in antipatterns_text


@pytest.mark.unit
def test_adr_manager_warns_against_ignoring_violations(adr_manager_parser: AgentParser):
    """Test that anti-patterns warn about ignoring violations."""
    antipatterns = adr_manager_parser.extract_antipatterns()
    antipatterns_text = " ".join(antipatterns).lower()

    assert "ignoring" in antipatterns_text or "violation" in antipatterns_text


# ============================================================================
# Test: Code Examples
# ============================================================================


@pytest.mark.unit
def test_adr_manager_provides_adr_format_example(adr_manager_parser: AgentParser):
    """Test that agent provides complete ADR format example."""
    code_blocks = adr_manager_parser.extract_code_blocks("markdown")

    assert len(code_blocks) > 0, "Should have markdown ADR examples"


@pytest.mark.unit
def test_adr_manager_provides_compliance_report_example(adr_manager_parser: AgentParser):
    """Test that agent provides compliance report example."""
    content = adr_manager_parser.content.lower()

    assert "compliance report" in content and "example" in content


# ============================================================================
# Test: Output Specifications
# ============================================================================


@pytest.mark.unit
def test_adr_manager_output_defines_adr_structure(adr_manager_parser: AgentParser):
    """Test that output defines complete ADR structure."""
    output_section = adr_manager_parser.get_section("Output")

    # Should define ADR file format
    assert "ADR" in output_section
    assert "Context" in output_section or "context" in output_section.lower()
    assert "Decision" in output_section or "decision" in output_section.lower()


@pytest.mark.unit
def test_adr_manager_output_defines_compliance_report_structure(adr_manager_parser: AgentParser):
    """Test that output defines compliance report structure."""
    content = adr_manager_parser.content

    # Should have compliance report format section
    assert "Compliance Report Format" in content or "compliance report" in content.lower()


# ============================================================================
# Test: Violation Detection Patterns
# ============================================================================


@pytest.mark.unit
def test_adr_manager_defines_violation_patterns(adr_manager_parser: AgentParser):
    """Test that agent defines violation detection patterns."""
    content = adr_manager_parser.content.lower()

    assert "violation detection pattern" in content or "technology violations" in content


@pytest.mark.unit
def test_adr_manager_classifies_violation_severity(adr_manager_parser: AgentParser):
    """Test that agent classifies violation severity."""
    content = adr_manager_parser.content

    assert "CRITICAL" in content
    assert "HIGH" in content
    assert "MEDIUM" in content
    assert "LOW" in content


# ============================================================================
# Test: File Operations
# ============================================================================


@pytest.mark.unit
def test_adr_manager_reads_technical_decisions(adr_manager_parser: AgentParser):
    """Test that agent reads technical-decisions.md."""
    files_section = adr_manager_parser.get_section("Files")

    assert "technical-decisions.md" in files_section


@pytest.mark.unit
def test_adr_manager_writes_to_technical_decisions(adr_manager_parser: AgentParser):
    """Test that agent writes to technical-decisions.md."""
    files_section = adr_manager_parser.get_section("Files")

    assert "**Write**:" in files_section or "write" in files_section.lower()
    assert "technical-decisions.md" in files_section


# ============================================================================
# Test: Framework Compliance
# ============================================================================


@pytest.mark.unit
def test_adr_manager_enforces_rule_7(adr_manager_parser: AgentParser):
    """Test that agent enforces Rule #7 (Technical Decisions Are Binding)."""
    content = adr_manager_parser.content.lower()

    assert (
        "rule #7" in content or "rule 7" in content or "technical decisions are binding" in content
    )


# ============================================================================
# Test: Lifecycle Management
# ============================================================================


@pytest.mark.unit
def test_adr_manager_documents_deprecation_process(adr_manager_parser: AgentParser):
    """Test that agent documents ADR deprecation process."""
    content = adr_manager_parser.content

    assert "Deprecating an ADR" in content or "deprecation" in content.lower()


@pytest.mark.unit
def test_adr_manager_documents_superseding_process(adr_manager_parser: AgentParser):
    """Test that agent documents ADR superseding process."""
    content = adr_manager_parser.content

    assert "Superseding an ADR" in content or "supersed" in content.lower()


@pytest.mark.unit
def test_adr_manager_lifecycle_preserves_history(adr_manager_parser: AgentParser):
    """Test that lifecycle management preserves history."""
    content = adr_manager_parser.content.lower()

    assert "history preserved" in content or "original content preserved" in content


# ============================================================================
# Test: Next Steps
# ============================================================================


@pytest.mark.unit
def test_adr_manager_next_steps_mention_enforcement(adr_manager_parser: AgentParser):
    """Test that next steps mention ADR enforcement."""
    next_steps = adr_manager_parser.get_section("Next Steps")

    if next_steps:
        next_steps_lower = next_steps.lower()
        assert "enforce" in next_steps_lower or "compliance" in next_steps_lower


@pytest.mark.unit
def test_adr_manager_next_steps_mention_code_references(adr_manager_parser: AgentParser):
    """Test that next steps mention adding ADR references to code."""
    next_steps = adr_manager_parser.get_section("Next Steps")

    if next_steps:
        next_steps_lower = next_steps.lower()
        assert "reference in code" in next_steps_lower or "code reference" in next_steps_lower


# ============================================================================
# Test: Content Quality
# ============================================================================


@pytest.mark.unit
def test_adr_manager_provides_examples_of_worthy_decisions(adr_manager_parser: AgentParser):
    """Test that agent provides examples of ADR-worthy decisions."""
    content = adr_manager_parser.content

    assert "Examples of ADR-worthy" in content or "adr-worthy decisions" in content.lower()


@pytest.mark.unit
def test_adr_manager_provides_examples_of_non_worthy_decisions(adr_manager_parser: AgentParser):
    """Test that agent provides examples of non-ADR-worthy decisions."""
    content = adr_manager_parser.content

    assert "Examples of NOT ADR-worthy" in content or "not adr-worthy" in content.lower()
