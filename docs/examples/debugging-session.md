# Example: Debugging Session Walkthrough

**Purpose**: Step-by-step demonstration of debugging a failing test using the Claude Development Framework principles

**Last Updated**: 2025-10-01

---

## Scenario

You're working on Iteration 008: Entity Extraction. Tests were passing, but after implementing confidence scoring, a test started failing.

**Failing Test**:
```bash
$ pytest tests/unit/services/test_entity_extractor.py::test_extract_person_entities -v

====================================== FAILURES =======================================
__________________ test_extract_person_entities __________________

    def test_extract_person_entities():
        """EntityExtractor should extract person entities from text."""

        extractor = EntityExtractor()
        text = "John Smith met Sarah Johnson at the conference."

        result = extractor.extract_entities(text, entity_type="PERSON")

>       assert len(result) == 2
E       AssertionError: assert 3 == 2

tests/unit/services/test_entity_extractor.py:42: AssertionError
================================== 1 failed in 0.15s ===================================
```

**Your task**: Debug this failure using proper root cause analysis.

---

## Session Start: Phase 1 - Initial Assessment

### Step 1: Don't Change the Test!

**Common mistake**: Immediately weakening the test
```python
# ❌ WRONG - Weakening test to make it pass
assert len(result) >= 2  # Changed from == 2
```

**Framework Rule**: Rule 2 - Tests Define Correctness. The test is correct until proven otherwise.

### Step 2: Understand Test Intent

**Read the specification**:
```bash
$ cat specs/use-cases/UC-008-entity-extraction.md
```

**Relevant section**:
```markdown
## Acceptance Criteria

1. **Person extraction**: Extract all person names from text
2. **Accuracy**: Extracted entities must match actual person names in text
3. **Confidence scoring**: Each entity has confidence score 0.0-1.0
```

**Test is correct**: Text has 2 person names ("John Smith", "Sarah Johnson"), test expects 2 results.

### Step 3: Gather Information

**What changed recently**:
```bash
$ git log --oneline -5
abc123 feat: add confidence scoring to entity extraction
def456 refactor: extract person detection logic
...
```

**Hypothesis**: The confidence scoring commit (abc123) introduced the bug.

---

## Phase 2: Reproduce and Investigate

### Step 4: Add Debug Output

**Modify test temporarily** (for debugging only):
```python
def test_extract_person_entities():
    """EntityExtractor should extract person entities from text."""

    extractor = EntityExtractor()
    text = "John Smith met Sarah Johnson at the conference."

    result = extractor.extract_entities(text, entity_type="PERSON")

    # DEBUG: Print actual results
    print(f"\n==== DEBUG ====")
    print(f"Expected: 2 entities")
    print(f"Got: {len(result)} entities")
    for i, entity in enumerate(result):
        print(f"  {i+1}. {entity}")
    print(f"===============\n")

    assert len(result) == 2
```

**Run with output**:
```bash
$ pytest tests/unit/services/test_entity_extractor.py::test_extract_person_entities -v -s

==== DEBUG ====
Expected: 2 entities
Got: 3 entities
  1. {'text': 'John Smith', 'type': 'PERSON', 'confidence': 0.95}
  2. {'text': 'Sarah Johnson', 'type': 'PERSON', 'confidence': 0.92}
  3. {'text': 'conference', 'type': 'PERSON', 'confidence': 0.15}
===============

FAILED
```

**Key finding**: "conference" is being incorrectly identified as a PERSON with low confidence (0.15).

---

## Phase 3: Root Cause Analysis

### Step 5: Review Recent Changes

**Examine the confidence scoring commit**:
```bash
$ git show abc123:src/services/entity_extractor.py
```

**Relevant code**:
```python
class EntityExtractor:
    def extract_entities(self, text, entity_type="PERSON"):
        """Extract entities from text with confidence scores."""
        entities = []

        # Use NLP library to detect entities
        for candidate in self._detect_candidates(text):
            confidence = self._calculate_confidence(candidate)

            # BUG: Not filtering by confidence threshold!
            entities.append({
                "text": candidate.text,
                "type": entity_type,
                "confidence": confidence
            })

        return entities
```

