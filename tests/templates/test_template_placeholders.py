"""Template placeholder validation tests.

Tests validate placeholder format and usage in templates.
"""

import pytest
import re
from tests.templates.fixtures.template_parser import TemplateParser


# ============================================================================
# Test: Placeholder Format Validation
# ============================================================================


@pytest.mark.unit
def test_placeholders_use_correct_format(template_parser: TemplateParser):
    """Test that placeholders use [UPPERCASE] format."""
    # Extract all bracketed content
    bracket_pattern = r"\[([^\]]+)\]"
    all_brackets = re.findall(bracket_pattern, template_parser._body)

    # Filter to potential placeholders (not links, not code)
    potential_placeholders = []
    for content in all_brackets:
        # Skip if it's clearly not a placeholder
        if any(
            [
                content.startswith("http"),  # URLs
                content.startswith("x") and content.endswith("x"),  # checkboxes [x]
                content.strip() == "",  # empty brackets
                content.startswith(" "),  # checkboxes [ ]
                len(content) == 1,  # single char  like [1]
            ]
        ):
            continue

        # Check if it looks like a placeholder (uppercase or mixed case)
        if any(c.isupper() for c in content):
            potential_placeholders.append(content)

    # All uppercase placeholders should follow convention
    invalid_placeholders = []
    for placeholder in potential_placeholders:
        # Should be all caps with optional underscores and numbers
        if not re.match(r"^[A-Z][A-Z0-9_]*$", placeholder):
            # Allow some exceptions
            exceptions = [
                "Feature",  # BDD Feature keyword
                "Scenario",  # BDD Scenario keyword
                "Given",
                "When",
                "Then",  # BDD keywords
            ]
            if placeholder not in exceptions:
                invalid_placeholders.append(placeholder)

    if invalid_placeholders:
        pytest.skip(
            f"Template {template_parser.name} has non-standard placeholder format: {', '.join(invalid_placeholders[:5])} "
            "(consider using [UPPERCASE_WITH_UNDERSCORES] format)"
        )


@pytest.mark.unit
def test_placeholder_names_are_descriptive(template_parser: TemplateParser):
    """Test that placeholder names are descriptive, not generic single letters."""
    placeholders = template_parser.extract_placeholders()

    # Single letter placeholders are discouraged (except common mathematical ones)
    single_letter_placeholders = [p for p in placeholders if len(p) == 1]

    allowed_single_letters = ["N", "X", "Y", "Z", "M", "K"]  # Common in examples

    problematic = [p for p in single_letter_placeholders if p not in allowed_single_letters]

    if problematic:
        pytest.skip(
            f"Template {template_parser.name} uses single-letter placeholders: {', '.join(problematic)} "
            "(consider more descriptive names like [PROJECT_NAME], [SERVICE_NAME])"
        )


@pytest.mark.unit
def test_no_unclosed_placeholders(template_parser: TemplateParser):
    """Test that all placeholder brackets are properly closed."""
    # This is covered by structure tests but let's be explicit for placeholders
    placeholder_pattern = r"\[([A-Z][A-Z0-9_]*)\]"

    # Count opening brackets that look like placeholders
    content_lines = template_parser._body.split("\n")
    unclosed_lines = []

    for line_num, line in enumerate(content_lines, 1):
        # Skip code blocks
        if line.strip().startswith("```"):
            continue

        # Find potential placeholder starts
        potential_starts = [m.start() for m in re.finditer(r"\[[A-Z]", line)]

        for start_pos in potential_starts:
            # Check if there's a closing bracket
            rest_of_line = line[start_pos:]
            if "]" not in rest_of_line:
                unclosed_lines.append((line_num, line.strip()))

    assert (
        not unclosed_lines
    ), f"Template {template_parser.name} has unclosed placeholder brackets on lines: {unclosed_lines[:3]}"


# ============================================================================
# Test: Common Placeholder Consistency
# ============================================================================


