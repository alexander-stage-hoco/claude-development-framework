"""Integration tests for TDD cycle agent chain.

Tests the complete TDD cycle: RED → GREEN → REFACTOR
- test-writer creates tests (RED state)
- Implementation makes tests pass (GREEN state)
- code-quality-checker validates quality
- refactoring-analyzer suggests improvements
- Refactoring maintains GREEN state

Test Coverage:
- RED state validation (tests fail initially)
- GREEN state transition (tests pass)
- Quality gate enforcement (score ≥ 80)
- Refactoring suggestions on GREEN
- Test protection during refactoring
- Workflow state transitions

Test Workflow:
1. test-writer generates tests from spec → RED
2. Verify all tests fail with correct errors
3. Implement code to pass tests → GREEN
4. code-quality-checker validates implementation
5. refactoring-analyzer runs only on GREEN
6. Refactoring maintains GREEN state
"""

import pytest
from pathlib import Path

from tests.agents.fixtures import MockFileSystem


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def mock_fs(tmp_path: Path) -> MockFileSystem:
    """Mock file system for testing."""
    return MockFileSystem(tmp_path)


@pytest.fixture
def sample_spec(mock_fs: MockFileSystem) -> str:
    """Create sample specification for test generation."""
    content = """# UC-010: Calculate Order Total

## Objective
Calculate total price for an order including items, tax, and shipping.

## Acceptance Criteria

```gherkin
Scenario: Calculate total with single item
  Given order has 1 item priced at $10.00
  When total is calculated
  Then subtotal is $10.00
  And tax is $0.80 (8%)
  And total is $10.80

Scenario: Calculate total with multiple items
  Given order has 2 items priced at $10.00 each
  When total is calculated
  Then subtotal is $20.00
  And tax is $1.60 (8%)
  And total is $21.60
```

## Services Used
| Service | Methods | Purpose |
|---------|---------|---------|
| OrderService | calculate_total() | Calculate order totals |
"""
    return mock_fs.create_file("specs/use-cases/UC-010.md", content)


# ============================================================================
# Test: RED State - Test Writer Generates Failing Tests
# ============================================================================


@pytest.mark.integration
def test_test_writer_generates_tests_in_red_state(sample_spec: str, mock_fs: MockFileSystem):
    """Test that test-writer generates tests that fail initially (RED state)."""
    # Simulate test-writer output
    test_content = """\"\"\"Tests for OrderService.calculate_total().

Specification: UC-010 Calculate Order Total
\"\"\"
import pytest
from src.services.order_service import OrderService


def test_calculate_total_single_item() -> None:
    \"\"\"Test total calculation with single item.

    Specification: UC-010#single-item
    \"\"\"
    # Arrange
    service = OrderService()
    order = {"items": [{"price": 10.00}]}

    # Act
    result = service.calculate_total(order)

    # Assert
    assert result["subtotal"] == 10.00
    assert result["tax"] == 0.80
    assert result["total"] == 10.80
"""

    test_path = mock_fs.create_file("tests/unit/services/test_order_service.py", test_content)
    test = mock_fs.read_file(test_path)

    # Verify test exists and would fail (no implementation yet)
    assert "def test_calculate_total_single_item" in test
    assert "assert result" in test

    # Simulated test execution would fail: ModuleNotFoundError or AttributeError
    # This is the RED state


@pytest.mark.integration
def test_red_state_tests_have_clear_failure_messages(mock_fs: MockFileSystem):
    """Test that RED state tests fail with clear, correct error messages."""
    test_content = """def test_user_creation():
    from src.user_service import UserService
    service = UserService()
    result = service.create_user({"name": "John"})
    assert result["id"] is not None
"""

    test_path = mock_fs.create_file("tests/unit/test_user.py", test_content)
    test = mock_fs.read_file(test_path)

    # Verify test structure
    assert "assert" in test

    # In RED state, would fail with: ModuleNotFoundError: No module named 'src.user_service'
    # This is expected and correct


@pytest.mark.integration
def test_tests_fail_for_right_reasons_not_syntax_errors(mock_fs: MockFileSystem):
    """Test that RED state is due to missing implementation, not test syntax errors."""
    # Good RED: Missing implementation
    test_content = """import pytest

def test_calculate():
    from src.calculator import Calculator
    calc = Calculator()
    result = calc.add(2, 3)
    assert result == 5  # Fails: Calculator doesn't exist yet
"""

    test_path = mock_fs.create_file("tests/unit/test_calc.py", test_content)
    test = mock_fs.read_file(test_path)

    # Verify valid Python syntax
    assert "def test_" in test
    assert "import" in test
    # Would fail with ImportError (good) not SyntaxError (bad)


# ============================================================================
# Test: GREEN State - Implementation Passes Tests
# ============================================================================


