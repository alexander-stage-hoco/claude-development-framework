"""Tests for agent structure and content validation.

Tests that all agents follow consistent markdown structure, formatting
conventions, and content quality standards.

Test Coverage:
- Required sections presence
- Section formatting conventions
- Content quality and completeness
- Code examples and documentation
"""

import pytest
import warnings
from pathlib import Path
from typing import List

from tests.agents.fixtures import AgentParser


# ============================================================================
# Constants
# ============================================================================

REQUIRED_SECTIONS = ["Responsibilities", "Process", "Output", "Quality Checks", "Files"]

RECOMMENDED_SECTIONS = ["Next Steps", "Anti-Patterns"]

# Anti-pattern section can have variations
ANTIPATTERN_VARIATIONS = ["Anti-Patterns", "Anti-patterns", "Antipatterns"]


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def all_agents(agents_dir: Path) -> List[AgentParser]:
    """Load all agent parsers."""
    return [AgentParser(f) for f in agents_dir.glob("*.md")]


@pytest.fixture(
    params=[
        f
        for f in (Path(__file__).parent.parent.parent.parent / ".claude" / "subagents").glob("*.md")
    ]
)
def agent_parser(request) -> AgentParser:
    """Parametrized fixture providing individual agent parsers."""
    return AgentParser(request.param)


# ============================================================================
# Test: Required Sections Presence
# ============================================================================


@pytest.mark.unit
def test_agent_has_responsibilities_section(agent_parser: AgentParser):
    """Test that agent has Responsibilities section."""
    assert agent_parser.has_section(
        "Responsibilities"
    ), f"Agent {agent_parser.name} missing Responsibilities section"


@pytest.mark.unit
def test_agent_has_process_section(agent_parser: AgentParser):
    """Test that agent has Process section."""
    assert agent_parser.has_section("Process"), f"Agent {agent_parser.name} missing Process section"


@pytest.mark.unit
def test_agent_has_output_section(agent_parser: AgentParser):
    """Test that agent has Output section."""
    assert agent_parser.has_section("Output"), f"Agent {agent_parser.name} missing Output section"


@pytest.mark.unit
def test_agent_has_quality_checks_section(agent_parser: AgentParser):
    """Test that agent has Quality Checks section."""
    assert agent_parser.has_section(
        "Quality Checks"
    ), f"Agent {agent_parser.name} missing Quality Checks section"


@pytest.mark.unit
def test_agent_has_antipatterns_section(agent_parser: AgentParser):
    """Test that agent has Anti-Patterns section (any variation)."""
    has_antipatterns = any(
        agent_parser.has_section(variation) for variation in ANTIPATTERN_VARIATIONS
    )

    assert has_antipatterns, (
        f"Agent {agent_parser.name} missing Anti-Patterns section "
        f"(checked: {', '.join(ANTIPATTERN_VARIATIONS)})"
    )


@pytest.mark.unit
def test_agent_has_files_section(agent_parser: AgentParser):
    """Test that agent has Files section."""
    assert agent_parser.has_section("Files"), f"Agent {agent_parser.name} missing Files section"


def test_all_agents_have_required_sections(all_agents: List[AgentParser]):
    """Test that all agents have all required sections."""
    incomplete_agents = []

    for agent in all_agents:
        missing = []

        for section in REQUIRED_SECTIONS:
            if not agent.has_section(section):
                missing.append(section)

        # Check anti-patterns (any variation)
        has_antipatterns = any(agent.has_section(var) for var in ANTIPATTERN_VARIATIONS)
        if not has_antipatterns:
            missing.append("Anti-Patterns")

        if missing:
            incomplete_agents.append(f"{agent.name}: missing {', '.join(missing)}")

    assert not incomplete_agents, f"Agents with incomplete sections:\n" + "\n".join(
        f"  - {a}" for a in incomplete_agents
    )


# ============================================================================
# Test: Process Section Format
# ============================================================================


@pytest.mark.unit
def test_process_has_numbered_steps(agent_parser: AgentParser):
    """Test that Process section uses numbered steps."""
    process_steps = agent_parser.extract_process_steps()

    assert len(process_steps) >= 3, (
        f"Agent {agent_parser.name}: Process should have ≥3 steps, " f"found {len(process_steps)}"
    )


@pytest.mark.unit
def test_process_steps_are_actionable(agent_parser: AgentParser):
    """Test that process steps use action verbs."""
    steps = agent_parser.extract_process_steps()

    if not steps:
        pytest.skip(f"Agent {agent_parser.name} has no extractable process steps")

    action_verbs = [
        "read",
        "write",
        "parse",
        "generate",
        "create",
        "analyze",
        "extract",
        "validate",
        "verify",
        "check",
        "run",
        "execute",
        "identify",
        "design",
        "implement",
        "test",
        "add",
        "ensure",
        "document",
        "update",
        "ask",
        "gather",
        "determine",
        "build",
        "scan",
        "detect",
        "calculate",
        "compare",
        "suggest",
        "review",
    ]

    # Check if steps start with action verbs
    actionable_steps = []
    for step in steps:
        step_lower = step.lower()
        is_actionable = any(step_lower.startswith(verb) for verb in action_verbs)
        actionable_steps.append(is_actionable)

    # At least 50% of steps should be actionable
    actionable_percentage = sum(actionable_steps) / len(steps)

    assert actionable_percentage >= 0.5, (
        f"Agent {agent_parser.name}: Only {actionable_percentage:.0%} of process steps "
        f"are actionable (need ≥50%)\n"
        f"Steps: {steps[:3]}"  # Show first 3 steps
    )