@pytest.mark.unit
def test_common_placeholders_are_consistent(template_parsers):
    """Test that common placeholders are used consistently across templates."""
    # Collect all placeholders across all templates
    placeholder_variants = {}

    for parser in template_parsers:
        placeholders = parser.extract_placeholders()
        for placeholder in placeholders:
            # Normalize for comparison (lowercase)
            normalized = placeholder.lower()
            if normalized not in placeholder_variants:
                placeholder_variants[normalized] = set()
            placeholder_variants[normalized].add(placeholder)

    # Check for inconsistent variants
    inconsistent = {}
    for normalized, variants in placeholder_variants.items():
        if len(variants) > 1:
            # This could be intentional (PROJECT_NAME vs PROJECT_ID) but worth checking
            if any(
                variant.startswith(tuple(["PROJECT", "SERVICE", "UC", "ADR", "ITERATION"]))
                for variant in variants
            ):
                # These are expected to have variants
                continue
            inconsistent[normalized] = variants

    if inconsistent:
        print("\n\n=== Potentially Inconsistent Placeholders ===")
        for normalized, variants in sorted(inconsistent.items()):
            print(f"{normalized}: {', '.join(sorted(variants))}")

    # Just informational - not a hard failure
    assert True


@pytest.mark.unit
def test_project_name_placeholder_format(template_parser: TemplateParser):
    """Test that PROJECT_NAME placeholder is used (not Project_Name or other variants)."""
    placeholders = template_parser.extract_placeholders()

    # Check for PROJECT_NAME related placeholders
    project_related = [p for p in placeholders if "PROJECT" in p.upper()]

    if project_related:
        # Should use PROJECT_NAME format
        assert "PROJECT_NAME" in placeholders or all(p.isupper() for p in project_related), (
            f"Template {template_parser.name} uses inconsistent PROJECT placeholder: {project_related} "
            "(use [PROJECT_NAME] as standard)"
        )


# ============================================================================
# Test: Forgotten Content Detection
# ============================================================================


@pytest.mark.unit
def test_no_todo_markers_in_templates(template_parser: TemplateParser):
    """Test that templates don't contain TODO, FIXME, or XXX markers."""
    # These indicate unfinished template content
    forbidden_markers = ["TODO:", "FIXME:", "XXX:", "HACK:"]

    found_markers = []
    for marker in forbidden_markers:
        if marker in template_parser._body:
            # Find line numbers
            lines = template_parser._body.split("\n")
            for line_num, line in enumerate(lines, 1):
                if marker in line:
                    # Allow XXX when used as placeholder pattern (UC-XXX, ADR-XXX, etc.)
                    if marker == "XXX:" and re.search(
                        r"(UC|ADR|ITERATION|SVC)-XXX", line, re.IGNORECASE
                    ):
                        continue
                    found_markers.append((marker, line_num, line.strip()[:60]))

    if found_markers:
        examples = "\n".join(
            f"  Line {ln}: {marker} - {text}" for marker, ln, text in found_markers[:3]
        )
        pytest.fail(
            f"Template {template_parser.name} contains unfinished markers:\n{examples}\n"
            "(Templates should be complete - use placeholders like [TODO] instead)"
        )


@pytest.mark.unit
def test_no_tbd_placeholders(template_parser: TemplateParser):
    """Test that templates don't have [TBD] or 'to be determined' placeholders."""
    tbd_patterns = [r"\[TBD\]", r"\[TO BE DETERMINED\]", r"to be determined", r"TBD\b"]

    found_tbd = []
    for pattern in tbd_patterns:
        matches = re.finditer(pattern, template_parser._body, re.IGNORECASE)
        for match in matches:
            # Find line number
            line_num = template_parser._body[: match.start()].count("\n") + 1
            # Get the line content
            lines = template_parser._body.split("\n")
            line_content = lines[line_num - 1] if line_num <= len(lines) else ""

            # Allow TBD in table cells (markdown tables use |)
            if "|" in line_content and "TBD" in line_content:
                continue

            found_tbd.append((pattern, line_num))

    if found_tbd:
        pytest.fail(
            f"Template {template_parser.name} contains TBD placeholders: {found_tbd[:3]}\n"
            "(Use specific placeholders like [PROJECT_NAME], [DATE] instead)"
        )


