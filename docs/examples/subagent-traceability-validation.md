# Example: Traceability Validation with Subagent

**Scenario**: After services implemented, validate UC-Service traceability is complete
**Complexity**: Medium
**Duration**: ~15 minutes
**Framework Features**: UC-Service traceability, bidirectional validation
**Subagents Used**: uc-service-tracer

---

## Context

**Project**: E-commerce Order Management API
**Session**: 12 (after most services implemented)
**Current State**:
- ✅ 4 of 6 services implemented
- ⚠️ Some UCs may have outdated service references
- ❌ No traceability validation yet

**User Goal**: Ensure all use cases properly reference the services they use

---

## Session Transcript

### User Request

```
User: "We've implemented several services. Please validate that all use cases
correctly reference their services and there are no orphan services."
```

---

### Claude's Response

```
Claude: I'll use the uc-service-tracer subagent to validate UC-Service
traceability in both directions.

Launching uc-service-tracer subagent...
```

---

### Subagent Report (Summary)

```markdown
# UC-Service Traceability Report

**Status**: ⚠️ Issues Found

**Summary**:
- Total Use Cases: 5
- UCs with Service References: 4/5 (80%)
- Orphan Services: 0
- Traceability Violations: 2

---

## Issues Detected

### ❌ Missing Service References

**UC-004: View Order History**
- **Issue**: No "Services Used" section found
- **Expected Services**: AuthService, OrderService
- **Action Required**: Add service references

### ⚠️ Bidirectional Mismatch

**SVC-002: UserService**
- **UC References**: UC-001, UC-002 (from UC specs)
- **Service Declares**: UC-001 only (from service-spec.md)
- **Mismatch**: UC-002 references UserService but service spec doesn't list UC-002
- **Action Required**: Update service-spec.md to include UC-002

---

## Recommendations

### Priority 1: Fix UC-004 (Missing References)
- Add "Services Used" section
- **Effort**: 10 minutes
- **Impact**: High (complete traceability)

### Priority 2: Fix SVC-002 Mismatch
- Update service specification
- **Effort**: 5 minutes
- **Impact**: High (data integrity)

---

**Traceability Coverage**: 80% (target: 100%)
```

---

### Claude Presents Results

```
Claude: ⚠️ Traceability validation found 2 issues:

1. **UC-004** is missing service references
2. **UserService** spec doesn't list UC-002 (but UC-002 references it)

**I cannot proceed with further implementation** (Rule #1: Specifications Are Law)
until these are fixed.

Would you like me to:
1. Fix both issues now? (15 minutes)
2. Or discuss what services UC-004 actually needs?
```

---

### User Response

```
User: "Yes, fix both issues."
```

---

### Claude Fixes Issues

```
Claude: Fixing traceability violations...

**Fix 1: UC-004 Service References**

Updated `specs/use-cases/UC-004-view-order-history.md`:

## Services Used

| Service | Methods Used | Purpose |
|---------|-------------|---------|
| AuthService | `validate_session()` | Verify user is authenticated |
| OrderService | `get_user_orders()` | Retrieve user's order history |

✅ UC-004 fixed

**Fix 2: UserService Spec Update**

Updated `services/user-service/service-spec.md`:

Used By: UC-001 (User Registration), UC-002 (User Login)

✅ SVC-002 fixed

**Re-running uc-service-tracer to verify...**

✅ All checks pass! 100% traceability achieved.
```

---

## Key Takeaways

**Framework Enforcement**: Traceability validated, gaps caught before they cause issues
**Subagent Value**: Automated bidirectional validation catches human errors
**Quality Maintained**: 100% UC-Service traceability enforced
**Time Saved**: 15 minutes to find and fix vs. hours debugging integration issues later

---

## Files Created/Modified

**Modified**:
- `specs/use-cases/UC-004-view-order-history.md` (added service references)
- `services/user-service/service-spec.md` (added UC-002)

**Created**:
- `planning/traceability-report-2024-09-30.md`

---

**Session End**: 100% traceability achieved, ready to continue implementation ✅
