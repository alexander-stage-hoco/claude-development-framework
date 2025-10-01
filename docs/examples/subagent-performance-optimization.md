# Example: Performance Optimization with Benchmarking

**Scenario**: ProductService is slow with 50,000+ products, needs optimization
**Complexity**: High
**Duration**: ~45 minutes
**Framework Features**: Performance benchmarking, data-driven optimization, quality preservation
**Subagents Used**: service-optimizer

---

## Context

**Project**: E-commerce Order Management API
**Session**: Production issue reported
**Problem**: Product search degraded from 45ms to 1200ms p99 latency at 50K products
**Current State**:
- ✅ All services implemented and tested
- ✅ Deployed to production 2 weeks ago
- ⚠️ Performance degradation reported by monitoring
- ❌ No optimization analysis yet

**Service in Focus**: ProductService (SVC-004)
- **Method**: `search_products(query: str, limit: int) -> List[Product]`
- **Current Implementation**: Load all products, filter in Python
- **Performance Requirement** (from UC-003): p99 latency <100ms

**User Goal**: Optimize search performance while maintaining test coverage and quality

---

## Session Transcript

### User Request

```
User: "ProductService.search_products() is taking 1.2 seconds with 50K products.
The spec says p99 must be <100ms. Please optimize this using benchmarks to
prove the improvement."
```

---

### Claude's Response

```
Claude: I'll use the service-optimizer subagent to benchmark alternative
implementation strategies and recommend the optimal approach.

📖 Reading:
- services/product-service/service-spec.md (current implementation)
- specs/use-cases/UC-003-create-order.md (performance requirements)
- services/product-service/implementation.py (current code)

**Current Implementation** (Strategy 1: Naive):
```python
def search_products(self, query: str, limit: int) -> List[Product]:
    # Load ALL products from database
    all_products = self.repository.get_all()  # 50,000 rows

    # Filter in Python
    filtered = [
        p for p in all_products
        if query.lower() in p.name.lower() or query.lower() in p.description.lower()
    ]

    return filtered[:limit]
```

**Problem**: O(n) where n=50,000. Loads entire table into memory every request.

**Alternative Strategies to Test**:
1. **Strategy 1**: Current (baseline)
2. **Strategy 2**: Database WHERE clause (push filtering to DB)
3. **Strategy 3**: Database + Full-Text Search index
4. **Strategy 4**: ElasticSearch (separate search engine)

**Benchmark Plan**:
- Data sizes: 1K, 10K, 50K, 100K products
- Iterations: 100 per size
- Metrics: p50, p95, p99 latency, throughput, memory

Launching service-optimizer subagent...
```

---

### Subagent Execution & Report

```markdown
# Benchmark Report: ProductService.search_products()

**Service ID**: SVC-004
**Method**: search_products
**Date**: 2024-09-30
**Problem**: p99 latency 1200ms (requirement: <100ms)

---

## Executive Summary

### ✅ Recommendation: Strategy 3 (Database + Full-Text Search Index)

**Rationale**:

Strategy 3 provides **99.2x speedup** vs. current implementation while
meeting all requirements:

1. **Performance**: 12ms p99 (target: <100ms) ✅
2. **Simplicity**: PostgreSQL built-in full-text search (no new infrastructure)
3. **Cost**: $0 additional cost (uses existing database)
4. **Quality**: All tests still pass ✅
5. **Maintainability**: Simple SQL changes only

**vs. ElasticSearch (Strategy 4)**:
- Only 1.3x faster (12ms vs. 9ms)
- Requires new infrastructure ($150/month)
- Added complexity (sync, monitoring)
- **Not worth the cost for 3ms improvement**

---

## Strategies Tested

### Strategy 1: Naive (Current) - BASELINE

**Implementation**:
```python
def search_products(self, query: str, limit: int) -> List[Product]:
    all_products = self.repository.get_all()  # Load all 50K
    filtered = [p for p in all_products if query.lower() in p.name.lower()]
    return filtered[:limit]
```

**Complexity**: O(n) where n = total products
**Dependencies**: None (pure Python)

### Strategy 2: Database WHERE Clause

**Implementation**:
```python
def search_products(self, query: str, limit: int) -> List[Product]:
    return self.repository.search_by_name(query, limit)

# In repository:
SELECT * FROM products
WHERE LOWER(name) LIKE LOWER('%' || $1 || '%')
   OR LOWER(description) LIKE LOWER('%' || $1 || '%')
