# Library Evaluation: [SERVICE_NAME]

**Service**: [SERVICE_NAME] (SVC-XXX)
**Evaluation Date**: [YYYY-MM-DD]
**Evaluated By**: [Name/Claude]
**Purpose**: [What functionality are we looking for?]

---

## Executive Summary

**Recommendation**: ✅ **[Library Name]** OR **[Build Custom]**

**Rationale**: [1-2 sentence summary of recommendation]

**Key Finding**: [Most important insight from evaluation]

---

## Requirements

### Functional Requirements

**Must Have**:
- [ ] [Requirement 1]
- [ ] [Requirement 2]
- [ ] [Requirement 3]

**Nice to Have**:
- [ ] [Optional feature 1]
- [ ] [Optional feature 2]

**Example**:
```
Must Have:
- Send templated emails via SMTP
- Support HTML and plain text
- Attachment support
- Error handling with retries

Nice to Have:
- Multiple SMTP provider support (SendGrid, AWS SES)
- Email tracking/analytics
- Batch sending
```

---

### Non-Functional Requirements

| Requirement | Target | Importance |
|------------|--------|------------|
| Performance | [e.g., < 100ms latency] | High |
| Reliability | [e.g., > 99.9% success rate] | High |
| Maintenance | [e.g., Active development] | High |
| License | [e.g., MIT/Apache 2.0] | High |
| Documentation | [e.g., Comprehensive docs] | Medium |
| Community | [e.g., > 100 stars] | Medium |
| Dependencies | [e.g., Minimal dependencies] | Medium |

---

## Library Candidates

### Candidate 1: [Library Name]

