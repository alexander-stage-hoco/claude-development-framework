# Comparable Agent Mappings - Revised & Honest Assessment

**Purpose**: Honest evaluation of comparable agents with confidence ratings
**Date**: 2025-10-01
**Status**: Critical Review Complete

---

## Methodology

For each of our 6 agents, this analysis:
1. **Defines core task** - What it actually does (inputs → process → outputs)
2. **Evaluates comparable agents** - Based on workflow similarity, not keywords
3. **Assigns confidence rating** - 1-10 scale based on actual alignment
4. **Identifies extractable patterns** - What we can genuinely learn
5. **Acknowledges differences** - What doesn't transfer

**Confidence Scale**:
- **9-10/10**: Near-perfect match, same workflow, extractable domain expertise
- **7-8/10**: Good match, similar methodology, extractable patterns with adaptation
- **5-6/10**: Partial match, useful methodology but different domain
- **3-4/10**: Weak match, only generic patterns extractable
- **1-2/10**: No meaningful match, forced comparison

**Inclusion criteria**: Only present mappings with confidence ≥6/10

---

## High Confidence Mappings (8-10/10)

### 1. service-designer ← api-designer (8/10)

**Our Agent**: service-designer
**Comparable**: VoltAgent/api-designer

#### What service-designer Does:
```
Input: Service specification (high-level)
Process:
  1. Design Protocol-based interface
  2. Define immutable data models
  3. Create error type hierarchy
  4. Document 2-3 implementation strategies
  5. Plan testing approach
Output: Detailed service specification with interfaces, models, strategies
```

#### What api-designer Does:
```
Input: API requirements
Process:
  1. Design REST/GraphQL interface
  2. Define request/response schemas
  3. Create error response formats
  4. Document API contract (OpenAPI/GraphQL schema)
  5. Plan testing approach
Output: API specification with endpoints, schemas, examples
```

#### Why This Mapping Works:

✅ **Core similarity**: Both do **contract-first interface design**
- Both start with requirements
- Both create formal interface specifications
- Both define data models/schemas
- Both plan for error handling
- Both include testing strategies

✅ **Methodology transfers**:
- Contract-first approach
- Type specification discipline
- Multiple implementation strategies
- Systematic design workflow

#### Critical Differences:

⚠️ **Protocol layer**:
- api-designer: HTTP-based (REST/GraphQL)
- service-designer: In-process (Python Protocols)

⚠️ **Type systems**:
- api-designer: OpenAPI schemas, GraphQL schemas
- service-designer: Python type hints, Protocol classes

⚠️ **Scope**:
- api-designer: External-facing APIs (client-server)
- service-designer: Internal interfaces (service-to-service)

#### What We Can Extract:

✅ **From api-designer checklist**:
```markdown
### API Design Checklist (adapted to service-designer)
- **Interface Design**: Methods, signatures, protocols
- **Data Models**: Domain models, DTOs, validation
- **Error Handling**: Error types, Result pattern
- **Documentation**: Docstrings, examples, specifications
- **Versioning**: Interface evolution strategy
```

✅ **From api-designer workflow**:
```markdown
1. Requirements - Understand use cases
2. Design - Create interface contract
3. Review - Validate design
4. Document - Comprehensive documentation
5. Mock - Create test implementations
```

✅ **From api-designer best practices**:
- Design contract first (before implementation)
- Use consistent naming conventions
- Provide comprehensive examples
- Document all error cases
- Support evolution (versioning)

#### What NOT to Extract:

❌ REST-specific patterns (HTTP methods, status codes, HATEOAS)
❌ GraphQL-specific patterns (queries, mutations, subscriptions)
❌ API gateway concepts (rate limiting, authentication headers)
❌ Network-related concerns (caching, ETags, CORS)

#### Confidence: 8/10

**Rationale**: Both agents do interface design with type specifications and contract-first approach. The methodology is highly transferable despite different protocol layers (HTTP vs. Python).

---

### 2. service-optimizer ← ml-engineer (8/10)

**Our Agent**: service-optimizer
**Comparable**: VoltAgent/ml-engineer

#### What service-optimizer Does:
```
Input: Service specification with multiple implementation strategies
Process:
  1. Implement 2-3 alternative strategies
  2. Create benchmark suite (realistic data)
  3. Run benchmarks (measure latency, throughput, memory)
  4. Analyze results (compare metrics)
  5. Recommend optimal strategy (data-driven)
Output: Benchmark report with recommendation and rationale
```