# ============================================================================
# Test: Quality Checks Section Format
# ============================================================================


@pytest.mark.unit
def test_quality_checks_use_checkbox_format(agent_parser: AgentParser):
    """Test that Quality Checks section uses checkbox format."""
    checkboxes = agent_parser.get_section_checkboxes("Quality Checks")

    assert len(checkboxes) >= 5, (
        f"Agent {agent_parser.name}: Quality Checks should have ≥5 checklist items, "
        f"found {len(checkboxes)}"
    )


@pytest.mark.unit
def test_quality_checks_cover_key_aspects(agent_parser: AgentParser):
    """Test that quality checks cover spec/test/quality aspects."""
    checkboxes = agent_parser.get_section_checkboxes("Quality Checks")

    if not checkboxes:
        pytest.skip(f"Agent {agent_parser.name} has no checkboxes in Quality Checks")

    content = " ".join(checkboxes).lower()

    # Should mention at least 2 of these aspects
    aspects = ["spec", "test", "quality", "coverage", "validation", "file", "output"]
    found_aspects = [aspect for aspect in aspects if aspect in content]

    assert len(found_aspects) >= 2, (
        f"Agent {agent_parser.name}: Quality Checks should cover multiple aspects "
        f"(found: {', '.join(found_aspects) if found_aspects else 'none'})"
    )


# ============================================================================
# Test: Anti-Patterns Section Format
# ============================================================================


@pytest.mark.unit
def test_antipatterns_exist(agent_parser: AgentParser):
    """Test that agent has anti-patterns defined."""
    antipatterns = agent_parser.extract_antipatterns()

    assert len(antipatterns) >= 3, (
        f"Agent {agent_parser.name}: Should have ≥3 anti-patterns, " f"found {len(antipatterns)}"
    )


@pytest.mark.unit
def test_antipatterns_provide_guidance(agent_parser: AgentParser):
    """Test that anti-patterns explain what NOT to do."""
    antipatterns = agent_parser.extract_antipatterns()

    if not antipatterns:
        pytest.skip(f"Agent {agent_parser.name} has no extractable anti-patterns")

    # Anti-patterns should contain negation or warning words
    negations = ["not", "never", "don't", "avoid", "no", "without", "missing", "skip", "weak"]

    patterns_with_negation = []
    for pattern in antipatterns:
        has_negation = any(neg in pattern.lower() for neg in negations)
        patterns_with_negation.append(has_negation)

    # At least 60% should have clear negation
    negation_percentage = sum(patterns_with_negation) / len(antipatterns)

    assert negation_percentage >= 0.6, (
        f"Agent {agent_parser.name}: {negation_percentage:.0%} of anti-patterns have negation "
        f"(need ≥60%)\n"
        f"Examples: {antipatterns[:2]}"
    )


# ============================================================================
# Test: Files Section Format
# ============================================================================


@pytest.mark.unit
def test_files_section_lists_operations(agent_parser: AgentParser):
    """Test that Files section lists Read/Write operations."""
    files_section = agent_parser.get_section("Files")

    assert files_section, f"Agent {agent_parser.name} missing Files section"

    # Should mention Read and/or Write operations
    has_read = "Read:" in files_section or "read:" in files_section.lower()
    has_write = "Write:" in files_section or "write:" in files_section.lower()

    assert (
        has_read or has_write
    ), f"Agent {agent_parser.name}: Files section should list Read or Write operations"


# ============================================================================
# Test: Code Examples
# ============================================================================


@pytest.mark.unit
def test_agent_code_blocks_extraction(agent_parser: AgentParser):
    """Test that code block extraction works."""
    code_blocks = agent_parser.extract_code_blocks()

    # Just verify extraction works (agents may have 0 blocks)
    assert isinstance(code_blocks, list), f"Agent {agent_parser.name}: code block extraction failed"


def test_agents_with_examples_report(all_agents: List[AgentParser]):
    """Generate report of agents with/without code examples."""
    with_examples = []
    without_examples = []

    for agent in all_agents:
        code_blocks = agent.extract_code_blocks()
        if code_blocks:
            with_examples.append(f"{agent.name} ({len(code_blocks)} blocks)")
        else:
            without_examples.append(agent.name)

    print(f"\n{'='*60}")
    print(f"Code Examples Report")
    print(f"{'='*60}")
    print(f"\nAgents with code examples ({len(with_examples)}):")
    for item in with_examples:
        print(f"  ✓ {item}")

    print(f"\nAgents without code examples ({len(without_examples)}):")
    for name in without_examples:
        print(f"  - {name}")

    percentage = (len(with_examples) / len(all_agents)) * 100
    print(f"\nCoverage: {percentage:.0f}% of agents have code examples")
    print(f"{'='*60}\n")

    # Most agents should have examples
    assert (
        len(with_examples) >= len(all_agents) * 0.7
    ), f"Only {percentage:.0f}% of agents have code examples (expected ≥70%)"


