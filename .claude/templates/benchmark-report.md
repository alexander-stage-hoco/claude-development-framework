# Benchmark Report: [SERVICE_NAME]

**Service**: [SERVICE_NAME] (SVC-XXX)
**Benchmark Date**: [YYYY-MM-DD]
**Conducted By**: [Name/Claude]
**Purpose**: [Why was this benchmark performed?]

---

## Executive Summary

**Recommendation**: ✅ **[Strategy Name]**

**Rationale**: [1-2 sentence summary of why this strategy was chosen]

**Key Finding**: [Most important insight from benchmarks]

---

## Benchmark Scenario

### Test Environment

| Component | Specification |
|-----------|--------------|
| CPU | [e.g., Intel i7-9750H @ 2.6GHz, 6 cores] |
| Memory | [e.g., 16GB DDR4] |
| OS | [e.g., macOS 12.3, Linux Ubuntu 22.04] |
| Python Version | [e.g., Python 3.11.4] |
| Database | [e.g., PostgreSQL 15.2 (local)] |
| Cache | [e.g., Redis 7.0 (local)] |

### Workload Profile

**Scenario**: [Describe the workload being tested]

**Parameters**:
- **Total operations**: [N]
- **Concurrent users/threads**: [M]
- **Read/write ratio**: [e.g., 80% reads, 20% writes]
- **Data size**: [e.g., 10K records, 100MB dataset]
- **Duration**: [e.g., 60 seconds sustained load]
- **Warm-up**: [e.g., 10 seconds before measurement]

**Example**:
```
Scenario: High-read caching workload
- 10,000 total operations
- 100 concurrent requests
- 90% cache hits, 10% cache misses
- Avg payload: 1KB per request
- Duration: 60 seconds
```

---

## Strategies Compared

### Strategy A: [Strategy Name]

**Implementation**: [Brief description]

**Key Characteristics**:
- [Characteristic 1]
- [Characteristic 2]

**Dependencies**:
- [Library/infrastructure used]

---

### Strategy B: [Strategy Name]

**Implementation**: [Brief description]

**Key Characteristics**:
- [Characteristic 1]
- [Characteristic 2]

**Dependencies**:
- [Library/infrastructure used]

---

### Strategy C: [Strategy Name]

**Implementation**: [Brief description]

**Key Characteristics**:
- [Characteristic 1]
- [Characteristic 2]

**Dependencies**:
- [Library/infrastructure used]

---

## Performance Results

### Latency Comparison

| Strategy | p50 (median) | p95 | p99 | p99.9 | Max |
|----------|-------------|-----|-----|-------|-----|
| Strategy A | [X]ms | [Y]ms | [Z]ms | [W]ms | [V]ms |
| Strategy B | [X]ms | [Y]ms | [Z]ms | [W]ms | [V]ms |
| Strategy C | [X]ms | [Y]ms | [Z]ms | [W]ms | [V]ms |

**Winner (Latency)**: ✅ [Strategy Name] - [X]% faster at p95

**Visualization**:
```
p95 Latency (ms):
Strategy A: ████████████████████ 20ms
Strategy B: ██████████ 10ms  ← BEST
Strategy C: ███████████████ 15ms
```

---

### Throughput Comparison

| Strategy | Avg Throughput | Peak Throughput | Sustained Throughput |
|----------|---------------|----------------|---------------------|
| Strategy A | [X] ops/sec | [Y] ops/sec | [Z] ops/sec |
| Strategy B | [X] ops/sec | [Y] ops/sec | [Z] ops/sec |
| Strategy C | [X] ops/sec | [Y] ops/sec | [Z] ops/sec |

**Winner (Throughput)**: ✅ [Strategy Name] - [X]% higher sustained throughput

---

### Resource Utilization

| Strategy | CPU Usage (avg) | Memory Usage (avg) | Memory Peak | Network I/O |
|----------|----------------|-------------------|-------------|-------------|
| Strategy A | [X]% | [Y] MB | [Z] MB | [N] MB/s |
| Strategy B | [X]% | [Y] MB | [Z] MB | [N] MB/s |
| Strategy C | [X]% | [Y] MB | [Z] MB | [N] MB/s |

