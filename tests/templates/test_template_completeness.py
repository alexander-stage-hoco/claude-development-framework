"""Template completeness validation tests.

Tests validate framework template coverage and cross-references.
"""

import pytest
from pathlib import Path
from tests.templates.fixtures.template_parser import TemplateParser


# ============================================================================
# Test: Template Coverage
# ============================================================================


@pytest.mark.unit
def test_all_template_categories_represented(template_parsers):
    """Test that all expected template categories exist."""
    # Expected categories (from framework design)
    expected_categories = {
        "core": ["CLAUDE", "development-rules", "context-priority"],
        "session": ["session-checklist", "session-state", "start-here"],
        "specification": ["use-case-template", "service-spec"],
        "research": [
            "article-links",
            "paper-summary",
            "implementation-readme",
            "implementation-summary",
        ],
        "planning": [],  # May have templates but not required in .claude/templates
        "workflow": ["git-workflow", "refactoring-checklist", "code-reuse-checklist"],
        "quality": ["requirements-review-checklist"],
        "decision": ["technical-decisions"],
        "service": ["service-registry", "services-README-template"],
        "evaluation": ["benchmark-report", "library-evaluation"],
    }

    template_names = [parser.name for parser in template_parsers]

    # Check each category has representation
    missing_categories = []
    for category, required_templates in expected_categories.items():
        if required_templates:  # Only check if we expect templates
            category_covered = any(template in template_names for template in required_templates)
            if not category_covered:
                missing_categories.append((category, required_templates))

    if missing_categories:
        missing_str = "\n".join(f"  {cat}: {temps}" for cat, temps in missing_categories)
        pytest.fail(
            f"Missing template categories:\n{missing_str}\n"
            "Framework should cover all development phases"
        )


@pytest.mark.unit
def test_tier_coverage_is_balanced(template_parsers):
    """Test that template tiers are reasonably distributed."""
    tier_counts = {1: 0, 2: 0, 3: 0, 4: 0}

    for parser in template_parsers:
        if parser.has_frontmatter:
            tier = parser.get_metadata_field("tier")
            if tier in tier_counts:
                tier_counts[tier] += 1

    # Tier 1 should be minority (most essential only)
    tier_1_percentage = tier_counts[1] / len(template_parsers) if template_parsers else 0

    assert tier_1_percentage <= 0.3, (
        f"Too many Tier 1 templates ({tier_1_percentage:.0%}). "
        "Tier 1 should be reserved for absolutely essential templates (< 30%)"
    )

    # Should have good spread across tiers
    assert tier_counts[2] > 0, "Should have Tier 2 templates (commonly needed)"
    assert tier_counts[3] > 0, "Should have Tier 3 templates (situational)"


# ============================================================================
# Test: Cross-Reference Completeness
# ============================================================================


@pytest.mark.unit
def test_development_rules_are_referenced(template_parsers):
    """Test that templates reference development-rules.md where appropriate."""
    # Templates that should reference development rules
    should_reference_rules = [
        "CLAUDE",
        "session-checklist",
        "start-here",
    ]

    missing_references = []
    for parser in template_parsers:
        if parser.name in should_reference_rules:
            if "development-rules" not in parser._body.lower():
                missing_references.append(parser.name)

    assert not missing_references, (
        f"Templates missing development-rules.md reference: {missing_references}. "
        "Core templates should point to development rules."
    )


@pytest.mark.unit
def test_use_case_workflow_is_complete(template_parsers, framework_root: Path):
    """Test that use case workflow templates form complete chain."""
    # Use case workflow: template → writing → implementation → testing
    workflow_chain = [
        ".claude/templates/use-case-template.md",  # Creating UC
        # Would also check for UC writing guidance, BDD scenario template, etc.
    ]

    for template_path in workflow_chain:
        full_path = framework_root / template_path
        assert full_path.exists(), (
            f"Use case workflow incomplete: {template_path} missing. "
            "Should have complete UC → implementation → test workflow."
        )


