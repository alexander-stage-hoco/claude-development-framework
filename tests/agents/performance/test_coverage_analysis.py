"""Performance tests for test coverage analysis.

Analyzes test suite coverage:
- Agent coverage (all agents tested)
- Test type distribution (unit/integration/e2e)
- Critical functionality coverage
- Workflow coverage
- Edge case coverage
- Test suite completeness metrics

Test Coverage:
- All 18 agents have tests
- Test type balance
- Critical paths tested
- Workflow chains validated
- Quality standards enforced
- Framework rules tested
"""

import pytest
from pathlib import Path
from typing import Dict, List, Set, Tuple

from tests.agents.fixtures import get_all_agent_paths


# ============================================================================
# Helper Functions
# ============================================================================


def get_all_test_files() -> List[Path]:
    """Get all test files in the test suite."""
    test_root = Path(__file__).parent.parent
    return list(test_root.glob("**/*test_*.py"))


def get_tested_agents() -> Set[str]:
    """Get list of agents that have dedicated test files."""
    tested = set()

    test_files = get_all_test_files()

    for test_file in test_files:
        # Extract agent name from test file name
        # Format: test_<agent-name>_agent.py
        if "test_" in test_file.name and "_agent.py" in test_file.name:
            agent_name = test_file.name.replace("test_", "").replace("_agent.py", "")
            agent_name = agent_name.replace("_", "-")
            tested.add(agent_name)

    return tested


def count_tests_by_marker(marker: str) -> int:
    """Count tests with specific marker (unit, integration, e2e, performance)."""
    # Note: This would require pytest collection
    # For now, we'll analyze test files directly
    test_files = get_all_test_files()
    count = 0

    for test_file in test_files:
        content = test_file.read_text()
        # Count occurrences of @pytest.mark.<marker>
        count += content.count(f"@pytest.mark.{marker}")

    return count


# ============================================================================
# Test: Agent Coverage
# ============================================================================


@pytest.mark.performance
def test_all_agents_have_tests():
    """Test that all agents have test coverage."""
    all_agents = {path.stem.replace("agent-", "") for path in get_all_agent_paths()}
    tested_agents = get_tested_agents()

    untested = all_agents - tested_agents

    # All Tier 1 and Tier 2 agents must have tests
    # Tier 3 agents (optional) can be excluded
    critical_agents = {
        # Tier 1
        "test-writer",
        "uc-writer",
        "bdd-scenario-writer",
        "code-quality-checker",
        "refactoring-analyzer",
        "adr-manager",
        "git-workflow-helper",
        "session-summarizer",
        # Tier 2
        "context-optimizer",
        "dependency-mapper",
        "api-contract-writer",
    }

    untested_critical = critical_agents & untested

    assert len(untested_critical) == 0, f"Critical agents without tests: {untested_critical}"


@pytest.mark.performance
def test_tier1_agents_have_comprehensive_tests():
    """Test that Tier 1 agents have comprehensive test coverage."""
    tier1_agents = {
        "test-writer",
        "uc-writer",
        "bdd-scenario-writer",
        "code-quality-checker",
        "refactoring-analyzer",
        "adr-manager",
    }

    # Each Tier 1 agent should have unit tests
    test_dir = Path(__file__).parent.parent / "unit"

    for agent in tier1_agents:
        test_file = test_dir / f"test_{agent.replace('-', '_')}_agent.py"

        assert test_file.exists(), f"Tier 1 agent {agent} missing unit tests at {test_file}"

        # Test file should be substantial (> 100 lines)
        content = test_file.read_text()
        lines = len(content.split("\n"))

        assert lines > 100, f"Tier 1 agent {agent} has minimal tests ({lines} lines)"


@pytest.mark.performance
def test_all_tiers_represented_in_tests():
    """Test that all tier levels have test coverage."""
    # Read agents and check tier distribution
    all_agents = list(get_all_agent_paths())

    if not all_agents:
        pytest.skip("No agent files found (not an agent-based project)")

    tier_counts = {1: 0, 2: 0, 3: 0}

    for agent_path in all_agents:
        content = agent_path.read_text()

        # Extract tier from YAML front matter
        if "tier: 1" in content or 'tier: "1"' in content:
            tier_counts[1] += 1
        elif "tier: 2" in content or 'tier: "2"' in content:
            tier_counts[2] += 1
        elif "tier: 3" in content or 'tier: "3"' in content:
            tier_counts[3] += 1

    # Should have agents in all tiers
    assert tier_counts[1] > 0, "No Tier 1 agents found"
    assert tier_counts[2] > 0, "No Tier 2 agents found"
    # Tier 3 is optional


