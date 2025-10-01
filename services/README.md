# Services Directory

**Framework**: Claude Development Framework v2.0
**Purpose**: Service-oriented architecture layer
**Last Updated**: 2025-10-01

---

## Overview

This directory contains **service specifications and implementations** for the project.

**What is a Service?**
- Reusable business logic component
- Clear interface (Protocol with type hints)
- Testable in isolation (dependency injection)
- Single Responsibility Principle
- Minimal dependencies on other services

**Services vs. Use Cases**:
- **Use Cases**: What the user needs (business requirements)
- **Services**: How the system delivers it (implementation components)
- **Relationship**: Use cases *use* services to fulfill requirements

---

## Directory Structure

```
services/
├── README.md                          # This file
├── auth-service/                      # Example service
│   ├── service-spec.md                # Service specification
│   ├── __init__.py
│   ├── interface.py                   # Protocol (abstract interface)
│   ├── implementation.py              # Concrete implementation
│   ├── tests/
│   │   ├── test_unit.py               # Unit tests
│   │   ├── test_integration.py        # Integration tests
│   │   └── test_contract.py           # Contract tests (verifies interface)
│   ├── benchmarks/                    # Performance benchmarks
│   │   ├── benchmark_suite.py
│   │   └── report-2025-10-01.md
│   └── library-evaluation.md          # If using external library
├── user-service/
│   └── ...
└── email-service/
    └── ...
```

---

## Service Lifecycle

### 1. Extraction Phase

**Trigger**: Use case specification complete

**Process**:
1. Analyze use case for required capabilities
2. Check `.claude/service-registry.md` for existing services
3. If new service needed, create `services/[name]/` directory
4. Copy `.claude/templates/service-spec.md` to `services/[name]/service-spec.md`
5. Fill in service specification

**Output**: `services/[name]/service-spec.md` (status: Draft)

---

### 2. Design Phase

**Trigger**: Service identified and spec created

**Process**:
1. Define interface (Protocol with methods, parameters, return types)
2. Define internal data models
3. Identify dependencies (minimize!)
4. List infrastructure requirements (DB, cache, APIs)
5. Document error handling strategy
6. Plan testing approach

**Output**: `services/[name]/service-spec.md` (status: Design)

---

### 3. Library Evaluation Phase (Optional)

**Trigger**: Before implementing complex functionality

**Process**:
1. Search for existing libraries (PyPI, GitHub)
2. Evaluate 3-5 candidates
3. Compare: features, quality, license, maintenance, dependencies
4. Decision: use library OR build custom
5. Document decision

**Output**: `services/[name]/library-evaluation.md`

---

### 4. Implementation Phase

**Trigger**: Design complete, ready to code

**Process** (TDD):
1. Create `interface.py` (Protocol definition)
2. Write contract tests (`tests/test_contract.py`)
3. Write unit tests for first method (RED)
4. Implement method (GREEN)
5. Refactor
6. Repeat for all methods
7. Write integration tests

**Files Created**:
- `services/[name]/interface.py`
- `services/[name]/implementation.py`
- `services/[name]/tests/test_unit.py`
- `services/[name]/tests/test_integration.py`
- `services/[name]/tests/test_contract.py`

**Output**: `services/[name]/service-spec.md` (status: Implemented)

---

### 5. Optimization Phase (Optional)

**Trigger**: Performance is critical for use case

**Process**:
1. Identify implementation strategies (e.g., in-memory vs. Redis cache)
2. Implement multiple strategies
3. Create benchmark suite
4. Run benchmarks
5. Compare results (latency, throughput, cost, complexity)
6. Choose optimal strategy
7. Document decision

**Output**:
- `services/[name]/benchmarks/report-YYYY-MM-DD.md`
- `services/[name]/service-spec.md` (status: Optimized)

---

## Service Design Principles

### 1. Single Responsibility Principle

✅ **Good**:
```
- EmailService: Send emails
- AuthService: Authenticate users
- UserService: Manage user data
```

