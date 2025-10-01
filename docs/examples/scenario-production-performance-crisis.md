# Scenario: Production Performance Crisis

**Scenario**: Production API degraded, urgent fix needed while maintaining quality
**Complexity**: High
**Duration**: ~2 hours (emergency protocol)
**Problem**: API response time degraded from 50ms to 3000ms at peak load
**Solution**: Hotfix with benchmarking, quality maintained

---

## Context

**Project**: E-commerce API (Production)
**Time**: 2:00 AM, Black Friday weekend
**Alert**: "API p99 latency exceeded 3000ms (SLA: 200ms)"
**Impact**: Customer complaints, lost revenue (~$500/min)

---

## Emergency Session Transcript

### User Alert (Urgent!)

```
User: "URGENT! Production API is down. Customers can't checkout. Response times
are 3+ seconds. We're losing $500/minute. Need fix NOW but we can't break tests!"
```

---

### Claude's Response (Emergency Protocol)

```
Claude: 🚨 **Production Emergency Detected**

Following Emergency Hotfix Protocol (from troubleshooting.md):

**Step 1: Triage** (5 minutes)

Reading production metrics and logs...

**Root Cause Identified**:
- Endpoint: POST /api/orders/create
- Problem: OrderService.calculate_total() doing N+1 queries
- Load: 500 req/sec (normal: 50 req/sec - Black Friday traffic!)
- Database: 98% CPU usage

**Impact**:
- Revenue loss: $500/minute
- Customer satisfaction: Critical
- SLA violation: Yes (p99: 3000ms vs. 200ms SLA)

**Step 2: Emergency Fix Decision**

**Hotfix Option**: Add database query optimization (10 min implementation)
**Impact**: Reduces queries from O(n²) to O(1)
**Risk**: Low (query optimization only, logic unchanged)
**Tests**: All existing tests must still pass ✅

**I will NOT skip tests even in emergency** (Rule #6: Never Compromise Tests)

May I proceed with hotfix?
```

---

### User Response

```
User: "YES! Fix it but make sure tests pass!"
```

---

### Emergency Implementation (TDD Under Pressure)

```
Claude: **Emergency Hotfix Protocol**

**Step 1: Reproduce Issue Locally** (5 min)

```python
def test_calculate_total_performance():
    """Regression test for production issue"""
    # Simulate 100 items (Black Friday cart size)
    order = create_test_order(items=100)

    start = time.perf_counter()
    total = order_service.calculate_total(order)
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert elapsed_ms < 50, f"calculate_total too slow: {elapsed_ms}ms"
```

Run: ❌ FAILS (2800ms)

✅ Issue reproduced locally

**Step 2: Root Cause Analysis**

Current code (N+1 queries):
```python
def calculate_total(self, order: Order) -> Decimal:
    total = Decimal("0.00")
    for item in order.items:  # N iterations
        product = self.product_repo.get(item.product_id)  # 1 query each!
        total += product.price * item.quantity
    return total
```

**Problem**: 100 items = 100 database queries! 🔥

**Step 3: Write Optimized Version**

```python
def calculate_total(self, order: Order) -> Decimal:
    """Optimized: Single query with JOIN"""
    # Get all products in one query
    product_ids = [item.product_id for item in order.items]
    products = self.product_repo.get_many(product_ids)  # 1 query only!

    product_map = {p.id: p for p in products}

    total = Decimal("0.00")
    for item in order.items:
        product = product_map[item.product_id]
        total += product.price * item.quantity
    return total
```

**Step 4: Run ALL Tests** (Emergency - Still Required!)

```bash
pytest services/order-service/ -v
```

Result:
```
test_calculate_total_empty_order ✅
test_calculate_total_single_item ✅
test_calculate_total_multiple_items ✅
test_calculate_total_performance ✅  (was ❌, now 8ms)
... (45 more tests)
✅ All 49 tests PASS
```

**Step 5: Benchmark Improvement**

Run service-optimizer benchmark:
```
Before: 2800ms (100 items)
After: 8ms (100 items)
Improvement: 350x faster ✅
```

**Step 6: Emergency Deployment**

```bash
# Create hotfix branch
git checkout -b hotfix/order-calculation-n-plus-1

