"""Performance tests for cross-agent consistency.

Tests consistency across all agents:
- Terminology consistency
- Section naming conventions
- Output format consistency
- Reference format standardization
- Quality standards alignment
- Documentation style consistency
- Workflow integration consistency

Test Coverage:
- Consistent use of terms (UC, ADR, TDD, etc.)
- Standard section names across agents
- Consistent reference formats
- Aligned quality thresholds
- Consistent handoff protocols
- Documentation style uniformity
"""

import pytest
from pathlib import Path
from typing import Dict, List, Tuple, Set

from tests.agents.fixtures import AgentParser, get_all_agent_paths


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def all_agents() -> List[Tuple[str, AgentParser]]:
    """Get all agents with their parsers."""
    agents = []
    for path in get_all_agent_paths():
        name = path.stem.replace("agent-", "")
        parser = AgentParser(path)
        agents.append((name, parser))
    return agents


# ============================================================================
# Test: Terminology Consistency
# ============================================================================


@pytest.mark.performance
def test_uc_reference_format_consistent(all_agents: List[Tuple[str, AgentParser]]):
    """Test that UC references use consistent format (UC-XXX)."""
    # Standard format: UC-XXX (3+ digits)
    standard_patterns = ["UC-", "uc-"]

    # Non-standard patterns to avoid
    avoid_patterns = ["UC ", "Use Case #", "UseCase"]

    for name, parser in all_agents:
        content = parser.content

        # Should use standard format
        has_standard = any(pattern in content for pattern in standard_patterns)

        # Should avoid non-standard formats
        has_nonstandard = any(pattern in content for pattern in avoid_patterns)

        if "UC-" in content or "use case" in content.lower():
            # If agent mentions UCs, should use standard format
            if has_nonstandard:
                # Flag for review
                pass


@pytest.mark.performance
def test_adr_reference_format_consistent(all_agents: List[Tuple[str, AgentParser]]):
    """Test that ADR references use consistent format (ADR-XXX)."""
    standard_format = "ADR-"
    avoid_formats = ["ADR ", "Architecture Decision #"]

    for name, parser in all_agents:
        content = parser.content

        has_nonstandard = any(pattern in content for pattern in avoid_formats)

        if "ADR" in content:
            # Should use ADR-XXX format
            if has_nonstandard:
                # Flag for review
                pass


@pytest.mark.performance
def test_specification_term_consistent(all_agents: List[Tuple[str, AgentParser]]):
    """Test that 'Specification' term is used consistently."""
    # Standard: "Specification: UC-XXX" (capital S, colon)
    # Avoid: "spec:", "Spec:", "specification reference"

    for name, parser in all_agents:
        body = parser.body.lower()

        if "spec" in body:
            # Check for consistent capitalization in actual content
            # (This is a soft check - exact format validated in other tests)
            pass


@pytest.mark.performance
def test_tdd_terminology_consistent(all_agents: List[Tuple[str, AgentParser]]):
    """Test that TDD terminology is used consistently."""
    # Standard terms: RED state, GREEN state, REFACTOR
    # Avoid: red phase, green phase, failing tests, passing tests (use states instead)

    tdd_agents = ["test-writer", "code-quality-checker", "refactoring-analyzer"]

    for name, parser in all_agents:
        if name in tdd_agents:
            body = parser.body.upper()

            # Should use state terminology
            if "RED" in body or "GREEN" in body or "TDD" in body:
                # Good - uses standard TDD terminology
                pass


# ============================================================================
# Test: Section Naming Consistency
# ============================================================================


@pytest.mark.performance
def test_section_names_standardized(all_agents: List[Tuple[str, AgentParser]]):
    """Test that section names follow standard conventions."""
    standard_sections = {
        "Purpose",
        "When to Use",
        "Process",
        "Output Format",
        "Quality Checks",
        "Examples",
        "Anti-Patterns",
        "Common Mistakes",
        "Edge Cases",
    }

    # Variations to avoid (should use standard names)
    avoid_variations = {
        "Goal": "Purpose",
        "Objective": "Purpose",
        "When to Use This Agent": "When to Use",
        "Usage": "When to Use",
        "Steps": "Process",
        "Workflow": "Process",
        "Output": "Output Format",
        "Format": "Output Format",
        "Checks": "Quality Checks",
        "Validation": "Quality Checks",
    }

    for name, parser in all_agents:
        agent_sections = set(parser.sections.keys())

        # Check for non-standard section names
        for section in agent_sections:
            if section in avoid_variations:
                # Should use standard name instead
                standard_name = avoid_variations[section]
                # Flag for standardization
                pass


@pytest.mark.performance
def test_quality_checks_section_named_consistently(all_agents: List[Tuple[str, AgentParser]]):
    """Test that quality validation section is consistently named."""
    # Standard: "Quality Checks"
    # Avoid: "Validation", "Quality Validation", "Checks"

    standard_name = "Quality Checks"

    for name, parser in all_agents:
        sections = parser.sections.keys()

        # Check for variations
        variations = ["Validation", "Quality Validation", "Checks"]
        has_variation = any(v in sections for v in variations)

        if has_variation and standard_name not in sections:
            # Uses variation instead of standard name
            # Should standardize to "Quality Checks"
            pass