**Winner (Efficiency)**: ✅ [Strategy Name] - Lowest resource footprint

---

### Cost Analysis

| Strategy | Infrastructure Cost | Operational Cost | Total Monthly Cost |
|----------|-------------------|-----------------|-------------------|
| Strategy A | [e.g., $50 Redis] | [e.g., $20 bandwidth] | **$70/month** |
| Strategy B | [e.g., $0 in-memory] | [e.g., $10 bandwidth] | **$10/month** |
| Strategy C | [e.g., $100 managed DB] | [e.g., $30 bandwidth] | **$130/month** |

**Winner (Cost)**: ✅ [Strategy Name] - [X]% lower cost

**Assumptions**:
- [Assumption 1 about pricing]
- [Assumption 2 about scale]

---

### Error Rates

| Strategy | Success Rate | Timeout Rate | Error Rate | Retry Rate |
|----------|-------------|-------------|-----------|-----------|
| Strategy A | [X]% | [Y]% | [Z]% | [W]% |
| Strategy B | [X]% | [Y]% | [Z]% | [W]% |
| Strategy C | [X]% | [Y]% | [Z]% | [W]% |

**Winner (Reliability)**: ✅ [Strategy Name] - Highest success rate

---

## Detailed Analysis

### Strategy A: [Name]

**Strengths**:
- ✅ [Specific advantage observed in benchmarks]
- ✅ [Another strength with metrics]

**Weaknesses**:
- ❌ [Specific disadvantage observed]
- ❌ [Another weakness with metrics]

**Best For**:
- [Use case 1 where this strategy excels]
- [Use case 2]

**Avoid When**:
- [Condition where this strategy underperforms]

---

### Strategy B: [Name]

**Strengths**:
- ✅ [Specific advantage observed in benchmarks]
- ✅ [Another strength with metrics]

**Weaknesses**:
- ❌ [Specific disadvantage observed]
- ❌ [Another weakness with metrics]

**Best For**:
- [Use case 1 where this strategy excels]
- [Use case 2]

**Avoid When**:
- [Condition where this strategy underperforms]

---

### Strategy C: [Name]

**Strengths**:
- ✅ [Specific advantage observed in benchmarks]
- ✅ [Another strength with metrics]

**Weaknesses**:
- ❌ [Specific disadvantage observed]
- ❌ [Another weakness with metrics]

**Best For**:
- [Use case 1 where this strategy excels]
- [Use case 2]

**Avoid When**:
- [Condition where this strategy underperforms]

---

## Trade-Off Analysis

### Performance vs. Cost

```
High Performance
     │
  B  │  A
     │
─────┼───── Low Cost ────► High Cost
     │
  C  │
     │
Low Performance
```

**Analysis**: [Describe the trade-off space]

---

### Performance vs. Complexity

| Strategy | Implementation Complexity | Operational Complexity | Maintainability |
|----------|--------------------------|----------------------|----------------|
| Strategy A | Medium | Low | High |
| Strategy B | Low | Low | High |
| Strategy C | High | High | Medium |

---

### Scalability Considerations

| Strategy | Horizontal Scaling | Vertical Scaling | Max Capacity |
|----------|------------------|-----------------|-------------|
| Strategy A | ✅ Excellent | ✅ Good | [X] ops/sec |
| Strategy B | ❌ Poor | ✅ Good | [Y] ops/sec |
| Strategy C | ✅ Excellent | ✅ Excellent | [Z] ops/sec |

---

## Recommendation

### ✅ Selected Strategy: [Strategy Name]

**Justification**: [Multi-sentence explanation of why this strategy is chosen]

**Key Factors**:
1. **Performance**: [How performance influenced decision]
2. **Cost**: [How cost influenced decision]
3. **Reliability**: [How reliability influenced decision]
4. **Scalability**: [How scalability needs influenced decision]
5. **Complexity**: [How implementation/operational complexity influenced decision]