❌ **Bad**:
```
- UtilityService: Send emails, hash passwords, validate input, log events
```

**Rule**: If service name ends in "Utility", "Helper", "Manager" → likely too broad

---

### 2. Interface-First Design

**Always define Protocol first**:

```python
from typing import Protocol, Result

class EmailServiceProtocol(Protocol):
    """Email service interface contract"""

    def send_email(
        self,
        to: EmailAddress,
        template: TemplateName,
        data: Dict[str, Any],
    ) -> Result[EmailSent, EmailError]:
        """Send templated email"""
        ...
```

**Benefits**:
- Testability (easy to mock)
- Flexibility (swap implementations)
- Clear contracts (explicit expectations)

---

### 3. Minimize Dependencies

**Dependency Budget**: Each service should depend on ≤3 other services

**Strategies to Reduce Dependencies**:
- ✅ **Pass data, not services**: `user_service.create(user_data)` not `user_service.create(auth_service)`
- ✅ **Event-based communication**: Publish events instead of calling services
- ✅ **Layered architecture**: Services in higher layers depend on lower layers only
- ❌ **Avoid circular dependencies**: A→B→C→A (use events to break cycles)

---

### 4. Stateless Preferred

**Stateless** (preferred):
```python
class EmailService:
    def send_email(self, to, subject, body):
        # No instance state
        # All data passed as parameters
        ...
```

**Stateful** (justify in spec):
```python
class SessionService:
    def __init__(self, cache):
        self._cache = cache  # Stateful: manages session cache

    def create_session(self, user_id):
        session = Session(user_id)
        self._cache.set(session.id, session)
        return session
```

**When Stateful is OK**:
- Managing connections (DB, cache)
- Caching for performance
- Session/context management

**Document in spec**:
- State stored where?
- State lifecycle (created/destroyed when?)
- Concurrency handling

---

### 5. Testability Built-In

**Dependency Injection**:
```python
class AuthService:
    def __init__(
        self,
        user_service: UserServiceProtocol,
        hash_service: HashServiceProtocol,
    ):
        self._user_service = user_service
        self._hash_service = hash_service

    def authenticate(self, email, password):
        user = self._user_service.get_by_email(email)
        if user and self._hash_service.verify(password, user.password_hash):
            return Success(user)
        return Error("Invalid credentials")
```

**Benefits**:
- Easy to mock dependencies in tests
- Can swap implementations
- Clear dependency graph

---

## Testing Strategy

### Contract Tests

**Purpose**: Verify service implements Protocol correctly

```python
def test_email_service_implements_protocol():
    service: EmailServiceProtocol = ConcreteEmailService()

    result = service.send_email(
        to=EmailAddress("test@example.com"),
        template=TemplateName("welcome"),
        data={"name": "Alice"}
    )

    # Verify return type matches interface
    assert isinstance(result, Result)
```

**Location**: `services/[name]/tests/test_contract.py`

---

### Unit Tests

**Purpose**: Test service methods in isolation with mocked dependencies

```python
def test_authenticate_with_valid_credentials():
    # Mock dependencies
    mock_user_service = Mock(UserServiceProtocol)
    mock_hash_service = Mock(HashServiceProtocol)

    mock_user_service.get_by_email.return_value = User(id=1, email="test@example.com")
    mock_hash_service.verify.return_value = True

    # Test service
    auth_service = AuthService(mock_user_service, mock_hash_service)
    result = auth_service.authenticate("test@example.com", "password123")

    assert result.is_ok()
    assert result.value.id == 1
```

**Location**: `services/[name]/tests/test_unit.py`

**Coverage Target**: 100% of service methods

---

### Integration Tests

**Purpose**: Test service with real dependencies (database, cache, etc.)

```python
def test_create_user_stores_in_database(test_db):
    # Use real database (test container or test DB)
    db_service = DatabaseService(test_db)
    user_service = UserService(db_service)

    result = user_service.create_user(
        email="test@example.com",
        name="Alice"
    )

    assert result.is_ok()

    # Verify in database
    user = test_db.query(User).filter_by(email="test@example.com").first()
    assert user is not None
    assert user.name == "Alice"
```