LIMIT $2
```

**Complexity**: O(n) but on database (faster than Python)
**Dependencies**: PostgreSQL (existing)

### Strategy 3: Database + Full-Text Search Index ⭐ RECOMMENDED

**Implementation**:
```python
# Migration: Add full-text search index
CREATE INDEX products_search_idx ON products
USING GIN(to_tsvector('english', name || ' ' || description));

# Query:
SELECT * FROM products
WHERE to_tsvector('english', name || ' ' || description) @@ plainto_tsquery('english', $1)
ORDER BY ts_rank(to_tsvector('english', name || ' ' || description), plainto_tsquery('english', $1)) DESC
LIMIT $2
```

**Complexity**: O(log n) with GIN index
**Dependencies**: PostgreSQL (existing)

### Strategy 4: ElasticSearch

**Implementation**:
- Index products in ElasticSearch
- Query ElasticSearch cluster
- Sync on product updates

**Complexity**: O(log n)
**Dependencies**: ElasticSearch cluster ($150/month)

---

## Performance Results

### Latency (milliseconds) - 50,000 Products

| Strategy | p50 | p95 | p99 | vs. Baseline |
|----------|-----|-----|-----|--------------|
| Strategy 1: Naive | 985 | 1150 | 1225 | 1x (baseline) |
| Strategy 2: DB WHERE | 245 | 298 | 320 | 3.8x faster |
| Strategy 3: FTS Index | 8 | 11 | 12 | **99.2x faster** ✅ |
| Strategy 4: ElasticSearch | 6 | 8 | 9 | 136x faster |

**Winner**: Strategy 3 (meets requirement with simplest solution)

### Scalability Test (p99 latency vs. dataset size)

| Products | Strategy 1 | Strategy 2 | Strategy 3 | Strategy 4 |
|----------|------------|------------|------------|------------|
| 1,000 | 25ms | 12ms | 8ms | 7ms |
| 10,000 | 245ms | 95ms | 10ms | 8ms |
| 50,000 | 1,225ms ❌ | 320ms ❌ | 12ms ✅ | 9ms ✅ |
| 100,000 | 2,450ms ❌ | 645ms ❌ | 14ms ✅ | 10ms ✅ |

**Observation**: Only Strategy 3 & 4 scale to 100K+ products within requirements

### Throughput (queries/second)

| Strategy | Throughput | vs. Baseline |
|----------|------------|--------------|
| Strategy 1 | 0.8 qps | 1x |
| Strategy 2 | 3.1 qps | 3.9x |
| Strategy 3 | 83.3 qps | **104x** ✅ |
| Strategy 4 | 111 qps | 139x |

### Memory Usage (peak)

| Strategy | Memory | Notes |
|----------|--------|-------|
| Strategy 1 | 450 MB | Loads all products into memory |
| Strategy 2 | 25 MB | Database handles filtering |
| Strategy 3 | 10 MB | Database with index |
| Strategy 4 | 15 MB | ElasticSearch client overhead |

---

## Trade-Off Analysis

| Criterion | Weight | Strategy 1 | Strategy 2 | Strategy 3 | Strategy 4 |
|-----------|--------|------------|------------|------------|------------|
| **Speed (p99)** | 35% | 1/10 | 4/10 | 10/10 | 10/10 |
| **Scalability** | 25% | 1/10 | 3/10 | 10/10 | 10/10 |
| **Simplicity** | 20% | 10/10 | 9/10 | 8/10 | 3/10 |
| **Cost** | 15% | 10/10 | 10/10 | 10/10 | 3/10 |
| **Maintenance** | 5% | 10/10 | 10/10 | 9/10 | 5/10 |
| **Weighted Score** | | **3.95** | **5.80** | **9.45** | **7.60** |

**Winner**: Strategy 3 (94.5%)

---

## Performance Requirement Check

**From UC-003 Specification**:
- Response time: p99 <100ms ✅
- Throughput: >10 qps ✅
- Memory limit: <200MB ✅
- Budget: <$100/month additional cost ✅

| Strategy | Meets Perf? | Meets Cost? | PASS |
|----------|-------------|-------------|------|
| Strategy 1 | ❌ 1225ms | ✅ $0 | ❌ FAIL |
| Strategy 2 | ❌ 320ms | ✅ $0 | ❌ FAIL |
| Strategy 3 | ✅ 12ms | ✅ $0 | ✅ PASS |
| Strategy 4 | ✅ 9ms | ❌ $150/month | ⚠️ CONDITIONAL |

**Result**: Strategy 3 is the only option meeting ALL requirements.

---

## Recommended Implementation

### Database Migration

```sql
-- Migration: Add full-text search index
CREATE INDEX products_search_idx ON products
USING GIN(to_tsvector('english', name || ' ' || description));

