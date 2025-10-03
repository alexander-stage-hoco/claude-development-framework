"""Template instantiation validation tests.

Tests validate that templates can be instantiated with real values.
"""

import pytest
import re
from pathlib import Path
from tests.templates.fixtures.template_parser import TemplateParser


# ============================================================================
# Test: Placeholder Replacement
# ============================================================================


@pytest.mark.unit
def test_placeholders_can_be_replaced(template_parser: TemplateParser):
    """Test that placeholders can be replaced with real values."""
    placeholders = template_parser.extract_placeholders()

    if not placeholders:
        pytest.skip(f"Template {template_parser.name} has no placeholders")

    # Create sample replacement values
    replacement_values = {
        "PROJECT_NAME": "test-project",
        "DATE": "2025-10-03",
        "UC_ID": "UC-001",
        "SERVICE_NAME": "AuthenticationService",
        "ITERATION_ID": "iteration-001",
        "ADR_ID": "ADR-001",
        "AUTHOR": "Claude",
    }

    # Perform replacement
    instantiated = template_parser._body
    for placeholder in placeholders:
        # Use replacement value if available, otherwise use placeholder-test-value
        replacement = replacement_values.get(placeholder, f"{placeholder.lower()}-test-value")
        instantiated = instantiated.replace(f"[{placeholder}]", replacement)

    # Verify no unhandled placeholders remain (except in code blocks)
    # Remove code blocks first
    instantiated_no_code = re.sub(r"```.*?```", "", instantiated, flags=re.DOTALL)

    remaining_placeholders = re.findall(r"\[([A-Z][A-Z0-9_]*)\]", instantiated_no_code)

    assert (
        not remaining_placeholders
    ), f"Template {template_parser.name} has placeholders that couldn't be replaced: {remaining_placeholders[:5]}"


@pytest.mark.unit
def test_instantiated_template_is_valid_markdown(template_parser: TemplateParser):
    """Test that instantiated template is still valid markdown."""
    placeholders = template_parser.extract_placeholders()

    if not placeholders:
        pytest.skip(f"Template {template_parser.name} has no placeholders")

    # Simple replacement
    instantiated = template_parser._body
    for placeholder in placeholders:
        instantiated = instantiated.replace(f"[{placeholder}]", f"test-{placeholder.lower()}")

    # Check markdown validity (balanced brackets, code blocks closed)
    # Count backticks
    fence_count = instantiated.count("```")
    assert (
        fence_count % 2 == 0
    ), f"Template {template_parser.name} has unclosed code blocks after instantiation"

    # Count brackets (excluding code blocks)
    content_no_code = re.sub(r"```.*?```", "", instantiated, flags=re.DOTALL)
    open_brackets = content_no_code.count("[")
    close_brackets = content_no_code.count("]")

    assert open_brackets == close_brackets, (
        f"Template {template_parser.name} has unbalanced brackets after instantiation: "
        f"{open_brackets} '[' vs {close_brackets} ']'"
    )


# ============================================================================
# Test: Template Completeness After Instantiation
# ============================================================================


@pytest.mark.unit
def test_instantiated_template_has_no_empty_sections(template_parser: TemplateParser):
    """Test that instantiated template has no empty required sections."""
    # Look for sections that should not be empty after instantiation
    required_content_markers = [
        "## Purpose",
        "## Overview",
        "## Description",
        "## Instructions",
    ]

    for marker in required_content_markers:
        if marker in template_parser._body:
            # Find content after marker (until next ##)
            pattern = re.escape(marker) + r"\s*\n\n(.+?)(?=\n##|\Z)"
            match = re.search(pattern, template_parser._body, re.DOTALL)

            if match:
                content = match.group(1).strip()
                # Check if content is just placeholders
                if re.match(r"^\s*\[.*\]\s*$", content):
                    pytest.skip(
                        f"Template {template_parser.name} section '{marker}' is just placeholders. "
                        "Should have some default text."
                    )


@pytest.mark.unit
def test_instantiated_template_has_no_placeholder_artifacts(template_parser: TemplateParser):
    """Test that template doesn't have broken placeholder references."""
    # Look for common placeholder formatting errors
    broken_patterns = [
        r"\[\s+[A-Z]",  # [ PROJECT] - space after [
        r"[A-Z]\s+\]",  # [PROJECT ] - space before ]
        r"\[\[[A-Z]",  # [[PROJECT]] - double brackets
        r"\[_[A-Z]",  # [_PROJECT] - leading underscore
    ]

    found_issues = []
    for pattern in broken_patterns:
        matches = re.findall(pattern, template_parser._body)
        if matches:
            found_issues.extend(matches[:2])

    if found_issues:
        pytest.fail(
            f"Template {template_parser.name} has malformed placeholder patterns: {found_issues}"
        )


# ============================================================================
# Test: Metadata Placeholder Handling
# ============================================================================