**Location**: `services/[name]/tests/test_integration.py`

**Setup**: Use test containers (Testcontainers library) or test database

---

### Performance Tests (Benchmarks)

**Purpose**: Measure and compare implementation strategies

**Location**: `services/[name]/benchmarks/benchmark_suite.py`

**Tools**: pytest-benchmark, locust, or custom harness

**See**: `benchmarks/report-YYYY-MM-DD.md` for results

---

## Service TDD Cycle

```
┌─────────────────────────┐
│ SERVICE EXTRACTION      │ Derive from UCs → Define interface
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ CONTRACT TEST (RED)     │ Write interface contract test → FAIL
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ UNIT TEST (RED)         │ Write unit tests for method → FAIL
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ IMPLEMENT (GREEN)       │ Implement service method → Tests PASS
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ REFACTOR                │ Improve code quality
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ INTEGRATION TEST        │ Test with real dependencies
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ OPTIMIZE (Optional)     │ Benchmark strategies → Choose best
└─────────────────────────┘
```

---

## Common Service Patterns

### Pattern 1: Repository Service

**Purpose**: Data access abstraction

```python
class UserRepositoryProtocol(Protocol):
    def get_by_id(self, user_id: int) -> Optional[User]: ...
    def get_by_email(self, email: str) -> Optional[User]: ...
    def create(self, user: User) -> User: ...
    def update(self, user: User) -> User: ...
    def delete(self, user_id: int) -> None: ...
```

**Benefits**: Swappable storage (SQL → NoSQL, in-memory for tests)

---

### Pattern 2: Adapter Service

**Purpose**: Wrap external libraries/APIs in our interface

```python
class EmailServiceProtocol(Protocol):
    def send(self, email: Email) -> Result[Sent, Error]: ...

class SendGridAdapter:
    """Adapts SendGrid library to our interface"""

    def __init__(self, api_key: str):
        self._client = SendGridClient(api_key)

    def send(self, email: Email) -> Result[Sent, Error]:
        try:
            response = self._client.send(email.to_sendgrid_format())
            return Success(Sent(message_id=response.id))
        except SendGridException as e:
            return Error(str(e))
```

**Benefits**: Isolate external dependency, easy to switch providers

---

### Pattern 3: Validator Service

**Purpose**: Centralize validation logic

```python
class ValidationServiceProtocol(Protocol):
    def validate_email(self, email: str) -> Result[Valid, Invalid]: ...
    def validate_password(self, password: str) -> Result[Valid, Invalid]: ...
```

**Benefits**: Reusable validation, consistent rules across UCs

---

### Pattern 4: Factory Service

**Purpose**: Complex object creation

```python
class OrderFactoryProtocol(Protocol):
    def create_order(
        self,
        user_id: int,
        items: List[Item],
        payment_method: PaymentMethod,
    ) -> Order:
        ...
```

**Benefits**: Encapsulate creation logic, handle complexity

---

## Error Handling Best Practices

### Use Result Type

**Preferred** (explicit error handling):
```python
def authenticate(self, email, password) -> Result[User, AuthError]:
    if not email:
        return Error(AuthError.INVALID_INPUT)

    user = self._user_repo.get_by_email(email)
    if not user:
        return Error(AuthError.USER_NOT_FOUND)

    if not self._hash.verify(password, user.password_hash):
        return Error(AuthError.INVALID_PASSWORD)

    return Success(user)
```

**Avoid** (exceptions for control flow):
```python
def authenticate(self, email, password) -> User:
    if not email:
        raise ValueError("Email required")  # Bad: exception for validation
    ...
```

**When to Use Exceptions**:
- Truly exceptional conditions (DB connection lost, out of memory)
- Unrecoverable errors
- Programming errors (should never happen in prod)

---

## Performance Optimization

### When to Optimize

