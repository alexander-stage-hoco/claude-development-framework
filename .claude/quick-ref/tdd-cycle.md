# Quick Ref: TDD Cycle (RED-GREEN-REFACTOR)

**Purpose**: The mandatory 3-step development cycle

---

## The Cycle

```
┌─────────────┐
│   1. RED    │  Write failing test
│   (Test)    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  2. GREEN   │  Make test pass (minimal code)
│  (Implement)│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 3. REFACTOR │  Improve code quality (MANDATORY)
│  (Clean)    │
└──────┬──────┘
       │
       ▼ (repeat for next feature)
```

---

## Step 1: RED (Write Failing Test)

### Actions:
1. Write test for next small increment of functionality
2. **Run test** - verify it FAILS for the right reason
3. Show failing test output to user
4. Get approval to proceed to GREEN

### Checklist:
- [ ] Test is specific and focused
- [ ] Test fails with clear error message
- [ ] Failure reason makes sense (not syntax error!)
- [ ] User approves moving to implementation

### Example Output:
```
test_create_task FAILED
AssertionError: Expected status code 201, got 404
(Reason: POST /tasks endpoint doesn't exist yet - correct!)
```

---

## Step 2: GREEN (Make Test Pass)

### Actions:
1. Write **minimal** code to make test pass
2. **Run test** - verify it PASSES
3. Show passing test output

### Rules:
- ✅ Write simplest code that works
- ✅ Hard-code values if needed at first
- ✅ Make THIS test pass (don't over-engineer)
- ❌ Don't add extra features "while you're there"
- ❌ Don't skip error handling specified in test

### Checklist:
- [ ] Test now passes
- [ ] No other tests broken
- [ ] Implementation matches spec

### Example Output:
```
test_create_task PASSED
test_list_tasks PASSED
8 tests passing / 8 total
```

---

## Step 3: REFACTOR (Improve Quality) ← MANDATORY

### This Step Is NOT Optional!

After implementation passes, ALWAYS refactor for:

#### Refactoring Checklist:
- [ ] **Duplication?** Extract repeated code to functions
- [ ] **Complexity?** Break large functions into smaller ones
- [ ] **Naming?** Improve variable/function names
- [ ] **Magic Numbers?** Extract to named constants
- [ ] **Single Responsibility?** Each function does one thing
- [ ] **Type Hints?** Add if missing
- [ ] **Docstrings?** Add spec references

### Actions:
1. Review code for refactoring opportunities
2. Apply refactorings one at a time
3. **Run tests after EACH refactoring** - must still pass!
4. Commit refactoring separately from implementation

### Example Refactorings:

**Before**:
```python
def process(data):
    if data["type"] == "a":
        x = data["val"] * 1.08
        db.save(x)
    elif data["type"] == "b":
        x = data["val"] * 1.08
        db.save(x + 10)
```

**After**:
```python
TAX_RATE = 1.08
TYPE_B_SURCHARGE = 10

def process(data: Dict) -> None:
    """Process data based on type.

    Specification: UC-001#process-data
    """
    taxed_value = _apply_tax(data["val"])

    if data["type"] == "a":
        _save_value(taxed_value)
    elif data["type"] == "b":
        _save_value(taxed_value + TYPE_B_SURCHARGE)

def _apply_tax(value: float) -> float:
    return value * TAX_RATE

def _save_value(value: float) -> None:
    db.save(value)
```

**What Changed**:
- ✅ Extracted magic numbers to constants
- ✅ Extracted tax calculation
- ✅ Eliminated duplication
- ✅ Added type hints
- ✅ Added docstring with spec reference
- ✅ Each function has single responsibility

---

## Commit Strategy

### Two Separate Commits:

**Commit 1** (Implementation):
```bash
git commit -m "feat: Add task creation endpoint

Specification: UC-003
Tests: 8 passing / 8 total

Implements POST /tasks with validation."
```

**Commit 2** (Refactoring):
```bash
git commit -m "refactor: Extract validation logic

- Extract _validate_task_data function
- Extract constants for limits
- Improve function naming

Tests: 8 passing / 8 total (no behavior change)"
```

---

## Anti-Patterns (What NOT to Do)

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| "Let's skip tests for now" | Violates Rule #2 | Write test FIRST (RED) |
| "This test is too strict" | Weakening test to pass | Fix implementation, not test |
| "Tests pass, commit!" | Skipped REFACTOR step | RED → GREEN → **REFACTOR** |
| "We'll refactor later" | Tech debt accumulates | Refactor NOW (part of cycle) |
| "Let's mock away the problem" | Hiding real issues | Fix the actual issue |

---

## Success Metrics

You're doing TDD right if:
- ✅ Every feature starts with a failing test
- ✅ Implementation makes test pass
- ✅ Code improves after GREEN (refactoring)
- ✅ Tests remain green after refactoring
- ✅ Test count increases with each iteration
- ✅ Code quality improves over time

---

## Quick Decision Tree

```
Need to add feature?
  │
  ├─→ Write test (RED) → Fails? → Yes ───┐
  │                        │              │
  │                        └─→ No (syntax error?) → Fix test
  │                                       │
  │                                       ▼
  ├─→ Implement (GREEN) → Passes? → Yes ─┐
  │                        │              │
  │                        └─→ No → Debug implementation
  │                                       │
  │                                       ▼
  └─→ Refactor → Tests still pass? → Yes → Commit (2 commits)
                      │
                      └─→ No → Revert refactoring, try again
```

---

**Remember**: RED-GREEN-REFACTOR is not optional. All three steps are mandatory.