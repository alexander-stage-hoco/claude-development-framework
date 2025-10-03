"""Template structure validation tests.

Tests validate markdown structure and formatting in templates.
"""

import pytest
import re
from pathlib import Path
from tests.templates.fixtures.template_parser import TemplateParser


# ============================================================================
# Test: H1 Title
# ============================================================================


@pytest.mark.unit
def test_template_has_exactly_one_h1_title(template_parser: TemplateParser):
    """Test that template has exactly one H1 (#) title."""
    h1_count = template_parser._body.count("\n# ")
    # Also check if starts with #
    if template_parser._body.startswith("# "):
        h1_count += 1

    assert (
        h1_count == 1
    ), f"Template {template_parser.name} should have exactly 1 H1 title, found {h1_count}"


@pytest.mark.unit
def test_h1_title_is_descriptive(template_parser: TemplateParser):
    """Test that H1 title is descriptive."""
    h1_title = template_parser.get_h1_title()

    assert h1_title, f"Template {template_parser.name} has no H1 title"

    assert len(h1_title) >= 5, f"Template {template_parser.name} H1 title too short: '{h1_title}'"

    # Should not be all caps (unless acronym)
    if len(h1_title.replace(" ", "")) > 10:  # Longer than typical acronym
        assert not h1_title.isupper(), (
            f"Template {template_parser.name} H1 title should not be all caps: '{h1_title}' "
            "(use title case instead)"
        )


# ============================================================================
# Test: Section Headers
# ============================================================================


@pytest.mark.unit
def test_sections_use_h2_headers(template_parser: TemplateParser):
    """Test that main sections use H2 (##) headers."""
    # Count H2 headers
    h2_count = len(template_parser.sections)

    # Template should have at least one section
    assert (
        h2_count >= 1
    ), f"Template {template_parser.name} should have at least 1 section (## header)"


@pytest.mark.unit
def test_no_h4_or_deeper_headers(template_parser: TemplateParser):
    """Test that template doesn't use H4 (####) or deeper headers."""
    # H4 or deeper suggests too much nesting
    h4_pattern = r"^####+ "
    h4_matches = re.findall(h4_pattern, template_parser._body, re.MULTILINE)

    assert (
        not h4_matches
    ), f"Template {template_parser.name} uses H4+ headers (too deep). Use H2 (##) or H3 (###) only"


# ============================================================================
# Test: Internal Links
# ============================================================================


@pytest.mark.unit
def test_no_broken_internal_links(template_parser: TemplateParser, framework_root: Path):
    """Test that internal file links are valid."""
    file_refs = template_parser.extract_file_references()

    broken_links = []

    for file_ref in file_refs:
        # Resolve relative to .claude/ directory (where templates live)
        templates_dir = framework_root / ".claude" / "templates"

        if file_ref.startswith("./"):
            file_path = templates_dir / file_ref[2:]
        elif file_ref.startswith("../"):
            file_path = (templates_dir / file_ref).resolve()
        elif file_ref.startswith(".claude/"):
            file_path = framework_root / file_ref
        else:
            file_path = templates_dir / file_ref

        if not file_path.exists():
            broken_links.append((file_ref, str(file_path)))

    assert (
        not broken_links
    ), f"Template {template_parser.name} has broken internal links:\n" + "\n".join(
        f"  - {ref} → {path}" for ref, path in broken_links
    )


# ============================================================================
# Test: Markdown Syntax
# ============================================================================


@pytest.mark.unit
def test_code_blocks_are_closed(template_parser: TemplateParser):
    """Test that all code blocks are properly closed."""
    fence_count = template_parser._body.count("```")

    assert (
        fence_count % 2 == 0
    ), f"Template {template_parser.name} has unclosed code block (odd number of ``` fences: {fence_count})"


@pytest.mark.unit
def test_no_unclosed_brackets(template_parser: TemplateParser):
    """Test that markdown link brackets are balanced."""
    # Count [ and ] (excluding code blocks)
    content_no_code = re.sub(r"```.*?```", "", template_parser._body, flags=re.DOTALL)

    open_brackets = content_no_code.count("[")
    close_brackets = content_no_code.count("]")

    assert open_brackets == close_brackets, (
        f"Template {template_parser.name} has unbalanced brackets: "
        f"{open_brackets} '[' vs {close_brackets} ']'"
    )


