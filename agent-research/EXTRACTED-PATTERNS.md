# Extracted Patterns from Community Agents

**Purpose**: Reusable patterns from wshobson/agents and VoltAgent for improving our 6 service-oriented agents
**Date**: 2025-10-01
**Status**: Ready for Review and Implementation

---

## Pattern Categories

1. [Trigger Keywords](#trigger-keywords) - Automatic invocation patterns
2. [Description Structures](#description-structures) - Role + expertise + skills
3. [Checklist Formats](#checklist-formats) - Actionable task lists
4. [Workflow Patterns](#workflow-patterns) - Process steps
5. [Best Practices](#best-practices) - Concise, practical advice
6. [Output Formats](#output-formats) - Report structures

---

## Trigger Keywords

### From wshobson/agents (100% use these)

**Pattern 1: "Use PROACTIVELY when..."**
```yaml
# General automatic invocation
description: "... Use PROACTIVELY when [trigger condition]."
```

**Examples**:
- backend-architect: "Use PROACTIVELY when creating new backend services or APIs."
- code-reviewer: "Use PROACTIVELY for code quality assurance."

**Pattern 2: "MUST BE USED for..."**
```yaml
# Enforcement - stronger than PROACTIVELY
description: "... MUST BE USED for [critical task]."
```

**Pattern 3: Conditional "Use when..."**
```yaml
# Conditional invocation
description: "... Use when [specific condition exists]."
```

### Application to Our Agents

| Agent | Keyword | Trigger Pattern |
|-------|---------|-----------------|
| **service-extractor** | PROACTIVELY | "Use PROACTIVELY when analyzing use cases or designing service boundaries" |
| **service-designer** | PROACTIVELY | "Use PROACTIVELY when designing service interfaces or data models" |
| **service-library-finder** | PROACTIVELY | "Use PROACTIVELY before implementing any service to find existing solutions" |
| **service-dependency-analyzer** | MUST BE USED | "MUST BE USED before TDD implementation to validate service dependencies" |
| **uc-service-tracer** | MUST BE USED | "MUST BE USED after service extraction and before implementation" |
| **service-optimizer** | Use when | "Use when performance requirements exist in UC specs or benchmarking needed" |

---

## Description Structures

### Pattern 1: wshobson Style (Concise, 200-300 chars)

**Structure**: `Role + Expertise + Trigger`

**Template**:
```yaml
description: "[Verb] [domain]. [Specialization details]. Use PROACTIVELY when [trigger]."
```

**Examples**:
- backend-architect (202 chars): "Design RESTful APIs, microservice boundaries, and database schemas. Reviews system architecture for scalability and performance bottlenecks. Use PROACTIVELY when creating new backend services or APIs."

### Pattern 2: VoltAgent Style (Detailed, 250-350 chars)

**Structure**: `Expert [role] + specializing in [expertise] + Focus on [outcomes]`

**Template**:
```yaml
description: "Expert [role] specializing in [expertise]. [Action verb] [deliverables] with focus on [qualities]."
```

**Examples**:
- api-designer (235 chars): "API architecture expert designing scalable, developer-friendly interfaces. Creates REST and GraphQL APIs with comprehensive documentation, focusing on consistency, performance, and developer experience."

### Pattern 3: Extended Expertise (For complex agents)

**Structure**: `Expert [role] + specializing in [expertise] + Masters [key skills]`

**Template**:
```yaml
description: "Expert [role] specializing in [expertise]. Masters [skill1], [skill2], and [skill3] with focus on [outcomes]."
```

**Example** (synthesized):
- code-reviewer: "Elite code review expert specializing in modern AI-powered code analysis, security vulnerabilities, performance optimization, and production reliability. Masters static analysis tools, security scanning, and configuration review with 2024/2025 best practices."

### Application to Our Agents

**service-extractor** (Target: 245 chars):
```yaml
description: "Expert service architect specializing in extracting reusable services from use case specifications. Masters service-oriented architecture, domain-driven design, and minimal dependency patterns. Use PROACTIVELY when analyzing use cases or designing service boundaries."
```

**service-designer** (Target: 250 chars):
```yaml
description: "Expert interface designer specializing in Protocol-based interfaces, type-safe data models, and Result types. Masters Python typing, dependency injection, immutable data patterns, and test-driven design. Use PROACTIVELY when designing service interfaces or data models."
```

**service-dependency-analyzer** (Target: 230 chars):
```yaml
description: "Expert dependency analyst detecting circular dependencies and validating layered architecture compliance. Masters graph algorithms, dependency injection patterns, and architectural quality metrics. MUST BE USED before TDD implementation to validate service dependencies."
```

**service-optimizer** (Target: 255 chars):
```yaml
description: "Expert performance engineer specializing in benchmarking implementation strategies and data-driven optimization decisions. Masters profiling, statistical analysis, trade-off evaluation, and cost-benefit analysis. Use when performance requirements exist in UC specs or benchmarking needed."
```

**service-library-finder** (Target: 260 chars):
```yaml
description: "Expert library evaluator specializing in finding, assessing, and recommending external libraries before custom implementation. Masters PyPI/npm search, quality assessment, feature matrices, and build-vs-buy decisions. Use PROACTIVELY before implementing any service to find existing solutions."
```

**uc-service-tracer** (Target: 245 chars):
```yaml
description: "Expert traceability validator ensuring bidirectional UC-Service traceability and detecting orphan services. Masters graph validation, compliance checking, traceability matrices, and architectural quality metrics. MUST BE USED after service extraction and before implementation."
```

---

## Checklist Formats

### VoltAgent Pattern (Comprehensive)

**Structure**: Categorized checklist with bold categories + specific tasks

```markdown
## [Agent Name] Checklist
- **Category 1**: Specific tasks, deliverables
- **Category 2**: Specific tasks, deliverables
- **Category 3**: Specific tasks, deliverables
- **Category 4**: Specific tasks, deliverables
```

**Example from backend-developer**:
```markdown
### Backend Development Checklist
- **API Design**: RESTful/GraphQL endpoints, versioning, documentation
- **Database Architecture**: Schema design, indexing, query optimization
- **Security**: Authentication, authorization, data encryption, OWASP compliance
- **Performance**: Caching strategies, load balancing, horizontal scaling
- **Testing**: Unit tests, integration tests, API tests
- **Microservices**: Service boundaries, inter-service communication, orchestration
- **Message Queues**: Event-driven architecture, async processing
```

**Example from api-designer**:
```markdown
### API Design Checklist
- **REST Design**: Resources, HTTP methods, status codes, HATEOAS
- **GraphQL Design**: Schema, queries, mutations, subscriptions
- **Documentation**: OpenAPI 3.0, GraphQL schema, examples
- **Versioning**: URL versioning, header versioning, deprecation
- **Authentication**: OAuth2, JWT, API keys, RBAC
- **Error Handling**: Consistent error format, problem details (RFC 7807)
- **Pagination**: Cursor-based, offset-based pagination
- **Filtering & Sorting**: Query parameters, GraphQL arguments
- **Rate Limiting**: Per-user limits, rate limit headers
- **Performance**: Caching, ETags, conditional requests
```

### Application to Our Agents

**service-extractor checklist**:
```markdown
## Service Extraction Checklist
- **Context**: Read all UC specs, extract capabilities
- **Boundaries**: Group by domain, ensure single responsibility
- **Dependencies**: Validate ≤3 deps, detect cycles
- **Specs**: Create service-spec.md files
- **Registry**: Update catalog, dependency graph, UC references
```

**service-designer checklist**:
```markdown
## Interface Design Checklist
- **Protocols**: Type-safe interfaces with docstrings
- **Data Models**: Immutable, validated domain models
- **Error Types**: Result[Success, Error] pattern
- **Dependencies**: Interface-based (Protocol), not concrete
- **Strategies**: Document 2-3 implementation approaches
- **Testing**: Define contract, unit, integration tests
```

**service-dependency-analyzer checklist**:
```markdown
## Dependency Analysis Checklist
- **Mapping**: Build adjacency list of all dependencies
- **Cycles**: Run DFS to detect circular dependencies
- **Layers**: Compute via topological sort
- **Limits**: Validate ≤3 service deps per service
- **Violations**: Document with refactoring recommendations
- **Registry**: Update with layer information
```

**service-optimizer checklist**:
```markdown
## Optimization Checklist
- **Strategies**: Identify 2-3 alternatives from spec
- **Implementation**: Code each approach
- **Benchmarks**: Create suite with realistic data
- **Execution**: Run with multiple data sizes
- **Analysis**: Compare latency, throughput, memory, cost
- **Decision**: Recommend based on requirements + trade-offs
```

**service-library-finder checklist**:
```markdown
## Library Evaluation Checklist
- **Search**: Find 3-5 candidates (PyPI, GitHub, Awesome Lists)
- **Screening**: Active, documented, tested, compatible
- **Features**: Must-have coverage ≥80%
- **Quality**: Types, tests, docs, maintenance
- **Community**: Stars, downloads, contributors
- **Decision**: Score ≥70% = use library
```

**uc-service-tracer checklist**:
```markdown
## Traceability Validation Checklist
- **UC Parsing**: Extract service references from all UCs
- **Validation**: Service specs exist, methods match
- **Bidirectional**: UC→Service and Service→UC agree
- **Orphans**: Identify services not used by any UC
- **Matrices**: Build UC→Service and Service→UC views
- **Report**: Document violations with action items
```

---

## Workflow Patterns

### wshobson Pattern (Simple, 3-5 steps)

**Structure**: High-level approach steps

**Example from backend-architect**:
```markdown
## Approach
1. Start with clear service boundaries
2. Design APIs contract-first
3. Consider data consistency requirements
4. Plan for horizontal scaling from day one
5. Keep it simple - avoid premature optimization
```

### VoltAgent Pattern (Detailed, 7-8 phases)

**Structure**: Phase name + description

**Example from backend-developer**:
```markdown
### Workflow
1. **Analyze** - Review requirements, existing architecture, constraints
2. **Design** - Create API contracts, data models, service boundaries
3. **Implement** - Write code following best practices and patterns
4. **Test** - Comprehensive test coverage at all levels
5. **Optimize** - Performance tuning, caching, query optimization
6. **Deploy** - CI/CD, monitoring, logging, alerting
7. **Document** - API docs, architecture diagrams, runbooks
```

**Example from ml-engineer**:
```markdown
### Workflow
1. **Problem Definition** - Understand business problem and success metrics
2. **Data Analysis** - Explore data, identify issues, feature engineering
3. **Model Development** - Train and validate models iteratively
4. **Optimization** - Hyperparameter tuning, model compression
5. **Evaluation** - Comprehensive evaluation on test set
6. **Deployment** - Deploy to production with monitoring
7. **Monitor** - Track model performance, detect drift
8. **Iterate** - Continuous improvement based on feedback
```

### Application to Our Agents

All our agents already have good process sections. Pattern to preserve:
- Use numbered steps
- Keep to 5-7 steps (not 8-10)
- Use brief descriptions
- Reference framework templates/files

---

## Best Practices

### wshobson Pattern (Concise bullets)

**Structure**: Short, actionable statements

**Example from backend-architect**:
```markdown
Always provide concrete examples and focus on practical implementation over theory.
```

**Example from code-reviewer**:
```markdown
## Review Principles
- Be constructive and educational
- Explain the "why" behind recommendations
- Provide code examples for fixes
- Balance perfection with pragmatism
- Prioritize security and correctness over style
- Consider the broader system context

Focus on issues that matter - don't bikeshed minor style points when there are real problems to address.
```

### VoltAgent Pattern (Comprehensive list)

**Structure**: Bullet list of specific practices

**Example from backend-developer**:
```markdown
## Best Practices
- Design APIs contract-first with OpenAPI/GraphQL schemas
- Implement comprehensive error handling and logging
- Use database transactions for data consistency
- Apply caching at multiple layers (Redis, CDN)
- Follow 12-factor app methodology
- Implement health checks and observability
- Use environment-based configuration
- Version APIs properly
- Document everything

Focus on building scalable, maintainable, and secure backend systems that can grow with business needs.
```

**Example from api-designer**:
```markdown
## Best Practices
- Design API contract first
- Use consistent naming conventions
- Provide comprehensive examples
- Version APIs from the start
- Use appropriate HTTP status codes
- Implement proper error responses
- Support filtering, sorting, pagination
- Document rate limits clearly
- Provide SDKs in popular languages
- Maintain changelog for API changes
- Use JSON:API or similar standard
- Implement CORS properly
- Support both JSON and form data where appropriate

Focus on creating APIs that are intuitive, well-documented, and provide an excellent developer experience.
```

### Application to Our Agents

Our agents should adopt concise best practices lists (5-7 bullets) with:
- Framework-specific practices (reference development-rules.md)
- Service-oriented principles
- Traceability requirements
- Template usage

---

## Output Formats

### wshobson Pattern (Simple bullets)

**Example from backend-architect**:
```markdown
## Output
- API endpoint definitions with example requests/responses
- Service architecture diagram (mermaid or ASCII)
- Database schema with key relationships
- List of technology recommendations with brief rationale
- Potential bottlenecks and scaling considerations
```

### VoltAgent Pattern (Structured sections)

**Example from code-reviewer**:
```markdown
## Review Output Format
For each issue:
- **Severity**: Critical / High / Medium / Low
- **Category**: Security / Performance / Bug / Maintainability / Style
- **Location**: File and line number
- **Issue**: Clear description
- **Recommendation**: Specific fix or improvement
- **Example**: Code snippet showing better approach
```

### Application to Our Agents

Our agents already have good output formats. Keep structured report formats with:
- Clear sections
- Metrics/statistics
- Traceability information
- Next steps

---

## Model Selection Patterns

### From wshobson/agents only (100% specify)

**Pattern**: Strategic use based on task complexity

**opus** (complex reasoning):
- backend-architect: "Design RESTful APIs, microservice boundaries, and database schemas"
- code-reviewer: "Elite code review expert specializing in modern AI-powered code analysis"

**sonnet** (standard development):
- frontend-developer: "Build React components..."
- Most other developers

### Application to Our Agents

| Agent | Model | Rationale |
|-------|-------|-----------|
| **service-extractor** | opus | Complex architecture reasoning (service boundaries, dependencies) |
| **service-designer** | opus | Complex interface design (Protocols, data models, strategies) |
| **service-dependency-analyzer** | sonnet | Analysis task (graph algorithms, validation) |
| **service-optimizer** | sonnet | Analysis and comparison (benchmarking, metrics) |
| **service-library-finder** | sonnet | Research and evaluation (searching, scoring) |
| **uc-service-tracer** | sonnet | Validation and reporting (traceability checking) |

---

## Comparable Agent Mappings

### service-extractor

**Comparable agents**:
- wshobson/backend-architect (architecture, service boundaries, API design)
- VoltAgent/backend-developer (microservices, service boundaries)
- VoltAgent/api-designer (API architecture, interface design)

**Extract patterns**:
- Architecture design approach (backend-architect)
- Service boundary definition (backend-developer checklist)
- Contract-first design (api-designer best practices)

**Preserve our style**:
- Service-oriented architecture focus
- UC-driven extraction
- Service registry integration
- Template-based specs

---

### service-designer

**Comparable agents**:
- VoltAgent/api-designer (interface design, documentation)
- VoltAgent/backend-developer (data models, API design)

**Extract patterns**:
- API design checklist (api-designer)
- Interface design workflow (api-designer)
- Testing strategy (backend-developer)

**Preserve our style**:
- Protocol-based interfaces
- Result type pattern
- Immutable data models
- Framework template integration

---

### service-dependency-analyzer

**Comparable agents**:
- wshobson/code-reviewer (systematic analysis, validation)
- VoltAgent/code-reviewer (checklist approach)
- VoltAgent/cloud-architect (architecture validation)

**Extract patterns**:
- Systematic review approach (code-reviewer)
- Checklist format (VoltAgent code-reviewer)
- Validation workflow (security-auditor)

**Preserve our style**:
- Graph algorithms (DFS, topological sort)
- Layered architecture validation
- 3-dependency limit enforcement
- Service registry integration

---

### service-optimizer

**Comparable agents**:
- VoltAgent/ml-engineer (benchmarking, optimization, hyperparameter tuning)

**Extract patterns**:
- Optimization workflow (ml-engineer)
- Metrics to measure (latency, throughput, memory)
- Evaluation approach (ml-engineer)

**Preserve our style**:
- Strategy-based optimization
- Benchmark-driven decisions
- Service spec integration

---

### service-library-finder

**Comparable agents**:
- (No direct equivalent, but can extract general patterns)

**Extract patterns**:
- Evaluation criteria (from quality checklists)
- Decision thresholds (from various agents)
- Systematic evaluation approach

**Preserve our style**:
- Library-first mindset
- PyPI/npm focus
- Score-based decisions (≥70%)
- Service spec integration

---

### uc-service-tracer

**Comparable agents**:
- wshobson/code-reviewer (validation, systematic checking)
- VoltAgent/code-reviewer (checklist validation)
- VoltAgent/security-auditor (compliance checking)

**Extract patterns**:
- Validation approach (code-reviewer)
- Compliance checking (security-auditor)
- Systematic verification (both)

**Preserve our style**:
- UC-Service bidirectional traceability (unique!)
- Orphan service detection
- Traceability matrices
- Framework integration

---

## Key Takeaways for Implementation

### DO Extract and Use:
1. ✅ **Trigger keywords** - Exact phrasing from wshobson
2. ✅ **Description structure** - Expert + specializing + Masters + trigger
3. ✅ **Checklists** - VoltAgent's actionable categories
4. ✅ **Model selection** - opus for complex, sonnet for standard
5. ✅ **Concise workflows** - 5-7 steps with brief descriptions
6. ✅ **Best practices lists** - 5-10 actionable bullets

### DON'T Copy Blindly:
1. ❌ **Technology stacks** - Our agents are language-agnostic or Python-focused
2. ❌ **Generic advice** - Keep service-oriented focus
3. ❌ **Tool lists** - Our agents have appropriate tool restrictions
4. ❌ **Domain-specific jargon** - Use our framework terminology

### PRESERVE Our Style:
1. ✅ **Service-oriented architecture** - No equivalent in community
2. ✅ **UC-Service traceability** - Unique to our framework
3. ✅ **Framework template integration** - References to .claude/templates/
4. ✅ **Development rules** - References to development-rules.md
5. ✅ **Spec-driven approach** - service-spec.md as source of truth
6. ✅ **Layered architecture validation** - 3-dependency limit, acyclic graphs

---

## Next Steps

1. Review extracted patterns (this file)
2. Implement Phase 2: Apply patterns to all 6 agents
3. Validate: Ensure community best practices + our unique style preserved

---

**Document Version**: 1.0
**Date**: 2025-10-01
**Status**: Ready for Implementation
**Total Patterns Extracted**: 50+
**Sources**: wshobson/agents (5 agents), VoltAgent (8 agents)