# ============================================================================
# Test: Content Quality
# ============================================================================


@pytest.mark.unit
def test_responsibilities_are_specific(agent_parser: AgentParser):
    """Test that Responsibilities section is detailed."""
    responsibilities = agent_parser.get_section("Responsibilities")

    assert responsibilities, f"Agent {agent_parser.name} missing Responsibilities section"

    assert len(responsibilities) >= 100, (
        f"Agent {agent_parser.name}: Responsibilities too brief "
        f"({len(responsibilities)} chars, need ≥100)"
    )


@pytest.mark.unit
def test_output_section_describes_deliverables(agent_parser: AgentParser):
    """Test that Output section describes what agent produces."""
    output_section = agent_parser.get_section("Output")

    assert output_section, f"Agent {agent_parser.name} missing Output section"

    # Should mention files, content, results, or deliverables
    keywords = [
        "file",
        "content",
        "result",
        "report",
        "generate",
        "create",
        "output",
        "produce",
        "return",
        "deliver",
        "provide",
    ]

    has_deliverable = any(kw in output_section.lower() for kw in keywords)

    assert has_deliverable, (
        f"Agent {agent_parser.name}: Output section should describe deliverables "
        f"(mention file/content/result/report/etc.)"
    )


@pytest.mark.unit
def test_next_steps_section_recommended(agent_parser: AgentParser):
    """Test that agent has Next Steps section (recommended)."""
    has_next_steps = agent_parser.has_section("Next Steps")

    # Don't fail, just warn
    if not has_next_steps:
        warnings.warn(
            f"Agent {agent_parser.name} missing 'Next Steps' section (recommended)", UserWarning
        )


# ============================================================================
# Test: Structure Consistency Report
# ============================================================================


def test_structure_consistency_report(all_agents: List[AgentParser]):
    """Generate comprehensive structure consistency report."""

    all_required = REQUIRED_SECTIONS + ["Anti-Patterns"]

    print(f"\n{'='*70}")
    print(f"Agent Structure Consistency Report ({len(all_agents)} agents)")
    print(f"{'='*70}\n")

    # Check each required section
    print("Required Sections:")
    for section in all_required:
        if section == "Anti-Patterns":
            # Check variations
            agents_with_section = sum(
                1
                for agent in all_agents
                if any(agent.has_section(var) for var in ANTIPATTERN_VARIATIONS)
            )
        else:
            agents_with_section = sum(1 for agent in all_agents if agent.has_section(section))

        percentage = (agents_with_section / len(all_agents)) * 100
        status = "✓" if percentage == 100 else "⚠"

        print(f"  {status} {section}: {agents_with_section}/{len(all_agents)} ({percentage:.0f}%)")

    # Check recommended sections
    print("\nRecommended Sections:")
    for section in RECOMMENDED_SECTIONS:
        agents_with_section = sum(1 for agent in all_agents if agent.has_section(section))
        percentage = (agents_with_section / len(all_agents)) * 100
        print(f"    {section}: {agents_with_section}/{len(all_agents)} ({percentage:.0f}%)")

    # Code examples
    agents_with_examples = sum(1 for agent in all_agents if agent.extract_code_blocks())
    percentage = (agents_with_examples / len(all_agents)) * 100
    print(f"\nCode Examples:")
    print(f"    {agents_with_examples}/{len(all_agents)} agents ({percentage:.0f}%)")

    # Process steps distribution
    print(f"\nProcess Steps Distribution:")
    step_counts = [(agent.name, len(agent.extract_process_steps())) for agent in all_agents]
    step_counts.sort(key=lambda x: x[1], reverse=True)

    print(f"  Top 5:")
    for name, count in step_counts[:5]:
        print(f"    {name}: {count} steps")

    print(f"  Bottom 5:")
    for name, count in step_counts[-5:]:
        print(f"    {name}: {count} steps")

    # Quality check distribution
    print(f"\nQuality Checks Distribution:")
    qc_counts = [
        (agent.name, len(agent.get_section_checkboxes("Quality Checks"))) for agent in all_agents
    ]
    qc_counts.sort(key=lambda x: x[1], reverse=True)

    avg_qc = sum(c for _, c in qc_counts) / len(qc_counts)
    print(f"  Average: {avg_qc:.1f} checks per agent")
    print(f"  Range: {qc_counts[-1][1]} - {qc_counts[0][1]} checks")

    print(f"{'='*70}\n")

    # All required sections should be 100%
    all_complete = all(
        all(agent.has_section(sec) for sec in REQUIRED_SECTIONS)
        and any(agent.has_section(var) for var in ANTIPATTERN_VARIATIONS)
        for agent in all_agents
    )

    assert all_complete, "Not all agents have complete required sections"
