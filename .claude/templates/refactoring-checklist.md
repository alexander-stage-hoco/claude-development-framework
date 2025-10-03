---
tier: 3
purpose: RED-GREEN-REFACTOR process
reload_trigger: After GREEN phase
estimated_read_time: 15 minutes
---

# Refactoring Checklist

**Version**: 2.1
**Last Updated**: 2025-09-30
**Purpose**: Systematic refactoring guidance after implementation phase

---

## Overview

Refactoring is the **third mandatory step** in the TDD cycle:
1. **RED**: Write failing test
2. **GREEN**: Implement minimal code to pass test
3. **REFACTOR**: Improve code quality while maintaining passing tests ← **THIS STEP**

**Key Principle**: Refactoring changes code structure without changing behavior. Tests ensure no behavior change.

---

## When to Refactor

### ✅ Always Refactor After:
- Implementation passes all tests
- Feature is complete
- Before committing code
- When complexity exceeds threshold

### ❌ Never Refactor:
- During initial implementation (get to GREEN first)
- Without passing tests (no safety net)
- While tests are failing
- Without version control (git)

---

## Comprehensive Refactoring Checklist

Run through EVERY item after implementation passes tests:

### 1. Code Duplication
- [ ] **Repeated code blocks?** → Extract to shared function
- [ ] **Duplicated strings/numbers?** → Extract to named constants
- [ ] **Similar logic with variations?** → Extract with parameters

**Example**:
```python
# Before: Duplicated validation
def process_payment(amount):
    if amount < 0:
        raise ValueError("Amount must be positive")
    # process...

def process_refund(amount):
    if amount < 0:
        raise ValueError("Amount must be positive")
    # process...

# After: Extracted
def validate_amount(amount: float) -> None:
    if amount < 0:
        raise ValueError("Amount must be positive")

def process_payment(amount: float):
    validate_amount(amount)
    # process...
```

---

### 2. Function Complexity
- [ ] **Function > 20-30 lines?** → Split into smaller functions
- [ ] **Multiple responsibilities?** → One function per responsibility
- [ ] **Nesting > 3 levels?** → Use guard clauses or extract
- [ ] **Cyclomatic complexity > 10?** → Simplify branching logic

**Example**:
```python
# Before: Function does too much (4 responsibilities)
def process_order(order_data):
    # Validate
    if not order_data.get("items"):
        raise ValueError("No items")
    if not order_data.get("customer_id"):
        raise ValueError("No customer")

    # Calculate total
    total = 0
    for item in order_data["items"]:
        if item["quantity"] < 0:
            raise ValueError("Invalid quantity")
        total += item["price"] * item["quantity"]

    # Apply discount
    if order_data.get("discount_code"):
        discount = get_discount(order_data["discount_code"])
        if discount:
            total = total * (1 - discount)

    # Save order
    order = Order(customer_id=order_data["customer_id"],
                  items=order_data["items"], total=total)
    db.save(order)
    return order

# After: Extracted to focused functions
def process_order(order_data: Dict) -> Order:
    """Process customer order: validate, calculate, save."""
    validate_order_data(order_data)
    total = calculate_order_total(order_data)
    total = apply_discount(total, order_data.get("discount_code"))
    return save_order(order_data, total)

def validate_order_data(order_data: Dict) -> None:
    """Validate order data completeness."""
    if not order_data.get("items"):
        raise ValueError("Order must contain items")
    if not order_data.get("customer_id"):
        raise ValueError("Order must have customer")
```

---

### 3. Naming Quality
- [ ] **Variable names descriptive?** → Rename for clarity
- [ ] **Function names reveal intent?** → Use verbs describing action
- [ ] **Abbreviations used?** → Use full words
- [ ] **Single-letter variables?** → Descriptive names (except i, j in loops)

**Example**:
```python
# Before: Unclear names
def proc(d):
    x = d["amt"]
    return x * 1.1

# After: Descriptive names
TAX_RATE = 1.1

def calculate_price_with_tax(order_data: Dict) -> float:
    """Calculate total price including tax."""
    subtotal = order_data["amount"]
    return subtotal * TAX_RATE
```

**Naming Guidelines**:
- Functions: Use verbs (`calculate_`, `get_`, `create_`, `validate_`)
- Variables: Descriptive names (`user_email` not `e`)
- Constants: ALL_CAPS (`MAX_RETRIES`, `TAX_RATE`)
- Booleans: Use is/has/can (`is_valid`, `has_permission`)

---

### 4. Magic Numbers and Strings
- [ ] **Hardcoded numbers (except 0, 1)?** → Extract to named constants
- [ ] **Repeated string literals?** → Extract to constants
- [ ] **Configuration values in code?** → Move to config

**Example**:
```python
# Before: Magic numbers
total = subtotal * 1.08
if subtotal > 100:
    discount = subtotal * 0.1

# After: Named constants
TAX_RATE = 1.08
DISCOUNT_THRESHOLD = 100
DISCOUNT_RATE = 0.1

total = subtotal * TAX_RATE
if subtotal > DISCOUNT_THRESHOLD:
    discount = subtotal * DISCOUNT_RATE
```

---