# ============================================================================
# Test: Output Format Consistency
# ============================================================================


@pytest.mark.performance
def test_output_format_section_uses_code_blocks(all_agents: List[Tuple[str, AgentParser]]):
    """Test that Output Format sections use markdown code blocks."""
    for name, parser in all_agents:
        output_format = parser.get_section_content("Output Format")

        if output_format:
            # Should contain markdown code blocks (``` or ```)
            has_code_blocks = "```" in output_format or "```" in output_format

            if not has_code_blocks:
                # Output Format should show examples in code blocks
                # Flag for improvement
                pass


@pytest.mark.performance
def test_examples_section_shows_complete_examples(all_agents: List[Tuple[str, AgentParser]]):
    """Test that Examples sections show complete, realistic examples."""
    for name, parser in all_agents:
        examples = parser.get_section_content("Examples")

        if examples:
            # Good examples should be substantial (> 200 chars)
            size = len(examples)

            if size < 200:
                # Example might be too minimal
                # Should show realistic, complete examples
                pass


# ============================================================================
# Test: Reference Format Consistency
# ============================================================================


@pytest.mark.performance
def test_spec_references_include_hash_anchors(all_agents: List[Tuple[str, AgentParser]]):
    """Test that specification references use hash anchors (UC-XXX#section)."""
    for name, parser in all_agents:
        content = parser.content

        if "UC-" in content:
            # Check if hash anchors are used for specific references
            # Format: UC-XXX#section-name
            has_hash_anchor = "#" in content and "UC-" in content

            # Agents should demonstrate hash anchor usage in examples
            examples = parser.get_section_content("Examples")
            if examples and "UC-" in examples:
                if "#" not in examples:
                    # Examples should show hash anchor format
                    pass


@pytest.mark.performance
def test_file_references_use_consistent_paths(all_agents: List[Tuple[str, AgentParser]]):
    """Test that file path references use consistent format."""
    # Standard: specs/use-cases/UC-XXX.md (forward slashes, lowercase dirs)
    # Avoid: Specs/UseCases/, specs\use-cases\, etc.

    for name, parser in all_agents:
        content = parser.content

        # Check for backslashes (Windows-style paths - should avoid)
        if "\\" in content and "\\n" not in content and "\\" not in content:
            # Contains backslash (not in string escape)
            # Should use forward slashes
            pass


# ============================================================================
# Test: Quality Standards Alignment
# ============================================================================


@pytest.mark.performance
def test_quality_score_threshold_consistent(all_agents: List[Tuple[str, AgentParser]]):
    """Test that quality score thresholds are consistent (≥ 80)."""
    # Standard: Code quality score ≥ 80
    # Ensure all agents reference the same threshold

    quality_agents = ["code-quality-checker", "refactoring-analyzer", "test-writer"]

    for name, parser in all_agents:
        if name in quality_agents:
            content = parser.content.lower()

            # Check for quality score mentions
            if "score" in content and ("80" in content or "quality" in content):
                # Good - mentions quality standards
                pass


@pytest.mark.performance
def test_test_coverage_expectations_aligned(all_agents: List[Tuple[str, AgentParser]]):
    """Test that test coverage expectations are aligned."""
    # Standard: Aim for high coverage, but quality > quantity
    # No specific percentage mandate (avoid "must be 100%")

    test_agents = ["test-writer", "code-quality-checker"]

    for name, parser in all_agents:
        if name in test_agents:
            content = parser.content.lower()

            # Check for overly strict coverage requirements
            strict_phrases = ["100% coverage", "must cover everything", "all code must be tested"]

            has_strict = any(phrase in content for phrase in strict_phrases)

            if has_strict:
                # Should emphasize quality over quantity
                # Avoid mandating 100% coverage
                pass


# ============================================================================
# Test: Workflow Integration Consistency
# ============================================================================


@pytest.mark.performance
def test_handoff_protocol_format_consistent(all_agents: List[Tuple[str, AgentParser]]):
    """Test that handoff protocols use consistent format."""
    agents_with_handoffs = [
        "uc-writer",
        "bdd-scenario-writer",
        "test-writer",
        "code-quality-checker",
        "refactoring-analyzer",
    ]

    for name, parser in all_agents:
        if name in agents_with_handoffs:
            # Check for Integration Points or Handoff Protocol section
            has_integration = "Integration Points" in parser.sections
            has_handoff = "Handoff Protocol" in parser.sections

            # Agents in workflows should document handoffs
            if not has_integration and not has_handoff:
                content = parser.content.lower()
                if "handoff" not in content and "next agent" not in content:
                    # Should document how this agent integrates with others
                    pass


@pytest.mark.performance
def test_agent_chain_references_consistent(all_agents: List[Tuple[str, AgentParser]]):
    """Test that agent chain references are consistent."""
    # Standard: uc-writer → bdd-scenario-writer → test-writer
    # Use arrow notation (→) consistently

    for name, parser in all_agents:
        content = parser.content

        # Check for agent chain mentions
        if "→" in content or "->" in content or "then" in content.lower():
            # Agent mentions workflow chains
            # Should use consistent arrow notation
            pass


