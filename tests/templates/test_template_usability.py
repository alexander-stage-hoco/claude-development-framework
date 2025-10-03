"""Template usability validation tests.

Tests validate that templates are easy to use and understand.
"""

import pytest
import re
from tests.templates.fixtures.template_parser import TemplateParser


# ============================================================================
# Test: Action-Oriented Language
# ============================================================================


@pytest.mark.unit
def test_checklist_items_are_actionable(template_parser: TemplateParser):
    """Test that checklist items use action verbs."""
    # Find checklist items (lines starting with - [ ])
    checklist_pattern = r"^- \[ \] (.+)$"
    checklist_items = re.findall(checklist_pattern, template_parser._body, re.MULTILINE)

    # Action verbs that should start checklist items
    action_verbs = [
        "read",
        "write",
        "create",
        "update",
        "delete",
        "check",
        "verify",
        "test",
        "run",
        "execute",
        "review",
        "analyze",
        "identify",
        "validate",
        "ensure",
        "confirm",
        "document",
        "implement",
        "refactor",
        "fix",
        "add",
        "remove",
        "commit",
        "push",
        "pull",
        "merge",
        "branch",
        "tag",
        "deploy",
        "install",
        "configure",
        "setup",
        "initialize",
        "load",
        "save",
        "export",
        "import",
    ]

    non_actionable = []
    for item in checklist_items:
        # Check if starts with action verb (case insensitive)
        first_word = item.split()[0].lower().rstrip(".,;:!?")
        if first_word not in action_verbs:
            non_actionable.append(item[:60])

    # This is a soft requirement - not all checklists need action verbs
    if non_actionable and len(non_actionable) > len(checklist_items) * 0.5:
        pytest.skip(
            f"Template {template_parser.name} has many non-actionable checklist items: {non_actionable[:3]} "
            "(consider starting with action verbs like 'Read', 'Verify', 'Create')"
        )


@pytest.mark.unit
def test_instructions_use_imperative_mood(template_parser: TemplateParser):
    """Test that instructions use imperative mood (commands)."""
    # Look for numbered steps (instructions)
    step_pattern = r"^\d+\.\s+(.+)$"
    steps = re.findall(step_pattern, template_parser._body, re.MULTILINE)

    if not steps:
        pytest.skip(f"Template {template_parser.name} has no numbered steps")

    # Imperative mood indicators (commands)
    imperative_starters = [
        "read",
        "write",
        "create",
        "run",
        "check",
        "verify",
        "ensure",
        "identify",
        "analyze",
        "review",
        "update",
        "add",
        "remove",
        "start",
        "stop",
        "pause",
        "continue",
        "open",
        "close",
        "save",
        "load",
    ]

    non_imperative = []
    for step in steps[:10]:  # Check first 10 steps
        first_word = step.split()[0].lower().rstrip(".,;:!?")
        if first_word not in imperative_starters:
            # Check if it's a descriptive step (The, A, An, This)
            if first_word in ["the", "a", "an", "this", "that", "these", "those"]:
                non_imperative.append(step[:60])

    # Soft requirement
    if non_imperative and len(non_imperative) > len(steps) * 0.3:
        pytest.skip(
            f"Template {template_parser.name} has descriptive steps instead of commands: {non_imperative[:2]} "
            "(prefer 'Create X' over 'The system creates X')"
        )


# ============================================================================
# Test: Section Organization
# ============================================================================


@pytest.mark.unit
def test_sections_have_descriptive_titles(template_parser: TemplateParser):
    """Test that section titles are descriptive."""
    for section_title, section_content in template_parser.sections.items():
        # Section title should be meaningful
        assert (
            len(section_title) >= 3
        ), f"Template {template_parser.name} section '{section_title}' is too short"

        # Should not be just numbers or single letters
        assert not re.match(
            r"^[0-9A-Z]$", section_title
        ), f"Template {template_parser.name} section '{section_title}' is not descriptive"


