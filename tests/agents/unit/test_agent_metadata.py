"""Tests for agent metadata validation.

Tests that all agents have valid YAML front matter with required fields.

Test Coverage:
- YAML syntax validation
- Required field presence
- Field value validation
- Name consistency
"""

import pytest
from pathlib import Path
from typing import List

from tests.agents.fixtures import AgentParser


# ============================================================================
# Constants
# ============================================================================

REQUIRED_METADATA_FIELDS = ["name", "description", "tools", "model"]

VALID_CLAUDE_TOOLS = [
    "Read", "Write", "Edit", "Bash", "Glob", "Grep",
    "WebSearch", "WebFetch", "Task", "TodoWrite"
]

VALID_MODELS = ["opus", "sonnet", "sonnet-3-5", "claude-3-5-sonnet-20241022"]


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def all_agents(agents_dir: Path) -> List[AgentParser]:
    """Load all agent parsers."""
    return [AgentParser(f) for f in agents_dir.glob("*.md")]


@pytest.fixture(params=[f for f in (Path(__file__).parent.parent.parent.parent / ".claude" / "subagents").glob("*.md")])
def agent_parser(request) -> AgentParser:
    """Parametrized fixture providing individual agent parsers."""
    return AgentParser(request.param)


# ============================================================================
# Test: YAML Front Matter Presence
# ============================================================================

def test_all_agents_have_yaml_frontmatter(all_agents: List[AgentParser]):
    """Test that all agents have YAML front matter."""
    agents_without_frontmatter = [
        agent.name for agent in all_agents if not agent.has_frontmatter
    ]

    assert not agents_without_frontmatter, (
        f"Agents missing YAML front matter: {', '.join(agents_without_frontmatter)}"
    )


@pytest.mark.unit
def test_agent_has_valid_yaml_frontmatter(agent_parser: AgentParser):
    """Test that agent has valid YAML front matter."""
    assert agent_parser.has_frontmatter, (
        f"Agent {agent_parser.name} is missing YAML front matter"
    )

    assert isinstance(agent_parser.metadata, dict), (
        f"Agent {agent_parser.name} has invalid YAML (not a dict)"
    )


# ============================================================================
# Test: Required Fields
# ============================================================================

@pytest.mark.unit
def test_agent_has_required_metadata_fields(agent_parser: AgentParser):
    """Test that agent has all required metadata fields."""
    missing_fields = [
        field for field in REQUIRED_METADATA_FIELDS
        if field not in agent_parser.metadata
    ]

    assert not missing_fields, (
        f"Agent {agent_parser.name} missing required fields: {', '.join(missing_fields)}"
    )


def test_all_agents_have_complete_metadata(all_agents: List[AgentParser]):
    """Test that all agents have complete metadata."""
    incomplete_agents = []

    for agent in all_agents:
        missing = [
            field for field in REQUIRED_METADATA_FIELDS
            if field not in agent.metadata
        ]
        if missing:
            incomplete_agents.append(f"{agent.name} (missing: {', '.join(missing)})")

    assert not incomplete_agents, (
        f"Agents with incomplete metadata:\n" + "\n".join(f"  - {a}" for a in incomplete_agents)
    )


# ============================================================================
# Test: Field Values
# ============================================================================

@pytest.mark.unit
def test_agent_name_matches_filename(agent_parser: AgentParser):
    """Test that agent name in metadata matches filename."""
    metadata_name = agent_parser.get_metadata_field("name")

    assert metadata_name == agent_parser.name, (
        f"Agent {agent_parser.name}: metadata name '{metadata_name}' doesn't match filename"
    )


@pytest.mark.unit
def test_agent_description_is_comprehensive(agent_parser: AgentParser):
    """Test that agent description is sufficiently detailed."""
    description = agent_parser.get_metadata_field("description")

    assert isinstance(description, str), (
        f"Agent {agent_parser.name}: description must be a string"
    )

    assert len(description) >= 50, (
        f"Agent {agent_parser.name}: description too short ({len(description)} chars, need ≥50)"
    )

    # Check that description mentions key aspects
    lower_desc = description.lower()
    assert any(keyword in lower_desc for keyword in ["agent", "specialist", "expert", "helper"]), (
        f"Agent {agent_parser.name}: description should identify agent role"
    )


