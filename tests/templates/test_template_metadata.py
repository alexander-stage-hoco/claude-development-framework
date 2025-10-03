"""Template metadata validation tests.

Tests validate YAML front matter in all templates.
"""

import pytest
from tests.templates.fixtures.template_parser import TemplateParser


# ============================================================================
# Test: YAML Front Matter Presence
# ============================================================================


@pytest.mark.unit
def test_all_templates_have_yaml_frontmatter(template_parsers):
    """Test that all templates have YAML front matter."""
    templates_without_frontmatter = [
        parser.name for parser in template_parsers if not parser.has_frontmatter
    ]

    assert (
        not templates_without_frontmatter
    ), f"Templates without YAML front matter: {', '.join(templates_without_frontmatter)}"


# ============================================================================
# Test: Required Metadata Fields
# ============================================================================


@pytest.mark.unit
def test_template_has_required_metadata_fields(template_parser: TemplateParser):
    """Test that template has required metadata fields."""
    required_fields = ["tier", "purpose", "reload_trigger"]

    validation = template_parser.validate_required_metadata(required_fields)
    missing_fields = [field for field, present in validation.items() if not present]

    assert (
        not missing_fields
    ), f"Template {template_parser.name} missing required metadata fields: {', '.join(missing_fields)}"


@pytest.mark.unit
def test_template_has_estimated_read_time(template_parser: TemplateParser):
    """Test that template has estimated_read_time field (optional but recommended)."""
    if not template_parser.has_frontmatter:
        pytest.skip(f"Template {template_parser.name} has no front matter")

    has_read_time = "estimated_read_time" in template_parser.metadata

    # This is a soft requirement - warn but don't fail
    if not has_read_time:
        pytest.skip(f"Template {template_parser.name} missing 'estimated_read_time' (recommended)")


# ============================================================================
# Test: Tier Values
# ============================================================================


@pytest.mark.unit
def test_tier_value_is_valid(template_parser: TemplateParser):
    """Test that tier value is valid (1, 2, 3, or 4)."""
    if not template_parser.has_frontmatter:
        pytest.skip(f"Template {template_parser.name} has no front matter")

    tier = template_parser.get_metadata_field("tier")

    assert tier is not None, f"Template {template_parser.name} missing 'tier' field"

    assert tier in [
        1,
        2,
        3,
        4,
    ], f"Template {template_parser.name} has invalid tier value: {tier} (must be 1, 2, 3, or 4)"


@pytest.mark.unit
def test_tier_1_templates_are_essential(template_parser: TemplateParser):
    """Test that Tier 1 templates have appropriate purpose."""
    if not template_parser.has_frontmatter:
        pytest.skip(f"Template {template_parser.name} has no front matter")

    tier = template_parser.get_metadata_field("tier")

    if tier == 1:
        purpose = template_parser.get_metadata_field("purpose") or ""
        purpose_lower = purpose.lower()

        # Tier 1 should be essential/critical
        essential_keywords = ["session", "protocol", "mandatory", "essential", "rules"]
        has_essential_keyword = any(keyword in purpose_lower for keyword in essential_keywords)

        assert has_essential_keyword, (
            f"Template {template_parser.name} is Tier 1 but purpose doesn't indicate essentiality: '{purpose}'. "
            f"Tier 1 should contain keywords like: {', '.join(essential_keywords)}"
        )


# ============================================================================
# Test: Purpose Field
# ============================================================================


@pytest.mark.unit
def test_purpose_is_descriptive(template_parser: TemplateParser):
    """Test that purpose field is descriptive (non-empty, reasonable length)."""
    if not template_parser.has_frontmatter:
        pytest.skip(f"Template {template_parser.name} has no front matter")

    purpose = template_parser.get_metadata_field("purpose")

    assert purpose, f"Template {template_parser.name} has empty 'purpose' field"

    assert isinstance(
        purpose, str
    ), f"Template {template_parser.name} purpose must be string, got {type(purpose)}"

    assert (
        len(purpose) >= 10
    ), f"Template {template_parser.name} purpose too short: '{purpose}' (should be descriptive)"

    assert (
        len(purpose) <= 200
    ), f"Template {template_parser.name} purpose too long: {len(purpose)} chars (should be concise)"


# ============================================================================
# Test: Reload Trigger
# ============================================================================


@pytest.mark.unit
def test_reload_trigger_is_descriptive(template_parser: TemplateParser):
    """Test that reload_trigger field is descriptive."""
    if not template_parser.has_frontmatter:
        pytest.skip(f"Template {template_parser.name} has no front matter")

    reload_trigger = template_parser.get_metadata_field("reload_trigger")

    assert reload_trigger, f"Template {template_parser.name} has empty 'reload_trigger' field"

    assert isinstance(
        reload_trigger, str
    ), f"Template {template_parser.name} reload_trigger must be string, got {type(reload_trigger)}"

    assert (
        len(reload_trigger) >= 5
    ), f"Template {template_parser.name} reload_trigger too short: '{reload_trigger}'"


# ============================================================================
# Test: Estimated Read Time Format
# ============================================================================


@pytest.mark.unit
def test_estimated_read_time_format(template_parser: TemplateParser):
    """Test that estimated_read_time follows expected format."""
    if not template_parser.has_frontmatter:
        pytest.skip(f"Template {template_parser.name} has no front matter")

    read_time = template_parser.get_metadata_field("estimated_read_time")

    if not read_time:
        pytest.skip(f"Template {template_parser.name} doesn't have estimated_read_time (optional)")

    assert isinstance(
        read_time, str
    ), f"Template {template_parser.name} estimated_read_time must be string, got {type(read_time)}"

    # Should contain "minute" or "min"
    read_time_lower = read_time.lower()
    assert (
        "minute" in read_time_lower or "min" in read_time_lower
    ), f"Template {template_parser.name} estimated_read_time should specify minutes: '{read_time}'"


# ============================================================================
# Test: Metadata Consistency Report
# ============================================================================


@pytest.mark.unit
def test_metadata_consistency_report(template_parsers):
    """Generate report of metadata consistency across templates."""
    tier_distribution = {1: [], 2: [], 3: [], 4: []}

    for parser in template_parsers:
        if parser.has_frontmatter:
            tier = parser.get_metadata_field("tier")
            if tier in tier_distribution:
                tier_distribution[tier].append(parser.name)

    # Print distribution for visibility
    print("\n\n=== Template Tier Distribution ===")
    for tier, templates in sorted(tier_distribution.items()):
        print(f"Tier {tier}: {len(templates)} templates")
        for template in sorted(templates):
            print(f"  - {template}")

    # Validation: Should have some Tier 1 templates
    assert tier_distribution[1], "No Tier 1 templates found - should have essential templates"

    # Should have balanced distribution (soft check - just warn)
    total_with_tiers = sum(len(templates) for templates in tier_distribution.values())
    if total_with_tiers > 0:
        tier_1_percentage = len(tier_distribution[1]) / total_with_tiers
        assert tier_1_percentage < 0.5, (
            f"Too many Tier 1 templates ({tier_1_percentage:.0%}). "
            "Tier 1 should be reserved for essential templates only"
        )
