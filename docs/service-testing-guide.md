# Service Layer Testing Guide

**Purpose**: Best practices for testing services in isolation with proper mocking, integration testing patterns, and TDD workflows

**Last Updated**: 2025-10-01

---

## Overview

Services are the core business logic components in the Claude Development Framework. Testing them properly is critical for maintainability and reliability.

**This guide covers**:
1. Service testing philosophy
2. Unit testing services in isolation
3. Mocking strategies and anti-patterns
4. Integration testing with real dependencies
5. TDD workflow for services
6. Common testing patterns

---

## Service Testing Philosophy

### Three Levels of Service Testing

**1. Unit Tests** - Service in complete isolation
- Mock ALL dependencies (other services, databases, external APIs)
- Test business logic only
- Fast execution (< 100ms per test)
- High code coverage (aim for 90%+)

**2. Integration Tests** - Service with real dependencies
- Use real database (test database)
- Use real dependent services
- Test actual integrations work
- Slower execution (< 5s per test)
- Focus on critical paths

**3. BDD/E2E Tests** - Full user workflows
- All services working together
- Real or production-like environment
- Test user-facing acceptance criteria
- Slowest execution (< 30s per scenario)
- Cover happy paths + critical edge cases

**Rule**: Write MORE unit tests, FEWER integration tests, MINIMAL E2E tests

---

## Unit Testing Services

### Test Structure

**Pattern**: Arrange-Act-Assert (AAA)

```python
# tests/unit/services/test_user_service.py
import pytest
from src.services.user_service import UserService
from unittest.mock import Mock, patch

def test_create_user_with_valid_data():
    """Test that UserService.create_user() creates user with valid data."""

    # Arrange (Setup)
    mock_db = Mock()
    mock_db.save.return_value = {"id": "123", "name": "John"}

    service = UserService(database=mock_db)
    user_data = {"name": "John", "email": "john@example.com"}

    # Act (Execute)
    result = service.create_user(user_data)

    # Assert (Verify)
    assert result["id"] == "123"
    assert result["name"] == "John"
    mock_db.save.assert_called_once_with(user_data)
```

### Service Test Checklist

For each service method, test:
- [ ] **Happy path** - Valid inputs produce correct outputs
- [ ] **Edge cases** - Boundary values, empty inputs, extreme values
- [ ] **Error cases** - Invalid inputs raise appropriate errors
- [ ] **State changes** - Service state updated correctly
- [ ] **Side effects** - Dependencies called with correct parameters
- [ ] **Return values** - Correct data structure and values returned

---

## Dependency Injection for Testability

### Problem: Hard Dependencies

**Bad** (not testable):
```python
# src/services/user_service.py
from src.database import Database

class UserService:
    def __init__(self):
        self.db = Database()  # ❌ Hard dependency - can't mock!

    def create_user(self, data):
        return self.db.save(data)
```

**Cannot test in isolation** - will always hit real database.

### Solution: Inject Dependencies

**Good** (testable):
```python
# src/services/user_service.py
class UserService:
    def __init__(self, database):
        self.db = database  # ✅ Injected - can pass mock!

    def create_user(self, data):
        return self.db.save(data)


# Production usage:
from src.database import Database
service = UserService(database=Database())

# Test usage:
from unittest.mock import Mock
mock_db = Mock()
service = UserService(database=mock_db)
```

### Constructor Injection Pattern

**All dependencies via constructor**:
```python
class OrderService:
    def __init__(self, database, email_service, payment_gateway):
        self.db = database
        self.email = email_service
        self.payment = payment_gateway

    def place_order(self, order_data):
        # Use injected dependencies
        order = self.db.save_order(order_data)
        self.payment.charge(order.total)
        self.email.send_confirmation(order.customer_email)
        return order
```

**Benefits**:
- Easy to mock all dependencies
- Clear what service depends on
- Explicit contract

---

## Mocking Strategies

### When to Mock

**Mock**:
- ✅ Other services (to isolate current service)
- ✅ Database connections
- ✅ External APIs (HTTP requests)
- ✅ File system operations
- ✅ Time/date functions
- ✅ Random number generators

**Don't Mock**:
- ❌ Simple data classes / DTOs
- ❌ Pure functions with no side effects
- ❌ Built-in language features
- ❌ The service you're testing!

### Mock Types

**1. Simple Mock** - Dummy object with no behavior
```python
mock_db = Mock()
```

**2. Configured Mock** - Returns specific values
```python
mock_db = Mock()
mock_db.find_user.return_value = {"id": "123", "name": "John"}
```

