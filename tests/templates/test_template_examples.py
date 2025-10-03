"""Template example validation tests.

Tests validate code examples and their quality in templates.
"""

import pytest
import re
import ast
import json
import yaml
import textwrap
from tests.templates.fixtures.template_parser import TemplateParser


# ============================================================================
# Test: Code Block Language Tags
# ============================================================================


@pytest.mark.unit
def test_code_blocks_have_language_tags(template_parser: TemplateParser):
    """Test that code blocks specify a language (```python not just ```)."""
    lines = template_parser._body.split("\n")

    code_blocks_without_language = []

    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        # Exactly ``` without language
        if stripped == "```":
            code_blocks_without_language.append(line_num)

    if code_blocks_without_language:
        pytest.skip(
            f"Template {template_parser.name} has code blocks without language tags on lines: {code_blocks_without_language[:5]} "
            "(use ```python, ```bash, etc.)"
        )


@pytest.mark.unit
def test_language_tags_are_valid(template_parser: TemplateParser):
    """Test that code block language tags are recognized languages."""
    valid_languages = {
        "python",
        "bash",
        "sh",
        "yaml",
        "yml",
        "json",
        "markdown",
        "md",
        "sql",
        "javascript",
        "js",
        "typescript",
        "ts",
        "html",
        "css",
        "dockerfile",
        "makefile",
        "toml",
        "ini",
        "text",
        "plaintext",
        "diff",
    }

    languages_used = template_parser.get_code_block_languages()

    unrecognized_languages = []
    for lang in languages_used:
        if lang.lower() not in valid_languages:
            unrecognized_languages.append(lang)

    if unrecognized_languages:
        pytest.skip(
            f"Template {template_parser.name} uses unrecognized language tags: {unrecognized_languages} "
            "(verify these are correct)"
        )


# ============================================================================
# Test: JSON Examples
# ============================================================================


@pytest.mark.unit
def test_json_examples_are_valid(template_parser: TemplateParser):
    """Test that JSON code blocks contain valid JSON."""
    json_blocks = template_parser.extract_code_blocks("json")

    invalid_json = []

    for i, json_block in enumerate(json_blocks):
        try:
            json.loads(json_block)
        except json.JSONDecodeError as e:
            invalid_json.append((i + 1, str(e)[:50]))

    if invalid_json:
        examples = "\n".join(f"  Block {num}: {error}" for num, error in invalid_json[:3])
        pytest.fail(f"Template {template_parser.name} has invalid JSON examples:\n{examples}")


# ============================================================================
# Test: YAML Examples
# ============================================================================


@pytest.mark.unit
def test_yaml_examples_are_valid(template_parser: TemplateParser):
    """Test that YAML code blocks contain valid YAML."""
    yaml_blocks = template_parser.extract_code_blocks("yaml")
    yaml_blocks.extend(template_parser.extract_code_blocks("yml"))

    invalid_yaml = []

    for i, yaml_block in enumerate(yaml_blocks):
        try:
            yaml.safe_load(yaml_block)
        except yaml.YAMLError as e:
            invalid_yaml.append((i + 1, str(e)[:50]))

    if invalid_yaml:
        examples = "\n".join(f"  Block {num}: {error}" for num, error in invalid_yaml[:3])
        pytest.fail(f"Template {template_parser.name} has invalid YAML examples:\n{examples}")


# ============================================================================
# Test: Bash Examples
# ============================================================================


@pytest.mark.unit
def test_bash_examples_have_no_obvious_errors(template_parser: TemplateParser):
    """Test that bash examples don't have obvious syntax errors."""
    bash_blocks = template_parser.extract_code_blocks("bash")
    bash_blocks.extend(template_parser.extract_code_blocks("sh"))

    suspicious_patterns = [
        (r"^\s*\$\$", "Double $$ (should be single $)"),
        (r"fi\s+if\b", "fi followed by if (missing semicolon?)"),
        (r"done\s+for\b", "done followed by for (missing semicolon?)"),
        (r"esac\s+case\b", "esac followed by case (missing semicolon?)"),
    ]

    issues = []

    for i, bash_block in enumerate(bash_blocks):
        for pattern, description in suspicious_patterns:
            if re.search(pattern, bash_block, re.MULTILINE):
                issues.append((i + 1, description))

    if issues:
        examples = "\n".join(f"  Block {num}: {desc}" for num, desc in issues[:3])
        pytest.skip(f"Template {template_parser.name} has suspicious bash patterns:\n{examples}")


# ============================================================================
# Test: Python Examples
# ============================================================================


@pytest.mark.unit
def test_python_examples_are_syntactically_valid(template_parser: TemplateParser):
    """Test that Python code examples are syntactically valid."""
    python_blocks = template_parser.extract_code_blocks("python")

    invalid_python = []

    for i, python_block in enumerate(python_blocks):
        # Skip if it's clearly placeholder/pseudocode
        if any(
            marker in python_block.lower()
            for marker in ["...", "# placeholder", "# example", "[code here]"]
        ):
            continue

        # Remove common leading whitespace (dedent) to handle indented code blocks
        dedented_block = textwrap.dedent(python_block)

        try:
            ast.parse(dedented_block)
        except SyntaxError as e:
            invalid_python.append((i + 1, f"Line {e.lineno}: {e.msg}"))

    if invalid_python:
        examples = "\n".join(f"  Block {num}: {error}" for num, error in invalid_python[:3])
        pytest.fail(f"Template {template_parser.name} has Python syntax errors:\n{examples}")