#### What ml-engineer Does:
```
Input: ML problem specification
Process:
  1. Define problem and metrics
  2. Implement multiple models/approaches
  3. Train and validate models
  4. Tune hyperparameters (systematic search)
  5. Evaluate on test set (measure accuracy, loss, latency)
  6. Compare alternatives (A/B testing)
  7. Recommend optimal model (data-driven)
Output: Model evaluation report with recommendation
```

#### Why This Mapping Works:

✅ **Core similarity**: Both do **systematic benchmarking for optimization**
- Both implement multiple alternatives
- Both measure performance metrics
- Both use data-driven decision making
- Both compare trade-offs (accuracy vs. speed, complexity vs. performance)
- Both recommend based on empirical evidence

✅ **Methodology is nearly identical**:
- Create benchmark/test suite
- Run systematic experiments
- Measure multiple metrics
- Analyze trade-offs
- Make evidence-based recommendations

#### Critical Differences:

⚠️ **Domain**:
- ml-engineer: ML models (hyperparameters, architecture, training)
- service-optimizer: Code implementations (algorithms, data structures, libraries)

⚠️ **Metrics**:
- ml-engineer: Accuracy, precision, recall, F1, loss, convergence
- service-optimizer: Latency, throughput, memory, CPU, cost

⚠️ **Optimization target**:
- ml-engineer: Model performance (prediction quality)
- service-optimizer: Code performance (execution speed)

#### What We Can Extract:

✅ **From ml-engineer optimization workflow**:
```markdown
1. Problem Definition - Understand requirements and success metrics
2. Strategy Identification - Identify 2-3 alternatives to test
3. Implementation - Code each approach
4. Benchmarking - Create comprehensive test suite
5. Evaluation - Measure all relevant metrics
6. Analysis - Compare trade-offs (performance vs. complexity vs. cost)
7. Recommendation - Data-driven decision with rationale
```

✅ **From ml-engineer metrics approach**:
- Multiple metrics (not just one): latency p50/p95/p99, throughput, memory
- Trade-off analysis: Fast but memory-heavy vs. slow but efficient
- Cost analysis: Development time vs. runtime efficiency
- Realistic data: Test with production-like workloads