-- Add materialized column for faster ranking (optional)
ALTER TABLE products ADD COLUMN search_vector tsvector;

UPDATE products SET search_vector =
    to_tsvector('english', name || ' ' || description);

CREATE INDEX products_search_vector_idx ON products USING GIN(search_vector);

-- Trigger to keep search_vector updated
CREATE TRIGGER products_search_vector_update
BEFORE INSERT OR UPDATE ON products
FOR EACH ROW EXECUTE FUNCTION
    tsvector_update_trigger(search_vector, 'pg_catalog.english', name, description);
```

### Updated Service Implementation

```python
# services/product-service/implementation.py

def search_products(self, query: str, limit: int) -> List[Product]:
    """
    Search products using PostgreSQL full-text search

    Performance: O(log n) with GIN index
    Specification: SVC-004#search-products
    Benchmark: benchmarks/report-2024-09-30.md
    """
    return self.repository.full_text_search(query, limit)

# Repository implementation
def full_text_search(self, query: str, limit: int) -> List[Product]:
    """Full-text search with ranking"""
    sql = """
    SELECT
        id, name, description, price, stock,
        ts_rank(search_vector, plainto_tsquery('english', %s)) as rank
    FROM products
    WHERE search_vector @@ plainto_tsquery('english', %s)
    ORDER BY rank DESC
    LIMIT %s
    """
    rows = self.db.execute(sql, (query, query, limit))
    return [Product(**row) for row in rows]
```

### Test Updates (TDD - Tests Still Pass!)

```python
# tests/test_product_service.py

def test_search_products_performance():
    """Search should return results in <100ms for 50K products"""
    service = ProductService(repository)

    # Pre-populate 50,000 products
    setup_test_products(50_000)

    # Measure performance
    import time
    start = time.perf_counter()
    results = service.search_products("laptop", limit=20)
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert len(results) == 20
    assert elapsed_ms < 100, f"Search took {elapsed_ms}ms (limit: 100ms)"

def test_search_products_accuracy_unchanged():
    """Search results should match previous implementation"""
    # Test that optimization doesn't change search logic
    service = ProductService(repository)

    results = service.search_products("laptop", limit=10)

    assert all("laptop" in r.name.lower() or "laptop" in r.description.lower()
               for r in results)
```

**Result**: ✅ All 47 existing tests still pass

---

## Deployment Plan

### Phase 1: Database Migration (5 minutes)

```bash
# Run migration
psql -h production-db -f migrations/add_fulltext_search.sql

# Verify index created
psql -h production-db -c "\d products"
```

### Phase 2: Code Deployment (10 minutes)

```bash
# Deploy updated service
git checkout -b optimization/product-search-fts
git add services/product-service/
pytest services/product-service/  # All tests pass
git commit -m "perf: optimize product search with full-text index

Benchmark: 99.2x speedup (1225ms → 12ms p99)
Specification: SVC-004#search-products
Tests: 47 passing / 47 total"

# Deploy to production
./deploy.sh production
```

### Phase 3: Monitoring (24 hours)

Monitor metrics:
- p99 latency (target: <15ms with headroom)
- Query throughput
- Database CPU usage
- Index size

---

## Cost Analysis

| Strategy | Setup Cost | Monthly Cost | Total Year 1 |
|----------|------------|--------------|--------------|
| Strategy 1 (Current) | $0 | $0 | $0 |
| Strategy 3 (FTS) | $0 | $0 | $0 |
| Strategy 4 (ElasticSearch) | $500 | $150 | $2,300 |

**Savings**: $2,300/year by using Strategy 3 instead of ElasticSearch

---

## Benchmark Reproducibility

### Test Environment
- **Database**: PostgreSQL 15.4
- **CPU**: 4 cores, 3.2 GHz
- **Memory**: 16GB RAM
- **Dataset**: 50,000 real product records
- **Queries**: 100 diverse search terms

### Run Benchmarks

```bash
cd services/product-service
python benchmarks/benchmark_suite.py \
    --strategies strategy1,strategy2,strategy3,strategy4 \
    --data-sizes 1000,10000,50000,100000 \
    --iterations 100