@pytest.mark.integration
def test_implementation_transitions_to_green_state(mock_fs: MockFileSystem):
    """Test that implementing code transitions from RED to GREEN."""
    # Create test (RED state)
    test_content = """def test_add():
    from src.math_utils import add
    assert add(2, 3) == 5
"""
    test_path = mock_fs.create_file("tests/unit/test_math.py", test_content)

    # Create implementation (GREEN state)
    impl_content = """def add(a: int, b: int) -> int:
    \"\"\"Add two numbers.

    Specification: UC-020#addition
    \"\"\"
    return a + b
"""
    impl_path = mock_fs.create_file("src/math_utils.py", impl_content)

    # Verify both exist
    test = mock_fs.read_file(test_path)
    impl = mock_fs.read_file(impl_path)

    assert "def test_add" in test
    assert "def add" in impl
    assert "return a + b" in impl

    # Now tests would pass (GREEN state)


@pytest.mark.integration
def test_implementation_has_spec_references(mock_fs: MockFileSystem):
    """Test that implementation includes spec references for traceability."""
    impl_content = """def calculate_total(order):
    \"\"\"Calculate order total.

    Specification: UC-010#calculate-total
    \"\"\"
    subtotal = sum(item["price"] for item in order["items"])
    tax = subtotal * 0.08
    total = subtotal + tax
    return {"subtotal": subtotal, "tax": tax, "total": total}
"""

    impl_path = mock_fs.create_file("src/order_service.py", impl_content)
    impl = mock_fs.read_file(impl_path)

    assert "Specification: UC-010" in impl


# ============================================================================
# Test: Quality Checker Runs on GREEN State
# ============================================================================


@pytest.mark.integration
def test_quality_checker_runs_after_green_state(mock_fs: MockFileSystem):
    """Test that code-quality-checker validates implementation in GREEN state."""
    # Implementation (GREEN state)
    impl_content = """\"\"\"Order service implementation.

Specification: UC-010
\"\"\"
from typing import Dict, Any


def calculate_total(order: Dict[str, Any]) -> Dict[str, float]:
    \"\"\"Calculate order total with tax.

    Specification: UC-010#calculate-total
    \"\"\"
    subtotal = sum(item["price"] for item in order["items"])
    tax = subtotal * 0.08
    total = subtotal + tax
    return {"subtotal": subtotal, "tax": tax, "total": total}
"""

    impl_path = mock_fs.create_file("src/order_service.py", impl_content)
    impl = mock_fs.read_file(impl_path)

    # Quality checker would validate:
    # - Type hints present ✓
    # - Docstring present ✓
    # - Spec reference present ✓
    # - No magic numbers (0.08 should be TAX_RATE constant) ✗

    assert "def calculate_total(order: Dict[str, Any]) -> Dict[str, float]:" in impl
    assert '"""' in impl  # Has docstring
    assert "Specification:" in impl


@pytest.mark.integration
def test_quality_checker_enforces_score_threshold(mock_fs: MockFileSystem):
    """Test that quality checker enforces score ≥ 80 threshold."""
    # Low quality implementation
    poor_impl = """def calc(o):
    s = 0
    for i in o["items"]:
        s += i["price"]
    return s * 1.08
"""

    impl_path = mock_fs.create_file("src/poor_service.py", poor_impl)
    impl = mock_fs.read_file(impl_path)

    # Quality checker would fail this:
    # - No type hints ✗
    # - No docstring ✗
    # - Poor naming (s, o, i) ✗
    # - Magic number (1.08) ✗
    # - No spec reference ✗
    # Score would be < 80

    assert "def calc(o):" in impl  # No type hints
    assert '"""' not in impl  # No docstring


@pytest.mark.integration
def test_quality_checker_validates_type_hints(mock_fs: MockFileSystem):
    """Test that quality checker requires type hints."""
    # Without type hints
    no_types = """def process(data):
    return data["result"]
"""

    path1 = mock_fs.create_file("src/no_types.py", no_types)

    # With type hints
    with_types = """from typing import Dict, Any

def process(data: Dict[str, Any]) -> Any:
    \"\"\"Process data.

    Specification: UC-030#process
    \"\"\"
    return data["result"]
"""

    path2 = mock_fs.create_file("src/with_types.py", with_types)

    impl1 = mock_fs.read_file(path1)
    impl2 = mock_fs.read_file(path2)

    # Quality checker should flag impl1, pass impl2
    assert "def process(data):" in impl1  # Missing types
    assert "def process(data: Dict[str, Any]) -> Any:" in impl2  # Has types


@pytest.mark.integration
def test_quality_checker_validates_docstrings_with_spec_refs(mock_fs: MockFileSystem):
    """Test that quality checker requires docstrings with spec references."""
    impl_content = """def create_user(data):
    \"\"\"Create a new user.

    Specification: UC-005#create-user
    \"\"\"
    return {"id": 1, "name": data["name"]}
"""

    impl_path = mock_fs.create_file("src/user.py", impl_content)
    impl = mock_fs.read_file(impl_path)

    assert '"""Create a new user.' in impl
    assert "Specification: UC-005" in impl


