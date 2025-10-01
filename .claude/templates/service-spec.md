# Service Specification: [SERVICE_NAME]

**Service ID**: SVC-XXX
**Version**: 1.0
**Status**: [Draft | Design | Implemented | Optimized]
**Last Updated**: [DATE]
**Owner**: [Team/Person]

---

## Purpose

[Single sentence describing what this service does and why it exists]

**Business Value**: [How this service supports business goals]

---

## Scope

**In Scope** (What this service handles):
- [Capability 1]
- [Capability 2]
- [Capability 3]

**Out of Scope** (Handled by other services or not needed):
- [What this service explicitly does NOT do]
- [Responsibilities delegated to other services]

---

## Interface

### Public Methods

```python
from typing import Protocol, Result

class [ServiceName]Protocol(Protocol):
    """
    Service interface contract.

    This protocol defines the public API that all implementations must satisfy.
    Use dependency injection to provide concrete implementations.
    """

    def method_name(
        self,
        param: ParamType,
        optional_param: Optional[OtherType] = None,
    ) -> Result[SuccessType, ErrorType]:
        """
        Brief description of what this method does.

        Specification: SVC-XXX#method-name

        Args:
            param: Description of required parameter
            optional_param: Description of optional parameter (default: None)

        Returns:
            Result containing:
            - Success: SuccessType instance with [describe fields]
            - Error: ErrorType with error code and message

        Raises:
            SpecificError: When [condition occurs]
            ValidationError: When [invalid input provided]

        Example:
            >>> service = ConcreteService()
            >>> result = service.method_name(param="value")
            >>> if result.is_ok():
            ...     print(result.value)
        """
        ...

    def another_method(self, arg: Type) -> Result[Success, Error]:
        """[Method description]"""
        ...
```

---

## State Management

**Strategy**: [Stateless | Stateful]

### If Stateless
- No state maintained between calls
- Thread-safe by design
- Horizontally scalable
- Restart-safe

### If Stateful
- **State stored in**: [Memory | Database | Cache | External Service]
- **State scope**: [Per-request | Per-user | Per-session | Global]
- **State lifecycle**:
  - Created when: [Condition]
  - Updated when: [Condition]
  - Destroyed when: [Condition]
- **State persistence**: [Volatile | Persisted | Hybrid]
- **Concurrency**: [How concurrent access is handled]

---

## Internal Data Model

### Domain Models (Internal Only)

```python
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class InternalModel:
    """
    Internal representation used within service.
    NOT exposed in public interface.
    """
    field_one: str
    field_two: int
    optional_field: Optional[str] = None

    def validate(self) -> None:
        """Validate invariants"""
        if self.field_two < 0:
            raise ValueError("field_two must be non-negative")
```

**Design Rationale**: [Why these models? What problem do they solve?]

---

## Dependencies

### Service Dependencies

**Minimize dependencies!** Each dependency increases coupling and complexity.

