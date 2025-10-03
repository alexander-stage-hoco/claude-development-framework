---
tier: 3
purpose: Before writing new code
reload_trigger: Before implementing new capability
estimated_read_time: 5 minutes
---

# Code Reuse Checklist

**Version**: 2.0
**Purpose**: Protocol for safely reusing code from reference implementations
**Part of**: Implementation Analysis Workflow

---

## Overview

This checklist ensures code reused from reference implementations is:
- ✅ Legally compliant (license)
- ✅ Quality-verified (meets our standards)
- ✅ Properly adapted (fits our architecture)
- ✅ Fully tested (no blind copying)
- ✅ Properly attributed (if required)

**Key Principle**: Adapt, don't copy. Understand, don't paste.

---

## Phase 1: Pre-Reuse Assessment

### Legal / License Check
- [ ] **License identified**: What license does the source code use?
- [ ] **License compatible**: Compatible with our project license?
- [ ] **Attribution required**: Do we need to credit the source?
- [ ] **Share-alike clause**: Does license require us to open-source our code?
- [ ] **Commercial use allowed**: Can we use this commercially?

**If any checkbox fails**: DO NOT reuse this code. Find alternative.

**License Quick Reference**:
| License | Attribution | Share-Alike | Commercial | Copy-Friendly |
|---------|-------------|-------------|------------|---------------|
| MIT | Suggested | No | Yes | ✅ Yes |
| Apache 2.0 | Required | No | Yes | ✅ Yes |
| BSD | Suggested | No | Yes | ✅ Yes |
| GPL v3 | Required | Yes | Yes | ⚠️ Requires open-source |
| LGPL | Required | Partial | Yes | ⚠️ Complex |
| Proprietary | Varies | Varies | Maybe | ❌ Usually no |

---

### Code Quality Check
- [ ] **Meets our standards**: Code follows our quality bar?
- [ ] **Type safety**: Has type hints (Python) / types (TypeScript)?
- [ ] **Documentation**: Code is documented (docstrings, comments)?
- [ ] **Error handling**: Proper exception handling present?
- [ ] **No security issues**: No obvious vulnerabilities?
- [ ] **No deprecated code**: Uses current APIs and patterns?
- [ ] **Dependencies acceptable**: Dependencies are maintained and secure?

**If quality is poor**: Rewrite from scratch using their approach as inspiration, don't copy code.

---

### Fit Assessment
- [ ] **Solves our problem**: Actually addresses our use case?
- [ ] **Fits our architecture**: Compatible with our design patterns?
- [ ] **Reasonable complexity**: Not over-complicated for our needs?
- [ ] **Maintainable**: We can understand and maintain this code?
- [ ] **Adaptation effort justified**: Adaptation time < rewrite time?

**If fit is poor**: Use as learning reference, don't reuse code directly.

---

## Phase 2: Extraction

### Isolate the Code
1. **Create staging area**:
   ```bash
   mkdir -p implementation/src/staging/[component-name]/
   ```

2. **Copy relevant code**:
   - Copy only the specific function/class/module needed
   - Include dependencies if minimal
   - Do NOT copy entire files if only need one function

3. **Note source location**:
   ```markdown
   Extracted from: research/implementations/[project]/[file]:lines X-Y
   Original project: [URL]
   License: [Type]
   Date extracted: [Date]
   ```

---

## Phase 3: Adaptation

### Adapt to Our Architecture

**Follow these steps**:

#### 1. Rename for Clarity
- [ ] Rename variables to match our naming conventions
- [ ] Rename functions to match our verb-noun pattern
- [ ] Rename classes to match our domain model

#### 2. Add Type Hints
- [ ] Add/improve parameter type hints
- [ ] Add/improve return type hints
- [ ] Add type hints for complex data structures
- [ ] Run type checker (mypy/pyright)

#### 3. Improve Documentation
- [ ] Add comprehensive docstring
- [ ] Reference our specification
- [ ] Note source and adaptation
- [ ] Document assumptions and limitations

**Docstring Template**:
```python
def extracted_function(param: Type) -> ReturnType:
    """
    [What this function does in our context]

    Specification: UC-XXX#[section] / SVC-XXX#[section]
    Adapted from: [Project Name] ([URL])
    License: [License Type]

    Original implementation: research/implementations/[project]/summary.md
    Modifications:
    - [Change 1]
    - [Change 2]

    Args:
        param: [Description in our context]

    Returns:
        [Description of return value]

    Raises:
        [Exceptions that can be raised]

    Example:
        >>> extracted_function(value)
        expected_result
    """
```

#### 4. Integrate with Our Patterns
- [ ] Use our error handling patterns
- [ ] Use our logging patterns
- [ ] Use our dependency injection (if applicable)
- [ ] Follow our code organization

#### 5. Remove Unnecessary Code
- [ ] Remove features we don't need
- [ ] Remove excessive abstraction
- [ ] Simplify if possible (without losing correctness)

---

### Security Review
- [ ] **Input validation**: All inputs validated?
- [ ] **SQL injection**: No SQL injection vulnerabilities?
- [ ] **XSS prevention**: Output properly escaped?
- [ ] **Authentication**: Auth checks in place?
- [ ] **Authorization**: Permission checks in place?
- [ ] **Secrets management**: No hardcoded secrets?
- [ ] **Dependency vulnerabilities**: Dependencies scanned?