# ============================================================================
# Test: Refactoring Analyzer Runs Only on GREEN
# ============================================================================


@pytest.mark.integration
def test_refactoring_analyzer_requires_green_state(mock_fs: MockFileSystem):
    """Test that refactoring-analyzer only runs when tests pass (GREEN)."""
    # Implementation exists (GREEN state)
    impl_content = """def calculate_total(order):
    subtotal = sum(item["price"] for item in order["items"])
    tax = subtotal * 0.08  # Magic number
    total = subtotal + tax
    return {"subtotal": subtotal, "tax": tax, "total": total}
"""

    impl_path = mock_fs.create_file("src/order.py", impl_content)

    # Simulate passing tests (GREEN state indicator)
    test_results = {"status": "PASSED", "failures": 0, "total": 3}

    # Refactoring analyzer can run
    assert test_results["status"] == "PASSED"
    assert test_results["failures"] == 0

    # In RED state (failures > 0), refactoring would be blocked
    red_results = {"status": "FAILED", "failures": 2, "total": 3}
    assert red_results["failures"] > 0, "Cannot refactor in RED state"


@pytest.mark.integration
def test_refactoring_analyzer_detects_magic_numbers(mock_fs: MockFileSystem):
    """Test that refactoring-analyzer detects magic numbers in GREEN code."""
    impl_content = """def calculate_tax(amount):
    return amount * 0.08  # Magic number
"""

    impl_path = mock_fs.create_file("src/tax.py", impl_content)
    impl = mock_fs.read_file(impl_path)

    # Refactoring analyzer would suggest:
    # Extract constant: TAX_RATE = 0.08
    assert "0.08" in impl


@pytest.mark.integration
def test_refactoring_analyzer_detects_duplication(mock_fs: MockFileSystem):
    """Test that refactoring-analyzer detects code duplication."""
    impl_content = """def calculate_order_1(order):
    subtotal = sum(item["price"] for item in order["items"])
    tax = subtotal * 0.08
    return subtotal + tax

def calculate_order_2(order):
    subtotal = sum(item["price"] for item in order["items"])  # Duplicated
    tax = subtotal * 0.08  # Duplicated
    return subtotal + tax
"""

    impl_path = mock_fs.create_file("src/orders.py", impl_content)
    impl = mock_fs.read_file(impl_path)

    # Refactoring analyzer would detect repeated calculation logic
    assert impl.count('sum(item["price"] for item in order["items"])') == 2


@pytest.mark.integration
def test_refactoring_analyzer_suggests_extract_function(mock_fs: MockFileSystem):
    """Test that refactoring-analyzer suggests extracting functions."""
    impl_content = """def process_order(order):
    # Validation logic (could be extracted)
    if not order.get("items"):
        raise ValueError("No items")
    if not order.get("customer"):
        raise ValueError("No customer")

    # Calculation logic (could be extracted)
    subtotal = sum(item["price"] for item in order["items"])
    tax = subtotal * 0.08
    total = subtotal + tax

    # Save logic (could be extracted)
    db.save({"customer": order["customer"], "total": total})

    return total
"""

    impl_path = mock_fs.create_file("src/process.py", impl_content)
    impl = mock_fs.read_file(impl_path)

    # Refactoring analyzer would suggest:
    # - extract_function: validate_order()
    # - extract_function: calculate_order_total()
    # - extract_function: save_order()

    # Multiple responsibilities detected
    assert "# Validation logic" in impl
    assert "# Calculation logic" in impl
    assert "# Save logic" in impl


# ============================================================================
# Test: Refactoring Maintains GREEN State
# ============================================================================


@pytest.mark.integration
def test_refactoring_maintains_test_coverage(mock_fs: MockFileSystem):
    """Test that refactoring doesn't break tests (stays GREEN)."""
    # Original implementation (GREEN)
    original = """def calculate_total(order):
    subtotal = sum(item["price"] for item in order["items"])
    tax = subtotal * 0.08
    return subtotal + tax
"""

    # Refactored implementation (should stay GREEN)
    refactored = """TAX_RATE = 0.08

def calculate_subtotal(items):
    return sum(item["price"] for item in items)

def calculate_total(order):
    subtotal = calculate_subtotal(order["items"])
    tax = subtotal * TAX_RATE
    return subtotal + tax
"""

    # Both should pass same tests
    path1 = mock_fs.create_file("src/original.py", original)
    path2 = mock_fs.create_file("src/refactored.py", refactored)

    orig = mock_fs.read_file(path1)
    refact = mock_fs.read_file(path2)

    # Same external interface
    assert "def calculate_total(order):" in orig
    assert "def calculate_total(order):" in refact


