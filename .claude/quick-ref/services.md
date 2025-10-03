---
tier: 4
purpose: Service patterns quick reference
reload_trigger: When designing services (quick ref)
estimated_read_time: 5 minutes
---

# Services Quick Reference

**Framework**: Claude Development Framework v2.2
**Purpose**: Quick operational reference for service development
**Complete Guide**: `docs/service-architecture.md`

---

## Common Service Patterns

### 1. Repository Service
**Purpose**: Data access abstraction

```python
class UserRepositoryProtocol(Protocol):
    def get_by_id(self, user_id: int) -> Optional[User]: ...
    def get_by_email(self, email: str) -> Optional[User]: ...
    def create(self, user: User) -> User: ...
    def update(self, user: User) -> User: ...
    def delete(self, user_id: int) -> None: ...
```

### 2. Adapter Service
**Purpose**: Wrap external libraries/APIs

```python
class EmailServiceProtocol(Protocol):
    def send(self, email: Email) -> Result[Sent, Error]: ...

class SendGridAdapter:
    def __init__(self, api_key: str):
        self._client = SendGridClient(api_key)

    def send(self, email: Email) -> Result[Sent, Error]:
        try:
            response = self._client.send(email.to_sendgrid_format())
            return Success(Sent(message_id=response.id))
        except SendGridException as e:
            return Error(str(e))
```

### 3. Validator Service
**Purpose**: Centralize validation logic

```python
class ValidationServiceProtocol(Protocol):
    def validate_email(self, email: str) -> Result[Valid, Invalid]: ...
    def validate_password(self, password: str) -> Result[Valid, Invalid]: ...
```

### 4. Factory Service
**Purpose**: Complex object creation

```python
class OrderFactoryProtocol(Protocol):
    def create_order(
        self,
        user_id: int,
        items: List[Item],
        payment_method: PaymentMethod,
    ) -> Order: ...
```

---

## Service Naming Guidelines

✅ **Good Names** (noun-based, clear):
- EmailService
- AuthService
- PaymentService
- CacheService

❌ **Bad Names** (vague, too broad):
- UtilityService
- HelperService
- ManagerService
- HandlerService

**Rule**: If you can't describe purpose in one sentence → too broad

---

## Error Handling Pattern

**Use Result Type** (preferred):
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

**When to Use Exceptions**:
- Truly exceptional conditions (DB connection lost)
- Unrecoverable errors
- Programming errors (should never happen in prod)

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
- [ ] Used by at least 1 use case
- [ ] `.claude/service-registry.md` updated
- [ ] Dependencies minimized (<3 service deps)
- [ ] No circular dependencies

---

## FAQs

### Q: How do I know when to create a new service vs. extending existing?

**Create new service when**:
- New capability unrelated to existing services
- Existing service already has >5 methods (too broad)
- Extending would create unwanted dependencies

**Extend existing service when**:
- Capability is natural extension
- Related to existing methods
- Doesn't violate SRP

### Q: Should every use case have its own service?

**No!** Services are reusable across use cases.

**Example**:
- UserService used by UC-001 (Registration), UC-004 (View Profile), UC-005 (Update Profile)
- Don't create: RegistrationService, ProfileViewService, ProfileUpdateService

### Q: How do I handle transactions across multiple services?

**Options**:
1. **Single service handles transaction** (preferred if possible)
2. **Saga pattern** (compensating transactions)
3. **Event sourcing** (eventual consistency)
4. **Two-phase commit** (if absolutely necessary, but avoid)

Document in ADR and service spec.

### Q: Can services call other services?

**Yes, but minimize!**

**Guidelines**:
- ≤3 service dependencies per service
- Avoid circular dependencies (A→B→A)
- Prefer layered architecture
- Consider events to decouple

### Q: Where do I put database migrations?

**In infrastructure service** (e.g., DatabaseService) or separate `migrations/` directory

**Not in domain services** (UserService shouldn't manage DB schema)

---

## Quick Commands

### Service Extraction
```bash
# Session 9: Service Extraction
"Extract services from use cases. Follow service extraction protocol."
```

### Service Optimization
```bash
# Session 10: Service Optimization
"Benchmark [ServiceName] implementations. Compare [Strategy A] vs [Strategy B]."
```

### Create Service Specification
```bash
# Copy template
cp .claude/templates/service-spec.md services/my-service/service-spec.md

# Edit with service details
```

### Run Service Tests
```bash
# Unit tests
pytest services/my-service/tests/test_unit.py

# Integration tests
pytest services/my-service/tests/test_integration.py

# Contract tests
pytest services/my-service/tests/test_contract.py

# All service tests
pytest services/my-service/tests/
```

---

## Service Dependency Rules

**Dependency Budget**: ≤3 service dependencies per service

**Decoupling Strategies**:
1. **Pass data, not services**: `user_service.create(user_data)` not `user_service.create(auth_service)`
2. **Event-based communication**: Publish events instead of calling services
3. **Layered architecture**: Higher layers depend on lower layers only

**Check Dependencies**:
```bash
# See dependency graph
grep "def __init__" services/*/implementation.py
```

---

## Service Testing Strategy

### Contract Tests (Verify Protocol)
```python
def test_service_implements_protocol():
    service: ServiceProtocol = ConcreteService()
    result = service.method(param="value")
    assert isinstance(result, Result)
```

### Unit Tests (Isolated with Mocks)
```python
def test_method_with_mocked_deps():
    mock_dep = Mock(DepProtocol)
    service = ConcreteService(mock_dep)
    result = service.method("input")
    assert result.is_ok()
```

### Integration Tests (Real Dependencies)
```python
def test_with_real_database(test_db):
    db_service = DatabaseService(test_db)
    service = ConcreteService(db_service)
    result = service.method("input")
    assert result.is_ok()
    # Verify in database
```

---

## When to Optimize

**Don't optimize prematurely!**

**Optimize when**:
- UC has strict performance requirements (< 100ms)
- High throughput needed (> 1000 req/s)
- Resource constraints (memory, CPU)
- Cost optimization opportunity

**Optimization Workflow**:
1. Baseline measurement
2. Identify strategies
3. Implement alternatives
4. Benchmark (see `.claude/templates/benchmark-report.md`)
5. Choose optimal
6. Document decision

---

## Templates Reference

| Template | Location | Purpose |
|----------|----------|---------|
| Service Spec | `.claude/templates/service-spec.md` | Complete service specification |
| Benchmark Report | `.claude/templates/benchmark-report.md` | Performance comparison |
| Library Evaluation | `.claude/templates/library-evaluation.md` | Library selection |
| Service Registry | `.claude/templates/service-registry.md` | Central catalog |

---

## Complete Documentation

**See**: `docs/service-architecture.md` for comprehensive 900+ line guide covering:
- Service extraction methodology
- Interface design principles
- Dependency management patterns
- Complete examples
- Anti-patterns

---

**Framework Version**: 2.0
**Last Updated**: 2025-10-01
