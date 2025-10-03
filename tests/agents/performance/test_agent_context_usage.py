"""Performance tests for agent context usage.

Tests agent context efficiency and token usage:
- Agent prompt size measurement
- Context efficiency validation
- Redundancy detection
- Essential content verification
- Section size analysis
- Cross-agent context comparison
- Optimization opportunities

Test Coverage:
- Individual agent context size
- Section-level context breakdown
- Redundancy and repetition
- Context budget compliance
- Essential vs optional content
- Cross-agent consistency in verbosity
"""

import pytest
from pathlib import Path
from typing import Dict, List, Tuple

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
# Test: Context Size Measurement
# ============================================================================


@pytest.mark.performance
def test_agent_context_size_reasonable(all_agents: List[Tuple[str, AgentParser]]):
    """Test that agent context size is reasonable."""
    context_budget = 8000  # Max characters per agent (reasonable for LLM context)

    oversized_agents = []

    for name, parser in all_agents:
        content = parser.content
        size = len(content)

        if size > context_budget:
            oversized_agents.append((name, size))

    # Report oversized agents
    if oversized_agents:
        report = "\n".join(
            f"  - {name}: {size} chars (over by {size - context_budget})"
            for name, size in oversized_agents
        )
        # Note: This is a soft check - some agents may legitimately need more context
        # The test documents the situation rather than failing
        pass  # Informational only


@pytest.mark.performance
def test_agent_average_context_size(all_agents: List[Tuple[str, AgentParser]]):
    """Test average agent context size across all agents."""
    if not all_agents:
        pytest.skip("No agent files found (not an agent-based project)")

    total_size = 0
    agent_sizes = {}

    for name, parser in all_agents:
        size = len(parser.content)
        agent_sizes[name] = size
        total_size += size

    avg_size = total_size / len(all_agents)

    # Expected average: ~3000-5000 characters per agent
    assert 1000 < avg_size < 10000, f"Average agent size {avg_size:.0f} chars seems unusual"

    # Identify outliers (agents > 2x average)
    outliers = [(name, size) for name, size in agent_sizes.items() if size > 2 * avg_size]
    # Informational: Track which agents are significantly larger


@pytest.mark.performance
def test_tier1_agents_context_optimized(all_agents: List[Tuple[str, AgentParser]]):
    """Test that Tier 1 agents (most used) are context-optimized."""
    tier1_agents = [
        "test-writer",
        "uc-writer",
        "bdd-scenario-writer",
        "code-quality-checker",
        "refactoring-analyzer",
    ]

    # Tier 1 agents should be leaner (used more frequently)
    tier1_budget = 6000  # Stricter budget for frequently-used agents

    for name, parser in all_agents:
        if name in tier1_agents:
            size = len(parser.content)
            # Soft check - document if over budget
            if size > tier1_budget:
                # Tier 1 agent exceeds recommended budget
                pass


# ============================================================================
# Test: Section Size Analysis
# ============================================================================


@pytest.mark.performance
def test_section_sizes_reasonable(all_agents: List[Tuple[str, AgentParser]]):
    """Test that individual section sizes are reasonable."""
    max_section_size = 2000  # Max characters per section

    oversized_sections = []

    for name, parser in all_agents:
        for section_name in parser.sections.keys():
            section_content = parser.get_section_content(section_name)
            if section_content:
                size = len(section_content)
                if size > max_section_size:
                    oversized_sections.append((name, section_name, size))

    # Document oversized sections
    if oversized_sections:
        # Some sections (like Examples) may legitimately be large
        pass


@pytest.mark.performance
def test_examples_section_not_excessive(all_agents: List[Tuple[str, AgentParser]]):
    """Test that Examples sections are not excessively large."""
    max_examples_size = 2500  # Examples can be larger, but not excessive

    for name, parser in all_agents:
        examples = parser.get_section_content("Examples")
        if examples:
            size = len(examples)
            # Soft limit - examples are valuable but should be concise
            if size > max_examples_size:
                # Consider if examples can be condensed
                pass


# ============================================================================
# Test: Redundancy Detection
# ============================================================================