@pytest.mark.unit
def test_lists_properly_formatted(template_parser: TemplateParser):
    """Test that lists use consistent formatting."""
    lines = template_parser._body.split("\n")

    # Check for mixed list markers (- and *)
    has_dash_lists = any(line.strip().startswith("- ") for line in lines)
    has_star_lists = any(
        line.strip().startswith("* ") and not line.strip().startswith("**") for line in lines
    )

    # Prefer not mixing, but not a hard failure
    if has_dash_lists and has_star_lists:
        pytest.skip(
            f"Template {template_parser.name} uses both - and * for lists (prefer consistent)"
        )


# ============================================================================
# Test: Tables
# ============================================================================


@pytest.mark.unit
def test_tables_properly_formatted(template_parser: TemplateParser):
    """Test that markdown tables are properly formatted."""
    lines = template_parser._body.split("\n")

    # Find table separator lines (e.g., |---|---|)
    separator_pattern = r"^\s*\|[\s\-:|]+\|\s*$"

    for i, line in enumerate(lines):
        if re.match(separator_pattern, line):
            # This is a table separator - check header above and data below
            if i == 0:
                pytest.fail(
                    f"Template {template_parser.name} line {i+1}: Table separator without header"
                )

            header_line = lines[i - 1]
            if not header_line.strip().startswith("|"):
                pytest.fail(
                    f"Template {template_parser.name} line {i}: Table separator but no header above"
                )

            # Count pipes in header and separator
            header_pipes = header_line.count("|")
            separator_pipes = line.count("|")

            assert header_pipes == separator_pipes, (
                f"Template {template_parser.name} line {i+1}: "
                f"Table column mismatch (header has {header_pipes} pipes, separator has {separator_pipes})"
            )


# ============================================================================
# Test: Horizontal Rules
# ============================================================================


@pytest.mark.unit
def test_horizontal_rules_use_triple_dash(template_parser: TemplateParser):
    """Test that horizontal rules use --- format (consistent with YAML)."""
    # Look for horizontal rules
    hr_variants = [
        template_parser._body.count("\n---\n"),
        template_parser._body.count("\n***\n"),
        template_parser._body.count("\n___\n"),
    ]

    # If using horizontal rules, should be ---
    if any(hr_variants):
        # Prefer --- (matches YAML delimiter)
        assert (
            hr_variants[0] > 0 or sum(hr_variants) == 0
        ), f"Template {template_parser.name} should use --- for horizontal rules (not *** or ___)"


# ============================================================================
# Test: File Size
# ============================================================================


@pytest.mark.unit
def test_template_size_reasonable(template_parser: TemplateParser):
    """Test that template file size is reasonable."""
    file_size_kb = len(template_parser.content) / 1024

    assert (
        file_size_kb < 100
    ), f"Template {template_parser.name} is very large ({file_size_kb:.1f}KB). Consider splitting or simplifying."


# ============================================================================
# Test: Structure Report
# ============================================================================


@pytest.mark.unit
def test_structure_consistency_report(template_parsers):
    """Generate report of structure patterns across templates."""
    section_patterns = {}

    for parser in template_parsers:
        for section_title in parser.sections.keys():
            if section_title not in section_patterns:
                section_patterns[section_title] = []
            section_patterns[section_title].append(parser.name)

    # Print common sections
    print("\n\n=== Common Template Sections ===")
    common_sections = {
        title: templates
        for title, templates in section_patterns.items()
        if len(templates) >= 3  # Appears in 3+ templates
    }

    for section, templates in sorted(
        common_sections.items(), key=lambda x: len(x[1]), reverse=True
    ):
        print(f"\n'{section}' ({len(templates)} templates):")
        for template in sorted(templates)[:5]:  # Show first 5
            print(f"  - {template}")
        if len(templates) > 5:
            print(f"  ... and {len(templates) - 5} more")

    # Just informational - always pass
    assert True