**3. Side Effect Mock** - Raises exceptions or varies by call
```python
mock_db = Mock()
mock_db.save.side_effect = DatabaseError("Connection failed")
```

**4. Spec Mock** - Enforces interface contract
```python
from src.database import Database

mock_db = Mock(spec=Database)  # Only allows methods that Database has
mock_db.invalid_method()  # Raises AttributeError
```

### Mock Verification

**Verify calls made**:
```python
# Verify method was called
mock_db.save.assert_called()

# Verify called once
mock_db.save.assert_called_once()

# Verify called with specific args
mock_db.save.assert_called_with({"name": "John"})

# Verify call count
assert mock_db.save.call_count == 3

# Verify never called
mock_db.delete.assert_not_called()
```

---

## Mocking Anti-Patterns

### Anti-Pattern 1: Over-Mocking

**Problem**: Mocking everything including simple objects
```python
# ❌ BAD
mock_user = Mock()
mock_user.name = "John"
mock_user.email = "john@example.com"

result = service.validate_user(mock_user)
```

**Solution**: Use real simple objects
```python
# ✅ GOOD
user = User(name="John", email="john@example.com")  # Real data class

result = service.validate_user(user)
```

### Anti-Pattern 2: Mocking the System Under Test

**Problem**: Mocking the service you're testing
```python
# ❌ BAD
mock_service = Mock(spec=UserService)
mock_service.create_user.return_value = {"id": "123"}

result = mock_service.create_user(data)  # Testing the mock, not the service!
```

**Solution**: Test the real service, mock dependencies
```python
# ✅ GOOD
mock_db = Mock()
real_service = UserService(database=mock_db)

result = real_service.create_user(data)  # Testing real service
```

### Anti-Pattern 3: Brittle Mocks

**Problem**: Mocks break when implementation details change
```python
# ❌ BAD - Too specific
mock_db.save.assert_called_with(
    table="users",
    data={"name": "John", "email": "john@example.com", "created_at": "2025-10-01 12:00:00"}
)
# Breaks if timestamp format changes!
```

**Solution**: Verify essential behavior only
```python
# ✅ GOOD - Focus on contract
call_args = mock_db.save.call_args[1]  # Get kwargs
assert call_args["data"]["name"] == "John"
assert call_args["data"]["email"] == "john@example.com"
# Don't care about exact timestamp
```

### Anti-Pattern 4: Mock Leakage

**Problem**: Mocks affect other tests
```python
# ❌ BAD - Global mock affects all tests
from src.database import Database
Database.save = Mock()  # Modifies global class!

def test_create_user():
    # ...
```

**Solution**: Use fixtures or patching with proper cleanup
```python
# ✅ GOOD - Isolated per test
@pytest.fixture
def mock_database():
    return Mock(spec=Database)

def test_create_user(mock_database):
    service = UserService(database=mock_database)
    # Mock is fresh for this test only
```

---

## Integration Testing

### When to Write Integration Tests

**Write integration tests for**:
- Database queries (SELECT, INSERT, UPDATE, DELETE)
- Cross-service communication
- External API calls
- File system operations
- Message queue interactions

**Pattern**: Use real dependencies but in test environment

### Database Integration Tests

**Setup test database**:
```python
# tests/integration/conftest.py
import pytest
from src.database import Database

@pytest.fixture(scope="function")
def test_db():
    """Provide a clean test database for each test."""
    db = Database(connection_string="postgresql://localhost/test_db")
    db.migrate()  # Run migrations
    db.seed_test_data()  # Optional: Add test data

    yield db

    db.rollback()  # Clean up after test
    db.close()
```

**Integration test example**:
```python
# tests/integration/services/test_user_service_integration.py
import pytest
from src.services.user_service import UserService

def test_create_user_persists_to_database(test_db):
    """Test that UserService.create_user() actually saves to database."""

    # Arrange
    service = UserService(database=test_db)
    user_data = {"name": "John", "email": "john@example.com"}

    # Act
    result = service.create_user(user_data)

    # Assert - Query database directly to verify
    saved_user = test_db.query("SELECT * FROM users WHERE id = %s", [result["id"]])
    assert saved_user["name"] == "John"
    assert saved_user["email"] == "john@example.com"
```

### Cross-Service Integration Tests