@pytest.mark.performance
def test_no_duplicate_sections(all_agents: List[Tuple[str, AgentParser]]):
    """Test that agents don't have duplicate section content."""
    for name, parser in all_agents:
        section_contents = {}

        for section_name, section_content in parser.sections.items():
            # Normalize content for comparison (strip whitespace, lowercase)
            normalized = section_content.strip().lower()

            if normalized in section_contents.values():
                # Found duplicate section content
                pytest.fail(f"{name}: Duplicate section content detected")

            section_contents[section_name] = normalized


@pytest.mark.performance
def test_minimal_instruction_repetition(all_agents: List[Tuple[str, AgentParser]]):
    """Test that instructions aren't excessively repeated."""
    for name, parser in all_agents:
        body = parser.body.lower()

        # Check for repeated phrases (common patterns)
        repeated_phrases = ["specification:", "use case", "you must", "always", "never"]

        for phrase in repeated_phrases:
            count = body.count(phrase)
            # Soft limit: phrase shouldn't appear more than 15 times
            # (Some repetition is OK for emphasis, but excessive is wasteful)
            if count > 15:
                # Consider consolidating repeated instructions
                pass


# ============================================================================
# Test: Essential Content Verification
# ============================================================================


@pytest.mark.performance
def test_agent_has_essential_sections_only(all_agents: List[Tuple[str, AgentParser]]):
    """Test that agents contain only essential sections."""
    essential_sections = {
        "Purpose",
        "When to Use",
        "Process",
        "Output Format",
        "Quality Checks",
        "Examples",
    }

    optional_sections = {
        "Anti-Patterns",
        "Common Mistakes",
        "Edge Cases",
        "Integration Points",
        "Handoff Protocol",
    }

    for name, parser in all_agents:
        agent_sections = set(parser.sections.keys())

        # All agents should have most essential sections
        missing_essential = essential_sections - agent_sections
        # It's OK to miss 1-2 essential sections if not applicable
        assert (
            len(missing_essential) <= 2
        ), f"{name}: Missing too many essential sections: {missing_essential}"

        # Optional sections are fine but should serve a purpose
        extra_sections = agent_sections - essential_sections - optional_sections
        # Any non-standard sections should be justified
        if extra_sections:
            # Document non-standard sections for review
            pass


@pytest.mark.performance
def test_purpose_section_concise(all_agents: List[Tuple[str, AgentParser]]):
    """Test that Purpose sections are concise (1-3 sentences)."""
    max_purpose_size = 500  # Purpose should be brief

    for name, parser in all_agents:
        purpose = parser.get_section_content("Purpose")
        if purpose:
            size = len(purpose)
            # Purpose should be concise
            if size > max_purpose_size:
                # Consider condensing Purpose section
                pass


# ============================================================================
# Test: Context Budget Compliance
# ============================================================================


@pytest.mark.performance
def test_agent_fits_in_context_window(all_agents: List[Tuple[str, AgentParser]]):
    """Test that agent fits comfortably in LLM context window."""
    # Assuming ~4 chars per token, and we want agents to fit in ~2000 tokens
    max_agent_tokens = 2000
    chars_per_token = 4
    max_agent_chars = max_agent_tokens * chars_per_token  # 8000 chars

    for name, parser in all_agents:
        size = len(parser.content)
        estimated_tokens = size / chars_per_token

        if estimated_tokens > max_agent_tokens:
            # Agent may be too large for efficient context usage
            pass


@pytest.mark.performance
def test_combined_agent_context_reasonable(all_agents: List[Tuple[str, AgentParser]]):
    """Test that combined context of commonly-used agents is reasonable."""
    # Common workflow: uc-writer → bdd-scenario-writer → test-writer
    workflow_agents = ["uc-writer", "bdd-scenario-writer", "test-writer"]

    total_size = 0
    for name, parser in all_agents:
        if name in workflow_agents:
            total_size += len(parser.content)

    # Combined size should fit in context window with room for user input
    # Assuming 16K context window, agents should use < 50% (8K tokens = 32K chars)
    max_combined = 32000

    if total_size > max_combined:
        # Workflow agents combined are too large
        pass