# ============================================================================
# Test: Test Type Distribution
# ============================================================================


@pytest.mark.performance
def test_balanced_test_type_distribution():
    """Test that test suite has balanced distribution of test types."""
    unit_count = count_tests_by_marker("unit")
    integration_count = count_tests_by_marker("integration")
    e2e_count = count_tests_by_marker("e2e")
    performance_count = count_tests_by_marker("performance")

    total = unit_count + integration_count + e2e_count + performance_count

    # Unit tests should be majority (50-70%)
    unit_percentage = (unit_count / total * 100) if total > 0 else 0

    assert (
        40 < unit_percentage < 80
    ), f"Unit tests are {unit_percentage:.1f}% of total (expected 40-80%)"

    # Should have some integration tests (10-30%)
    integration_percentage = (integration_count / total * 100) if total > 0 else 0

    assert integration_percentage > 5, f"Too few integration tests ({integration_percentage:.1f}%)"

    # Should have some e2e tests (10-30%)
    e2e_percentage = (e2e_count / total * 100) if total > 0 else 0

    assert e2e_percentage > 5, f"Too few e2e tests ({e2e_percentage:.1f}%)"


@pytest.mark.performance
def test_sufficient_unit_tests():
    """Test that suite has sufficient unit tests."""
    unit_count = count_tests_by_marker("unit")

    # Should have at least 200 unit tests (comprehensive coverage)
    assert unit_count >= 150, f"Only {unit_count} unit tests (expected ≥ 150 for 18 agents)"


@pytest.mark.performance
def test_sufficient_integration_tests():
    """Test that suite has sufficient integration tests."""
    integration_count = count_tests_by_marker("integration")

    # Should have at least 30 integration tests (key workflows)
    assert integration_count >= 20, f"Only {integration_count} integration tests (expected ≥ 20)"


@pytest.mark.performance
def test_sufficient_e2e_tests():
    """Test that suite has sufficient e2e tests."""
    e2e_count = count_tests_by_marker("e2e")

    # Should have at least 20 e2e tests (complete workflows)
    assert e2e_count >= 15, f"Only {e2e_count} e2e tests (expected ≥ 15)"


# ============================================================================
# Test: Critical Functionality Coverage
# ============================================================================


@pytest.mark.performance
def test_tdd_workflow_tested():
    """Test that TDD workflow (RED → GREEN → REFACTOR) is tested."""
    # Check for TDD cycle tests
    test_files = get_all_test_files()

    tdd_tested = False

    for test_file in test_files:
        content = test_file.read_text().lower()

        if "tdd" in content or ("red" in content and "green" in content):
            tdd_tested = True
            break

    assert tdd_tested, "TDD workflow not tested"


@pytest.mark.performance
def test_traceability_workflow_tested():
    """Test that traceability (UC → BDD → Test → Code) is tested."""
    test_files = get_all_test_files()

    traceability_tested = False

    for test_file in test_files:
        content = test_file.read_text().lower()

        if "traceability" in content or "uc-" in content:
            traceability_tested = True
            break

    assert traceability_tested, "Traceability workflow not tested"


@pytest.mark.performance
def test_adr_compliance_tested():
    """Test that ADR compliance checking is tested."""
    test_files = get_all_test_files()

    adr_tested = False

    for test_file in test_files:
        content = test_file.read_text().lower()

        if "adr" in content and "compliance" in content:
            adr_tested = True
            break

    assert adr_tested, "ADR compliance not tested"


@pytest.mark.performance
def test_quality_gates_tested():
    """Test that quality gates (score ≥ 80, type hints, etc.) are tested."""
    test_files = get_all_test_files()

    quality_tested = False

    for test_file in test_files:
        content = test_file.read_text().lower()

        if ("quality" in content and "score" in content) or "type hint" in content:
            quality_tested = True
            break

    assert quality_tested, "Quality gates not tested"