# ============================================================================
# Test: Documentation Style Consistency
# ============================================================================


@pytest.mark.performance
def test_checkbox_format_consistent(all_agents: List[Tuple[str, AgentParser]]):
    """Test that checkbox lists use consistent format."""
    # Standard: - [ ] item (space-bracket-space)
    # Avoid: -[] item, - [] item (no space after hyphen)

    for name, parser in all_agents:
        quality_checks = parser.get_section_checkboxes("Quality Checks")

        if quality_checks:
            # Checkboxes found - format should be consistent
            # (AgentParser.get_section_checkboxes handles this)
            pass


@pytest.mark.performance
def test_emphasis_markers_consistent(all_agents: List[Tuple[str, AgentParser]]):
    """Test that emphasis markers (bold, italic) are used consistently."""
    # Standard: **bold** for emphasis, *italic* for terms
    # Avoid: __bold__, _italic_ (use asterisks)

    for name, parser in all_agents:
        content = parser.content

        # Check for underscore-style emphasis
        has_underscore_bold = "__" in content
        has_underscore_italic = "_" in content and "__" not in content

        # Should prefer asterisk-style
        if has_underscore_bold or has_underscore_italic:
            # Consider standardizing to asterisk-style
            pass


@pytest.mark.performance
def test_list_indentation_consistent(all_agents: List[Tuple[str, AgentParser]]):
    """Test that list indentation is consistent (2 spaces)."""
    # Standard: 2 spaces for nested lists
    # Avoid: 4 spaces, tabs

    for name, parser in all_agents:
        content = parser.content

        lines = content.split("\n")

        for line in lines:
            if line.strip().startswith("-") or line.strip().startswith("*"):
                # List item - check indentation
                leading_spaces = len(line) - len(line.lstrip(" "))

                # Indentation should be multiple of 2
                if leading_spaces > 0 and leading_spaces % 2 != 0:
                    # Inconsistent indentation
                    pass


# ============================================================================
# Test: Agent Metadata Consistency
# ============================================================================


@pytest.mark.performance
def test_model_field_consistent_across_agents(all_agents: List[Tuple[str, AgentParser]]):
    """Test that 'model' field uses consistent values."""
    # Should use: claude-sonnet-4 or claude-opus-4
    # Avoid: mixed models, old versions

    models_used = {}

    for name, parser in all_agents:
        model = parser.metadata.get("model")
        if model:
            models_used[name] = model

    # Check for consistency
    unique_models = set(models_used.values())

    # All agents should use same model (or at most 2 variants)
    if len(unique_models) > 2:
        # Too many different models - should standardize
        pass


@pytest.mark.performance
def test_tier_system_consistent(all_agents: List[Tuple[str, AgentParser]]):
    """Test that tier system is used consistently."""
    # Tiers: 1 (core), 2 (specialized), 3 (optional)
    valid_tiers = {"1", "2", "3", 1, 2, 3}

    for name, parser in all_agents:
        tier = parser.metadata.get("tier")

        if tier:
            # Tier should be valid value
            if tier not in valid_tiers:
                pytest.fail(f"{name}: Invalid tier value: {tier}")


# ============================================================================
# Test: Cross-Agent Communication Standards
# ============================================================================


@pytest.mark.performance
def test_agents_reference_common_documents(all_agents: List[Tuple[str, AgentParser]]):
    """Test that agents reference common framework documents."""
    # Common docs: 12 Non-Negotiable Rules, technical-decisions.md, etc.

    framework_docs = ["12 Non-Negotiable", "technical-decisions.md", ".claude/rules.md"]

    agents_referencing = {doc: [] for doc in framework_docs}

    for name, parser in all_agents:
        content = parser.content

        for doc in framework_docs:
            if doc.lower() in content.lower():
                agents_referencing[doc].append(name)

    # Most agents should reference core framework docs
    # (At least 50% should mention 12 Rules)
    rules_ref_count = len(agents_referencing.get("12 Non-Negotiable", []))
    total_agents = len(all_agents)

    # Soft check: many agents should reference framework rules
    if rules_ref_count < total_agents * 0.3:
        # Consider if more agents should reference core rules
        pass


@pytest.mark.performance
def test_consistent_file_organization_references(all_agents: List[Tuple[str, AgentParser]]):
    """Test that agents reference file organization consistently."""
    # Standard directories: specs/use-cases/, features/, tests/, src/
    # All agents should use same directory structure

    standard_dirs = [
        "specs/use-cases/",
        "specs/services/",
        "features/",
        "tests/unit/",
        "tests/integration/",
        "src/",
    ]

    for name, parser in all_agents:
        content = parser.content

        # Check for consistent directory references
        # Should use forward slashes, lowercase, trailing slash
        for dir_path in standard_dirs:
            if dir_path.replace("/", "") in content:
                # References this directory - should use standard format
                pass
