# Scenario: Fixing Circular Dependency

**Scenario**: service-dependency-analyzer detects circular dependency, needs refactoring
**Complexity**: High
**Duration**: ~60 minutes
**Problem**: PaymentService → OrderService → InventoryService → PaymentService (cycle!)
**Solution**: Event-based decoupling

---

## Context

**Project**: E-commerce Platform
**Session**: 8 (during dependency validation)
**Problem Detected**: Circular dependency preventing TDD implementation

**Cycle Path**:
```
PaymentService → OrderService → InventoryService → PaymentService
```

---

## Session Transcript

### Dependency Analyzer Report

```
❌ **Circular Dependency Detected**

**Cycle Path**: SVC-007 → SVC-008 → SVC-009 → SVC-007

**Services Involved**:
- SVC-007: PaymentService depends on SVC-008 (OrderService)
- SVC-008: OrderService depends on SVC-009 (InventoryService)
- SVC-009: InventoryService depends on SVC-007 (PaymentService)

**Impact**: Cannot implement in isolation, testing impossible

**Root Cause**:
- PaymentService needs OrderService to get order total
- OrderService needs InventoryService to reserve stock
- InventoryService needs PaymentService to verify payment before releasing stock
```

---

### Claude's Analysis

```
Claude: ❌ Circular dependency detected. **I cannot proceed with implementation**
(Rule #7: Technical Decisions Are Binding + Clean Architecture Required).

**Two Refactoring Options**:

### Option 1: Event-Based Decoupling (Recommended)

Break cycle using event bus:
```
OrderService → Creates "payment_required" event
InventoryService → Subscribes to event
PaymentService → No longer direct dependency
```

**Pros**:
- Breaks cycle completely
- Services become truly independent
- Better scalability (async processing)

**Cons**:
- Requires event bus infrastructure
- Slightly more complex (but cleaner)

### Option 2: Extract Shared Logic

Create new service (PricingService):
```
Layer 1: PricingService (no dependencies)
Layer 2: PaymentService, InventoryService → PricingService
Layer 3: OrderService → All above
```

**Pros**:
- Simpler (no events needed)
- Explicit dependencies

**Cons**:
- Adds another service
- Doesn't fully decouple

**Recommendation**: Option 1 (event-based) - more scalable long-term

May I implement Option 1?
```

---

### User Response

```
User: "Yes, implement Option 1 with events."
```

---

### Implementation (Summary)

**Step 1: Update Specifications**

Updated service specs to remove circular dependencies:

```markdown
# SVC-007: PaymentService

**Dependencies**: None (was: OrderService) ✅

**Events Published**:
- `payment_completed`: When payment succeeds
- `payment_failed`: When payment fails

# SVC-008: OrderService

**Events Published**:
- `payment_required`: When order needs payment processing

# SVC-009: InventoryService

**Events Subscribed**:
- `payment_completed` → Release reserved stock
```

**Step 2: Re-Run Dependency Analyzer**

```
✅ **Dependency Analysis**: Clean

- Circular Dependencies: 0 (was: 1) ✅
- Max Dependencies: 2 (was: 3)
- Architecture: Clean layers

**Result**: Ready for implementation
```

**Step 3: Implement Event Bus (TDD)**

```python
# Write tests first
def test_payment_completed_event_releases_stock():
    event_bus.publish(PaymentCompleted(order_id=123))
    assert inventory.stock_released(order_id=123)

# Then implement
class EventBus:
    def publish(self, event: Event):
        for subscriber in self._subscribers[event.type]:
            subscriber.handle(event)
```

---

## Outcome

✅ **Circular Dependency Resolved**

**Before**:
```
PaymentService → OrderService → InventoryService → PaymentService ❌
```

**After**:
```
Layer 1: EventBus
Layer 2: PaymentService, OrderService, InventoryService (all independent) ✅
```

**Quality Maintained**:
- All tests pass
- Specifications updated
- ADR-005 created (documenting decision)

---

## Key Takeaways

**Framework Enforcement**: Dependency analyzer caught cycle before implementation started
**Solution Pattern**: Event-based decoupling for async workflows
**Quality Maintained**: Specifications updated first, then TDD implementation
**Time Saved**: Detected before implementation (saved days of debugging)

---

**Session End**: Clean architecture restored, ready for TDD implementation ✅