✅ **From ml-engineer best practices**:
- Start simple, iterate to complexity
- Track all experiments systematically
- Use held-out test set (don't overfit to benchmarks)
- Document assumptions and limitations
- Consider multiple dimensions (not just speed)

#### What NOT to Extract:

❌ ML-specific: Feature engineering, hyperparameter tuning, model architectures
❌ Training-specific: Epochs, batches, learning rates, convergence criteria
❌ Data-specific: Data cleaning, validation, versioning (not relevant to code optimization)
❌ Deployment-specific: Model serving, A/B testing with real users, drift detection

#### Confidence: 8/10

**Rationale**: The benchmarking and optimization methodology is nearly identical despite different domains. Both use systematic experimentation, multiple metrics, and data-driven decisions.

---

### 3. uc-service-tracer ← security-auditor (8/10)

**Our Agent**: uc-service-tracer
**Comparable**: VoltAgent/security-auditor

#### What uc-service-tracer Does:
```
Input: Use case specifications + Service specifications
Process:
  1. Parse "Services Used" sections from all UCs
  2. Validate service references (specs exist, methods match)
  3. Check bidirectional traceability (UC→Service and Service→UC agree)
  4. Detect orphans (services not referenced by any UC)
  5. Build traceability matrices (UC→Services, Service→UCs)
  6. Report violations with evidence
Output: Traceability compliance report with violations and recommendations
```

#### What security-auditor Does:
```
Input: System documentation + Security requirements/frameworks
Process:
  1. Scope Definition - Define audit objectives, compliance requirements
  2. Information Gathering - Inventory assets, review documentation
  3. Vulnerability Assessment - Scan for issues
  4. Compliance Review - Map controls to framework requirements
  5. Gap Analysis - Identify missing controls
  6. Findings Documentation - Document issues with evidence
  7. Remediation Plan - Provide specific recommendations
Output: Security audit report with findings, gaps, and recommendations
```

#### Why This Mapping Works:

✅ **Core similarity**: Both do **compliance validation against specifications**
- Both validate compliance to a standard (UC specs vs. security frameworks)
- Both check coverage (all UCs have services vs. all controls present)
- Both detect gaps/orphans (unused services vs. missing controls)
- Both validate bidirectional relationships (UC↔Service vs. Control↔Requirement)
- Both report violations with evidence

✅ **Methodology is highly similar**:
- Parse source documents
- Extract requirements/references
- Validate completeness
- Check bidirectional consistency
- Detect gaps and orphans
- Report findings with evidence
- Provide remediation recommendations

#### Critical Differences:

⚠️ **Domain**:
- security-auditor: Security compliance (OWASP, SOC 2, ISO 27001)
- uc-service-tracer: Specification traceability (UC ↔ Service)

⚠️ **Validation target**:
- security-auditor: Security controls, vulnerabilities, compliance
- uc-service-tracer: Service references, method signatures, traceability

⚠️ **Tools**:
- security-auditor: Vulnerability scanners (Nessus, Qualys, Prowler)
- uc-service-tracer: Document parsing (Grep, Glob)

#### What We Can Extract:

✅ **From security-auditor audit workflow**:
```markdown
1. Scope Definition - Define what to validate (all UCs, all services)
2. Information Gathering - Parse specifications, extract references
3. Compliance Review - Validate UC→Service and Service→UC mappings
4. Gap Analysis - Identify missing references, orphan services
5. Findings Documentation - Document violations with evidence
6. Remediation Plan - Recommend fixes (add service refs, remove orphans)
```

✅ **From security-auditor validation approach**:
- **Evidence-based**: Every finding has specific evidence (file, line number)
- **Severity levels**: Critical (missing service ref) vs. Warning (orphan service)
- **Bidirectional checking**: Requirement→Control AND Control→Requirement
- **Gap detection**: What's missing vs. what's there
- **Actionable recommendations**: Specific fixes, not just identification

✅ **From security-auditor best practices**:
- Document all findings with evidence
- Prioritize by impact (critical UCs without services)
- Provide specific remediation steps
- Map findings to compliance requirements (UC specs)
- Maintain confidentiality (service architecture)
- Track remediation progress

#### What NOT to Extract:

❌ Security-specific: Vulnerability scanning, penetration testing, threat modeling
❌ Compliance frameworks: SOC 2, ISO 27001, HIPAA, PCI-DSS specifics
❌ Security tools: Nessus, Qualys, OpenVAS, Prowler
❌ Network security: Firewall rules, encryption, access controls

#### Confidence: 8/10

**Rationale**: Both agents do compliance validation with very similar methodology: parse specifications, validate coverage, check bidirectional relationships, detect gaps, report violations. The audit/compliance workflow is nearly identical despite different domains.

---

## Medium Confidence Mappings (6-7/10)

### 4. service-extractor ← backend-architect (6/10)

**Our Agent**: service-extractor
**Comparable**: wshobson/backend-architect

#### What service-extractor Does:
```
Input: Use case specifications (requirements)
Process:
  1. Read all UC specs, extract capabilities
  2. Identify required capabilities (data, validation, integrations)
  3. Group capabilities by business domain
  4. Define service boundaries (single responsibility)
  5. Minimize dependencies (≤3 per service)
  6. Create high-level service specs
  7. Update service registry
Output: Service extraction report with service boundaries, dependency graph, traceability
```

#### What backend-architect Does:
```
Input: System requirements (somewhat implicit)
Process:
  1. Define service boundaries
  2. Design RESTful APIs
  3. Design database schemas
  4. Plan for scalability
  5. Identify bottlenecks
Output: API endpoint definitions, service architecture diagram, database schema, scaling plan
```

#### Why This Mapping Has Merit:

✅ **Overlap**: Both think about **service boundaries**
- Both define what services should exist
- Both consider scalability and dependencies
- Both create architecture diagrams/documentation

✅ **Shared concern**: Avoiding poor service boundaries
- Both avoid "God Services"
- Both think about cohesion and coupling
- Both consider dependencies

#### Critical Differences:

⚠️ **Phase of work**:
- service-extractor: **Discovery/Analysis** - "What services do we need?"
- backend-architect: **Design/Specification** - "How should these services work?"

⚠️ **Inputs**:
- service-extractor: Use case specifications (explicit requirements)
- backend-architect: System requirements (often implicit or high-level)

⚠️ **Outputs**:
- service-extractor: High-level service boundaries (name, responsibility, 3-5 methods)
- backend-architect: Detailed designs (API endpoints, database schemas, diagrams)

⚠️ **Process**:
- service-extractor: Requirements analysis → capability extraction → grouping → boundary definition
- backend-architect: Architecture design → API design → schema design → scalability planning

#### What We Can Extract (Limited):

✅ **From backend-architect approach**:
```markdown
1. Start with clear service boundaries (emphasis on clarity)
2. Consider scalability from day one
3. Think about dependencies early
4. Keep it simple - avoid premature complexity
```

✅ **From backend-architect mindset**:
- Single Responsibility Principle for services
- Plan for horizontal scaling
- Consider data consistency requirements
- Avoid premature optimization

#### What NOT to Extract:

❌ API design patterns (REST endpoints, versioning)
❌ Database schema design (our agent doesn't design schemas)
❌ Technology recommendations (our agent is implementation-agnostic)
❌ Detailed architecture diagrams (our agent creates high-level specs)

#### Confidence: 6/10

**Rationale**: Both agents think about service boundaries, but service-extractor is focused on **identification/discovery** while backend-architect is focused on **design/specification**. The overlap is real but limited to high-level architectural thinking. We can extract mindset and principles, but not specific methodology.

**Assessment**: Useful for borrowing architectural principles and service boundary thinking, but not a close process match.

---

### 5. service-library-finder ← cloud-architect (6/10)

**Our Agent**: service-library-finder
**Comparable**: VoltAgent/cloud-architect (platform selection aspect)

#### What service-library-finder Does:
```
Input: Service specification (requirements)
Process:
  1. Search for candidate libraries (PyPI, GitHub, Awesome Lists)
  2. Screen candidates (active, documented, tested, compatible)
  3. Evaluate quality (tests, types, docs, maintenance)
  4. Assess feature coverage (must-have ≥80%)
  5. Compare alternatives (weighted scoring: Features 40%, Quality 25%, etc.)
  6. Make build-vs-buy recommendation (score ≥70% = use library)
Output: Library evaluation report with recommendation, decision matrix, implementation guide
```

#### What cloud-architect Does (Platform Selection):
```
Input: System requirements (compute, storage, networking, compliance)
Process:
  1. Understand requirements (performance, compliance, budget)
  2. Evaluate platforms (AWS, Azure, GCP)
  3. Compare features (compute options, database offerings, networking)
  4. Assess costs (pricing models, reserved instances, spot instances)
  5. Consider compliance (HIPAA, SOC2, GDPR)
  6. Make platform recommendation
Output: Cloud architecture design with platform choice, cost estimates, compliance plan
```

#### Why This Mapping Has Merit:

✅ **Core similarity**: Both do **alternative evaluation and selection**
- Both evaluate multiple alternatives (libraries vs. platforms)
- Both use systematic evaluation criteria
- Both make recommendations based on requirements
- Both consider trade-offs (cost, features, complexity)

✅ **Methodology overlap**:
- Requirements analysis
- Alternative identification
- Criteria-based evaluation
- Trade-off analysis
- Recommendation with rationale

#### Critical Differences:

⚠️ **Scale**:
- service-library-finder: Library selection (small decisions, reversible)
- cloud-architect: Platform selection (large decisions, harder to reverse)

⚠️ **Domain**:
- service-library-finder: Software libraries (PyPI, npm packages)
- cloud-architect: Cloud platforms (AWS, Azure, GCP infrastructure)

⚠️ **Evaluation criteria**:
- service-library-finder: Features, quality, maintenance, community
- cloud-architect: Multi-cloud strategy, security, compliance, cost optimization

⚠️ **Scope**:
- service-library-finder: Single service, single library
- cloud-architect: Entire system, infrastructure architecture

#### What We Can Extract (Limited):

✅ **From cloud-architect evaluation methodology**:
```markdown
1. Requirements - Understand needs before evaluating alternatives
2. Platform/Library Selection - Identify candidates
3. Feature Comparison - Map features to requirements
4. Cost Analysis - Estimate costs (library: development time vs. maintenance)
5. Compliance/Quality Check - Validate against standards
6. Recommendation - Data-driven decision with rationale
```

✅ **From cloud-architect decision-making**:
- Multi-criteria decision matrix
- Weighted scoring
- Trade-off analysis (features vs. cost vs. complexity)
- Consider long-term implications (maintenance, vendor lock-in)

#### What NOT to Extract:

❌ Infrastructure-specific: VPC design, security groups, load balancers
❌ Cloud-specific: Multi-cloud strategy, reserved instances, auto-scaling
❌ Scale considerations: Multi-region deployment, disaster recovery
❌ Compliance frameworks: HIPAA, SOC2, GDPR (not relevant to library selection)

#### Confidence: 6/10

**Rationale**: Both agents do systematic evaluation and selection of alternatives, but the domains are quite different (libraries vs. cloud platforms). The evaluation methodology is transferable (requirements analysis, criteria-based comparison, trade-off analysis), but the specific criteria and scale are different.

**Assessment**: Useful for borrowing evaluation methodology and decision-making approach, but not domain expertise.

---

## No Good Mapping Found

### 6. service-dependency-analyzer (No comparable agent)

**Our Agent**: service-dependency-analyzer

#### What service-dependency-analyzer Does:
```
Input: Service specifications (with dependencies listed)
Process:
  1. Build dependency graph (adjacency list)
  2. Detect circular dependencies (DFS algorithm)
  3. Compute dependency layers (topological sort)
  4. Validate dependency limits (≤3 per service)
  5. Recommend refactoring for violations
  6. Update registry with layer information
Output: Dependency analysis report with graph, cycles, violations, recommendations
```

#### Why No Good Comparable Agent Exists:

❌ **None of the community agents do graph analysis**:
- code-reviewer: Reviews code quality, not dependency graphs
- cloud-architect: Designs infrastructure, not service dependencies
- security-auditor: Validates security compliance, not architectural structure

❌ **None use graph algorithms**:
- No DFS (depth-first search) for cycle detection
- No topological sort for layer computation
- No graph-based structural analysis

❌ **None validate architectural constraints**:
- No dependency limit validation
- No layered architecture enforcement
- No acyclic dependency graph (DAG) validation

#### What We Need (But Don't Have):

**Ideal comparable agents** (don't exist in wshobson/VoltAgent):
1. **Build system analyzer** - Analyzes build dependency graphs, detects cycles
2. **Package manager validator** - Validates package dependencies, detects conflicts
3. **Architecture compliance checker** - Validates architectural rules
4. **Static analysis agent** - Analyzes code structure, detects design issues

#### What We Can Extract (Generic Only):

✅ **Generic validation patterns** (from code-reviewer, security-auditor):
```markdown
1. Systematic approach - Step-by-step validation
2. Checklist format - Categories of things to check
3. Report structure - Summary, findings, recommendations
4. Severity levels - Critical (cycles) vs. Warning (>3 deps)
```

⚠️ **But NOT domain-specific methodology**:
- Graph algorithms: We already have these (DFS, topological sort)
- Dependency analysis: We already know how to do this
- Architectural validation: This is our unique expertise

#### Confidence: N/A (No comparable agent exists)

**Assessment**: service-dependency-analyzer is a **unique agent** with no good comparable in the community repositories. We can extract generic validation methodology (systematic approach, checklists, reporting), but the core graph analysis and architectural validation expertise is our own.

**What this means**: For this agent, we should:
1. ✅ Borrow generic patterns (checklists, report structure, systematic validation)
2. ✅ Keep our domain expertise (graph algorithms, architectural constraints)
3. ❌ Don't claim we "extracted patterns from comparable agents" - we're synthesizing

---

## Summary: Mapping Quality by Agent

| Agent | Comparable Agent | Confidence | What We Extract | Type |
|-------|------------------|------------|-----------------|------|
| **service-designer** | api-designer | 8/10 | Contract-first design, interface methodology | **Extract** |
| **service-optimizer** | ml-engineer | 8/10 | Benchmarking methodology, metrics approach | **Extract** |
| **uc-service-tracer** | security-auditor | 8/10 | Compliance validation, audit workflow | **Extract** |
| **service-extractor** | backend-architect | 6/10 | Architectural principles, service boundary thinking | **Adapt** |
| **service-library-finder** | cloud-architect | 6/10 | Evaluation methodology, decision-making | **Adapt** |
| **service-dependency-analyzer** | (none) | N/A | Generic validation patterns only | **Synthesize** |

---

## Key Insights

### Insight #1: Only 3/6 Agents Have Good Comparable Agents

**High confidence (8/10)**: service-designer, service-optimizer, uc-service-tracer
- These have genuinely similar workflows in community repos
- Methodology is directly transferable with adaptation
- Domain expertise can be extracted (not just generic patterns)

**Medium confidence (6/10)**: service-extractor, service-library-finder
- Related but not closely aligned workflows
- Can extract high-level methodology and principles
- Domain expertise doesn't transfer, only approach

**No good match**: service-dependency-analyzer
- Unique graph analysis focus
- No comparable agent in community
- Must rely on our own expertise

### Insight #2: What We're Actually Extracting

**Reality check**:
- ✅ **Generic methodology** (systematic approach, checklists, validation workflow)
- ✅ **Presentation structure** (sections, report formats, documentation)
- ✅ **Best practices** (contract-first, data-driven, evidence-based)
- ⚠️ **Adapted workflows** (benchmarking, compliance validation, interface design)
- ❌ **Domain expertise** (limited - mostly we already had this)

**Honest assessment**: We're borrowing *form* and *methodology*, not *content*.

### Insight #3: Our Agents Are More Specialized

**Community agents**: General-purpose (backend-developer, code-reviewer, cloud-architect)
**Our agents**: Highly specialized (service-extractor, uc-service-tracer, service-dependency-analyzer)

**Implication**: We operate in a niche (service-oriented architecture with UC-Service traceability) that doesn't have direct equivalents. This is fine - it means our framework offers unique value.

### Insight #4: Synthesis vs. Extraction

**For 3 agents (50%)**, we're not extracting patterns - we're synthesizing:
- service-extractor: Adapting architectural thinking to requirements analysis
- service-library-finder: Synthesizing evaluation criteria from general principles
- service-dependency-analyzer: Applying graph algorithms with validation patterns

**This is legitimate**, but we should be honest about it.

---

## Recommendations

### 1. Update EXTRACTED-PATTERNS.md

**Clarify confidence levels**:
- Mark high-confidence mappings: service-designer, service-optimizer, uc-service-tracer
- Mark medium-confidence mappings: service-extractor, service-library-finder
- Mark no-mapping: service-dependency-analyzer
- Add "Confidence: X/10" to each mapping section

### 2. Reframe "Extraction" Language

**Replace**: "Extracted patterns from comparable agents"
**With**: "Adapted patterns from comparable agents (where available) and synthesized from best practices (where needed)"

### 3. Focus on Strong Mappings

**Prioritize learnings from**:
- api-designer → service-designer (contract-first design)
- ml-engineer → service-optimizer (benchmarking methodology)
- security-auditor → uc-service-tracer (compliance validation)

**De-emphasize weaker mappings**:
- backend-architect → service-extractor (limited overlap)
- cloud-architect → service-library-finder (different scale/domain)

### 4. Acknowledge Our Unique Contributions

**Be proud that 50% of our agents are unique**:
- service-dependency-analyzer: Graph-based architectural validation (unique)
- uc-service-tracer: UC-Service bidirectional traceability (unique)
- service-extractor: UC-driven service identification (unique)

**These are valuable because they don't have equivalents** - they solve problems the community hasn't addressed.

---

## Conclusion

**Honest assessment**:
- We have **3 genuinely good comparable agents** (8/10 confidence)
- We have **2 partially useful comparables** (6/10 confidence)
- We have **1 unique agent** with no comparable

**What this means**:
- ✅ We can confidently extract patterns from api-designer, ml-engineer, security-auditor
- ⚠️ We should adapt (not copy) from backend-architect, cloud-architect
- ✅ We should synthesize our own patterns for service-dependency-analyzer

**Reality**: We're operating in a specialized niche (service-oriented architecture with traceability) that doesn't have full community coverage. That's fine - it's what makes our framework valuable.

**Grade**: **Revised mapping = B+** (Honest, defensible, acknowledges limitations)

---

**Document Version**: 2.0 (Revised)
**Date**: 2025-10-01
**Status**: Critical Review Complete
**Confidence Levels**: Clearly stated for all mappings
**Honest Assessment**: No forced comparisons, acknowledges synthesis where needed
