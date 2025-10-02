---
tier: 4
purpose: Services directory README template
reload_trigger: When creating services/ directory
estimated_read_time: 3 minutes
---

# Services Directory

**Project**: [PROJECT_NAME]
**Last Updated**: [DATE]

---

## Overview

This directory contains service implementations for this project.

**Services** are reusable components with clear interfaces that implement business logic.

**See Framework Documentation**:
- Complete guide: `docs/service-architecture.md` (comprehensive SOA guide)
- Quick reference: `.claude/quick-ref/services.md` (patterns, checklists, FAQs)
- Service registry: `.claude/service-registry.md` (central catalog)

---

## Services in This Project

| Service ID | Service Name | Status | Dependencies | Used By (UCs) | Location |
|------------|--------------|--------|--------------|---------------|----------|
| (No services yet - add as you create them) |

**Example**:
```
| Service ID | Service Name | Status | Dependencies | Used By (UCs) | Location |
|------------|--------------|--------|--------------|---------------|----------|
| SVC-001 | AuthService | Implemented | SVC-003 (ValidationService) | UC-001, UC-002 | auth-service/ |
| SVC-002 | UserService | Implemented | None | UC-001, UC-004 | user-service/ |
| SVC-003 | ValidationService | Implemented | None | SVC-001, SVC-002 | validation-service/ |
```

---

## Directory Structure

Each service follows this structure:

```
services/
├── [service-name]/
│   ├── service-spec.md           # Service specification
│   ├── interface.py               # Protocol (abstract interface)
│   ├── implementation.py          # Concrete implementation
│   ├── tests/
│   │   ├── test_unit.py          # Unit tests (isolated)
│   │   ├── test_integration.py   # Integration tests (real deps)
│   │   └── test_contract.py      # Contract tests (verify Protocol)
│   ├── benchmarks/                # Performance benchmarks (optional)
│   │   ├── benchmark_suite.py
│   │   └── report-YYYY-MM-DD.md
│   └── library-evaluation.md     # If using external library (optional)
```

---

## Quick Links

**Templates**:
- Service specification: `.claude/templates/service-spec.md`
- Benchmark report: `.claude/templates/benchmark-report.md`
- Library evaluation: `.claude/templates/library-evaluation.md`

**Documentation**:
- Service architecture guide: `docs/service-architecture.md`
- Quick reference: `.claude/quick-ref/services.md`
- Session types: `docs/session-types.md` (Session 9: Service Extraction, Session 10: Service Optimization)

**Registry**:
- Service catalog: `.claude/service-registry.md`

---

## Getting Started

### 1. Extract Services from Use Cases (Session 9)

```
Start Claude session:
"Extract services from use cases. Follow service extraction protocol."
```

Claude will:
- Analyze use case specifications
- Identify required capabilities
- Design service boundaries
- Create service specifications

### 2. Create Service Specification

```bash
# Create service directory
mkdir -p services/my-service

# Copy specification template
cp .claude/templates/service-spec.md services/my-service/service-spec.md

# Edit with your service details
# Define interface, dependencies, implementation strategies
```

### 3. Implement with TDD (Session 3)

**Service TDD Cycle**:
```
1. Extract Service → Define interface
2. Contract Test (RED) → Verify Protocol adherence
3. Unit Test (RED) → Test method
4. Implement (GREEN) → Make tests pass
5. Refactor → Improve code quality
6. Integration Test → Test with real dependencies
7. Optimize (Optional) → Benchmark if performance critical
```

### 4. Update Service Registry

After creating a service:
```
1. Add entry to table above
2. Update .claude/service-registry.md
3. Update use case specs (add service references)
```

### 5. Optimize if Needed (Session 10)

If service has performance requirements:
```
Start Claude session:
"Benchmark [ServiceName] implementations. Compare [Strategy A] vs [Strategy B]."
```

---

## Development Guidelines

### Service Design Principles

**Single Responsibility**: One service, one purpose
**Interface-First**: Define Protocol before implementation
**Minimal Dependencies**: ≤3 service dependencies per service
**Stateless Preferred**: Justify if stateful
**Test in Isolation**: Use dependency injection

### When to Create New Service

✅ **Create new when**:
- New capability unrelated to existing services
- Existing service >5 methods (too broad)
- Extending would create unwanted dependencies

❌ **Don't create when**:
- One-off utility function (use plain function)
- Already covered by existing service
- Would violate Single Responsibility Principle

### Service Naming

✅ **Good**: EmailService, AuthService, PaymentService
❌ **Bad**: UtilityService, HelperService, ManagerService

Rule: Describe purpose in one sentence. If you can't → too broad.

---

## Testing Services

### Run All Service Tests
```bash
pytest services/
```

### Run Specific Service Tests
```bash
# All tests for one service
pytest services/my-service/tests/

# Unit tests only
pytest services/my-service/tests/test_unit.py

# Integration tests only
pytest services/my-service/tests/test_integration.py
```

### Run Contract Tests (Verify Protocols)
```bash
pytest services/*/tests/test_contract.py
```

---

## Common Service Patterns

**See**: `.claude/quick-ref/services.md` for:
- Repository Service (data access)
- Adapter Service (wrap external APIs)
- Validator Service (centralize validation)
- Factory Service (complex object creation)

---

## Troubleshooting

**Q: Service has too many dependencies?**
→ Consider splitting into smaller services or using events

**Q: Circular dependency detected?**
→ Use event bus or inversion (callbacks) to break cycle

**Q: Service too broad?**
→ Apply Single Responsibility Principle, split into focused services

**Q: Should I use external library or build custom?**
→ Use `.claude/templates/library-evaluation.md` to evaluate

---

## Notes

*Add project-specific notes here as services evolve:*
- Service design decisions
- Common patterns used
- Infrastructure dependencies
- Performance considerations

---

**Framework**: Claude Development Framework v2.1
**Template Version**: 1.0