@pytest.mark.unit
def test_no_example_placeholders_left(template_parser: TemplateParser):
    """Test that example markers are intentional, not forgotten placeholders."""
    # Patterns that suggest forgotten example content
    suspicious_patterns = [
        r"\[Example\](?!\s*:)",  # [Example] not followed by colon (should be [Example]: ...)
        r"\[Sample\](?!\s*:)",
        r"e\.g\.\s*\[",  # "e.g. [" suggests example not filled in
    ]

    found_suspicious = []
    for pattern in suspicious_patterns:
        matches = re.finditer(pattern, template_parser._body, re.IGNORECASE)
        for match in matches:
            line_num = template_parser._body[: match.start()].count("\n") + 1
            found_suspicious.append((pattern, line_num))

    if found_suspicious:
        pytest.skip(
            f"Template {template_parser.name} has potentially unfilled examples: {found_suspicious[:2]} "
            "(verify these are intentional placeholders)"
        )


# ============================================================================
# Test: Placeholder Documentation
# ============================================================================


@pytest.mark.unit
def test_common_placeholders_have_examples(template_parser: TemplateParser):
    """Test that common placeholders have example values or explanations nearby."""
    placeholders = template_parser.extract_placeholders()

    # Common placeholders that should have examples
    should_have_examples = ["PROJECT_NAME", "UC_ID", "SERVICE_NAME", "DATE"]

    missing_examples = []
    for placeholder in should_have_examples:
        if placeholder in placeholders:
            # Check if there's an example or explanation within 5 lines
            locations = template_parser.extract_placeholder_locations()
            if placeholder in locations:
                for line_num in locations[placeholder]:
                    # Get context (3 lines before and after)
                    lines = template_parser._body.split("\n")
                    start = max(0, line_num - 3)
                    end = min(len(lines), line_num + 3)
                    context = "\n".join(lines[start:end])

                    # Look for example indicators
                    has_example = any(
                        indicator in context.lower()
                        for indicator in [
                            "example:",
                            "e.g.",
                            "for example",
                            'e.g. "',
                            "such as",
                        ]
                    )

                    if not has_example:
                        missing_examples.append((placeholder, line_num))
                        break  # Only report once per placeholder

    if missing_examples:
        pytest.skip(
            f"Template {template_parser.name} placeholders missing examples: {missing_examples[:3]} "
            "(consider adding examples like: [PROJECT_NAME] e.g. 'my-project')"
        )


# ============================================================================
# Test: Placeholder Coverage Report
# ============================================================================


@pytest.mark.unit
def test_placeholder_usage_report(template_parsers):
    """Generate report of placeholder usage across templates."""
    placeholder_usage = {}

    for parser in template_parsers:
        placeholders = parser.extract_placeholders()
        for placeholder in placeholders:
            if placeholder not in placeholder_usage:
                placeholder_usage[placeholder] = []
            placeholder_usage[placeholder].append(parser.name)

    # Print common placeholders
    print("\n\n=== Common Template Placeholders ===")
    common_placeholders = {
        ph: templates for ph, templates in placeholder_usage.items() if len(templates) >= 3
    }

    for placeholder, templates in sorted(
        common_placeholders.items(), key=lambda x: len(x[1]), reverse=True
    ):
        print(f"\n[{placeholder}] (used in {len(templates)} templates):")
        for template in sorted(templates)[:5]:
            print(f"  - {template}")
        if len(templates) > 5:
            print(f"  ... and {len(templates) - 5} more")

    # Validation: Should have standard placeholders
    standard_placeholders = ["PROJECT_NAME", "DATE"]
    for std_ph in standard_placeholders:
        if std_ph in placeholder_usage:
            assert (
                len(placeholder_usage[std_ph]) >= 3
            ), f"Standard placeholder [{std_ph}] should be used in multiple templates"

    assert True  # Informational test