| Service | Used For | Justification | Methods Used |
|---------|----------|---------------|--------------|
| ServiceA | [Purpose] | [Why needed?] | `method_x()`, `method_y()` |
| ServiceB | [Purpose] | [Why can't avoid?] | `method_z()` |

**Dependency Injection Pattern**:
```python
class ConcreteService:
    def __init__(
        self,
        service_a: ServiceAProtocol,
        service_b: ServiceBProtocol,
    ):
        self._service_a = service_a
        self._service_b = service_b
```

### Infrastructure Dependencies

| Infrastructure | Purpose | Configuration |
|----------------|---------|---------------|
| PostgreSQL | Primary data store | Tables: users, sessions |
| Redis | Caching layer | Keys: `user:*`, `session:*` |
| SMTP Server | Email delivery | Host: smtp.example.com |
| External API | [Third-party service] | Endpoint: https://api.example.com |

---

## Implementation Strategies

### Strategy 1: [Current/Recommended Strategy Name]

**Approach**: [Describe the implementation approach]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Performance** (if benchmarked):
- Latency: p50=[X]ms, p95=[Y]ms, p99=[Z]ms
- Throughput: [N] ops/sec
- Memory: [M] MB
- Cost: [C] $/month

**When to Use**: [Conditions that favor this strategy]

---

### Strategy 2: [Alternative Strategy Name]

**Approach**: [Describe alternative approach]

**Pros**:
- [Advantage 1]

**Cons**:
- [Disadvantage 1]

**Performance**:
- [Metrics if available]

**When to Use**: [Conditions that favor this strategy]

---

### Decision

**Chosen Strategy**: [Strategy Name]

**Rationale**: [Why this strategy was chosen over alternatives]

**Benchmark Reference**: See `benchmarks/report-YYYY-MM-DD.md` (if applicable)

---

## Library Usage

**Library**: [Library name and version] OR [Custom implementation]

**Reason for Choice**: [Why this library? OR Why custom implementation?]

**Evaluation**: See `library-evaluation.md` (if evaluation was conducted)

### If Using External Library

**Integration Approach**:
- Wrap library in adapter implementing our Protocol
- Isolate library-specific code
- Test adapter thoroughly
- Document library-specific quirks

**Example**:
```python
from external_library import ExternalClient

class LibraryAdapter:
    """Adapts ExternalClient to our ServiceProtocol"""

    def __init__(self, client: ExternalClient):
        self._client = client

    def our_method(self, param: Type) -> Result[Success, Error]:
        """Implement our interface using library"""
        try:
            result = self._client.library_method(param)
            return Success(result)
        except LibraryException as e:
            return Error(str(e))
```

---

## Error Handling

### Error Types

| Error Condition | Error Class | HTTP Status | Recovery Strategy |
|----------------|-------------|-------------|-------------------|
| Invalid input | ValidationError | 400 Bad Request | User corrects input |
| Resource not found | NotFoundError | 404 Not Found | Check resource exists |
| Permission denied | AuthorizationError | 403 Forbidden | Request elevated access |
| Rate limit exceeded | RateLimitError | 429 Too Many Requests | Retry with backoff |
| External service down | ServiceUnavailableError | 503 Service Unavailable | Retry with exponential backoff |
| Internal error | InternalError | 500 Internal Server Error | Log, alert, investigate |

### Error Handling Strategy

```python
class ServiceError(Exception):
    """Base class for all service errors"""
    error_code: str
    message: str

class ValidationError(ServiceError):
    """Input validation failed"""
    pass

class RetryableError(ServiceError):
    """Error that should trigger retry logic"""
    pass
```

**Retry Logic**:
- Retryable errors: [List which errors]
- Max retries: [N]
- Backoff strategy: [Exponential | Linear | Fixed]
- Timeout: [X seconds]

---

## Testing Strategy

### Unit Tests

**Scope**: Test individual methods in isolation with mocked dependencies

**Focus**:
- Input validation
- Business logic correctness
- Error handling
- Edge cases

**Example**:
```python
def test_method_with_valid_input():
    service = ConcreteService(mock_dep_a, mock_dep_b)
    result = service.method("valid_input")
    assert result.is_ok()
    assert result.value.field == "expected"
```

---

### Integration Tests

**Scope**: Test service with real dependencies (database, cache, etc.)

**Focus**:
- End-to-end workflows
- Dependency interactions
- State management
- Performance under load

**Setup**: Use test containers or test database

---

### Contract Tests

**Scope**: Verify service adheres to Protocol interface

**Focus**:
- All protocol methods implemented
- Return types match interface
- Error types match specification

**Example**:
```python
def test_service_implements_protocol():
    service: ServiceProtocol = ConcreteService()
    result = service.method("input")
    assert isinstance(result, Result)
```

---

### Performance Tests (Benchmarks)

**Scope**: Measure performance characteristics

**Metrics**:
- Latency (p50, p95, p99)
- Throughput (requests/sec)
- Memory usage
- CPU usage
- Resource utilization

**Tool**: pytest-benchmark or custom harness

**Location**: `benchmarks/benchmark_[service_name].py`

---

## Used By

### Use Cases

List all use cases that depend on this service:

| Use Case ID | Use Case Name | Methods Used | Purpose |
|-------------|---------------|--------------|---------|
| UC-001 | User Registration | `create_user()`, `send_welcome_email()` | Register new users |
| UC-002 | User Login | `authenticate()`, `create_session()` | User authentication |

**Traceability**: Every use case MUST reference the services it uses.

---

### Other Services

List services that depend on this service:

| Service ID | Service Name | Why Dependency Exists |
|------------|--------------|----------------------|
| SVC-005 | AuthService | Uses UserService to verify user exists |

**Coupling Alert**: If this list grows >3 items, consider:
- Is this service too broad? (God Service anti-pattern)
- Can we split into smaller services?
- Are dependencies justified?

---

## Metrics & Monitoring

### Performance Targets

| Metric | Target | Alert Threshold |
|--------|--------|----------------|
| Latency (p95) | < [X]ms | > [Y]ms |
| Latency (p99) | < [X]ms | > [Y]ms |
| Throughput | > [N] ops/sec | < [M] ops/sec |
| Error rate | < [Z]% | > [W]% |
| Availability | > 99.9% | < 99.5% |

### Monitoring

**Metrics to Collect**:
- Request count (by method, status)
- Latency distribution
- Error rate (by error type)
- Dependency call duration
- Resource usage (CPU, memory)

**Dashboards**: [Link to Grafana/monitoring dashboard if exists]

**Alerts**: [Link to alert configuration]

---

## Open Questions

Questions requiring stakeholder/technical decisions:

- [ ] **Question 1**: [Specific question requiring clarification]
  - **Impact**: [Why this matters, what's blocked]
  - **Options**: [Potential answers or approaches]
  - **Decision by**: [Date or milestone]

- [ ] **Question 2**: [Another unresolved question]
  - **Impact**: [Impact description]
  - **Options**: [Options to consider]
  - **Decision by**: [Date]

---

## Security Considerations

- **Authentication**: [How is caller authenticated?]
- **Authorization**: [How are permissions checked?]
- **Input Validation**: [What validation is performed?]
- **Output Sanitization**: [Is output sanitized?]
- **Data Encryption**: [Is sensitive data encrypted?]
- **Audit Logging**: [What is logged for audit?]
- **Rate Limiting**: [Is rate limiting applied?]
- **Secret Management**: [How are secrets handled?]

---

## Change History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| YYYY-MM-DD | 1.0 | [Name] | Initial service specification |
| YYYY-MM-DD | 1.1 | [Name] | Added error handling for [scenario] |

---

## Notes

### Design Rationale

[Why was this service designed this way? What alternatives were considered?]

### Known Limitations

[What are the current limitations? What technical debt exists?]

### Future Enhancements

[Features or improvements planned for future versions]

- [ ] Enhancement 1: [Description]
- [ ] Enhancement 2: [Description]

### References

- **Research**: `research/learnings/[topic].md`
- **ADRs**: `ADR-XXX` ([Decision name])
- **External Docs**: [Links to library docs, RFCs, etc.]
- **Related Services**: SVC-YYY, SVC-ZZZ

---

**Template Version**: 1.0
**Framework**: Claude Development Framework v2.0