**Testing service dependencies**:
```python
# tests/integration/services/test_order_service_integration.py
def test_place_order_creates_payment(test_db, test_payment_service, test_email_service):
    """Test that OrderService correctly integrates with PaymentService."""

    # Arrange - Use real services with test backends
    order_service = OrderService(
        database=test_db,
        payment_service=test_payment_service,  # Real service, test mode
        email_service=test_email_service  # Real service, test mode
    )

    order_data = {
        "items": [{"id": "item1", "quantity": 2, "price": 10.00}],
        "customer": {"email": "customer@example.com"}
    }

    # Act
    order = order_service.place_order(order_data)

    # Assert - Verify cross-service effects
    assert order["status"] == "confirmed"

    # Check payment was created
    payment = test_payment_service.get_payment(order["payment_id"])
    assert payment["amount"] == 20.00
    assert payment["status"] == "completed"

    # Check email was sent
    sent_emails = test_email_service.get_sent_emails()
    assert len(sent_emails) == 1
    assert sent_emails[0]["to"] == "customer@example.com"
```

---

## Test Doubles: Mocks vs Stubs vs Fakes

### Mock
**Purpose**: Verify interactions (calls made)
```python
mock_email = Mock()
service.send_notification(user)
mock_email.send.assert_called_once()  # Verifying the call
```

### Stub
**Purpose**: Provide canned responses
```python
stub_db = Mock()
stub_db.find_user.return_value = {"id": "123", "name": "John"}  # Stubbed response
user = service.get_user("123")
assert user["name"] == "John"  # Testing the return value
```

### Fake
**Purpose**: Working implementation with shortcuts (for integration tests)
```python
class FakeDatabase:
    """In-memory database for testing."""
    def __init__(self):
        self.users = {}

    def save(self, data):
        user_id = str(len(self.users) + 1)
        self.users[user_id] = data
        return {**data, "id": user_id}

    def find(self, user_id):
        return self.users.get(user_id)


# Use in integration tests
fake_db = FakeDatabase()
service = UserService(database=fake_db)
user = service.create_user({"name": "John"})
assert fake_db.find(user["id"])["name"] == "John"
```

---

## TDD Workflow for Services

### Step-by-Step Process

**1. Write Failing Test (RED)**
```python
# tests/unit/services/test_user_service.py
def test_create_user_validates_email():
    """UserService.create_user() should raise ValueError for invalid email."""

    mock_db = Mock()
    service = UserService(database=mock_db)

    with pytest.raises(ValueError, match="Invalid email"):
        service.create_user({"name": "John", "email": "not-an-email"})

    mock_db.save.assert_not_called()  # Should not save invalid data
```

Run test:
```bash
pytest tests/unit/services/test_user_service.py::test_create_user_validates_email -v
# FAILS: UserService.create_user() doesn't validate email yet
```

**2. Implement Minimum Code (GREEN)**
```python
# src/services/user_service.py
import re

class UserService:
    def __init__(self, database):
        self.db = database

    def create_user(self, data):
        # Validate email
        email = data.get("email", "")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email")

        return self.db.save(data)
```

Run test:
```bash
pytest tests/unit/services/test_user_service.py::test_create_user_validates_email -v
# PASSES
```

**3. Refactor (REFACTOR)**
```python
# src/services/user_service.py
import re

class UserService:
    def __init__(self, database):
        self.db = database

    def create_user(self, data):
        self._validate_user_data(data)
        return self.db.save(data)

    def _validate_user_data(self, data):
        """Validate user data before saving."""
        email = data.get("email", "")
        if not self._is_valid_email(email):
            raise ValueError("Invalid email")

    def _is_valid_email(self, email):
        """Check if email format is valid."""
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))
```

Run tests:
```bash
pytest tests/unit/services/test_user_service.py -v
# All tests still pass after refactoring
```

### TDD Cycle for Service Development

**Iteration cycle**:
```
1. Write test for next piece of functionality
   ↓
2. Run test → RED (fails)
   ↓
3. Write minimal code to pass test
   ↓
4. Run test → GREEN (passes)
   ↓
5. Run ALL tests → ensure nothing broke
   ↓
6. Refactor code (extract methods, improve naming)
   ↓
7. Run tests → still GREEN
   ↓
8. Repeat from step 1 for next functionality
```

---

## Common Service Testing Patterns

### Pattern 1: Testing Error Handling

**Test that service handles errors gracefully**:
```python
def test_create_user_handles_database_error():
    """UserService.create_user() should raise ServiceError when database fails."""

    mock_db = Mock()
    mock_db.save.side_effect = DatabaseError("Connection lost")

    service = UserService(database=mock_db)

    with pytest.raises(ServiceError, match="Failed to create user"):
        service.create_user({"name": "John", "email": "john@example.com"})
```

**Implementation**:
```python
class UserService:
    def create_user(self, data):
        try:
            return self.db.save(data)
        except DatabaseError as e:
            raise ServiceError(f"Failed to create user: {e}")
```

### Pattern 2: Testing State Changes