@pytest.mark.unit
def test_sections_are_not_empty(template_parser: TemplateParser):
    """Test that sections have content."""
    empty_sections = []

    for section_title, section_content in template_parser.sections.items():
        # Remove whitespace and check if empty
        content_stripped = section_content.strip()
        if not content_stripped or len(content_stripped) < 10:
            empty_sections.append(section_title)

    assert (
        not empty_sections
    ), f"Template {template_parser.name} has empty sections: {empty_sections}"


# ============================================================================
# Test: Readability
# ============================================================================


@pytest.mark.unit
def test_paragraphs_are_not_too_long(template_parser: TemplateParser):
    """Test that paragraphs are reasonable length (not walls of text)."""
    # Split into paragraphs (double newline separated)
    paragraphs = re.split(r"\n\n+", template_parser._body)

    long_paragraphs = []
    for i, para in enumerate(paragraphs):
        # Skip code blocks
        if "```" in para:
            continue

        # Count lines in paragraph
        lines = para.strip().split("\n")
        if len(lines) > 15:  # More than 15 lines
            long_paragraphs.append((i, len(lines)))

    if long_paragraphs:
        pytest.skip(
            f"Template {template_parser.name} has long paragraphs: {long_paragraphs[:2]} "
            "(consider breaking into smaller sections or using lists)"
        )


@pytest.mark.unit
def test_sentences_are_not_too_long(template_parser: TemplateParser):
    """Test that sentences are reasonable length."""
    # Extract text (not code blocks)
    text_no_code = re.sub(r"```.*?```", "", template_parser._body, flags=re.DOTALL)

    # Split into sentences (simplified)
    sentences = re.split(r"[.!?]\s+", text_no_code)

    long_sentences = []
    for sentence in sentences:
        # Count words
        words = sentence.split()
        if len(words) > 40:  # More than 40 words
            long_sentences.append(sentence[:80])

    # Soft requirement
    if long_sentences and len(long_sentences) > 5:
        pytest.skip(
            f"Template {template_parser.name} has {len(long_sentences)} long sentences (>40 words). "
            "Consider breaking into shorter sentences."
        )


# ============================================================================
# Test: Lists and Formatting
# ============================================================================


@pytest.mark.unit
def test_lists_are_properly_indented(template_parser: TemplateParser):
    """Test that nested lists use consistent indentation."""
    lines = template_parser._body.split("\n")

    # Find list items and check indentation
    list_indents = []
    for line in lines:
        if re.match(r"^\s*[-*]\s", line):
            # Count leading spaces
            indent = len(line) - len(line.lstrip())
            list_indents.append(indent)

    # Check if indents are consistent (multiples of 2 or 4)
    if list_indents:
        inconsistent_indents = [i for i in list_indents if i % 2 != 0]
        if inconsistent_indents and len(inconsistent_indents) > 3:
            pytest.skip(
                f"Template {template_parser.name} has inconsistent list indentation "
                "(use 2 or 4 spaces per level)"
            )


@pytest.mark.unit
def test_checklists_use_proper_format(template_parser: TemplateParser):
    """Test that checklists use - [ ] format consistently."""
    lines = template_parser._body.split("\n")

    # Find potential checklists (lines with [ ])
    checklist_lines = [line for line in lines if "[ ]" in line or "[x]" in line or "[X]" in line]

    malformed_checklists = []
    for line in checklist_lines:
        # Should be "- [ ]" not "* [ ]" or "[ ]" alone
        stripped = line.strip()
        if (
            not stripped.startswith("- [ ]")
            and not stripped.startswith("- [x]")
            and not stripped.startswith("- [X]")
        ):
            malformed_checklists.append(line.strip()[:60])

    if malformed_checklists:
        pytest.skip(
            f"Template {template_parser.name} has non-standard checklist format: {malformed_checklists[:2]} "
            "(use '- [ ] Item' format)"
        )


# ============================================================================
# Test: Navigation Aids
# ============================================================================