**Use Case Alignment**:
- **UC-001**: [How this strategy supports this use case]
- **UC-002**: [How this strategy supports this use case]

**Requirements Met**:
- ✅ Latency < [X]ms (achieved [Y]ms p95)
- ✅ Throughput > [N] ops/sec (achieved [M] ops/sec)
- ✅ Cost < $[Z]/month (achieved $[W]/month)
- ✅ Reliability > 99.9% (achieved [R]%)

---

## Optimal Parameters

Based on benchmarking, the following parameters yield best performance:

```python
# Recommended configuration for Strategy [Name]

CONFIG = {
    "param_1": value,  # Rationale: [why this value]
    "param_2": value,  # Rationale: [why this value]
    "param_3": value,  # Rationale: [why this value]
}
```

**Example (Redis Cache)**:
```python
REDIS_CONFIG = {
    "max_memory": "2GB",          # Supports 1M cached items
    "eviction_policy": "lru",      # Best for read-heavy workload
    "persistence": "AOF",          # 1sec fsync for durability
    "max_connections": 500,        # Handles peak load
}
```

---

## Implementation Notes

### Migration Plan

If changing from previous strategy:

1. **Phase 1**: [Step 1 of migration]
2. **Phase 2**: [Step 2 of migration]
3. **Rollback Plan**: [How to roll back if issues arise]

### Monitoring

**Metrics to Track**:
- [Metric 1] - Alert if > [threshold]
- [Metric 2] - Alert if < [threshold]
- [Metric 3] - Track for trends

### Testing in Production

**Gradual Rollout**:
1. Deploy to 5% of traffic
2. Monitor for [X] hours
3. If metrics stable, increase to 50%
4. Full deployment after [Y] hours

---

## Reproducibility

### Benchmark Code

**Location**: `benchmarks/benchmark_[service]_[date].py`

**How to Run**:
```bash
# Setup
pip install pytest pytest-benchmark

# Run benchmark
pytest benchmarks/benchmark_[service]_[date].py --benchmark-only

# Generate report
pytest benchmarks/ --benchmark-compare --benchmark-save=[name]
```

### Test Data

**Dataset**: [Description of test data used]
**Location**: [Where to find test data]
**Generation**: [How to regenerate test data]

---

## Appendix

### Raw Data

[Link to raw benchmark data CSV/JSON if available]

### Statistical Analysis

| Strategy | Mean | Std Dev | Variance | Min | Max | Samples |
|----------|------|---------|----------|-----|-----|---------|
| Strategy A | [X] | [Y] | [Z] | [W] | [V] | [N] |
| Strategy B | [X] | [Y] | [Z] | [W] | [V] | [N] |
| Strategy C | [X] | [Y] | [Z] | [W] | [V] | [N] |

### Environmental Factors

**Factors that May Affect Results**:
- [Factor 1: e.g., "Local database vs. remote"]
- [Factor 2: e.g., "Cold start vs. warmed up"]
- [Factor 3: e.g., "Single machine vs. distributed"]

**Production Differences**:
- [How production environment differs from test]
- [Expected impact on metrics]

---

## Follow-Up Actions

- [ ] **Action 1**: Update service-spec.md with recommended strategy
- [ ] **Action 2**: Create ADR if architectural change
- [ ] **Action 3**: Implement optimal configuration
- [ ] **Action 4**: Set up monitoring for key metrics
- [ ] **Action 5**: Re-benchmark after [X months] or when load increases

---

## References

- **Service Specification**: `services/[service-name]/service-spec.md`
- **Benchmark Code**: `services/[service-name]/benchmarks/benchmark_suite.py`
- **Previous Benchmarks**: [Link to prior benchmark reports]
- **Related ADRs**: ADR-XXX ([Decision name])

---

**Report Version**: 1.0
**Framework**: Claude Development Framework v2.0
**Next Benchmark**: [Recommended date or trigger condition]