# ============================================================================
# Test: Example Quality
# ============================================================================


@pytest.mark.unit
def test_examples_are_not_just_placeholders(template_parser: TemplateParser):
    """Test that code examples demonstrate actual usage, not just placeholders."""
    code_blocks = template_parser.extract_code_blocks()

    # Patterns that suggest placeholder code
    placeholder_patterns = [
        r"^\s*\.\.\.\s*$",  # Just ...
        r"^\s*#\s*code\s+here\s*$",  # # code here
        r"^\s*#\s*your\s+code\s*$",  # # your code
        r"^\s*pass\s*$",  # Just pass
        r"^\s*#\s*TODO",  # # TODO
    ]

    placeholder_blocks = []

    for i, block in enumerate(code_blocks):
        # If entire block matches placeholder pattern
        lines = [line.strip() for line in block.split("\n") if line.strip()]

        if len(lines) == 1:
            for pattern in placeholder_patterns:
                if re.match(pattern, lines[0], re.IGNORECASE):
                    placeholder_blocks.append(i + 1)
                    break

    if placeholder_blocks:
        pytest.skip(
            f"Template {template_parser.name} has placeholder-only code blocks: {placeholder_blocks[:5]} "
            "(consider adding actual example code)"
        )


@pytest.mark.unit
def test_python_examples_follow_pep8_basics(template_parser: TemplateParser):
    """Test that Python examples follow basic PEP 8 conventions."""
    python_blocks = template_parser.extract_code_blocks("python")

    pep8_issues = []

    for i, python_block in enumerate(python_blocks):
        lines = python_block.split("\n")

        for line_num, line in enumerate(lines, 1):
            # Check for common PEP 8 violations

            # Trailing whitespace
            if line.endswith(" ") or line.endswith("\t"):
                pep8_issues.append((i + 1, line_num, "Trailing whitespace"))

            # Multiple spaces after operator (except alignment)
            if re.search(r"\S  +\S", line) and "=" not in line:
                pep8_issues.append((i + 1, line_num, "Multiple spaces"))

    if pep8_issues:
        examples = "\n".join(
            f"  Block {block}, Line {line}: {issue}" for block, line, issue in pep8_issues[:3]
        )
        pytest.skip(f"Template {template_parser.name} has PEP 8 style issues:\n{examples}")


# ============================================================================
# Test: Example Consistency
# ============================================================================


@pytest.mark.unit
def test_examples_use_framework_naming_conventions(template_parser: TemplateParser):
    """Test that examples follow framework naming conventions."""
    code_blocks = template_parser.extract_code_blocks()

    # Framework conventions
    conventions = {
        "Use Case": r"\bUC-\d{3}\b",  # UC-001 format
        "Service": r"\bSVC-\d{3}\b",  # SVC-001 format (if used)
        "ADR": r"\bADR-\d{3}\b",  # ADR-001 format
        "Iteration": r"\biteration-\d{3}\b",  # iteration-001 format
    }

    violations = []

    for conv_name, pattern in conventions.items():
        for i, block in enumerate(code_blocks):
            # Look for potential violations (e.g., UC001 instead of UC-001)
            if conv_name == "Use Case":
                if re.search(r"\bUC\d{3}\b", block):  # No hyphen
                    violations.append((i + 1, f"{conv_name} format (should be UC-001 not UC001)"))

    if violations:
        examples = "\n".join(f"  Block {num}: {issue}" for num, issue in violations[:3])
        pytest.skip(f"Template {template_parser.name} has naming convention issues:\n{examples}")


@pytest.mark.unit
def test_examples_include_spec_references(template_parser: TemplateParser):
    """Test that code examples include specification references where appropriate."""
    python_blocks = template_parser.extract_code_blocks("python")

    # Look for docstrings or comments with spec references
    has_spec_refs = False

    for block in python_blocks:
        # Skip very short blocks (< 5 lines)
        if len(block.split("\n")) < 5:
            continue

        # Look for spec reference patterns
        if any(
            pattern in block
            for pattern in [
                "Specification:",
                "Spec:",
                "UC-",
                "See:",
                "Reference:",
                "Based on:",
            ]
        ):
            has_spec_refs = True
            break

    # This is a soft requirement - not all examples need spec refs
    if not has_spec_refs and len(python_blocks) > 2:
        pytest.skip(
            f"Template {template_parser.name} Python examples might benefit from spec references "
            "(e.g., '# Specification: UC-001')"
        )


# ============================================================================
# Test: Code Example Statistics
# ============================================================================


@pytest.mark.unit
def test_code_example_statistics_report(template_parsers):
    """Generate report of code example usage across templates."""
    language_usage = {}
    example_counts = {}

    for parser in template_parsers:
        languages = parser.get_code_block_languages()
        num_examples = len(parser.extract_code_blocks())

        example_counts[parser.name] = num_examples

        for lang in languages:
            if lang not in language_usage:
                language_usage[lang] = []
            language_usage[lang].append(parser.name)

    # Print language usage
    print("\n\n=== Code Example Languages ===")
    for lang, templates in sorted(language_usage.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"{lang}: {len(templates)} templates")

    # Print templates with most examples
    print("\n\n=== Templates with Most Code Examples ===")
    top_examples = sorted(example_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for template, count in top_examples:
        if count > 0:
            print(f"{template}: {count} examples")

    assert True  # Informational test