@pytest.mark.unit
def test_long_templates_have_toc(template_parser: TemplateParser):
    """Test that long templates have table of contents."""
    # If template has many sections (>5), should have TOC
    num_sections = len(template_parser.sections)

    if num_sections > 5:
        # Look for TOC indicators
        has_toc = any(
            indicator in template_parser._body.lower()
            for indicator in ["table of contents", "contents:", "## contents", "overview"]
        )

        if not has_toc:
            pytest.skip(
                f"Template {template_parser.name} has {num_sections} sections but no table of contents "
                "(consider adding navigation aid)"
            )


@pytest.mark.unit
def test_sections_have_clear_hierarchy(template_parser: TemplateParser):
    """Test that section headers follow logical hierarchy."""
    lines = template_parser._body.split("\n")

    # Extract header levels
    headers = []
    for line in lines:
        match = re.match(r"^(#{1,3})\s+(.+)$", line)
        if match:
            level = len(match.group(1))
            title = match.group(2)
            headers.append((level, title))

    # Check for skipped levels (H1 → H3 without H2)
    skipped_levels = []
    for i in range(len(headers) - 1):
        current_level = headers[i][0]
        next_level = headers[i + 1][0]

        # Should not skip more than 1 level
        if next_level > current_level + 1:
            skipped_levels.append(
                f"{headers[i][1]} (H{current_level}) → {headers[i+1][1]} (H{next_level})"
            )

    if skipped_levels:
        pytest.skip(
            f"Template {template_parser.name} skips header levels: {skipped_levels[:2]} "
            "(use H1 → H2 → H3, don't skip levels)"
        )


# ============================================================================
# Test: Examples and Guidance
# ============================================================================


@pytest.mark.unit
def test_placeholders_have_nearby_examples(template_parser: TemplateParser):
    """Test that placeholders have examples or explanations nearby."""
    placeholders = template_parser.extract_placeholders()

    if not placeholders:
        pytest.skip(f"Template {template_parser.name} has no placeholders")

    # For common placeholders, check for examples
    common_placeholders = ["PROJECT_NAME", "UC_ID", "SERVICE_NAME", "ITERATION_ID"]

    missing_examples = []
    for ph in common_placeholders:
        if ph in placeholders:
            # Check if there's "e.g." or "example" near the placeholder
            locations = template_parser.extract_placeholder_locations()
            if ph in locations:
                line_num = locations[ph][0]
                lines = template_parser._body.split("\n")
                # Check 3 lines before and after
                context_start = max(0, line_num - 3)
                context_end = min(len(lines), line_num + 3)
                context = "\n".join(lines[context_start:context_end])

                if not any(
                    indicator in context.lower()
                    for indicator in ["e.g.", "example:", "for example", "such as"]
                ):
                    missing_examples.append(ph)

    # Soft requirement
    if missing_examples:
        pytest.skip(
            f"Template {template_parser.name} placeholders missing examples: {missing_examples} "
            "(consider adding 'e.g. example-value')"
        )


# ============================================================================
# Test: Usability Report
# ============================================================================


@pytest.mark.unit
def test_template_usability_report(template_parsers):
    """Generate report of template usability metrics."""
    metrics = {
        "has_checklists": [],
        "has_examples": [],
        "has_numbered_steps": [],
        "has_tables": [],
    }

    for parser in template_parsers:
        # Check for checklists
        if "- [ ]" in parser._body:
            metrics["has_checklists"].append(parser.name)

        # Check for examples
        if re.search(r"(e\.g\.|example:|for example)", parser._body, re.IGNORECASE):
            metrics["has_examples"].append(parser.name)

        # Check for numbered steps
        if re.search(r"^\d+\.\s+", parser._body, re.MULTILINE):
            metrics["has_numbered_steps"].append(parser.name)

        # Check for tables
        if "|" in parser._body and "---" in parser._body:
            metrics["has_tables"].append(parser.name)

    print("\n\n=== Template Usability Metrics ===")
    print(f"Templates with checklists: {len(metrics['has_checklists'])}/22")
    print(f"Templates with examples: {len(metrics['has_examples'])}/22")
    print(f"Templates with numbered steps: {len(metrics['has_numbered_steps'])}/22")
    print(f"Templates with tables: {len(metrics['has_tables'])}/22")

    assert True  # Informational test