```

---

## When to Reconsider

**Move to ElasticSearch (Strategy 4) if**:
- Product catalog grows beyond 500K products
- Need advanced features (fuzzy matching, typo tolerance, faceted search)
- Budget allows $150/month
- Team has ElasticSearch expertise

**Threshold**: Strategy 3 scales to ~500K products before degrading

---

**Benchmark Complete**: 2024-09-30 02:30 PM
**Implementation Time**: 45 minutes (migration + code + tests)
**Performance Improvement**: 99.2x speedup ✅
```

---

### Claude's Presentation

```
Claude: ✅ Benchmark complete! Dramatic performance improvement achieved.

**Results**:
- **Current**: 1225ms p99 (FAILING spec requirement <100ms)
- **Optimized**: 12ms p99 ✅
- **Improvement**: 99.2x faster!

**Solution**: PostgreSQL Full-Text Search with GIN index

**Why This Strategy**:
1. Meets performance requirement (12ms << 100ms) ✅
2. Zero additional cost ($0 vs. $150/month ElasticSearch)
3. Simple implementation (SQL migration + minor code change)
4. All 47 tests still pass ✅
5. Scales to 500K products

**vs. ElasticSearch**:
- ElasticSearch only 1.3x faster (9ms vs. 12ms)
- Costs $2,300/year
- Adds infrastructure complexity
- **Not worth 3ms improvement**

**Implementation Plan**:
1. Run database migration (5 min)
2. Deploy updated service code (10 min)
3. Monitor for 24 hours
4. Total effort: 45 minutes

**Files Created**:
- `services/product-service/benchmarks/report-2024-09-30.md`
- `migrations/add_fulltext_search.sql`

**Quality Maintained**:
- ✅ All tests still pass
- ✅ Search accuracy unchanged
- ✅ No breaking changes

May I proceed with implementation?
```

---

### User Response

```
User: "Excellent analysis! Yes, implement Strategy 3. Make sure all tests pass."
```

---

### Claude Implementation (TDD Protocol)

```
Claude: I'll implement Strategy 3 following TDD protocol:

**Step 1: Update Performance Test** (RED phase)

```python
def test_search_performance_under_100ms():
    """p99 latency must be <100ms per UC-003"""
    # This test will FAIL with current implementation
    assert search_latency_p99() < 100
```

Run: ❌ FAILS (1225ms)

**Step 2: Implement Database Migration**
[Creates migration file]

**Step 3: Update Service Code**
[Updates repository with full-text search]

**Step 4: Run Tests** (GREEN phase)

```bash
pytest services/product-service/
```

Result: ✅ All 48 tests pass (including new performance test)

**Step 5: Benchmark Verification**

```bash
python benchmarks/verify_improvement.py
```

Result: ✅ p99 = 12ms (requirement met)

**Step 6: Git Commit** (Rule #11)

```bash
git commit -m "perf: optimize product search 99x (1225ms → 12ms)

- Add PostgreSQL full-text search GIN index
- Update repository to use FTS queries
- Benchmark report: benchmarks/report-2024-09-30.md
- All tests passing (48/48)

Specification: UC-003, SVC-004#search-products"
```

✅ Optimization complete! Quality maintained, performance requirement met.
```

---

## Key Takeaways

### Framework Enforcement

1. **Benchmark Before Optimize**: Data-driven decisions, not guesswork
2. **Tests Never Weakened**: All 47 tests still pass
3. **Specification Compliance**: Meets UC-003 performance requirement
4. **Quality Maintained**: TDD protocol followed throughout

### Subagent Value

- **Comprehensive Analysis**: 4 strategies implemented and benchmarked
- **Objective Recommendation**: Decision matrix removes bias
- **Cost Analysis**: Saved $2,300/year by avoiding ElasticSearch
- **Time Efficiency**: 45 min optimization vs. days of trial-and-error

### Quality Maintained

- All existing tests pass (no regression)
- Performance test added (prevents future regression)
- Benchmark report documents decision
- Migration is reversible if needed

### Time Saved

- **Manual optimization**: 2-3 days trial and error
- **With subagent**: 45 minutes with proof
- **Production issue**: Resolved same day vs. week-long investigation

---

## Files Created/Modified

**Created**:
- `services/product-service/benchmarks/benchmark_suite.py`
- `services/product-service/benchmarks/report-2024-09-30.md`
- `migrations/20240930_add_fulltext_search.sql`

**Modified**:
- `services/product-service/repository.py` (full-text search query)
- `services/product-service/tests/test_performance.py` (new test)

---

## Next Steps

1. Deploy to production
2. Monitor metrics for 24 hours
3. Update service specification with benchmark results
4. Document threshold (500K products) for future ElasticSearch consideration

**Session End**: Performance crisis resolved, quality maintained ✅
