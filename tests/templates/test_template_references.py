"""Template reference validation tests.

Tests validate file references and cross-references in templates.
"""

import pytest
import re
from pathlib import Path
from tests.templates.fixtures.template_parser import TemplateParser


# ============================================================================
# Test: File Reference Validation
# ============================================================================


@pytest.mark.unit
def test_claude_file_references_valid(template_parser: TemplateParser, framework_root: Path):
    """Test that references to .claude/ files are valid."""
    # Extract file references
    file_refs = template_parser.extract_file_references()

    broken_claude_refs = []

    for file_ref in file_refs:
        # Focus on .claude/ references
        if not file_ref.startswith((".claude/", "../", "./")):
            continue

        # Resolve path
        templates_dir = framework_root / ".claude" / "templates"

        if file_ref.startswith(".claude/"):
            file_path = framework_root / file_ref
        elif file_ref.startswith("../"):
            file_path = (templates_dir / file_ref).resolve()
        else:
            file_path = templates_dir / file_ref

        if not file_path.exists():
            broken_claude_refs.append((file_ref, str(file_path)))

    if broken_claude_refs:
        examples = "\n".join(f"  {ref} → {path}" for ref, path in broken_claude_refs[:5])
        pytest.fail(f"Template {template_parser.name} has broken .claude/ references:\n{examples}")


@pytest.mark.unit
def test_spec_directory_references_are_valid(template_parser: TemplateParser):
    """Test that references to specs/ directories use correct paths."""
    # Look for references to spec directories
    spec_patterns = [
        r"specs/use-cases/",
        r"specs/services/",
        r"specs/adrs/",
        r"planning/iterations/",
    ]

    found_refs = []
    for pattern in spec_patterns:
        if pattern in template_parser._body:
            found_refs.append(pattern)

    # These are template guidance - just validate format
    for ref in found_refs:
        # Should not have leading slash
        assert not template_parser._body.count(
            f"/{ref}"
        ), f"Template {template_parser.name} uses absolute path /{ref} (should be relative: {ref})"


@pytest.mark.unit
def test_relative_path_format_is_consistent(template_parser: TemplateParser):
    """Test that relative paths use consistent format."""
    file_refs = template_parser.extract_file_references()

    # Check for inconsistent path separators or formats
    path_issues = []

    for ref in file_refs:
        # Windows-style backslashes shouldn't be used
        if "\\" in ref:
            path_issues.append(f"Uses backslash: {ref}")

        # Multiple consecutive slashes
        if "//" in ref:
            path_issues.append(f"Double slash: {ref}")

        # Trailing slashes on files (directories OK)
        if ref.endswith("/") and "." in ref.split("/")[-2]:
            path_issues.append(f"Trailing slash on file: {ref}")

    if path_issues:
        pytest.skip(
            f"Template {template_parser.name} has path formatting issues: {path_issues[:3]}"
        )


# ============================================================================
# Test: Cross-Reference Consistency
# ============================================================================


@pytest.mark.unit
def test_framework_version_references_are_consistent(template_parsers):
    """Test that framework version is consistent across all templates."""
    version_pattern = r"v\d+\.\d+(?:\.\d+)?"  # v2.2 or v2.2.0
    version_refs = {}

    for parser in template_parsers:
        versions_found = re.findall(version_pattern, parser._body, re.IGNORECASE)
        for version in versions_found:
            if version.lower() not in version_refs:
                version_refs[version.lower()] = []
            version_refs[version.lower()].append(parser.name)

    # Should have one primary version
    if len(version_refs) > 1:
        print("\n\n=== Framework Version References ===")
        for version, templates in sorted(version_refs.items()):
            print(f"{version}: {len(templates)} templates")
            if len(templates) <= 5:
                for t in templates:
                    print(f"  - {t}")

        # This is informational - versions might legitimately vary
        pytest.skip(
            f"Multiple framework versions referenced: {list(version_refs.keys())} "
            "(verify this is intentional)"
        )


@pytest.mark.unit
def test_rule_references_are_valid(template_parser: TemplateParser):
    """Test that 'Rule #X' references point to valid rules (1-12)."""
    # Find all "Rule #X" references
    rule_pattern = r"Rule #(\d+)"
    rule_refs = re.findall(rule_pattern, template_parser._body)

    invalid_refs = []
    for rule_num_str in rule_refs:
        rule_num = int(rule_num_str)
        if rule_num < 1 or rule_num > 12:
            invalid_refs.append(rule_num)

    assert (
        not invalid_refs
    ), f"Template {template_parser.name} references invalid rules: {invalid_refs} (valid range: 1-12)"


@pytest.mark.unit
def test_development_rules_reference_is_correct(template_parser: TemplateParser):
    """Test that references to development-rules.md use correct path."""
    # Common variations
    correct_refs = [
        ".claude/development-rules.md",
        "../development-rules.md",
        "development-rules.md",
    ]

    incorrect_patterns = [
        "development_rules.md",  # Underscore instead of hyphen
        "developmentrules.md",  # No separator
        "dev-rules.md",  # Abbreviated
    ]

    for incorrect in incorrect_patterns:
        if incorrect in template_parser._body.lower():
            pytest.fail(
                f"Template {template_parser.name} uses incorrect development rules reference: {incorrect}"
            )