**Don't optimize prematurely**:
- Build correct implementation first
- Add tests
- Measure actual performance
- Optimize if targets not met

**Triggers for Optimization**:
- Use case has strict latency requirements (< 100ms)
- High throughput needed (> 1000 req/s)
- Resource constraints (memory, CPU)
- Cost optimization (reduce cloud costs)

### Optimization Workflow

1. **Baseline**: Measure current performance
2. **Identify Bottlenecks**: Profile code
3. **Propose Strategies**: Multiple implementation approaches
4. **Implement**: Code each strategy
5. **Benchmark**: Compare strategies
6. **Choose**: Select optimal based on metrics
7. **Document**: Create `benchmarks/report-YYYY-MM-DD.md`

**See**: `.claude/templates/benchmark-report.md` template

---

## Library vs. Custom Implementation

### When to Use External Library

✅ **Use library when**:
- Standard functionality (email, auth, caching)
- Library is mature and maintained
- License compatible
- Dependencies acceptable
- Integration effort < custom build effort

### When to Build Custom

✅ **Build custom when**:
- No suitable library exists
- Requirements very specific to domain
- Library too heavy (many unused features)
- License incompatible
- Maintenance burden acceptable

**Always evaluate first**: Use `.claude/templates/library-evaluation.md`

---

## Service Documentation Checklist

Before marking service "Implemented":

- [ ] `service-spec.md` complete and up-to-date
- [ ] Interface defined (Protocol in `interface.py`)
- [ ] Implementation complete (`implementation.py`)
- [ ] Contract tests passing (`tests/test_contract.py`)
- [ ] Unit tests passing, >90% coverage (`tests/test_unit.py`)
- [ ] Integration tests passing (`tests/test_integration.py`)
- [ ] Error handling comprehensive
- [ ] Type hints present on all methods
- [ ] Docstrings with spec references
- [ ] Used by at least 1 use case (or removal planned)
- [ ] `.claude/service-registry.md` updated
- [ ] Dependencies minimized (<3 service deps)
- [ ] No circular dependencies

---

## FAQs

### Q: How do I know when to create a new service vs. extending existing?

**A**: Create new service when:
- New capability unrelated to existing services (SRP violation)
- Existing service already has >5 methods (too broad)
- Extending would create unwanted dependencies

**Extend existing service when**:
- Capability is natural extension (e.g., `UserService.update_password()`)
- Related to existing methods
- Doesn't violate SRP

---

### Q: Should every use case have its own service?

**A**: No! Services are reusable across use cases.

**Example**:
- `UserService` used by UC-001 (Registration), UC-004 (View Profile), UC-005 (Update Profile)
- Don't create: `RegistrationService`, `ProfileViewService`, `ProfileUpdateService`

---

### Q: How do I handle transactions across multiple services?

**A**: Options:

1. **Single service handles transaction** (preferred if possible)
2. **Saga pattern** (compensating transactions)
3. **Event sourcing** (eventual consistency)
4. **Two-phase commit** (if absolutely necessary, but avoid)

Document in ADR and service spec.

---

### Q: Can services call other services?

**A**: Yes, but minimize!

**Guidelines**:
- ≤3 service dependencies per service
- Avoid circular dependencies (A→B→A)
- Prefer layered architecture (higher layers call lower layers)
- Consider events to decouple

---

### Q: Where do I put database migrations?

**A**: In infrastructure service (e.g., `DatabaseService`) or separate `migrations/` directory

**Not in domain services** (UserService shouldn't manage DB schema)

---

## References

- **Service Templates**: `.claude/templates/service-spec.md`, `benchmark-report.md`, `library-evaluation.md`
- **Service Registry**: `.claude/service-registry.md`
- **Development Rules**: `.claude/development-rules.md` (Service Architecture Requirements section)
- **Complete Guide**: `docs/service-architecture.md`
- **Use Case Template**: `.claude/templates/use-case-template.md` (Services Used section)

---

**Good luck building services!** 🚀