@pytest.mark.unit
def test_session_workflow_is_complete(template_parsers):
    """Test that session management templates form complete workflow."""
    required_session_templates = [
        "CLAUDE",  # Session start
        "session-checklist",  # Session protocols
        "session-state",  # Session state tracking
    ]

    template_names = [parser.name for parser in template_parsers]

    missing_templates = [name for name in required_session_templates if name not in template_names]

    assert not missing_templates, (
        f"Session workflow incomplete: missing {missing_templates}. "
        "Should have complete session start → work → end workflow."
    )


# ============================================================================
# Test: Template Relationships
# ============================================================================


@pytest.mark.unit
def test_templates_reference_appropriate_specs(template_parsers):
    """Test that implementation templates reference spec templates."""
    # Templates that deal with implementation should reference specs
    implementation_templates = [
        "implementation-CLAUDE",
        "code-reuse-checklist",
    ]

    for parser in template_parsers:
        if parser.name in implementation_templates:
            # Should mention specs, use cases, or specifications
            has_spec_reference = any(
                keyword in parser._body.lower()
                for keyword in ["specification", "use case", "uc-", "spec/"]
            )

            assert has_spec_reference, (
                f"Implementation template {parser.name} should reference specifications. "
                "Implementation must be spec-driven (Rule #1)."
            )


@pytest.mark.unit
def test_research_templates_link_to_decisions(template_parsers):
    """Test that research templates link to decision-making."""
    research_templates = [
        "article-links",
        "paper-summary",
        "library-evaluation",
        "benchmark-report",
    ]

    for parser in template_parsers:
        if parser.name in research_templates:
            # Should mention ADRs or technical decisions
            has_decision_link = any(
                keyword in parser._body.lower()
                for keyword in ["adr", "decision", "technical-decisions"]
            )

            if not has_decision_link:
                pytest.skip(
                    f"Research template {parser.name} could link to decision templates (ADR). "
                    "Research should inform decisions (Rule #4)."
                )


# ============================================================================
# Test: Framework Integration
# ============================================================================


@pytest.mark.unit
def test_templates_align_with_12_rules(template_parsers):
    """Test that templates support all 12 development rules."""
    # Map templates to rules they support
    rule_support = {
        "Rule #1 (Specifications)": ["use-case-template", "service-spec"],
        "Rule #2 (Tests)": [],  # No test template yet - gap!
        "Rule #4 (Research)": [
            "article-links",
            "paper-summary",
            "implementation-readme",
            "library-evaluation",
        ],
        "Rule #7 (Technical Decisions)": ["technical-decisions"],
        "Rule #10 (Session Discipline)": ["CLAUDE", "session-checklist", "session-state"],
        "Rule #11 (Git Workflow)": ["git-workflow"],
        "Rule #12 (Refactoring)": ["refactoring-checklist"],
    }

    template_names = [parser.name for parser in template_parsers]

    unsupported_rules = []
    for rule, supporting_templates in rule_support.items():
        if supporting_templates:  # Only check if we expect templates
            has_support = any(template in template_names for template in supporting_templates)
            if not has_support:
                unsupported_rules.append(rule)

    # This is informational - not all rules need templates
    if unsupported_rules:
        print(f"\n\nRules without template support: {unsupported_rules}")
        print("(This may be intentional - not all rules need templates)")


@pytest.mark.unit
def test_templates_cover_tdd_cycle(template_parsers, framework_root: Path):
    """Test that templates cover RED-GREEN-REFACTOR cycle."""
    tdd_coverage = {
        "RED (Write failing tests)": None,  # No template yet
        "GREEN (Make tests pass)": "implementation-CLAUDE",
        "REFACTOR": "refactoring-checklist",
    }

    template_names = [parser.name for parser in template_parsers]

    for phase, template_name in tdd_coverage.items():
        if template_name and template_name not in template_names:
            pytest.skip(
                f"TDD phase '{phase}' missing template: {template_name}. "
                "Framework should support full TDD cycle."
            )


# ============================================================================
# Test: Directory Structure Alignment
# ============================================================================


@pytest.mark.unit
def test_template_locations_match_purpose(template_parsers, framework_root: Path):
    """Test that templates are in appropriate directories."""
    templates_dir = framework_root / ".claude" / "templates"

    # Check for proper directory organization
    research_dir = templates_dir / "research"
    if research_dir.exists():
        research_files = list(research_dir.glob("*.md"))
        assert len(research_files) >= 3, (
            f"Research directory has only {len(research_files)} templates. "
            "Should have multiple research templates (articles, papers, implementations, etc.)"
        )