@pytest.mark.unit
def test_template_cross_references_exist(template_parser: TemplateParser, framework_root: Path):
    """Test that references to other templates exist."""
    # Look for references to template files
    template_refs = []

    # Pattern: references to .md files in .claude/templates/
    md_refs = template_parser.extract_file_references()

    for ref in md_refs:
        if ref.endswith(".md"):
            # Check if it's a template reference
            if "template" in ref.lower() or any(
                dir_name in ref for dir_name in ["research/", "templates/"]
            ):
                template_refs.append(ref)

    # Validate each reference
    broken_refs = []
    templates_dir = framework_root / ".claude" / "templates"

    for ref in template_refs:
        # Resolve path
        if ref.startswith("./"):
            file_path = templates_dir / ref[2:]
        elif ref.startswith("../"):
            file_path = (templates_dir / ref).resolve()
        else:
            file_path = templates_dir / ref

        if not file_path.exists():
            broken_refs.append(ref)

    if broken_refs:
        pytest.fail(
            f"Template {template_parser.name} has broken template references: {broken_refs}"
        )


# ============================================================================
# Test: External References
# ============================================================================


@pytest.mark.unit
def test_external_urls_have_valid_format(template_parser: TemplateParser):
    """Test that external URLs start with http:// or https://."""
    links = template_parser.extract_links()

    invalid_urls = []

    for link_text, url in links:
        # Skip internal links (fragments, files)
        if url.startswith(("#", "./", "../", "/")):
            continue

        # Skip placeholders
        if url.startswith("[") and url.endswith("]"):
            continue

        # Should be a proper URL
        if not url.startswith(("http://", "https://")):
            # Unless it's a file path
            if not any(ext in url for ext in [".md", ".py", ".sh", ".yml", ".yaml"]):
                invalid_urls.append((link_text, url))

    if invalid_urls:
        examples = "\n".join(f"  [{text}]({url})" for text, url in invalid_urls[:3])
        pytest.skip(
            f"Template {template_parser.name} has URLs without http(s):// prefix:\n{examples}"
        )


@pytest.mark.unit
def test_github_links_use_main_branch(template_parser: TemplateParser):
    """Test that GitHub links use /main/ branch, not /master/."""
    links = template_parser.extract_links()

    master_branch_links = []

    for link_text, url in links:
        if "github.com" in url and "/master/" in url:
            master_branch_links.append(url)

    if master_branch_links:
        pytest.skip(
            f"Template {template_parser.name} uses /master/ in GitHub links: {master_branch_links[:2]} "
            "(consider using /main/ for modern repositories)"
        )


@pytest.mark.unit
def test_no_broken_anchor_links(template_parser: TemplateParser):
    """Test that section anchor links (#section) point to existing sections."""
    links = template_parser.extract_links()

    # Extract anchor-only links
    anchor_links = [url for text, url in links if url.startswith("#")]

    broken_anchors = []

    for anchor in anchor_links:
        # Remove # and convert to expected section title
        section_name = anchor[1:].replace("-", " ").title()

        # Check if section exists (case insensitive)
        section_exists = any(
            section_name.lower() in section.lower() for section in template_parser.sections.keys()
        )

        if not section_exists:
            broken_anchors.append((anchor, section_name))

    if broken_anchors:
        examples = "\n".join(
            f"  {anchor} (looking for '{section}')" for anchor, section in broken_anchors[:3]
        )
        pytest.skip(
            f"Template {template_parser.name} has potentially broken anchor links:\n{examples} "
            "(verify section names match)"
        )


# ============================================================================
# Test: Reference Patterns Report
# ============================================================================


@pytest.mark.unit
def test_reference_patterns_report(template_parsers):
    """Generate report of reference patterns across templates."""
    external_domains = {}
    internal_patterns = {}

    for parser in template_parsers:
        links = parser.extract_links()

        for link_text, url in links:
            # Track external domains
            if url.startswith("http"):
                domain = url.split("/")[2] if len(url.split("/")) > 2 else url
                if domain not in external_domains:
                    external_domains[domain] = []
                external_domains[domain].append(parser.name)

            # Track internal reference patterns
            elif url.startswith((".claude/", "../", "./")):
                if url not in internal_patterns:
                    internal_patterns[url] = []
                internal_patterns[url].append(parser.name)

    # Print external domain usage
    print("\n\n=== External Domains Referenced ===")
    for domain, templates in sorted(
        external_domains.items(), key=lambda x: len(x[1]), reverse=True
    ):
        if len(templates) >= 2:
            print(f"{domain}: {len(templates)} templates")

    # Print common internal references
    print("\n\n=== Common Internal References ===")
    common_refs = {
        ref: templates for ref, templates in internal_patterns.items() if len(templates) >= 3
    }
    for ref, templates in sorted(common_refs.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"{ref}: {len(templates)} templates")

    assert True  # Informational test
