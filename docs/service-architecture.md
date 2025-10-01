# Service-Oriented Architecture Guide

**Framework**: Claude Development Framework v2.0
**Version**: 1.0
**Last Updated**: 2025-10-01
**Purpose**: Complete guide to service-oriented architecture in the framework

---

## Table of Contents

1. [Introduction](#introduction)
2. [Core Concepts](#core-concepts)
3. [Service Extraction](#service-extraction)
4. [Service Design](#service-design)
5. [Dependency Management](#dependency-management)
6. [Implementation](#implementation)
7. [Optimization](#optimization)
8. [Library Selection](#library-selection)
9. [UC-Service Traceability](#uc-service-traceability)
10. [Examples](#examples)

---

## Introduction

### What is Service-Oriented Architecture?

Service-Oriented Architecture (SOA) introduces a **middle layer** between use cases and implementation:

```
Use Cases (WHAT users need)
      ↓
Services (HOW system delivers)
      ↓
Implementation (CODE that executes)
```

**Benefits**:
- **Reusability**: Services used by multiple use cases
- **Testability**: Services tested in isolation
- **Maintainability**: Changes localized to services
- **Optimization**: Services benchmarked independently
- **Clarity**: Clear boundaries and responsibilities

---

### When to Use Services

✅ **Use services for**:
- Business logic (authentication, validation, calculations)
- Data access (repositories, queries)
- External integrations (email, payments, APIs)
- Cross-cutting concerns (logging, caching)

❌ **Don't use services for**:
- Simple data transformations (use functions)
- One-time scripts (not part of system)
- Pure UI logic (handled by presentation layer)

---

## Core Concepts

### Service Definition

**A service is**:
- Reusable component with clear interface
- Single responsibility (one purpose)
- Testable in isolation (dependency injection)
- Minimal dependencies on other services
- Stateless preferred, stateful justified

**Example**:
```python
class EmailServiceProtocol(Protocol):
    def send_email(
        self,
        to: EmailAddress,
        template: TemplateName,
        data: Dict[str, Any],
    ) -> Result[EmailSent, EmailError]:
        """Send templated email to recipient"""
        ...
```

---

### Services vs. Use Cases

| Aspect | Use Case | Service |
|--------|----------|---------|
| **Represents** | User need | System capability |
| **Scope** | End-to-end workflow | Specific function |
| **Reusability** | Not reusable | Highly reusable |
| **Testing** | BDD scenarios | Unit + integration tests |
| **Example** | "User Registration" | "EmailService", "AuthService" |

**Relationship**: Use cases **use** services to fulfill requirements

---

### Service Characteristics

**1. Clear Interface**:
```python
# Protocol defines contract
class ServiceProtocol(Protocol):
    def method(self, param: Type) -> Result[Success, Error]: ...
```

**2. Single Responsibility**:
- EmailService: Send emails (not: send emails + hash passwords + validate input)

**3. Dependency Injection**:
```python
class AuthService:
    def __init__(self, user_service: UserServiceProtocol):
        self._user_service = user_service  # Injected dependency
```

**4. Testability**:
```python
def test_auth():
    mock_user_service = Mock(UserServiceProtocol)
    auth = AuthService(mock_user_service)  # Easy to mock
    ...
```

---

## Service Extraction

### Extraction Process

**Input**: Use case specifications
**Output**: Service specifications

**Steps**:

1. **Analyze Use Cases**: Read all UC specifications
2. **Identify Capabilities**: Extract required capabilities
   - "send email", "validate user", "store data", "calculate total"
3. **Group Capabilities**: Group related capabilities
   - Email: send, template, track
   - Auth: register, login, logout, reset password
4. **Name Services**: Choose clear, noun-based names
   - EmailService, AuthService, UserService
5. **Define Boundaries**: Ensure Single Responsibility
6. **Check for Reuse**: Can existing service handle this?
7. **Create Specifications**: Fill service-spec.md template

---

### Extraction Example

**Use Cases**:
```
UC-001: User Registration
  Needs: validate email, hash password, store user, send welcome email

UC-002: User Login
  Needs: validate credentials, create session, log event

UC-003: Password Reset
  Needs: validate email, send reset email, update password
```

**Extracted Services**:
```
EmailService:
  - send_email(to, template, data)
  Purpose: Email delivery

AuthService:
  - hash_password(password)
  - verify_password(password, hash)
  - create_session(user_id)
  Purpose: Authentication

UserService:
  - create_user(email, password_hash)
  - get_user(email)
  - update_user(user_id, updates)
  Purpose: User data management

ValidationService:
  - validate_email(email)
  - validate_password_strength(password)
  Purpose: Input validation
```

---

### Service Naming Guidelines

✅ **Good Names** (noun-based, clear purpose):
- `EmailService`
- `AuthService`
- `PaymentService`
- `CacheService`

❌ **Bad Names** (vague, too broad):
- `UtilityService`
- `HelperService`
- `ManagerService`
- `HandlerService`

**Rule**: If you can't describe service purpose in one sentence → too broad

---

## Service Design

### Interface Design

**Always start with Protocol**:

```python
from typing import Protocol, Result

class ServiceNameProtocol(Protocol):
    """
    Service interface contract.

    This protocol defines the public API that all implementations
    must satisfy.
    """

    def method_name(
        self,
        required_param: ParamType,
        optional_param: Optional[OtherType] = None,
    ) -> Result[SuccessType, ErrorType]:
        """
        Method description.

        Specification: SVC-XXX#method-name

        Args:
            required_param: Description
            optional_param: Description (default: None)

        Returns:
            Result containing success or error

        Raises:
            SpecificError: When condition occurs
        """
        ...
```

**Benefits**:
- Testability (easy to mock)
- Flexibility (swap implementations)
- Documentation (explicit contract)
- Type safety (mypy verification)

---

### State Management

**Stateless** (preferred):
```python
class EmailService:
    """Stateless: no instance state"""

    def send_email(self, to, subject, body):
        # All data passed as parameters
        smtp_client = self._create_client()  # Create per request
        smtp_client.send(to, subject, body)
```

**Benefits**: Thread-safe, horizontally scalable, restart-safe

---

**Stateful** (justify in spec):
```python
class CacheService:
    """Stateful: manages cache connection"""

    def __init__(self, redis_client):
        self._redis = redis_client  # Persistent connection

    def get(self, key):
        return self._redis.get(key)
```

**When OK**:
- Connection pooling (DB, cache)
- Performance caching
- Session management

**Document**: State stored where? Lifecycle? Concurrency handling?

---

### Data Models

**Internal models** (not exposed):
```python
@dataclass(frozen=True)
class InternalUserModel:
    """Internal representation, NOT in public interface"""
    id: int
    email: str
    password_hash: str
    created_at: datetime
```

**Public models** (exposed in interface):
```python
@dataclass(frozen=True)
class PublicUser:
    """Returned by service methods"""
    id: int
    email: str
    # Note: password_hash NOT exposed
```

**Rule**: Don't leak internal details through interface

---

## Dependency Management

### Dependency Principles

**1. Minimize Dependencies**: Each service ≤3 service dependencies

**2. Layered Architecture**: Higher layers depend on lower layers only

```
Layer 3 (Application):  AuthService, OrderService
         ↓
Layer 2 (Domain):       UserService, EmailService
         ↓
Layer 1 (Infrastructure): DatabaseService, CacheService
```

**3. No Circular Dependencies**: A→B→C→A (forbidden!)

**4. Justify Dependencies**: Document why each dependency exists

---

### Dependency Injection

**Constructor Injection** (preferred):
```python
class AuthService:
    def __init__(
        self,
        user_service: UserServiceProtocol,
        hash_service: HashServiceProtocol,
        session_service: SessionServiceProtocol,
    ):
        self._user_service = user_service
        self._hash_service = hash_service
        self._session_service = session_service

    def authenticate(self, email, password):
        user = self._user_service.get_by_email(email)
        if user and self._hash_service.verify(password, user.password_hash):
            return self._session_service.create(user.id)
        return Error("Invalid credentials")
```

**Benefits**:
- Explicit dependencies (visible in constructor)
- Easy to mock in tests
- Immutable after construction

---

### Decoupling Strategies

**Problem**: Service A needs to notify Service B, but direct dependency creates coupling

**Solution 1: Event Bus**:
```python
class OrderService:
    def create_order(self, order):
        # Create order
        saved_order = self._repository.save(order)

        # Publish event (no dependency on AuditService!)
        self._event_bus.publish(OrderCreated(order_id=saved_order.id))

        return saved_order

class AuditService:
    def __init__(self, event_bus):
        event_bus.subscribe(OrderCreated, self.on_order_created)

    def on_order_created(self, event: OrderCreated):
        self.log_audit("Order created", event.order_id)
```

**Benefits**: A and B decoupled, no circular dependency

---

**Solution 2: Inversion (Lower Layer Calls Upper via Callback)**:
```python
class UserService:
    def create_user(self, user, on_created: Callable[[User], None]):
        saved_user = self._repository.save(user)
        on_created(saved_user)  # Callback to upper layer
        return saved_user

# Upper layer
auth_service.register(email, password, lambda user: email_service.send_welcome(user))
```

---

**Solution 3: Pass Data, Not Services**:
```python
# ❌ Bad: Service dependency
class OrderService:
    def __init__(self, user_service):
        self._user_service = user_service

    def create_order(self, user_id):
        user = self._user_service.get(user_id)  # Depends on UserService
        ...

# ✅ Good: Data dependency
class OrderService:
    def create_order(self, user: User):  # User passed in
        # No UserService dependency!
        ...
```

---

## Implementation

### Service TDD Cycle

```
1. Extract Service from UCs → Define interface
           ↓
2. Write Contract Test (RED) → Verify Protocol adherence
           ↓
3. Write Unit Test (RED) → Test first method
           ↓
4. Implement (GREEN) → Make tests pass
           ↓
5. Refactor → Improve code quality
           ↓
6. Integration Test → Test with real dependencies
           ↓
7. Optimize (Optional) → Benchmark if performance critical
```

---

### Contract Test Example

```python
def test_email_service_implements_protocol():
    """Verify service adheres to protocol"""
    service: EmailServiceProtocol = ConcreteEmailService()

    # Call method
    result = service.send_email(
        to=EmailAddress("test@example.com"),
        template=TemplateName("welcome"),
        data={"name": "Alice"}
    )

    # Verify return type matches interface
    assert isinstance(result, Result)
    if result.is_ok():
        assert isinstance(result.value, EmailSent)
    else:
        assert isinstance(result.error, EmailError)
```

---

### Unit Test Example

```python
def test_authenticate_with_valid_credentials():
    # Arrange: Mock dependencies
    mock_user_service = Mock(UserServiceProtocol)
    mock_hash_service = Mock(HashServiceProtocol)
    mock_session_service = Mock(SessionServiceProtocol)

    mock_user_service.get_by_email.return_value = User(
        id=1,
        email="test@example.com",
        password_hash="hashed"
    )
    mock_hash_service.verify.return_value = True
    mock_session_service.create.return_value = Session(token="abc123")

    # Act: Test service
    auth_service = AuthService(
        mock_user_service,
        mock_hash_service,
        mock_session_service
    )
    result = auth_service.authenticate("test@example.com", "password123")

    # Assert
    assert result.is_ok()
    assert result.value.token == "abc123"
    mock_hash_service.verify.assert_called_once_with("password123", "hashed")
```

---

### Integration Test Example

```python
def test_create_user_integration(test_db):
    """Test with real database"""
    # Arrange: Use real database service
    db_service = DatabaseService(test_db)
    user_service = UserService(db_service)

    # Act
    result = user_service.create_user(
        email="test@example.com",
        name="Alice",
        password_hash="hashed"
    )

    # Assert
    assert result.is_ok()

    # Verify in database
    user = test_db.query(User).filter_by(email="test@example.com").first()
    assert user is not None
    assert user.name == "Alice"
```

---

## Optimization

### When to Optimize

**Don't optimize prematurely!**

**Optimize when**:
- UC has strict performance requirements (< 100ms latency)
- High throughput needed (> 1000 req/s)
- Cost optimization opportunity (reduce cloud costs)
- Multiple implementation strategies exist

---

### Optimization Workflow

1. **Baseline**: Measure current performance
2. **Identify Strategies**: List alternative implementations
3. **Implement**: Code each strategy
4. **Benchmark**: Run performance tests
5. **Compare**: Analyze latency, throughput, cost, complexity
6. **Choose**: Select optimal strategy
7. **Document**: Create `benchmarks/report-YYYY-MM-DD.md`

---

### Benchmark Example

**Scenario**: Caching strategy for UserService

**Strategies**:
- Strategy A: In-memory dict
- Strategy B: Redis
- Strategy C: Memcached

**Benchmark Results**:
```
| Strategy | Latency (p95) | Throughput | Cost | Complexity |
|----------|--------------|------------|------|------------|
| A        | 0.3ms        | 50k ops/s  | $0   | Low        |
| B        | 3.1ms        | 10k ops/s  | $30  | Medium     |
| C        | 2.1ms        | 15k ops/s  | $20  | Medium     |
```

**Decision**: Strategy B (Redis) despite higher latency
**Rationale**:
- UC requires cache persistence across restarts
- Distributed caching needed for multi-instance deployment
- Latency acceptable (UC requirement: < 10ms)
- Cost justified by reliability

**See**: `.claude/templates/benchmark-report.md` for template

---

## Library Selection

### Evaluation Process

Before implementing complex functionality, evaluate existing libraries:

1. **Search**: PyPI, GitHub, awesome lists
2. **Shortlist**: 3-5 candidates
3. **Evaluate**: Features, quality, license, maintenance, dependencies
4. **Compare**: Matrix comparison
5. **Decide**: Library OR custom implementation
6. **Document**: Create `library-evaluation.md`

---

### Evaluation Criteria

| Criterion | Weight | Assessment |
|-----------|--------|------------|
| Feature coverage | 30% | Does it do what we need? |
| Code quality | 20% | Type hints? Tests? Docs? |
| Maintenance | 20% | Active development? Recent commits? |
| Documentation | 15% | Comprehensive? Examples? |
| Dependencies | 10% | Lightweight? Secure? |
| License | 5% | Compatible? Commercial use allowed? |

---

### Decision Matrix

✅ **Use library when**:
- Standard functionality (email, auth, caching)
- Library mature and maintained
- License compatible
- Integration effort < custom build effort
- Total Cost of Ownership (TCO) lower

✅ **Build custom when**:
- No suitable library exists
- Requirements very specific
- Library too heavy (many unused features)
- License incompatible
- Long-term maintenance acceptable

**See**: `.claude/templates/library-evaluation.md` for template

---

## UC-Service Traceability

### Requirement

**Every use case MUST reference services it uses**

**Why?**:
- Ensures UCs are implementable (not just ideas)
- Identifies missing services
- Validates service reusability
- Challenges serviceless UCs

---

### UC Services Section

**In every use case specification**:

```markdown
## Services Used

| Service | Methods Used | Purpose |
|---------|-------------|---------|
| AuthService | authenticate(), create_session() | User authentication |
| UserService | get_user(), update_last_login() | Retrieve user data |
| EmailService | send_email() | Login notification |
```

**Service Flow**:
```
1. User submits credentials
   ↓
2. AuthService.authenticate(email, password)
   ├─ Success → Continue
   └─ Failure → Return error
   ↓
3. UserService.get_user(user_id)
   ↓
4. AuthService.create_session(user_id)
   ↓
5. EmailService.send_email(user, "login_notification")
   ↓
6. Return success
```

---

### Challenging Serviceless UCs

**If UC has no services**:

**Ask**:
1. Is this really a use case or just UI change?
2. Is there hidden business logic?
3. Should it use an existing service?
4. Does it need a new service?

**Valid Serviceless UCs**:
- Pure UI changes (update theme, change language)
- Read-only views (no business logic)
- Navigation flows

**Document justification**: "No services needed: Pure UI change, no backend interaction"

---

## Examples

### Example 1: Complete Service (EmailService)

**1. Extracted from UCs**:
```
UC-001: User Registration → Send welcome email
UC-003: Password Reset → Send reset email
UC-010: Notification → Send notification email
```

**2. Service Specification**:
```python
# services/email-service/interface.py

from typing import Protocol, Result

class EmailServiceProtocol(Protocol):
    """Email delivery service"""

    def send_email(
        self,
        to: EmailAddress,
        template: TemplateName,
        data: Dict[str, Any],
        priority: Priority = Priority.NORMAL,
    ) -> Result[EmailSent, EmailError]:
        """
        Send templated email.

        Specification: SVC-005#send-email
        """
        ...
```

**3. Implementation**:
```python
# services/email-service/implementation.py

from emails import Message  # External library

class SendGridEmailService:
    """Concrete implementation using SendGrid"""

    def __init__(self, api_key: str):
        self._api_key = api_key

    def send_email(
        self,
        to: EmailAddress,
        template: TemplateName,
        data: Dict[str, Any],
        priority: Priority = Priority.NORMAL,
    ) -> Result[EmailSent, EmailError]:
        try:
            message = Message(
                subject=template.subject,
                html=template.render(data),
                mail_from=("noreply@example.com", "MyApp"),
            )
            response = message.send(
                to=str(to),
                smtp={"host": "smtp.sendgrid.net", "user": self._api_key}
            )
            if response.status_code == 250:
                return Success(EmailSent(message_id=response.message_id))
            else:
                return Error(EmailError(f"SMTP error: {response.status_code}"))
        except Exception as e:
            return Error(EmailError(str(e)))
```

**4. Tests**:
```python
# services/email-service/tests/test_unit.py

def test_send_email_success():
    service = SendGridEmailService(api_key="test_key")

    result = service.send_email(
        to=EmailAddress("test@example.com"),
        template=TemplateName("welcome"),
        data={"name": "Alice"}
    )

    assert result.is_ok()
    assert result.value.message_id is not None
```

**5. Service Registry**:
```markdown
| Service ID | Name | Status | Dependencies | Used By (UCs) |
|------------|------|--------|--------------|---------------|
| SVC-005 | EmailService | Implemented | None | UC-001, UC-003, UC-010 |
```

---

### Example 2: Service Dependency (AuthService → UserService)

**AuthService needs UserService to verify user exists**:

```python
class AuthService:
    def __init__(
        self,
        user_service: UserServiceProtocol,  # Dependency
        hash_service: HashServiceProtocol,
        session_service: SessionServiceProtocol,
    ):
        self._user_service = user_service
        self._hash_service = hash_service
        self._session_service = session_service

    def authenticate(
        self,
        email: str,
        password: str,
    ) -> Result[Session, AuthError]:
        # Use UserService to get user
        user_result = self._user_service.get_by_email(email)
        if user_result.is_err():
            return Error(AuthError.USER_NOT_FOUND)

        user = user_result.value

        # Verify password
        if not self._hash_service.verify(password, user.password_hash):
            return Error(AuthError.INVALID_PASSWORD)

        # Create session
        session = self._session_service.create(user.id)
        return Success(session)
```

**Dependency Graph**:
```
AuthService
├── UserService
├── HashService
└── SessionService
```

**Dependency Count**: 3 (at limit, don't add more!)

---

## Quick Reference

### Service Extraction Checklist

- [ ] Read all use case specifications
- [ ] Identify required capabilities
- [ ] Group related capabilities
- [ ] Name services (noun-based, clear)
- [ ] Check for existing services (reuse!)
- [ ] Create `services/[name]/service-spec.md`
- [ ] Update `.claude/service-registry.md`

---

### Service Design Checklist

- [ ] Define Protocol interface
- [ ] Specify state management strategy
- [ ] Define internal data models
- [ ] List dependencies (minimize!)
- [ ] Document infrastructure requirements
- [ ] Plan error handling
- [ ] Design testing strategy

---

### Service Implementation Checklist

- [ ] Write contract tests (verify Protocol)
- [ ] Write unit tests (TDD)
- [ ] Implement service methods
- [ ] Write integration tests
- [ ] Document in service-spec.md
- [ ] Update service registry
- [ ] Add to UCs (Services Used section)

---

### Service Optimization Checklist

- [ ] Identify implementation strategies
- [ ] Implement multiple strategies
- [ ] Create benchmark suite
- [ ] Run benchmarks
- [ ] Compare results
- [ ] Choose optimal strategy
- [ ] Document in `benchmarks/report-YYYY-MM-DD.md`

---

## Quick Reference

**For operational quick reference**, see `.claude/quick-ref/services.md`:
- Common service patterns (Repository, Adapter, Validator, Factory)
- Service naming guidelines
- Error handling patterns
- FAQs (when to create vs extend, transactions, etc.)
- Quick commands
- Service documentation checklist

---

## References

- **Quick Reference**: `.claude/quick-ref/services.md` - Patterns, checklists, FAQs
- **Templates**: `.claude/templates/service-spec.md`, `benchmark-report.md`, `library-evaluation.md`
- **Service Registry**: `.claude/templates/service-registry.md` - Central catalog template
- **Services README Template**: `.claude/templates/services-README-template.md` - For created projects
- **Development Rules**: `.claude/templates/development-rules.md` (Service Architecture Requirements)
- **Session Types**: `docs/session-types.md` (Service Extraction, Service Optimization sessions)

**Note**: `services/` directory does NOT exist in template root. It is created in new projects by `init-project.sh`.

---

**Framework Version**: 2.0
**Last Updated**: 2025-10-01
**Maintained By**: Claude Development Framework