### 5. Type Hints & Documentation
- [ ] **All parameters have type hints?**
- [ ] **Return values have type hints?**
- [ ] **Public functions have docstrings?**
- [ ] **Docstrings reference specifications?**

**Example**:
```python
def calculate_tax(amount: Decimal) -> Decimal:
    """
    Calculate sales tax.

    Specification: UC-003#tax-calculation
    """
```

---

### 6. Error Handling
- [ ] **Exceptions caught appropriately?**
- [ ] **Error messages clear and actionable?**
- [ ] **Errors logged with context?**
- [ ] **Proper exception types used?**

---

### 7. Conditional Logic
- [ ] **Complex conditions?** → Extract to named functions
- [ ] **If/elif chains?** → Use dictionaries or strategy pattern
- [ ] **Nested conditions?** → Flatten with guard clauses

---

### 8. Data Structures
- [ ] **Appropriate data structure used?**
- [ ] **Lists for membership testing?** → Use sets
- [ ] **Tuples for structured data?** → Use dataclasses
- [ ] **Dicts for type safety?** → Use enums

---

### 9. Code Organization
- [ ] **Related functions grouped?**
- [ ] **Logical ordering (high-level → low-level)?**
- [ ] **Too many functions in module?** → Split module

---

### 10. Design Patterns
- [ ] **Would a pattern improve code?**
  - Strategy (interchangeable algorithms)
  - Factory (object creation)
  - Repository (data access)
  - Decorator (add behavior)

---

## Refactoring Process

### Step 1: Baseline
```bash
pytest tests/ -v  # All tests pass
# Record count: "15 tests passing"
```

### Step 2: Apply Refactorings
1. Identify opportunity from checklist
2. Apply single refactoring
3. Run tests immediately
4. If fail → revert and investigate
5. If pass → proceed to next

### Step 3: Verify
```bash
pytest tests/ -v  # Still "15 tests passing"
# Same count, no regressions
```

### Step 4: Commit
```bash
git commit -m "refactor: [description]

Refactored [component]:
- [Change 1]
- [Change 2]

Tests: 15 passing / 15 total (no behavior change)"
```

---

## Common Refactoring Patterns

| Pattern | When | How |
|---------|------|-----|
| **Extract Function** | Code block reused or represents concept | Create new function with clear name |
| **Inline Function** | Function body as clear as name | Replace calls with body |
| **Rename** | Name doesn't reveal intent | Use IDE refactoring |
| **Extract Constant** | Magic number or repeated literal | Create named constant at module level |
| **Split Function** | Function does multiple things | Separate function per responsibility |
| **Introduce Parameter Object** | Many parameters (> 4) | Group into dataclass |

---

## Refactoring Red Flags

### 🚩 Stop and Revert If:
- Tests start failing unexpectedly
- You're unsure if behavior changed
- Refactoring takes > 15 minutes (too risky)
- You lose track of what you're doing

### ✅ Safe to Continue If:
- Tests still pass after each change
- Each refactoring is small and focused
- You can clearly explain what you changed

---

## Anti-Patterns to Reject

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| "We'll refactor later" | Tech debt accumulates | Refactor NOW (part of TDD) |
| "Tests pass, ship it" | Skips REFACTOR step | RED → GREEN → **REFACTOR** |
| "Might break things" | Avoiding refactoring | Tests protect you! |
| "Code works, don't touch" | Complexity accumulates | Refactor for maintainability |

---

## Metrics for Good Code

After refactoring, code should meet:

- **Cyclomatic Complexity**: < 10 per function
- **Function Length**: < 30 lines
- **Function Parameters**: < 4 parameters
- **Code Coverage**: Maintained or improved
- **Duplication**: Minimized or eliminated
- **Naming**: Clear and descriptive
- **Documentation**: Comprehensive docstrings

---

## Success Criteria

Refactoring succeeds if:
- ✅ All tests still pass (same count, no new failures)
- ✅ Code complexity reduced
- ✅ Duplication eliminated
- ✅ Naming improved
- ✅ Functions are smaller and focused
- ✅ Code is more readable
- ✅ You can explain what improved

---

## Quick Reference

**Decision Tree**:
```
Tests pass? → YES
  ↓
Check each checklist item
  ↓
Found opportunity? → YES
  ↓
Apply refactoring
  ↓
Tests still pass? → YES
  ↓
Commit with "refactor:" type ✅
```

**Essential Steps**:
1. Ensure tests pass (baseline)
2. Apply one refactoring at a time
3. Test after each change
4. Commit when complete

---

## Additional Resources

**Detailed Examples**:
- `.claude/examples/refactoring/duplication-example.md` - Extract functions & constants
- `.claude/examples/refactoring/complexity-example.md` - Split complex functions
- `.claude/examples/refactoring/naming-example.md` - Improve names

**Related Guides**:
- `development-rules.md` - Rule 12: Mandatory Refactoring
- `session-checklist.md` - Phase 6: Refactor
- `git-workflow.md` - Separate commits for refactoring

---

**Remember**: Refactoring is NOT optional. It's the third mandatory step in TDD: RED → GREEN → **REFACTOR**.
---

**Template Version**: 1.0
**Framework**: Claude Development Framework v2.2
**Last Updated**: 2025-10-01
**Compatibility**: Framework v2.2+