---

## Phase 4: Testing (CRITICAL)

### Write Tests BEFORE Integration

**Remember**: Test-first applies to reused code too!

#### 1. Write Unit Tests
- [ ] Test happy path
- [ ] Test error cases
- [ ] Test edge cases
- [ ] Test with our actual data types
- [ ] Achieve ≥90% coverage for adapted code

```python
def test_adapted_function_happy_path():
    """Test adapted function with valid input."""
    # Adapted from: [source], but tests are ours
    result = adapted_function(valid_input)
    assert result == expected_output

def test_adapted_function_error_handling():
    """Test adapted function handles errors properly."""
    with pytest.raises(ExpectedException):
        adapted_function(invalid_input)
```

#### 2. Integration Tests
- [ ] Test with our other components
- [ ] Test with our database (if applicable)
- [ ] Test with our API (if applicable)

#### 3. Run All Tests
- [ ] New tests pass
- [ ] ALL existing tests still pass
- [ ] No regressions introduced

**Only proceed if all tests pass.**

---

## Phase 5: Attribution (If Required)

### Add Attribution

**If license requires attribution**:

#### 1. In Source Code
Add comment block at top of file or before function:

```python
# Portions of this code adapted from [Project Name]
# Original source: [URL]
# License: [License Type]
# Copyright (c) [Year] [Original Author]
# Modifications by [Your Team/Name], [Year]
#
# [License text or reference to LICENSE file]
```

#### 2. In LICENSE File (if required by license)
Add attribution to project LICENSE file

#### 3. In Documentation
Add to `research/implementations/[project]/attribution.md`:
```markdown
# Attribution for [Component]

**Used in**: implementation/src/[location]
**Original**: [Project URL]
**License**: [License Type]
**Date Reused**: [Date]
**Attribution Added**: [Where in our codebase]
```

---

## Phase 6: Integration

### Move to Production Location

1. **Move from staging**:
   ```bash
   mv implementation/src/staging/[component]/ implementation/src/[proper-location]/
   ```

2. **Import and use**:
   - Import in relevant modules
   - Use in implementation
   - Ensure all tests still pass

3. **Update documentation**:
   - Add to `README.md` if significant component
   - Update architecture docs if applicable

---

## Phase 7: Final Verification

### Complete Checklist
- [ ] **License compliance verified**: Legal to use
- [ ] **Quality verified**: Meets our standards
- [ ] **Adapted properly**: Fits our architecture
- [ ] **Fully tested**: ≥90% coverage, all tests pass
- [ ] **Attributed properly**: Attribution added if required
- [ ] **Documented**: Docstrings and references complete
- [ ] **Specification aligned**: References our UC/SVC specs
- [ ] **No regressions**: All existing tests pass
- [ ] **Code reviewed**: Another team member reviewed

**Only commit if ALL checkboxes are checked.**

---

## Common Mistakes to Avoid

### ❌ Blind Copy-Paste
**Don't**: Copy entire files without understanding
**Do**: Extract specific functions, understand them, adapt them

### ❌ Skip Testing
**Don't**: Assume reused code works
**Do**: Write comprehensive tests for adapted code

### ❌ Ignore License
**Don't**: Copy without checking license
**Do**: Verify license compatibility FIRST

### ❌ Keep Unnecessary Code
**Don't**: Keep features/complexity you don't need
**Do**: Simplify to bare minimum for your use case

### ❌ No Documentation
**Don't**: Forget to document source and adaptations
**Do**: Comprehensive docstrings with source references

### ❌ Violate Our Patterns
**Don't**: Keep their error handling/logging/patterns
**Do**: Adapt to match our project patterns

---

## Emergency: Code Reuse Failed

**If reuse attempt fails** (tests fail, doesn't fit, too complex):

1. **Stop immediately**: Don't force it
2. **Options**:
   - Rewrite from scratch using their approach as inspiration
   - Find simpler reference implementation
   - Build custom solution

3. **Document lessons**: Update implementation summary with:
   ```markdown
   ## Reuse Attempt Failed

   **Date**: [Date]
   **Reason**: [Why reuse didn't work]
   **Lessons**: [What we learned]
   **Alternative Taken**: [What we did instead]
   ```

---

## Success Criteria

Code reuse succeeds if:
- ✅ All legal requirements met
- ✅ Code quality matches our standards
- ✅ Fully tested (≥90% coverage)
- ✅ All tests pass (new and existing)
- ✅ Properly documented and attributed
- ✅ Team understands the code
- ✅ Maintainable going forward

---

## Quick Decision Tree

```
Can we legally use this code?
├─ NO → Find alternative
└─ YES → Continue

Does code meet quality standards?
├─ NO → Rewrite using their approach as guide
└─ YES → Continue

Can we adapt it in < rewrite time?
├─ NO → Rewrite from scratch
└─ YES → Continue

Extract → Adapt → Test → Attribute → Integrate → Verify → Commit ✅
```

---

**Remember**: Good code reuse accelerates development. Bad code reuse creates technical debt. Take time to do it right.
---

**Template Version**: 1.0
**Framework**: Claude Development Framework v2.2
**Last Updated**: 2025-10-01
**Compatibility**: Framework v2.2+