**Root cause identified**: The code is including ALL candidates regardless of confidence score. It should filter out low-confidence results.

### Step 6: Verify Root Cause Hypothesis

**Check specification again**:
```bash
$ grep -A 5 "confidence" specs/use-cases/UC-008-entity-extraction.md
```

```markdown
3. **Confidence scoring**: Each entity has confidence score 0.0-1.0
   - Entities with confidence < 0.5 should be filtered out
   - Only high-confidence entities are returned
```

**Hypothesis confirmed**: Specification says entities with confidence < 0.5 should be filtered. Current implementation doesn't filter.

---

## Phase 4: Fix Implementation (Not Test)

### Step 7: Write Additional Test First

**Before fixing, add test for the actual requirement**:
```python
def test_extract_entities_filters_low_confidence():
    """EntityExtractor should filter out entities with confidence < 0.5."""

    extractor = EntityExtractor()
    text = "John Smith met Sarah Johnson at the conference."

    result = extractor.extract_entities(text, entity_type="PERSON")

    # All returned entities should have confidence >= 0.5
    for entity in result:
        assert entity["confidence"] >= 0.5, \
            f"Entity '{entity['text']}' has confidence {entity['confidence']} < 0.5"
```

**Run new test**:
```bash
$ pytest tests/unit/services/test_entity_extractor.py::test_extract_entities_filters_low_confidence -v

FAILED - AssertionError: Entity 'conference' has confidence 0.15 < 0.5
```

**Good**: New test also fails, confirming the root cause.

### Step 8: Implement Fix

**Fix the implementation**:
```python
class EntityExtractor:
    CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence to include entity

    def extract_entities(self, text, entity_type="PERSON"):
        """Extract entities from text with confidence scores."""
        entities = []

        for candidate in self._detect_candidates(text):
            confidence = self._calculate_confidence(candidate)

            # FIXED: Filter by confidence threshold
            if confidence >= self.CONFIDENCE_THRESHOLD:
                entities.append({
                    "text": candidate.text,
                    "type": entity_type,
                    "confidence": confidence
                })

        return entities
```

### Step 9: Verify Fix

**Run both tests**:
```bash
$ pytest tests/unit/services/test_entity_extractor.py::test_extract_person_entities -v
PASSED

$ pytest tests/unit/services/test_entity_extractor.py::test_extract_entities_filters_low_confidence -v
PASSED
```

**Run ALL tests** (ensure nothing broke):
```bash
$ pytest tests/unit/services/test_entity_extractor.py -v
================================== test session starts ====================================
collected 8 items

tests/unit/services/test_entity_extractor.py::test_extract_person_entities PASSED
tests/unit/services/test_entity_extractor.py::test_extract_org_entities PASSED
tests/unit/services/test_entity_extractor.py::test_extract_location_entities PASSED
tests/unit/services/test_entity_extractor.py::test_extract_entities_filters_low_confidence PASSED
tests/unit/services/test_entity_extractor.py::test_extract_entities_empty_text PASSED
tests/unit/services/test_entity_extractor.py::test_extract_entities_invalid_type PASSED
tests/unit/services/test_entity_extractor.py::test_confidence_scoring PASSED
tests/unit/services/test_entity_extractor.py::test_entity_deduplication PASSED

================================== 8 passed in 0.42s ===================================
```

**All tests passing!** ✅

---

## Phase 5: Update Documentation

### Step 10: Update Iteration Plan

```bash
$ cat planning/current-iteration.md
```

**Add to completed work**:
```markdown
## What Actually Happened

### Completed:
- ✅ Implemented confidence scoring for entities
- ✅ **BUG FIX**: Fixed missing confidence threshold filtering
  - Issue: All entities returned regardless of confidence
  - Root cause: Missing threshold check in extract_entities()
  - Fix: Added CONFIDENCE_THRESHOLD = 0.5 filter
  - New test: test_extract_entities_filters_low_confidence()
- ✅ All tests passing (8/8)
```

### Step 11: Document the Bug (Optional ADR)

**If this was a significant design issue**:
```bash
$ touch docs/decisions/ADR-008-entity-confidence-threshold.md
```