**Source**: [e.g., PyPI, GitHub]
**Link**: [https://github.com/org/library]
**Version**: [e.g., v2.5.0]

#### Overview

**Description**: [What is this library?]

**Maturity**:
- **First Release**: [Year]
- **Latest Release**: [Date]
- **Release Frequency**: [e.g., Monthly, Quarterly]

#### Community & Maintenance

| Metric | Value | Assessment |
|--------|-------|------------|
| GitHub Stars | [N] | ✅ Good / ⚠️ Fair / ❌ Poor |
| Forks | [N] | ✅ Good / ⚠️ Fair / ❌ Poor |
| Contributors | [N] | ✅ Good / ⚠️ Fair / ❌ Poor |
| Open Issues | [N] | ✅ Low / ⚠️ Moderate / ❌ High |
| Closed Issues | [N] | ✅ Responsive / ⚠️ Slow / ❌ Stale |
| Last Commit | [Date] | ✅ Active / ⚠️ Slow / ❌ Abandoned |
| PyPI Downloads/Month | [N] | ✅ Popular / ⚠️ Moderate / ❌ Low |

**Maintenance Status**: ✅ **Active** / ⚠️ **Slow** / ❌ **Abandoned**

#### Feature Coverage

| Feature | Supported | Notes |
|---------|-----------|-------|
| [Feature 1] | ✅ Yes / ⚠️ Partial / ❌ No | [Details] |
| [Feature 2] | ✅ Yes / ⚠️ Partial / ❌ No | [Details] |
| [Feature 3] | ✅ Yes / ⚠️ Partial / ❌ No | [Details] |

**Coverage**: [X]% of must-have requirements

#### Quality Assessment

**Code Quality**:
- Type hints: ✅ Yes / ❌ No
- Test coverage: [X]%
- Documentation: ✅ Excellent / ⚠️ Adequate / ❌ Poor
- Examples: ✅ Comprehensive / ⚠️ Basic / ❌ None

**Stability**:
- Known bugs: [N] critical, [M] minor
- Breaking changes: [Frequency]
- API stability: ✅ Stable / ⚠️ Evolving / ❌ Unstable

#### Dependencies

| Dependency | Version | Size | Notes |
|------------|---------|------|-------|
| [Package 1] | [Version] | [Size] | [Rationale] |
| [Package 2] | [Version] | [Size] | [Rationale] |

**Total Dependencies**: [N]
**Dependency Weight**: ✅ Light / ⚠️ Moderate / ❌ Heavy

**Security**:
- Known vulnerabilities: [N] (check: `safety check`)
- Dependency risk: ✅ Low / ⚠️ Moderate / ❌ High

#### License

**License**: [e.g., MIT]
**Commercial Use**: ✅ Allowed / ❌ Restricted
**Attribution Required**: ✅ Yes / ❌ No
**Copyleft**: ✅ Yes / ❌ No

**Compatibility**: ✅ Compatible / ⚠️ Review Needed / ❌ Incompatible

#### Integration Effort

**Estimated Integration Time**: [X hours]

**Integration Approach**:
```python
# Example integration code
from library import SomeClass

class ServiceAdapter(ServiceProtocol):
    def __init__(self):
        self._client = SomeClass()

    def method(self, param):
        return self._client.library_method(param)
```

**Complexity**: ✅ Simple / ⚠️ Moderate / ❌ Complex

**Configuration Required**:
- [Config item 1]
- [Config item 2]

#### Pros

- ✅ [Advantage 1]
- ✅ [Advantage 2]
- ✅ [Advantage 3]

#### Cons

- ❌ [Disadvantage 1]
- ❌ [Disadvantage 2]
- ❌ [Disadvantage 3]

#### Overall Score

| Category | Weight | Score (1-10) | Weighted |
|----------|--------|-------------|----------|
| Feature Coverage | 30% | [X] | [Y] |
| Code Quality | 20% | [X] | [Y] |
| Maintenance | 20% | [X] | [Y] |
| Documentation | 15% | [X] | [Y] |
| Dependencies | 10% | [X] | [Y] |
| License | 5% | [X] | [Y] |
| **TOTAL** | **100%** | - | **[Z]/10** |

---

### Candidate 2: [Library Name]

[Same structure as Candidate 1]

---

### Candidate 3: [Library Name]

[Same structure as Candidate 1]

---

### Option: Build Custom Implementation

**Rationale**: [Why consider building custom?]

#### Estimated Effort

- **Design**: [X hours]
- **Implementation**: [Y hours]
- **Testing**: [Z hours]
- **Documentation**: [W hours]
- **Total**: [N hours]

#### Pros

- ✅ [Advantage 1: e.g., "Exact fit for requirements"]
- ✅ [Advantage 2: e.g., "No external dependencies"]
- ✅ [Advantage 3: e.g., "Full control"]

#### Cons

- ❌ [Disadvantage 1: e.g., "Maintenance burden"]
- ❌ [Disadvantage 2: e.g., "Longer initial development"]
- ❌ [Disadvantage 3: e.g., "Reinventing the wheel"]

#### Long-Term Cost

| Cost Factor | Library | Custom | Winner |
|-------------|---------|--------|--------|
| Initial Development | [Low/Medium/High] | [Low/Medium/High] | ✅ |
| Maintenance (annual) | [Low/Medium/High] | [Low/Medium/High] | ✅ |
| Feature Additions | [Low/Medium/High] | [Low/Medium/High] | ✅ |
| Bug Fixes | [Low/Medium/High] | [Low/Medium/High] | ✅ |

**5-Year TCO**: [Library: $X, Custom: $Y]

---

## Comparison Matrix

| Feature/Metric | Candidate 1 | Candidate 2 | Candidate 3 | Custom |
|----------------|-------------|-------------|-------------|--------|
| **Feature Coverage** | [X]% | [Y]% | [Z]% | 100% |
| **Code Quality** | [Score] | [Score] | [Score] | TBD |
| **Maintenance** | ✅ | ⚠️ | ❌ | Self |
| **Documentation** | ✅ | ✅ | ⚠️ | Self |
| **Dependencies** | [N] | [N] | [N] | 0 |
| **License** | ✅ | ✅ | ❌ | N/A |
| **Integration Effort** | [X]h | [Y]h | [Z]h | [N]h |
| **Long-Term Cost** | Low | Medium | Low | High |
| **Overall Score** | [X]/10 | [Y]/10 | [Z]/10 | [W]/10 |

---

## Decision Matrix

### Must-Have Criteria (Eliminatory)

| Criterion | Candidate 1 | Candidate 2 | Candidate 3 | Custom |
|-----------|-------------|-------------|-------------|--------|
| Meets functional requirements | ✅ | ✅ | ❌ | ✅ |
| License compatible | ✅ | ✅ | ❌ | ✅ |
| Maintained | ✅ | ⚠️ | ❌ | ✅ |
| No critical vulnerabilities | ✅ | ✅ | ❌ | ✅ |

**Eliminated**: Candidate 3 (fails license and maintenance criteria)

---

### Weighted Scoring (Remaining Options)

| Criterion | Weight | Candidate 1 | Candidate 2 | Custom |
|-----------|--------|-------------|-------------|--------|
| Feature richness | 30% | 8 × 0.3 = 2.4 | 7 × 0.3 = 2.1 | 10 × 0.3 = 3.0 |
| Time to integrate | 25% | 9 × 0.25 = 2.25 | 8 × 0.25 = 2.0 | 3 × 0.25 = 0.75 |
| Long-term maintenance | 20% | 8 × 0.2 = 1.6 | 6 × 0.2 = 1.2 | 4 × 0.2 = 0.8 |
| Documentation quality | 15% | 9 × 0.15 = 1.35 | 8 × 0.15 = 1.2 | 5 × 0.15 = 0.75 |
| Community support | 10% | 9 × 0.1 = 0.9 | 5 × 0.1 = 0.5 | 0 × 0.1 = 0 |
| **TOTAL SCORE** | **100%** | **8.5** | **7.0** | **5.3** |

**Winner**: ✅ Candidate 1

---

## Final Recommendation

### ✅ Selected Option: [Library Name OR Custom]

**Rationale**: [Comprehensive explanation of the decision]

**Key Decision Factors**:

1. **Feature Coverage**: [How this option meets requirements]
2. **Integration Effort**: [Why integration effort is acceptable]
3. **Long-Term Viability**: [Why this is sustainable choice]
4. **Cost-Benefit**: [Why this is best value]

**Risks & Mitigations**:

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| [Risk 1] | [Low/Med/High] | [Low/Med/High] | [How to mitigate] |
| [Risk 2] | [Low/Med/High] | [Low/Med/High] | [How to mitigate] |

**Alignment with Use Cases**:
- **UC-001**: [How this supports the use case]
- **UC-002**: [How this supports the use case]

---

## Integration Plan

### Phase 1: Proof of Concept (X hours)

- [ ] Install library and dependencies
- [ ] Create minimal adapter
- [ ] Test with simple use case
- [ ] Verify performance expectations

### Phase 2: Full Integration (Y hours)

- [ ] Implement complete adapter implementing ServiceProtocol
- [ ] Add error handling
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Document configuration

### Phase 3: Production Readiness (Z hours)

- [ ] Load testing
- [ ] Security review
- [ ] Monitoring setup
- [ ] Documentation complete
- [ ] Team training (if needed)

**Total Estimated Time**: [N hours]

---

## Monitoring & Review

### Success Metrics

Track these metrics post-integration:

| Metric | Target | Alert Threshold |
|--------|--------|----------------|
| [Metric 1] | [Target] | [Threshold] |
| [Metric 2] | [Target] | [Threshold] |

### Re-Evaluation Triggers

Re-evaluate this decision if:

- [ ] Library becomes unmaintained (no commits for 12+ months)
- [ ] Critical security vulnerability discovered
- [ ] Performance degrades below acceptable threshold
- [ ] Requirements change significantly
- [ ] Better alternative emerges

**Next Review Date**: [Date or milestone]

---

## Appendix

### Detailed Research Notes

[Any additional notes from research]

### Alternative Approaches Considered

[Other approaches that were considered but not evaluated deeply]

### References

- **Library 1 Docs**: [URL]
- **Library 2 Docs**: [URL]
- **Benchmark Results**: [If performance tested]
- **Security Scans**: [Results of `safety check` or similar]
- **Related ADRs**: ADR-XXX ([Decision name])

### Evaluation Checklist

Used this checklist during evaluation:

- [ ] Functional requirements verified
- [ ] License compatibility confirmed
- [ ] Security scan completed
- [ ] Documentation reviewed
- [ ] Community health assessed
- [ ] Integration approach prototyped
- [ ] Performance acceptable
- [ ] Dependencies analyzed
- [ ] Long-term cost estimated

---

**Evaluation Version**: 1.0
**Framework**: Claude Development Framework v2.0
**Decision Status**: [Draft | Approved | Implemented]