@pytest.mark.unit
def test_agent_tools_are_valid(agent_parser: AgentParser):
    """Test that agent tools list contains only valid Claude Code tools."""
    tools = agent_parser.get_metadata_field("tools")

    assert isinstance(tools, list), (
        f"Agent {agent_parser.name}: tools must be a list"
    )

    assert len(tools) > 0, (
        f"Agent {agent_parser.name}: tools list cannot be empty"
    )

    invalid_tools = [tool for tool in tools if tool not in VALID_CLAUDE_TOOLS]

    assert not invalid_tools, (
        f"Agent {agent_parser.name}: invalid tools: {', '.join(invalid_tools)}\n"
        f"Valid tools: {', '.join(VALID_CLAUDE_TOOLS)}"
    )


@pytest.mark.unit
def test_agent_model_is_supported(agent_parser: AgentParser):
    """Test that agent specifies a supported Claude model."""
    model = agent_parser.get_metadata_field("model")

    assert isinstance(model, str), (
        f"Agent {agent_parser.name}: model must be a string"
    )

    assert model in VALID_MODELS, (
        f"Agent {agent_parser.name}: invalid model '{model}'\n"
        f"Valid models: {', '.join(VALID_MODELS)}"
    )


# ============================================================================
# Test: Metadata Statistics
# ============================================================================

def test_metadata_coverage_report(all_agents: List[AgentParser]):
    """Generate a report of metadata coverage across all agents."""
    total_agents = len(all_agents)

    # Count agents with each field
    field_coverage = {}
    for field in REQUIRED_METADATA_FIELDS:
        count = sum(1 for agent in all_agents if field in agent.metadata)
        field_coverage[field] = count

    # Report
    print(f"\n{'='*60}")
    print(f"Metadata Coverage Report ({total_agents} agents)")
    print(f"{'='*60}")

    for field, count in field_coverage.items():
        percentage = (count / total_agents) * 100
        status = "✓" if count == total_agents else "✗"
        print(f"  {status} {field}: {count}/{total_agents} ({percentage:.0f}%)")

    # Count unique tools used
    all_tools = set()
    for agent in all_agents:
        tools = agent.get_metadata_field("tools") or []
        all_tools.update(tools)

    print(f"\nTools used across agents: {len(all_tools)}")
    print(f"  {', '.join(sorted(all_tools))}")

    # Count models used
    models_used = {}
    for agent in all_agents:
        model = agent.get_metadata_field("model")
        models_used[model] = models_used.get(model, 0) + 1

    print(f"\nModels distribution:")
    for model, count in sorted(models_used.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_agents) * 100
        print(f"  {model}: {count} agents ({percentage:.0f}%)")

    print(f"{'='*60}\n")

    # All fields should be 100% coverage
    assert all(count == total_agents for count in field_coverage.values()), (
        "Not all agents have complete metadata"
    )


# ============================================================================
# Test: Metadata Quality
# ============================================================================

def test_agents_have_unique_names(all_agents: List[AgentParser]):
    """Test that all agent names are unique."""
    names = [agent.name for agent in all_agents]
    duplicates = [name for name in names if names.count(name) > 1]

    assert not duplicates, (
        f"Duplicate agent names found: {', '.join(set(duplicates))}"
    )


def test_agents_have_distinct_descriptions(all_agents: List[AgentParser]):
    """Test that agent descriptions are distinct (not copy-pasted)."""
    descriptions = [agent.get_metadata_field("description") for agent in all_agents]

    # Check for exact duplicates
    unique_descriptions = set(descriptions)
    duplicates = [desc for desc in descriptions if descriptions.count(desc) > 1]

    assert len(unique_descriptions) == len(descriptions), (
        f"Found {len(descriptions) - len(unique_descriptions)} duplicate descriptions"
    )


@pytest.mark.unit
def test_agent_description_mentions_framework_rules(agent_parser: AgentParser):
    """Test that agent description mentions framework integration when appropriate."""
    description = agent_parser.get_metadata_field("description")
    name = agent_parser.name

    # Agents that should mention rules or framework concepts
    rule_related_agents = [
        "test-writer", "uc-writer", "bdd-scenario-writer",
        "spec-validator", "code-quality-checker", "refactoring-analyzer",
        "adr-manager", "git-workflow-helper"
    ]

    if name in rule_related_agents:
        lower_desc = description.lower()
        mentions_framework = any(
            keyword in lower_desc
            for keyword in ["rule", "framework", "spec", "test", "quality", "discipline"]
        )

        assert mentions_framework, (
            f"Agent {name} should mention framework concepts in description"
        )