**Test that service maintains correct state**:
```python
def test_user_service_caches_last_created_user():
    """UserService should cache the last created user."""

    mock_db = Mock()
    mock_db.save.return_value = {"id": "123", "name": "John"}

    service = UserService(database=mock_db)

    assert service.last_created is None  # Initial state

    service.create_user({"name": "John"})

    assert service.last_created["id"] == "123"  # State updated
```

### Pattern 3: Testing with Multiple Calls

**Test service behavior over multiple operations**:
```python
def test_user_service_batch_create():
    """UserService.batch_create() should create multiple users."""

    mock_db = Mock()
    mock_db.save.side_effect = [
        {"id": "1", "name": "User1"},
        {"id": "2", "name": "User2"},
        {"id": "3", "name": "User3"}
    ]

    service = UserService(database=mock_db)

    users_data = [{"name": f"User{i}"} for i in range(1, 4)]
    results = service.batch_create(users_data)

    assert len(results) == 3
    assert mock_db.save.call_count == 3
    assert all(user["id"] for user in results)
```

### Pattern 4: Testing Async Services

**For async/await services**:
```python
import pytest

@pytest.mark.asyncio
async def test_async_create_user():
    """Test async UserService.create_user()."""

    mock_db = Mock()
    mock_db.save = AsyncMock(return_value={"id": "123", "name": "John"})

    service = AsyncUserService(database=mock_db)

    result = await service.create_user({"name": "John"})

    assert result["id"] == "123"
    mock_db.save.assert_called_once()
```

### Pattern 5: Parametrized Tests

**Test multiple scenarios efficiently**:
```python
@pytest.mark.parametrize("email,should_raise", [
    ("valid@example.com", False),
    ("another.valid@example.co.uk", False),
    ("invalid-email", True),
    ("@example.com", True),
    ("user@", True),
    ("", True),
])
def test_email_validation(email, should_raise):
    """UserService should validate email formats correctly."""

    mock_db = Mock()
    service = UserService(database=mock_db)

    if should_raise:
        with pytest.raises(ValueError, match="Invalid email"):
            service.create_user({"name": "User", "email": email})
    else:
        service.create_user({"name": "User", "email": email})
        mock_db.save.assert_called_once()
```

---

## Service Test Organization

### Directory Structure

```
tests/
├── unit/
│   └── services/
│       ├── test_user_service.py           # UserService unit tests
│       ├── test_order_service.py          # OrderService unit tests
│       └── test_payment_service.py        # PaymentService unit tests
├── integration/
│   └── services/
│       ├── test_user_service_integration.py
│       ├── test_order_flow_integration.py
│       └── test_payment_gateway_integration.py
└── bdd/
    └── features/
        ├── user-registration.feature       # E2E user flows
        └── order-placement.feature
```

### Naming Conventions

**Unit test files**:
- `test_{service_name}.py` (e.g., `test_user_service.py`)

**Test functions**:
- `test_{method}_{scenario}()` (e.g., `test_create_user_with_invalid_email()`)

**Fixtures**:
- `{dependency_name}_mock` (e.g., `database_mock`, `email_service_mock`)

---

## Testing Checklist

**Before committing service code**:
- [ ] All service methods have unit tests
- [ ] Happy path covered
- [ ] Error cases covered
- [ ] Edge cases covered
- [ ] Integration tests for database operations
- [ ] Integration tests for external dependencies
- [ ] All tests passing
- [ ] Test coverage ≥ 90% for service code
- [ ] No mocking anti-patterns
- [ ] Tests are readable and maintainable

---

## Common Pitfalls

### Pitfall 1: Testing Implementation, Not Behavior

**Bad**:
```python
def test_create_user_calls_validate_then_save():
    # Testing HOW it works (implementation)
    service.create_user(data)
    assert service._validate.called_before(service._save)
```

**Good**:
```python
def test_create_user_rejects_invalid_data():
    # Testing WHAT it does (behavior)
    with pytest.raises(ValueError):
        service.create_user(invalid_data)
```

### Pitfall 2: Slow Unit Tests

**Problem**: Unit tests taking > 100ms
- Likely hitting real database or external APIs
- Should use mocks for unit tests

**Solution**: Profile tests and ensure all I/O is mocked

### Pitfall 3: Test Interdependence

**Problem**: Tests fail when run in different order
- Tests sharing state
- Global variables being modified

**Solution**: Use fixtures, ensure cleanup, make tests independent

---

**Template Version**: 1.0
**Framework**: Claude Development Framework v2.0
**Last Updated**: 2025-10-01
**Compatibility**: Framework v2.0+