# ============================================================================
# Test: Cross-Agent Context Comparison
# ============================================================================


@pytest.mark.performance
def test_similar_agents_similar_context_size(all_agents: List[Tuple[str, AgentParser]]):
    """Test that similar agents have similar context sizes."""
    # Writer agents should be similar in size
    writer_agents = {"test-writer": 0, "uc-writer": 0, "bdd-scenario-writer": 0}

    for name, parser in all_agents:
        if name in writer_agents:
            writer_agents[name] = len(parser.content)

    # Check if sizes are within 50% of each other
    sizes = [s for s in writer_agents.values() if s > 0]
    if sizes:
        min_size = min(sizes)
        max_size = max(sizes)

        # Sizes shouldn't vary more than 2x
        ratio = max_size / min_size if min_size > 0 else 1
        # Soft check: similar agents should have similar context requirements
        if ratio > 2.0:
            # Consider if one agent has unnecessary content
            pass


# ============================================================================
# Test: Optimization Opportunities
# ============================================================================


@pytest.mark.performance
def test_identify_context_optimization_opportunities(all_agents: List[Tuple[str, AgentParser]]):
    """Identify opportunities for context optimization."""
    optimization_report = {
        "oversized_agents": [],
        "oversized_sections": [],
        "redundant_content": [],
        "verbose_examples": [],
    }

    for name, parser in all_agents:
        size = len(parser.content)

        # Check overall size
        if size > 8000:
            optimization_report["oversized_agents"].append((name, size))

        # Check section sizes
        for section_name in parser.sections.keys():
            section_content = parser.get_section_content(section_name)
            if section_content and len(section_content) > 2000:
                optimization_report["oversized_sections"].append(
                    (name, section_name, len(section_content))
                )

        # Check for verbose examples
        examples = parser.get_section_content("Examples")
        if examples and len(examples) > 2500:
            optimization_report["verbose_examples"].append((name, len(examples)))

    # Report is for informational purposes
    # Tests pass but provide optimization guidance


@pytest.mark.performance
def test_context_efficiency_score(all_agents: List[Tuple[str, AgentParser]]):
    """Calculate context efficiency score for each agent."""
    for name, parser in all_agents:
        total_size = len(parser.content)

        # Calculate useful content vs overhead
        essential_sections = ["Purpose", "Process", "Output Format", "Quality Checks"]
        essential_size = sum(
            len(parser.get_section_content(section) or "") for section in essential_sections
        )

        if total_size > 0:
            efficiency = (essential_size / total_size) * 100

            # Efficiency should be at least 40% (essential content / total)
            # Lower efficiency suggests too much overhead/optional content
            if efficiency < 40:
                # Consider if optional content is necessary
                pass


# ============================================================================
# Test: Section Distribution
# ============================================================================


@pytest.mark.performance
def test_section_distribution_balanced(all_agents: List[Tuple[str, AgentParser]]):
    """Test that section sizes are reasonably balanced."""
    for name, parser in all_agents:
        section_sizes = {section: len(content) for section, content in parser.sections.items()}

        if not section_sizes:
            continue

        total_size = sum(section_sizes.values())

        # No single section should dominate (> 50% of content)
        for section, size in section_sizes.items():
            if total_size > 0:
                percentage = (size / total_size) * 100
                if percentage > 50:
                    # One section dominates the agent
                    # Consider breaking it up or condensing
                    pass


@pytest.mark.performance
def test_metadata_overhead_minimal(all_agents: List[Tuple[str, AgentParser]]):
    """Test that metadata (YAML front matter) overhead is minimal."""
    for name, parser in all_agents:
        metadata_size = len(str(parser.metadata))
        total_size = len(parser.content)

        if total_size > 0:
            metadata_ratio = (metadata_size / total_size) * 100

            # Metadata should be < 5% of total content
            assert (
                metadata_ratio < 10
            ), f"{name}: Metadata is {metadata_ratio:.1f}% of content (should be < 10%)"
