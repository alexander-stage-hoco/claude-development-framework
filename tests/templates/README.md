# Template Validation Test Suite

Comprehensive automated testing suite for Claude Development Framework templates.

## Overview

This test suite validates **22 templates** across **6 validation dimensions**:

1. **Metadata & Structure** - YAML frontmatter, markdown formatting, section organization
2. **Content Quality** - Placeholders, references, code examples validity
3. **Usability** - Readability, actionable language, navigation aids
4. **Instantiation** - Template replacement logic and output quality
5. **Completeness** - Framework coverage, workflow chains, cross-references
6. **Project Templates** - init-project.sh validation and structure creation

**Total Tests**: ~1,487 comprehensive validation tests
**Runtime**: <3 seconds for full suite
**Coverage**: All 22 templates × 70+ test dimensions per template

---

## Quick Start

### Run All Template Tests

```bash
pytest tests/templates/ -v
```

### Run Specific Test Phase

```bash
# Metadata validation
pytest tests/templates/test_template_metadata.py -v

# Structure validation
pytest tests/templates/test_template_structure.py -v

# Content validation
pytest tests/templates/test_template_placeholders.py -v
pytest tests/templates/test_template_references.py -v
pytest tests/templates/test_template_examples.py -v

# Usability validation
pytest tests/templates/test_template_usability.py -v
pytest tests/templates/test_template_instantiation.py -v

# Completeness validation
pytest tests/templates/test_template_completeness.py -v

# Project template validation
pytest tests/templates/test_project_template_validation.py -v
```

### Run Tests for Specific Template

```bash
pytest tests/templates/ -v -k "CLAUDE"
pytest tests/templates/ -v -k "use-case-template"
```

---

## Test Architecture

### TemplateParser Infrastructure

Core parsing class that extracts template components for validation:

```python
from tests.templates.fixtures.template_parser import TemplateParser

parser = TemplateParser(Path(".claude/templates/CLAUDE.md"))

# Extract metadata
tier = parser.get_metadata_field("tier")  # → 1
purpose = parser.get_metadata_field("purpose")  # → "Session protocols..."

# Extract structure
sections = parser.sections  # → {"Session Protocol": "content...", ...}
h1_title = parser.get_h1_title()  # → "MANDATORY: Read This First..."

# Extract content
placeholders = parser.extract_placeholders()  # → ["PROJECT_NAME", "DATE", ...]
code_blocks = parser.extract_code_blocks("python")  # → ["code...", ...]
links = parser.extract_links()  # → [("text", "url"), ...]
```

### Pytest Parametrization

Single test function validates **all 22 templates** via parametrization:

```python
@pytest.mark.unit
def test_template_has_tier(template_parser: TemplateParser):
    """Test that template has tier metadata."""
    tier = template_parser.get_metadata_field("tier")
    assert tier in [1, 2, 3, 4]
```

This test runs 22 times (once per template), reporting per-template results.

---

## Validation Phases

### Phase 1-2: Metadata & Structure (399 tests)

**Files**: `test_template_metadata.py`, `test_template_structure.py`

**Validates**:
- YAML frontmatter presence and required fields (tier, purpose, reload_trigger)
- Tier value validity (1-4) and distribution
- Markdown structure (H1 count, H2 sections, no H4+)
- Code block closure, bracket balance, table formatting
- File size reasonableness (<100KB)

**Example Tests**:
```python
test_all_templates_have_yaml_frontmatter()
test_tier_value_is_valid()
test_template_has_exactly_one_h1_title()
test_code_blocks_are_closed()
test_no_broken_internal_links()
```

---

### Phase 3: Content Validation (599 tests)

**Files**: `test_template_placeholders.py`, `test_template_references.py`, `test_template_examples.py`

**Validates**:
- **Placeholders**: Format ([UPPERCASE_WITH_UNDERSCORES]), descriptiveness, no TODOs/FIXMEs
- **References**: .claude/ file validity, Rule #1-12 references, external URL formats
- **Code Examples**: Language tags, JSON/YAML/Python syntax, no placeholder-only blocks

**Example Tests**:
```python
test_placeholders_use_correct_format()
test_no_todo_markers_in_templates()
test_claude_file_references_valid()
test_python_examples_are_syntactically_valid()
test_json_examples_are_valid()
```

**Code Validation Features**:
- **Python**: AST parsing with `textwrap.dedent()` for indented blocks
- **JSON**: `json.loads()` validation
- **YAML**: `yaml.safe_load()` validation
- **Bash**: Regex pattern matching for common errors

---

### Phase 4: Usability & Instantiation (464 tests)

**Files**: `test_template_usability.py`, `test_template_instantiation.py`

**Validates**:
- **Usability**: Action verbs in checklists, imperative mood, readability, navigation
- **Instantiation**: Placeholder replacement, markdown validity after substitution

