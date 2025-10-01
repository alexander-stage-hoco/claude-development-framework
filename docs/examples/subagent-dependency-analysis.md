# Example: Dependency Analysis with Subagent

**Scenario**: Validate service dependencies after extraction to ensure clean architecture
**Complexity**: Medium
**Duration**: ~10 minutes
**Framework Features**: Dependency validation, cycle detection, layered architecture
**Subagents Used**: service-dependency-analyzer

---

## Context

**Project**: E-commerce Order Management API
**Session**: 6 (after service extraction and design)
**Current State**:
- ✅ 6 services extracted and designed
- ❌ Dependencies not validated yet
- ❌ No cycle detection performed

**User Goal**: Validate architecture before beginning TDD implementation

---

## Session Transcript

### User Request

```
User: "Validate the service dependencies before we start implementation.
Make sure there are no circular dependencies."
```

---

### Claude's Response

```
Claude: I'll use the service-dependency-analyzer subagent to validate the
architecture and detect any issues.

Launching service-dependency-analyzer subagent...
```

---

### Subagent Report (Summary)

```markdown
# Service Dependency Analysis Report

**Status**: ✅ Clean Architecture

**Summary**:
- Total Services: 6
- Circular Dependencies: 0 ✅
- Limit Violations: 0 ✅
- Dependency Layers: 3

**Dependency Graph**:

```
Layer 1 (No dependencies):
├── SVC-004: ProductService
├── SVC-005: EmailService
└── SVC-006: ValidationService

Layer 2 (Depends on Layer 1):
├── SVC-001: AuthService → SVC-006
└── SVC-003: OrderService → SVC-006

Layer 3 (Depends on Layers 1-2):
└── SVC-002: UserService → SVC-001, SVC-006
```

**Health Metrics**:
- Average dependencies per service: 0.67
- Max dependencies: 2 (well below limit of 3)
- Services with 0 dependencies: 3 (50%)

**Result**: ✅ Architecture is production-ready
```

---

### Claude Presents Results

```
Claude: ✅ Dependency analysis complete!

**Architecture Quality**: Excellent ✅

- No circular dependencies detected
- All services ≤2 dependencies (target: ≤3)
- Clean 3-layer architecture
- No refactoring needed

**Ready for TDD Implementation**

Implementation order (by layer):
1. **Layer 1**: ProductService, EmailService, ValidationService
2. **Layer 2**: AuthService, OrderService
3. **Layer 3**: UserService

Each layer can be implemented in parallel since dependencies are satisfied.

May I proceed with TDD implementation of Layer 1 services?
```

---

## Key Takeaways

**Framework Enforcement**: Architecture validated before implementation starts
**Subagent Value**: Automated cycle detection (DFS algorithm) and layer computation
**Quality Maintained**: Clean architecture guaranteed before coding begins
**Time Saved**: 10 minutes vs. 1-2 hours manual dependency analysis

---

## Files Created

- `planning/dependency-analysis-report-2024-09-30.md`

---

**Session End**: Architecture validated, ready for implementation ✅