```markdown
# ADR-008: Entity Confidence Threshold

**Date**: 2025-10-01
**Status**: Accepted

## Context

Entity extraction was returning low-confidence false positives.

## Decision

Implement confidence threshold filter at 0.5:
- Entities with confidence >= 0.5 are included
- Entities with confidence < 0.5 are filtered out

## Rationale

- UC-008 spec requires "only high-confidence entities"
- Testing showed 0.5 threshold provides good balance
- User feedback: low-confidence results are noise

## Consequences

- **Positive**: Fewer false positives, higher precision
- **Negative**: Might miss some valid entities (lower recall)
- **Mitigation**: Threshold is configurable if needed
```

---

## Phase 6: Commit

### Step 12: Clean Up Debug Code

**Remove debug output from test**:
```python
def test_extract_person_entities():
    """EntityExtractor should extract person entities from text."""

    extractor = EntityExtractor()
    text = "John Smith met Sarah Johnson at the conference."

    result = extractor.extract_entities(text, entity_type="PERSON")

    # DEBUG output removed
    assert len(result) == 2
```

### Step 13: Commit with Descriptive Message

```bash
$ git add src/services/entity_extractor.py \
         tests/unit/services/test_entity_extractor.py \
         planning/current-iteration.md

$ git commit -m "$(cat <<'EOF'
fix: add confidence threshold filtering to entity extraction

Problem:
- test_extract_person_entities was failing
- Returned 3 entities instead of 2
- "conference" incorrectly identified as PERSON (confidence 0.15)

Root Cause:
- extract_entities() was returning ALL candidates
- No filtering by confidence threshold
- Specification (UC-008) requires confidence >= 0.5 filter

Solution:
- Added CONFIDENCE_THRESHOLD = 0.5 constant
- Filter entities by confidence before returning
- Added test: test_extract_entities_filters_low_confidence()

Testing:
- All 8 tests passing
- Original failing test now passes
- New test covers confidence filtering requirement

Specification: UC-008
Tests: 8 passing / 8 total

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Key Takeaways

### What We Did RIGHT ✅

1. **Didn't weaken the test**
   - Resisted urge to change assertion
   - Analyzed why test was failing

2. **Read the specification**
   - Confirmed test matched spec
   - Found specification detail we missed

3. **Added debug output**
   - Printed actual vs expected
   - Identified the extra entity

4. **Root cause analysis**
   - Examined recent changes
   - Found exact line of code causing issue

5. **Fixed the system, not the test**
   - Implemented proper confidence filtering
   - Test passed without modification

6. **Wrote additional test**
   - Added test for the actual requirement
   - Prevents regression

7. **Verified all tests**
   - Ensured nothing else broke
   - Full test suite passing

8. **Documented the fix**
   - Updated iteration plan
   - Descriptive commit message

### What to AVOID ❌

1. **Changing test without analysis**
   ```python
   # ❌ DON'T DO THIS
   assert len(result) >= 2  # Weakened assertion
   ```

2. **Guessing at fixes**
   ```python
   # ❌ DON'T DO THIS
   if entity.text == "conference":  # Band-aid fix
       continue
   ```

3. **Skipping specification check**
   - Always verify test matches spec
   - Spec is source of truth

4. **Committing debug code**
   - Remove all debug output
   - Clean commits only

5. **Not running full test suite**
   - One passing test doesn't mean success
   - Always run ALL tests

---

## Debugging Flowchart

```
Test Failing
     |
     v
Did you change the test? → YES → STOP! Revert test change
     |                                       |
     NO                                      v
     |                            Read specification
     v                                      |
Read specification                         |
     |                                      |
     v                                      |
Does test match spec? → NO → Fix test to match spec
     |                                      |
    YES                                     |
     |                                      |
     v                                      |
Add debug output                            |
     |                                      |
     v                                      |
Run test with -s flag                       |
     |                                      |
     v                                      |
Analyze actual vs expected                  |
     |                                      |
     v                                      |
Review recent code changes                  |
     |                                      |
     v                                      |
Identify root cause                         |
     |                                      |
     v                                      |
Write test for bug (if missing)            |
     |                                      |
     v                                      |