# Commit with emergency tag
git commit -m "HOTFIX: fix N+1 queries in calculate_total

EMERGENCY: Production performance crisis (Black Friday)
Impact: 350x speedup (2800ms → 8ms)
Root cause: N+1 queries in order calculation
Fix: Single query with get_many()

Tests: 49 passing / 49 total ✅
Benchmark: benchmarks/hotfix-2024-11-24.md

Specification: SVC-003#calculate-total
Issue: PROD-1234"

# Deploy to production
./deploy.sh production --hotfix --skip-staging
```

**Step 7: Monitor**

Watch production metrics...

[5 minutes later]

✅ **Production Metrics**:
- p99 latency: 45ms (was: 3000ms) ✅
- Database CPU: 15% (was: 98%) ✅
- Revenue: Restored ($0 lost since fix)
- SLA: Compliant (45ms < 200ms) ✅

🎉 **CRISIS RESOLVED!**
```

---

### Post-Mortem (Next Day)

```
Claude: **Emergency Hotfix Post-Mortem**

**Timeline**:
- 02:00 AM: Alert received
- 02:05 AM: Root cause identified
- 02:15 AM: Fix implemented and tested
- 02:20 AM: Deployed to production
- 02:25 AM: Metrics confirmed resolution
- **Total**: 25 minutes

**What Went Well**:
- ✅ Emergency protocol followed
- ✅ Root cause identified quickly (logs + metrics)
- ✅ All tests passed before deployment
- ✅ Performance benchmarked
- ✅ No customer data loss
- ✅ SLA restored

**What Could Be Better**:
- ⚠️ No performance test existed before (caught in production)
- ⚠️ Should have load-tested before Black Friday

**Action Items**:

1. **Add Performance Tests** (High Priority)
   - Create performance test suite
   - Run in CI/CD
   - Prevent regression

2. **Load Testing** (High Priority)
   - Implement load testing before major events
   - Simulate Black Friday traffic

3. **Update Specification**
   - Add performance requirements to UC-003
   - Document N+1 query anti-pattern

**ADR Created**: ADR-012 (Performance Testing Required in CI)

**Lessons Learned**:
- Emergency protocol worked (quality maintained under pressure)
- Tests prevented breaking changes
- Benchmarking proved improvement
- Framework discipline saved the day ✅
```

---

## Outcome

✅ **Crisis Resolved in 25 Minutes**

**Framework Enforced Quality**:
- ✅ All 49 tests passed (even in emergency)
- ✅ Performance benchmarked (350x improvement)
- ✅ Specification updated post-fix
- ✅ ADR created (lessons learned)

**vs. Ad-Hoc Approach**:
- ❌ Might have skipped tests ("it's an emergency!")
- ❌ Could have introduced new bugs
- ❌ No benchmark proving improvement
- ❌ Lost tribal knowledge

**Impact**:
- Revenue saved: ~$12,500 (25 min × $500/min)
- Customer satisfaction: Restored
- SLA compliance: Achieved
- Quality debt: ZERO (tests passed, docs updated)

---

## Key Takeaways

**Framework Enforcement**: Emergency protocol maintains quality under pressure
**Tests Are Sacred**: Even in production crisis, tests must pass
**Benchmarking Proves Fix**: 350x improvement documented
**Post-Mortem Required**: Learn and prevent recurrence

---

## Files Created

**Hotfix**:
- `benchmarks/hotfix-2024-11-24.md` (performance proof)
- `.claude/technical-decisions.md` (ADR-012 added)

**Modified**:
- `services/order-service/implementation.py` (optimized query)
- `services/order-service/tests/test_performance.py` (regression test added)
- `specs/use-cases/UC-003-create-order.md` (performance NFR added)

---

**Crisis End**: Production restored, quality maintained, lessons documented ✅