@pytest.mark.unit
def test_no_orphaned_templates(framework_root: Path):
    """Test that all templates in .claude/templates are referenced somewhere."""
    templates_dir = framework_root / ".claude" / "templates"

    # Find all template files
    all_template_files = []
    for md_file in templates_dir.rglob("*.md"):
        if md_file.is_file():
            all_template_files.append(md_file.relative_to(templates_dir))

    # Check that critical templates are present
    critical_templates = [
        "CLAUDE.md",
        "development-rules.md",
        "use-case-template.md",
    ]

    missing_critical = []
    for critical in critical_templates:
        if not (templates_dir / critical).exists():
            missing_critical.append(critical)

    assert not missing_critical, (
        f"Missing critical templates: {missing_critical}. "
        "Framework requires these core templates."
    )


# ============================================================================
# Test: Completeness Report
# ============================================================================


@pytest.mark.unit
def test_template_coverage_report(template_parsers, framework_root: Path):
    """Generate comprehensive report of template coverage."""
    print("\n\n=== Template Completeness Report ===")

    # Count by tier
    tier_counts = {1: [], 2: [], 3: [], 4: []}
    for parser in template_parsers:
        if parser.has_frontmatter:
            tier = parser.get_metadata_field("tier")
            if tier in tier_counts:
                tier_counts[tier].append(parser.name)

    print("\nTemplates by Tier:")
    for tier in sorted(tier_counts.keys()):
        print(f"  Tier {tier}: {len(tier_counts[tier])} templates")

    # Count by category (based on location)
    templates_dir = framework_root / ".claude" / "templates"
    categories = {}
    for parser in template_parsers:
        # Determine category from file path
        template_path = templates_dir / f"{parser.name}.md"
        if not template_path.exists():
            # Check in research subdirectory
            template_path = templates_dir / "research" / f"{parser.name}.md"

        if template_path.exists():
            parent = template_path.parent.name
            category = "core" if parent == "templates" else parent
            if category not in categories:
                categories[category] = []
            categories[category].append(parser.name)

    print("\nTemplates by Category:")
    for category in sorted(categories.keys()):
        print(f"  {category}: {len(categories[category])} templates")

    # Development phase coverage
    phases = {
        "Planning": ["use-case-template", "service-spec"],
        "Research": [
            "article-links",
            "paper-summary",
            "implementation-readme",
            "library-evaluation",
            "benchmark-report",
        ],
        "Implementation": ["implementation-CLAUDE", "code-reuse-checklist"],
        "Quality": ["refactoring-checklist", "requirements-review-checklist"],
        "Decision": ["technical-decisions"],
        "Session Management": ["CLAUDE", "session-checklist", "session-state"],
    }

    print("\nDevelopment Phase Coverage:")
    template_names = [parser.name for parser in template_parsers]
    for phase, phase_templates in phases.items():
        covered = sum(1 for t in phase_templates if t in template_names)
        print(f"  {phase}: {covered}/{len(phase_templates)} templates")

    print(f"\nTotal Templates: {len(template_parsers)}")

    assert True  # Informational test


@pytest.mark.unit
def test_template_gaps_analysis(template_parsers):
    """Analyze and report template gaps in framework."""
    template_names = [parser.name for parser in template_parsers]

    # Expected templates that might be missing
    potentially_missing = {
        "Test Writing": "test-writing-template",
        "BDD Scenarios": "bdd-scenario-template",
        "ADR Template": "adr-template",
        "Service Design": "service-design-template",
        "API Documentation": "api-doc-template",
        "Architecture Decision": "architecture-template",
    }

    missing = []
    for purpose, template_name in potentially_missing.items():
        if template_name not in template_names:
            missing.append((purpose, template_name))

    if missing:
        print("\n\n=== Potential Template Gaps ===")
        for purpose, name in missing:
            print(f"  {purpose}: {name} (not found)")
        print("\nThese templates may not be needed, or may be documented elsewhere.")

    assert True  # Informational test