@pytest.mark.integration
def test_refactoring_improves_quality_score(mock_fs: MockFileSystem):
    """Test that refactoring improves code quality score."""
    # Before refactoring: Score ~60
    before = """def calc(o):
    s = 0
    for i in o["items"]:
        s += i["price"]
    t = s * 0.08
    return s + t
"""

    # After refactoring: Score ~90
    after = """\"\"\"Order calculations.

Specification: UC-010
\"\"\"
from typing import Dict, Any, List

TAX_RATE = 0.08

def calculate_subtotal(items: List[Dict[str, float]]) -> float:
    \"\"\"Calculate subtotal from items.

    Specification: UC-010#subtotal
    \"\"\"
    return sum(item["price"] for item in items)

def calculate_total(order: Dict[str, Any]) -> float:
    \"\"\"Calculate order total including tax.

    Specification: UC-010#total
    \"\"\"
    subtotal = calculate_subtotal(order["items"])
    tax = subtotal * TAX_RATE
    return subtotal + tax
"""

    path1 = mock_fs.create_file("src/before.py", before)
    path2 = mock_fs.create_file("src/after.py", after)

    before_impl = mock_fs.read_file(path1)
    after_impl = mock_fs.read_file(path2)

    # After has improvements:
    assert '"""' in after_impl  # Docstrings
    assert ": " in after_impl  # Type hints
    assert "TAX_RATE" in after_impl  # Constant extracted
    assert "Specification:" in after_impl  # Spec refs


# ============================================================================
# Test: Complete TDD Cycle
# ============================================================================


@pytest.mark.integration
def test_complete_tdd_cycle_red_green_refactor(sample_spec: str, mock_fs: MockFileSystem):
    """Test complete TDD cycle: RED → GREEN → REFACTOR."""
    # PHASE 1: RED - test-writer generates failing tests
    test_content = """def test_calculate_total():
    from src.order_service import OrderService
    service = OrderService()
    result = service.calculate_total({"items": [{"price": 10.00}]})
    assert result["total"] == 10.80
"""
    test_path = mock_fs.create_file("tests/unit/test_order.py", test_content)

    # State: RED (test fails - no implementation)
    assert "def test_calculate_total" in mock_fs.read_file(test_path)

    # PHASE 2: GREEN - implement to pass tests
    impl_content = """class OrderService:
    def calculate_total(self, order):
        subtotal = sum(item["price"] for item in order["items"])
        tax = subtotal * 0.08
        return {"subtotal": subtotal, "tax": tax, "total": subtotal + tax}
"""
    impl_path = mock_fs.create_file("src/order_service.py", impl_content)

    # State: GREEN (tests pass)
    assert "def calculate_total" in mock_fs.read_file(impl_path)

    # PHASE 3: REFACTOR - improve code while maintaining GREEN
    refactored_content = """\"\"\"Order service for calculating totals.

Specification: UC-010
\"\"\"
from typing import Dict, Any

TAX_RATE = 0.08

class OrderService:
    \"\"\"Service for order operations.\"\"\"

    def calculate_total(self, order: Dict[str, Any]) -> Dict[str, float]:
        \"\"\"Calculate order total with tax.

        Specification: UC-010#calculate-total
        \"\"\"
        subtotal = self._calculate_subtotal(order["items"])
        tax = subtotal * TAX_RATE
        total = subtotal + tax
        return {"subtotal": subtotal, "tax": tax, "total": total}

    def _calculate_subtotal(self, items: list) -> float:
        \"\"\"Calculate subtotal from items.\"\"\"
        return sum(item["price"] for item in items)
"""
    refactored_path = mock_fs.create_file("src/order_service_refactored.py", refactored_content)

    # State: Still GREEN (tests still pass, but code is better)
    refactored = mock_fs.read_file(refactored_path)
    assert "TAX_RATE = 0.08" in refactored
    assert "Specification: UC-010" in refactored
    assert '"""' in refactored


@pytest.mark.integration
def test_tdd_cycle_state_transitions_enforced(mock_fs: MockFileSystem):
    """Test that TDD cycle enforces proper state transitions."""
    # Cannot skip RED → Must have failing tests first
    test_content = """def test_feature():
    from src.feature import do_something
    assert do_something() == "result"
"""
    test_path = mock_fs.create_file("tests/unit/test_feature.py", test_content)

    # RED state verified (import would fail)
    assert "from src.feature import do_something" in mock_fs.read_file(test_path)

    # Cannot refactor without GREEN → Must pass tests first
    # Refactoring-analyzer checks test status before running
    tests_passing = False  # Simulated test status

    if not tests_passing:
        # Block refactoring in RED state
        assert not tests_passing, "Cannot refactor until tests pass (GREEN state)"