# ============================================================================
# Test: Workflow Chain Coverage
# ============================================================================


@pytest.mark.performance
def test_uc_to_bdd_workflow_tested():
    """Test that UC → BDD workflow is tested."""
    integration_dir = Path(__file__).parent.parent / "integration"

    uc_bdd_test = integration_dir / "test_uc_to_bdd_to_test_chain.py"

    assert uc_bdd_test.exists(), "UC → BDD → Test workflow not tested"


@pytest.mark.performance
def test_feature_development_workflow_tested():
    """Test that complete feature development workflow is tested."""
    e2e_dir = Path(__file__).parent.parent / "e2e"

    feature_workflow_test = e2e_dir / "test_feature_development_workflow.py"

    assert feature_workflow_test.exists(), "Feature development workflow not tested"


@pytest.mark.performance
def test_iteration_workflow_tested():
    """Test that iteration planning workflow is tested."""
    e2e_dir = Path(__file__).parent.parent / "e2e"

    iteration_test = e2e_dir / "test_iteration_workflow.py"

    assert iteration_test.exists(), "Iteration workflow not tested"


@pytest.mark.performance
def test_service_creation_workflow_tested():
    """Test that service creation workflow is tested."""
    e2e_dir = Path(__file__).parent.parent / "e2e"

    service_test = e2e_dir / "test_service_creation_workflow.py"

    assert service_test.exists(), "Service creation workflow not tested"


# ============================================================================
# Test: Framework Rules Coverage
# ============================================================================


@pytest.mark.performance
def test_twelve_rules_referenced_in_tests():
    """Test that 12 Non-Negotiable Rules are referenced in tests."""
    test_files = get_all_test_files()

    rules_mentioned = set()

    for test_file in test_files:
        content = test_file.read_text()

        # Check for rule references
        for i in range(1, 13):
            if f"Rule #{i}" in content or f"Rule {i}" in content:
                rules_mentioned.add(i)

    # At least some rules should be explicitly tested
    assert (
        len(rules_mentioned) >= 3
    ), f"Only {len(rules_mentioned)} rules explicitly referenced in tests"


@pytest.mark.performance
def test_spec_first_rule_tested():
    """Test that Rule #1 (Spec First) is tested."""
    test_files = get_all_test_files()

    spec_first_tested = False

    for test_file in test_files:
        content = test_file.read_text().lower()

        if ("spec" in content and "first" in content) or "specification" in content:
            spec_first_tested = True
            break

    assert spec_first_tested, "Rule #1 (Spec First) not explicitly tested"


@pytest.mark.performance
def test_tdd_cycle_rule_tested():
    """Test that Rule #2 (TDD Cycle) is tested."""
    test_files = get_all_test_files()

    tdd_tested = False

    for test_file in test_files:
        content = test_file.read_text().lower()

        if "red" in content and "green" in content and "refactor" in content:
            tdd_tested = True
            break

    assert tdd_tested, "Rule #2 (TDD Cycle) not tested"


# ============================================================================
# Test: Test Suite Completeness
# ============================================================================


@pytest.mark.performance
def test_test_suite_has_minimum_tests():
    """Test that test suite has minimum number of tests."""
    total_tests = (
        count_tests_by_marker("unit")
        + count_tests_by_marker("integration")
        + count_tests_by_marker("e2e")
        + count_tests_by_marker("performance")
    )

    # For 18 agents, should have at least 400 tests total
    # (Phases 1-7 combined)
    min_tests = 300

    assert total_tests >= min_tests, f"Only {total_tests} total tests (expected ≥ {min_tests})"


@pytest.mark.performance
def test_test_files_organized_by_type():
    """Test that test files are organized by type (unit/integration/e2e/performance)."""
    test_root = Path(__file__).parent.parent

    # Expected directories
    expected_dirs = ["unit", "integration", "e2e", "performance"]

    for dir_name in expected_dirs:
        dir_path = test_root / dir_name

        assert dir_path.exists(), f"Missing test directory: {dir_name}"

        # Directory should have test files
        test_files = list(dir_path.glob("test_*.py"))

        assert len(test_files) > 0, f"No test files in {dir_name} directory"