**Example Tests**:
```python
test_checklist_items_are_actionable()
test_instructions_use_imperative_mood()
test_paragraphs_are_not_too_long()
test_placeholders_can_be_replaced()
test_instantiated_template_is_valid_markdown()
```

---

### Phase 5-6: Completeness & Project Templates (25 tests)

**Files**: `test_template_completeness.py`, `test_project_template_validation.py`

**Validates**:
- **Completeness**: Template category coverage, workflow chains, 12-rule alignment
- **Project Templates**: init-project.sh syntax, structure creation, template copying

**Example Tests**:
```python
test_all_template_categories_represented()
test_session_workflow_is_complete()
test_templates_align_with_12_rules()
test_init_project_script_syntax_is_valid()
test_init_project_creates_required_structure()
```

---

## Interpreting Results

### Test Status Types

**PASSED** ✅ - Template meets validation criteria
**FAILED** ❌ - Template has real quality issue (fix template)
**SKIPPED** ⚠️ - Soft requirement or informational warning

### Common Failures and Fixes

#### Missing YAML Frontmatter

```
FAILED test_all_templates_have_yaml_frontmatter[my-template]
```

**Fix**: Add frontmatter to template:
```yaml
---
tier: 2
purpose: Brief description of template purpose
reload_trigger: When this template should be reloaded
estimated_read_time: 5 minutes
---
```

#### Invalid Tier Value

```
FAILED test_tier_value_is_valid[my-template]
AssertionError: Template my-template has invalid tier value: 5 (must be 1, 2, 3, or 4)
```

**Fix**: Set tier to 1 (essential), 2 (common), 3 (situational), or 4 (rare).

#### Multiple H1 Headers

```
FAILED test_template_has_exactly_one_h1_title[my-template]
AssertionError: Template my-template should have exactly 1 H1 title, found 2
```

**Fix**: Use only one `# Title` (H1). Use `## Section` (H2) for sections.

#### Unclosed Code Blocks

```
FAILED test_code_blocks_are_closed[my-template]
AssertionError: Template my-template has unclosed code block (odd number of ``` fences: 3)
```

**Fix**: Ensure every ` ``` ` opening has a matching ` ``` ` closing.

#### Broken Internal Links

```
FAILED test_no_broken_internal_links[my-template]
AssertionError: Template my-template has broken internal links:
  - ../nonexistent.md → /path/to/nonexistent.md
```

**Fix**: Update link to point to existing file or remove broken link.

#### Invalid Python Syntax

```
FAILED test_python_examples_are_syntactically_valid[my-template]
AssertionError: Template my-template has Python syntax errors:
  Block 1: Line 5: invalid syntax
```

**Fix**: Correct Python code example or add `# placeholder` marker to skip validation.

---

## Adding New Tests

### Test a New Template

1. Add template to `.claude/templates/` or `.claude/templates/research/`
2. Run test suite - it will automatically be picked up
3. Fix any validation failures

### Add New Validation Rule

**Example**: Validate that templates mention "Claude Code"

```python
# tests/templates/test_template_branding.py

import pytest
from tests.templates.fixtures.template_parser import TemplateParser


@pytest.mark.unit
def test_templates_mention_framework_name(template_parser: TemplateParser):
    """Test that templates mention Claude Development Framework."""
    # Core templates should mention the framework
    if template_parser.get_metadata_field("tier") == 1:
        assert "claude development framework" in template_parser._body.lower(), (
            f"Tier 1 template {template_parser.name} should mention framework name"
        )
```

This test will automatically run against all 22 templates.

---

## Performance

### Test Execution Speed

```
Phase 1-2 (Metadata/Structure): ~0.1s for 399 tests
Phase 3 (Content): ~1.0s for 599 tests
Phase 4 (Usability): ~0.5s for 464 tests
Phase 5-6 (Completeness): ~0.5s for 25 tests

Total Runtime: ~2.5s for 1,487 tests
```

### Optimization Techniques

1. **Session-scoped fixtures** - Parse each template once
2. **Pure parsing** - No I/O after initial file read
3. **Skip expensive tests** - Mark integration tests with `@pytest.mark.slow`
4. **Parametrization** - Reuse test logic across templates

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Template Validation

on: [push, pull_request]

jobs:
  validate-templates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest pyyaml

      - name: Run template validation tests
        run: pytest tests/templates/ -v --tb=short

      - name: Generate template quality report
        if: always()
        run: pytest tests/templates/ -v --tb=no -q > template-report.txt

      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: template-quality-report
          path: template-report.txt
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: validate-templates
        name: Validate Templates
        entry: pytest tests/templates/ -v --tb=short
        language: system
        pass_filenames: false
        files: \\.claude/templates/.*\\.md$