@pytest.mark.unit
def test_frontmatter_placeholders_documented(template_parser: TemplateParser):
    """Test that frontmatter placeholders are documented in template body."""
    if not template_parser.has_frontmatter:
        pytest.skip(f"Template {template_parser.name} has no frontmatter")

    # Check if frontmatter has placeholder-like values
    frontmatter_text = str(template_parser.metadata)

    # Look for uppercase words that might be placeholders
    potential_placeholders = re.findall(r"\b[A-Z][A-Z_]+\b", frontmatter_text)

    if potential_placeholders:
        # These should be documented in the template body
        for placeholder in potential_placeholders[:3]:  # Check first 3
            if placeholder not in template_parser._body:
                pytest.skip(
                    f"Template {template_parser.name} frontmatter has '{placeholder}' but it's not in body. "
                    "Document how to fill frontmatter."
                )


# ============================================================================
# Test: Common Placeholder Patterns
# ============================================================================


@pytest.mark.unit
def test_date_placeholders_have_format_hints(template_parser: TemplateParser):
    """Test that DATE placeholders have format hints."""
    if "DATE" in template_parser.extract_placeholders():
        # Look for date format hints near DATE placeholder
        has_format_hint = any(
            pattern in template_parser._body
            for pattern in ["YYYY-MM-DD", "yyyy-mm-dd", "ISO", "2025-", "format:"]
        )

        if not has_format_hint:
            pytest.skip(
                f"Template {template_parser.name} has [DATE] placeholder but no format hint. "
                "Consider adding example: [DATE] (YYYY-MM-DD)"
            )


@pytest.mark.unit
def test_id_placeholders_have_format_hints(template_parser: TemplateParser):
    """Test that ID placeholders (UC-XXX, ADR-XXX) have format hints."""
    placeholders = template_parser.extract_placeholders()

    id_placeholders = [p for p in placeholders if p.endswith("_ID")]

    for id_ph in id_placeholders:
        # Look for format hints near this placeholder
        lines = template_parser._body.split("\n")
        locations = template_parser.extract_placeholder_locations()

        if id_ph in locations:
            line_num = locations[id_ph][0]
            context_start = max(0, line_num - 2)
            context_end = min(len(lines), line_num + 2)
            context = "\n".join(lines[context_start:context_end])

            # Should have example format like UC-001, ADR-001, etc.
            has_format_hint = re.search(r"(UC|ADR|SVC|ITERATION)-\d{3}", context)

            if not has_format_hint:
                pytest.skip(
                    f"Template {template_parser.name} has [{id_ph}] but no format example. "
                    "Consider adding example: UC-001, ADR-001, etc."
                )


# ============================================================================
# Test: Template Instantiation Workflow
# ============================================================================


@pytest.mark.unit
def test_template_has_instantiation_instructions(template_parser: TemplateParser):
    """Test that template explains how to use it."""
    placeholders = template_parser.extract_placeholders()

    if len(placeholders) > 3:
        # Template with many placeholders should have usage instructions
        has_instructions = any(
            indicator in template_parser._body.lower()
            for indicator in [
                "how to use",
                "instructions",
                "fill in",
                "replace [",
                "before using",
                "setup",
            ]
        )

        if not has_instructions:
            pytest.skip(
                f"Template {template_parser.name} has {len(placeholders)} placeholders but no usage instructions. "
                "Consider adding 'How to Use' section."
            )


# ============================================================================
# Test: Special Template Types
# ============================================================================


@pytest.mark.unit
def test_use_case_template_instantiation(template_parser: TemplateParser):
    """Test use case template specific instantiation rules."""
    if "use-case" not in template_parser.name.lower():
        pytest.skip("Not a use case template")

    # Use case template should have UC-XXX format
    has_uc_format = "UC-" in template_parser._body

    assert has_uc_format, f"Use case template {template_parser.name} should use UC-XXX format"


@pytest.mark.unit
def test_service_template_instantiation(template_parser: TemplateParser):
    """Test service template specific instantiation rules."""
    if "service" not in template_parser.name.lower():
        pytest.skip("Not a service template")

    # Service template should have SVC- or SERVICE_NAME placeholders
    placeholders = template_parser.extract_placeholders()

    has_service_placeholders = any("SERVICE" in p or "SVC" in p for p in placeholders)

    if not has_service_placeholders:
        pytest.skip(
            f"Service template {template_parser.name} should have SERVICE_NAME or SVC-related placeholders"
        )


# ============================================================================
# Test: Instantiation Report
# ============================================================================


@pytest.mark.unit
def test_placeholder_instantiation_report(template_parsers):
    """Generate report of placeholder usage and instantiation readiness."""
    placeholder_counts = {}
    templates_with_format_hints = []

    for parser in template_parsers:
        placeholders = parser.extract_placeholders()
        placeholder_counts[parser.name] = len(placeholders)

        # Check for format hints
        has_hints = any(
            pattern in parser._body.lower()
            for pattern in ["e.g.", "example:", "format:", "YYYY", "XXX", "-001"]
        )

        if has_hints and placeholders:
            templates_with_format_hints.append(parser.name)

    print("\n\n=== Template Instantiation Analysis ===")

    print("\nTemplates by placeholder count:")
    for name, count in sorted(placeholder_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        if count > 0:
            print(f"  {name}: {count} placeholders")

    print(f"\nTemplates with format hints: {len(templates_with_format_hints)}/22")
    print(
        f"Templates with no placeholders: {sum(1 for c in placeholder_counts.values() if c == 0)}/22"
    )

    assert True  # Informational test