Fix implementation                          |
     |                                      |
     v                                      |
Run failing test → Still failing? → Back to analysis
     |                                      |
   PASSES                                   |
     |                                      |
     v                                      |
Run ALL tests → Any failing? → Debug those tests
     |                                      |
   ALL PASS                                 |
     |                                      |
     v                                      |
Remove debug output                         |
     |                                      |
     v                                      |
Update documentation                        |
     |                                      |
     v                                      |
Commit with detailed message                |
     |                                      |
     v                                      |
   DONE ✅ <--------------------------------|
```

---

## Common Debugging Scenarios

### Scenario 1: Test Fails Intermittently

**Symptom**: Test passes sometimes, fails other times

**Common causes**:
- Time-dependent code (using current time)
- Random number generation
- Unordered data structures (sets, dicts in Python < 3.7)
- Test interdependence
- Race conditions (async code)

**Debug approach**:
```python
# 1. Run test multiple times
pytest test_file.py::test_name -v --count=100

# 2. Add seed for random
random.seed(42)

# 3. Mock time
with patch('time.time', return_value=1696176000):
    result = function_that_uses_time()

# 4. Sort results before asserting
assert sorted(result) == sorted(expected)
```

### Scenario 2: Test Passes Locally, Fails in CI

**Common causes**:
- Environment differences
- Missing dependencies
- Time zone differences
- File path differences (Windows vs Linux)

**Debug approach**:
```bash
# 1. Check CI environment
echo $PATH
echo $PYTHONPATH
python --version

# 2. Run in Docker locally (same as CI)
docker run -it python:3.11 /bin/bash
# Run tests in container

# 3. Check timezone
TZ=UTC pytest tests/

# 4. Use absolute paths
```

### Scenario 3: Integration Test Fails, Unit Tests Pass

**Common causes**:
- Mock doesn't match real behavior
- Database state issues
- External service unavailable
- Timing issues

**Debug approach**:
```python
# 1. Compare mock vs real
# Unit test (mock)
mock_db.return_value = {"id": "123"}

# Integration test (real)
real_result = db.query()
print(f"Real DB returns: {real_result}")  # Check structure

# 2. Check database state
print(f"DB records before test: {db.count()}")

# 3. Add retries for timing
@retry(tries=3, delay=1)
def flaky_integration_test():
    # ...
```

---

## Emergency Procedures

### When Stuck

1. **Take a break** (5-10 minutes)
   - Often see issue with fresh eyes

2. **Explain to rubber duck**
   - Describe problem out loud
   - Often reveals solution

3. **Simplify**
   - Create minimal reproduction
   - Remove unrelated code

4. **Ask Claude**:
   ```
   "I have a failing test. Here's the test code [paste].
    Here's the implementation [paste].
    Here's the error [paste].
    The specification says [paste relevant section].
    What's the root cause?"
   ```

5. **Bisect the commit history**:
   ```bash
   git bisect start
   git bisect bad  # Current commit fails
   git bisect good abc123  # This older commit worked
   # Git will checkout commits to test
   # Run test at each step
   pytest test_file.py::test_name
   git bisect good  # if test passes
   git bisect bad   # if test fails
   # Repeat until git identifies the breaking commit
   ```

---

## Debugging Tools Reference

### Python Debugger (pdb)

```python
def test_something():
    result = some_function()

    # Add breakpoint
    import pdb; pdb.set_trace()

    assert result == expected
```

**Commands**:
- `n` (next) - Execute next line
- `s` (step) - Step into function
- `c` (continue) - Continue to next breakpoint
- `p variable` (print) - Print variable value
- `l` (list) - Show current code
- `q` (quit) - Exit debugger

### Pytest Options

```bash
# Show print output
pytest -s

# Verbose output
pytest -v

# Stop at first failure
pytest -x

# Show local variables on failure
pytest -l

# Run last failed tests only
pytest --lf

# Run tests matching pattern
pytest -k "test_create"

# Show slowest 10 tests
pytest --durations=10
```

---

**Template Version**: 1.0
**Framework**: Claude Development Framework v2.1
**Last Updated**: 2025-10-01
**Compatibility**: Framework v2.1+