```

---

## Template Quality Metrics

### Coverage Report

Run `test_template_coverage_report` to see:

- Templates by tier distribution
- Templates by category (core, research, workflow, etc.)
- Development phase coverage (planning, implementation, quality, etc.)
- Total template count and completeness percentage

### Gap Analysis

Run `test_template_gaps_analysis` to identify:

- Missing template categories
- Unsupported development phases
- Workflows without complete template chains
- Potential new template opportunities

---

## Best Practices

### Writing Template-Friendly Content

✅ **DO**:
- Use YAML frontmatter with required fields
- Use one H1 (`#`), multiple H2 (`##`), avoid H4+ (`####`)
- Use `[UPPERCASE_PLACEHOLDER]` format for placeholders
- Provide format hints for placeholders (e.g., `[DATE] (YYYY-MM-DD)`)
- Include valid code examples with language tags (` ```python `)
- Reference other templates with relative paths (`.claude/templates/file.md`)
- Use action verbs in checklists ("Read", "Write", "Create")
- Include examples near placeholders ("e.g. my-project")

❌ **DON'T**:
- Use TODO, FIXME, XXX markers (use `[TODO]` placeholder instead)
- Use [TBD] or "to be determined" (use specific placeholders)
- Skip language tags on code blocks (` ``` ` → ` ```python `)
- Use multiple H1 headers (only one per template)
- Reference non-existent files in links
- Use placeholder-only code examples (add real code)
- Write walls of text (break into sections and lists)

### Testing Custom Templates

```bash
# Test your new template during development
pytest tests/templates/ -v -k "my-new-template"

# Check specific validation phase
pytest tests/templates/test_template_structure.py -v -k "my-new-template"

# Generate quality report for your template
pytest tests/templates/ -v -k "my-new-template" --tb=no
```

---

## Troubleshooting

### Tests Fail for Your Template

1. **Read the assertion message** - it tells you exactly what's wrong
2. **Check similar passing templates** - see how they solve the issue
3. **Run specific test** - isolate the failing validation
4. **Check test code** - understand what's being validated

### Template Not Detected

**Problem**: New template not showing up in tests

**Solution**:
- Ensure template is in `.claude/templates/` or `.claude/templates/research/`
- Check filename ends with `.md`
- Verify frontmatter is present
- Run `pytest --collect-only tests/templates/` to see detected templates

### False Positives

**Problem**: Test fails but template is correct

**Solution**:
- Some tests use `pytest.skip()` for soft requirements (warnings)
- If test uses `assert` and template is correct, file an issue
- Tests may need adjustment for valid edge cases

---

## Maintenance

### Updating Test Suite

When adding new templates:
1. Add template file to appropriate directory
2. Run full test suite
3. Fix any failures (usually metadata issues)
4. Template automatically included in future runs

When changing test logic:
1. Update relevant test file (e.g., `test_template_structure.py`)
2. Run affected tests: `pytest tests/templates/test_template_structure.py -v`
3. Verify no regressions across all templates
4. Update this README if behavior changes

### Maintaining 100% Passing Rate

**Goal**: All templates pass all tests (failures indicate real quality issues)

**Process**:
1. CI runs tests on every commit
2. Fix template quality issues immediately
3. Only skip tests for soft requirements (warnings)
4. Never weaken tests to make them pass

---

## Statistics

### Test Distribution

| Phase | Files | Tests | Focus Area |
|-------|-------|-------|------------|
| Phase 1-2 | 2 | 399 | Metadata & Structure |
| Phase 3 | 3 | 599 | Content (placeholders, refs, examples) |
| Phase 4 | 2 | 464 | Usability & Instantiation |
| Phase 5-6 | 2 | 25 | Completeness & Project Templates |
| **Total** | **9** | **~1,487** | **Comprehensive Validation** |

### Template Coverage

- **22 templates** validated
- **70+ validation dimensions** per template
- **~67 tests per template** (average)
- **<3 second runtime** for full suite
- **6 validation categories** (metadata, structure, content, usability, completeness, project)

---

## Related Documentation

- **Agent Test Suite**: `tests/agents/README.md` - Similar test suite for agent validation
- **Development Rules**: `.claude/development-rules.md` - Framework's 12 non-negotiable rules
- **CLAUDE Template**: `.claude/templates/CLAUDE.md` - Session start template
- **Init Script**: `init-project.sh` - Project initialization script

---

## Version History

**v2.2** (2025-10-03):
- Initial Template Validation Test Suite release
- 1,487 comprehensive validation tests
- 6 validation phases (metadata, structure, content, usability, completeness, project)
- Full coverage across 22 templates
- <3 second runtime for entire suite
- Inspired by Agent Test Suite success (791/794 tests passing)

**Philosophy**: Just as agent tests ensure agent quality, template tests ensure template quality. Together they form the framework's quality assurance backbone.

---

**Framework**: Claude Development Framework v2.2
**Test Suite Version**: 1.0
**Last Updated**: 2025-10-03
**Maintainer**: Framework Quality Team