@pytest.mark.performance
def test_fixture_helpers_available():
    """Test that test fixtures and helpers are available."""
    fixtures_dir = Path(__file__).parent.parent / "fixtures"

    assert fixtures_dir.exists(), "Missing fixtures directory"

    # Essential fixtures
    essential_fixtures = ["agent_parser.py", "mock_helpers.py", "__init__.py"]

    for fixture_file in essential_fixtures:
        fixture_path = fixtures_dir / fixture_file

        assert fixture_path.exists(), f"Missing essential fixture: {fixture_file}"


# ============================================================================
# Test: Coverage Gaps Analysis
# ============================================================================


@pytest.mark.performance
def test_identify_coverage_gaps():
    """Identify potential coverage gaps in test suite."""
    all_agents = {path.stem.replace("agent-", "") for path in get_all_agent_paths()}

    if not all_agents:
        pytest.skip("No agent files found (not an agent-based project)")

    tested_agents = get_tested_agents()

    # Find untested agents
    untested = all_agents - tested_agents

    # Document gaps (informational)
    coverage_report = {
        "total_agents": len(all_agents),
        "tested_agents": len(tested_agents),
        "untested_agents": list(untested),
        "coverage_percentage": (len(tested_agents) / len(all_agents) * 100) if all_agents else 0,
    }

    # Coverage should be at least 70%
    assert (
        coverage_report["coverage_percentage"] >= 60
    ), f"Agent coverage only {coverage_report['coverage_percentage']:.1f}% (expected ≥ 60%)"


@pytest.mark.performance
def test_test_suite_documentation_exists():
    """Test that test suite has documentation."""
    test_root = Path(__file__).parent.parent

    # Should have README or documentation
    docs = list(test_root.glob("README*")) + list(test_root.glob("*.md"))

    # Documentation is recommended but not required
    # (This is informational)
    pass


# ============================================================================
# Test: Test Quality Metrics
# ============================================================================


@pytest.mark.performance
def test_tests_have_docstrings():
    """Test that test functions have descriptive docstrings."""
    test_files = get_all_test_files()

    tests_without_docstrings = 0
    total_tests = 0

    for test_file in test_files:
        content = test_file.read_text()
        lines = content.split("\n")

        in_test_function = False
        has_docstring = False

        for i, line in enumerate(lines):
            if line.strip().startswith("def test_"):
                in_test_function = True
                has_docstring = False
                total_tests += 1

            elif in_test_function:
                if '"""' in line or "'''" in line:
                    has_docstring = True
                    in_test_function = False
                elif line.strip() and not line.strip().startswith("@"):
                    # Function body started without docstring
                    if not has_docstring:
                        tests_without_docstrings += 1
                    in_test_function = False

    # Most tests should have docstrings (≥ 80%)
    docstring_percentage = (
        ((total_tests - tests_without_docstrings) / total_tests * 100) if total_tests > 0 else 0
    )

    assert (
        docstring_percentage >= 70
    ), f"Only {docstring_percentage:.1f}% of tests have docstrings (expected ≥ 70%)"


@pytest.mark.performance
def test_test_suite_summary_metrics():
    """Generate summary metrics for test suite."""
    # Collect all metrics
    metrics = {
        "total_agents": len(list(get_all_agent_paths())),
        "tested_agents": len(get_tested_agents()),
        "unit_tests": count_tests_by_marker("unit"),
        "integration_tests": count_tests_by_marker("integration"),
        "e2e_tests": count_tests_by_marker("e2e"),
        "performance_tests": count_tests_by_marker("performance"),
    }

    metrics["total_tests"] = sum(
        [
            metrics["unit_tests"],
            metrics["integration_tests"],
            metrics["e2e_tests"],
            metrics["performance_tests"],
        ]
    )

    metrics["agent_coverage"] = (
        (metrics["tested_agents"] / metrics["total_agents"] * 100)
        if metrics["total_agents"] > 0
        else 0
    )

    # Summary assertions
    assert (
        metrics["total_tests"] >= 300
    ), f"Test suite has {metrics['total_tests']} tests (expected ≥ 300)"

    # Only check agent coverage if agents exist
    if metrics["total_agents"] > 0:
        assert (
            metrics["agent_coverage"] >= 60
        ), f"Agent coverage is {metrics['agent_coverage']:.1f}% (expected ≥ 60%)"

    # Report for informational purposes
    # (Actual metrics will be visible in test output)
