# Session Types Guide

**Version**: 2.0
**Purpose**: Reference guide for different types of development sessions
**Framework**: Claude Development Framework v2.0

---

## Overview

The Claude Development Framework supports multiple session types, each with specific protocols and outcomes. This guide helps you identify which session type you need and how to conduct it.

---

## Session Types Quick Reference

| Type | Purpose | Duration | Key Files | Output |
|------|---------|----------|-----------|--------|
| **1. First Session** | Create initial specs | 30-60 min | start-here.md | Project overview, use cases |
| **2. Requirements Review** | Analyze user docs | 30-90 min | requirements-review-checklist.md | Spec'd use cases |
| **3. Implementation (TDD)** | Build features | 1-3 hours | session-checklist.md | Working code + tests |
| **4. Implementation Analysis** | Analyze reference code | 30-60 min | implementation-CLAUDE.md | summary.md, reusable components |
| **5. Research** | Study papers/articles | 1-2 hours | .claude/guides/research-organization.md | Learnings, ADRs |
| **6. Architecture Decision** | Make tech decisions | 30-60 min | technical-decisions.md | ADR documents |
| **7. Refactoring-Only** | Improve code quality | 30-90 min | refactoring-checklist.md | Cleaner code |
| **8. Continuation** | Resume work | Variable | session-state.md | Continued progress |
| **9. Service Extraction** | Extract services from UCs | 1-2 hours | service-spec.md | Service specifications |
| **10. Service Optimization** | Benchmark implementations | 1-3 hours | benchmark-report.md | Performance report, optimal strategy |

---

## 1. First Session (Discovery & Specification)

### When to Use
- Starting a brand new project
- Have project idea but no specifications
- Need to create initial structure

### Protocol

**Steps**:
1. **Claude reads framework files**
2. **Discovery questions** (5 questions about project)
3. **Specification creation** (project overview + use cases)
4. **Technical decisions** (ADRs for tech choices)
5. **Session state saved** (continuity for next session)

### User Prompt
```
Please analyze this project directory and tell me what this is and how to use it.
```

OR

```
I want to build [description]. Please read .claude/CLAUDE.md and help me set up this project.
```

### Expected Outcome
- ✅ `specs/00-project-overview.md` created
- ✅ 3-7 use case specifications (skeleton level)
- ✅ Technical decisions documented (ADRs)
- ✅ Session state saved
- ❌ NO implementation code (correct!)

### Next Step
→ Session 2 (Implementation) or Session 2 (Requirements Review if user has docs)

---

## 2. Requirements Review Session

### When to Use
- User has requirements document (PDF, Word, Markdown)
- User has acceptance criteria or PRD
- Need to convert external docs to framework specs

### Protocol
**Follow**: `.claude/templates/requirements-review-checklist.md`

**Steps**:
1. **Initial review** (completeness check)
2. **Critical analysis** (identify vague language, gaps)
3. **Gap analysis** (missing info, contradictions)
4. **Transformation** (convert to use case format)
5. **Validation** (review with user)
6. **Finalization** (create spec files)

### User Prompt
```
I have a requirements document. Please review it critically and create specifications.
[Attach or provide document]
```

### Expected Outcome
- ✅ Requirements analyzed and gaps identified
- ✅ Use case specifications created from requirements
- ✅ Open questions documented
- ✅ Improved/clarified requirements

### Next Step
→ Session 3 (Implementation) once specs are complete

---

## 3. Implementation Session (TDD)

### When to Use
- Have complete specification
- Ready to write code
- Normal feature development

### Protocol
**Follow**: `.claude/templates/session-checklist.md` (9 phases)

**Phases**:
1. **Orientation** - Read context, check git status
2. **Research** - If new concepts needed
3. **Planning** - Create iteration plan, branch
4. **Test-First** - Write failing tests (RED)
5. **Implement** - Make tests pass (GREEN)
6. **Refactor** - Improve code quality (REFACTOR)
7. **Validate** - All tests pass, quality check
8. **Document** - Update planning docs
9. **Close** - Commit, push, summarize

### User Prompt
```
Continue from session N. Ready to implement UC-XXX.
```

OR

```
Let's start implementing [feature name].
```

### Expected Outcome
- ✅ Tests written first (failing, then passing)
- ✅ Implementation complete
- ✅ Code refactored
- ✅ All tests green
- ✅ Committed to feature branch

### Next Step
→ Continue with next iteration or merge to main

---

## 4. Implementation Analysis Session ⭐ NEW

### When to Use
- Found reference implementation/codebase to learn from
- Need to analyze external code for reuse
- Want systematic analysis of open-source project

### Protocol
**Follow**: `research/implementations/[project]/CLAUDE.md`

**Setup**:
```bash
cd research/implementations/
mkdir [project-name]
cd [project-name]
git clone [repository-url] .
cp ../../.claude/templates/implementation-CLAUDE.md CLAUDE.md
cp ../../.claude/templates/implementation-summary.md summary.md
```

**Steps** (Claude follows automatically):
1. **Code structure discovery**
2. **Architecture analysis**
3. **Code quality assessment**
4. **Identify reusable components**
5. **Identify what to avoid**
6. **License & attribution check**
7. **Create summary.md**
8. **Create detailed analysis** (optional)

### User Prompt
```
Please analyze this reference implementation. Read CLAUDE.md for instructions.
```

### Expected Outcome
- ✅ `summary.md` - High-level findings
- ✅ `reusable-code.md` - Specific components to adapt
- ✅ `analysis.md` - Detailed technical analysis (optional)
- ✅ License compliance documented

### Usage
**Later, during main project development**:
- Reference `summary.md` for patterns and components
- Follow code-reuse-checklist.md to adapt code
- Add attribution if required

### Next Step
→ Use findings in main project Implementation Sessions

---

## 5. Research Session

### When to Use
- Need to understand new technology/pattern
- Exploring academic papers
- Reading articles/tutorials
- Learning before implementation

### Protocol
**Follow**: `.claude/guides/research-organization.md` workflow

**Steps**:
1. **Identify knowledge gap**
2. **Gather sources** (papers, articles)
3. **Read and analyze**
4. **Synthesize learnings** (`research/learnings/[topic].md`)
5. **Create ADRs** if decisions needed

### User Prompt
```
I need to research [topic] before implementing UC-XXX. Please help me understand [concept].
```

### Expected Outcome
- ✅ Papers/articles read and summarized
- ✅ `research/learnings/[topic].md` created
- ✅ Key insights documented
- ✅ ADR created if decision made

### Next Step
→ Implementation Session with informed approach

---

## 6. Architecture Decision Session

### When to Use
- Need to make technical choice (database, framework, pattern)
- Multiple options to evaluate
- Research complete, need decision

### Protocol
**Follow**: ADR template in `.claude/templates/technical-decisions.md`

**Steps**:
1. **Context**: What decision is needed?
2. **Research review**: What did we learn?
3. **Options evaluation**: Compare alternatives
4. **Decision**: Choose option with rationale
5. **Consequences**: Document tradeoffs
6. **ADR creation**: Formal record

### User Prompt
```
We need to decide on [technical choice]. Let's evaluate options and create an ADR.
```

### Expected Outcome
- ✅ ADR-XXX created in `research/decisions/`
- ✅ Options evaluated with pros/cons
- ✅ Decision documented with rationale
- ✅ Added to `.claude/technical-decisions.md`

### Next Step
→ Implementation Session following the decision

---

## 7. Refactoring-Only Session

### When to Use
- Code works but needs quality improvement
- Technical debt accumulated
- Want to clean up without adding features

### Protocol
**Follow**: `.claude/templates/refactoring-checklist.md`

**Steps**:
1. **Baseline tests** (all pass before starting)
2. **Apply refactorings** (one at a time)
3. **Test after each** (ensure no regression)
4. **Commit separately** (refactor: type)

### User Prompt
```
Let's refactor [module/component]. Code works but needs improvement.
```

### Expected Outcome
- ✅ Code quality improved
- ✅ Duplication removed
- ✅ Complexity reduced
- ✅ All tests still pass
- ✅ Separate refactor commit

### Next Step
→ Continue with next iteration

---

## 8. Continuation Session

### When to Use
- Resuming work from previous session
- Any time you continue existing project

### Protocol
**Follow**: Session protocol in `.claude/CLAUDE.md`

**Steps**:
1. **Read session-state.md**
2. **Read current-iteration.md**
3. **Check git status**
4. **Resume where left off**

### User Prompt
```
Continue from session N. Read planning/session-state.md first.
```

### Expected Outcome
- ✅ Context loaded
- ✅ Previous work understood
- ✅ Continued progress

### Next Step
→ Continue with appropriate session type based on current work

---

## 9. Service Extraction Session ⭐ NEW

### When to Use
- After use cases are specified
- Before implementation begins
- When refactoring to service-oriented architecture

### Protocol

**Steps**:
1. **Analysis** - Analyze UCs for required capabilities
2. **Extraction** - Identify service boundaries
3. **Design** - Create detailed service specs
4. **Dependency Analysis** - Validate dependencies, detect cycles
5. **Library Search** - Evaluate external libraries
6. **Traceability** - Validate UC-Service links

### User Prompt
```
Extract services from use cases. Follow service extraction protocol.
```

OR

```
Analyze use cases and identify required services.
```

### Expected Outcome
- ✅ Service specifications created in `services/`
- ✅ Service registry updated
- ✅ UC-Service traceability validated
- ✅ Library recommendations made
- ✅ Dependency graph clean (no cycles)
- ❌ NO implementation code (correct!)

### Next Step
→ Implementation Session (implementing services with TDD)

---

## 10. Service Optimization Session ⚡ NEW

### When to Use
- After service is implemented (multiple strategies exist)
- When performance issues identified
- Before production deployment (critical services)
- When evaluating implementation tradeoffs

### Protocol

**Steps**:
1. **Identify Strategies** - Read service-spec.md implementation strategies
2. **Implement Alternatives** - Code each strategy
3. **Create Benchmarks** - Write benchmark suite
4. **Run Benchmarks** - Execute performance tests
5. **Analyze Results** - Compare metrics (latency, throughput, cost)
6. **Make Decision** - Choose optimal strategy
7. **Document** - Create benchmark report, update spec

### User Prompt
```
Benchmark [ServiceName] implementations. Compare [Strategy A] vs [Strategy B] vs [Strategy C].
```

OR

```
Optimize [ServiceName] for performance. Current implementation doesn't meet UC requirements.
```

### Expected Outcome
- ✅ Benchmark report created (`benchmarks/report-YYYY-MM-DD.md`)
- ✅ Optimal strategy recommended with rationale
- ✅ Parameters tuned
- ✅ Service spec updated
- ✅ ADR created (if architectural decision)

### Next Step
→ Implementation Session (apply optimal strategy)

---

## Choosing the Right Session Type

### Decision Tree

```
Starting new project?
├─ YES → Session Type 1: First Session
└─ NO → Continue...

Have requirements document?
├─ YES → Session Type 2: Requirements Review
└─ NO → Continue...

Found reference code to analyze?
├─ YES → Session Type 4: Implementation Analysis
└─ NO → Continue...

Need to learn new concept?
├─ YES → Session Type 5: Research
└─ NO → Continue...

Need to make technical decision?
├─ YES → Session Type 6: Architecture Decision
└─ NO → Continue...

Use cases ready, need services?
├─ YES → Session Type 9: Service Extraction
└─ NO → Continue...

Service implemented, need optimization?
├─ YES → Session Type 10: Service Optimization
└─ NO → Continue...

Ready to write code?
├─ YES → Session Type 3: Implementation (TDD)
└─ NO → Continue...

Code works but needs cleanup?
├─ YES → Session Type 7: Refactoring-Only
└─ NO → Continue...

Resuming previous work?
└─ YES → Session Type 8: Continuation (then branch to appropriate type)
```

---

## Session Combinations

### Common Sequences

**New Project Startup** (with Service Architecture):
1. First Session → Initial specs
2. Research Session → Understand tech
3. Architecture Decision → Choose approach
4. Service Extraction → Derive services from UCs
5. Implementation Session → Build services
6. Service Optimization → Benchmark if needed

**With Requirements Doc**:
1. Requirements Review → Convert to specs
2. Service Extraction → Identify services
3. Implementation Session → Build services

**With Reference Code**:
1. Implementation Analysis → Analyze reference
2. Research Session → Study patterns (if needed)
3. Service Extraction → Design services
4. Implementation Session → Apply learnings

**Normal Development**:
1. Continuation → Resume
2. Implementation Session → Build feature
3. Refactoring Session → Clean up
4. Repeat

**Service-Focused Flow**:
1. Service Extraction → Design services
2. Library Evaluation → Find/evaluate libraries
3. Implementation Session → Implement with TDD
4. Service Optimization → Benchmark and tune
5. Repeat for next service

---

## Session Best Practices

### Start Every Session
- ✅ Read framework files (CLAUDE.md, development-rules.md)
- ✅ Check git status
- ✅ Review current iteration
- ✅ Load session state (if continuing)

### End Every Session
- ✅ Update planning docs
- ✅ Save session state
- ✅ Commit (if iteration complete)
- ✅ Summarize accomplishments

### During Sessions
- ✅ Follow session-specific protocol
- ✅ Test-first for implementation
- ✅ Refactor after implementation
- ✅ Document decisions
- ✅ Reference specifications

---

## Troubleshooting

**Claude seems confused about session type**:
→ Explicitly state: "This is a [session type] session"

**Jumped into wrong session type**:
→ Say: "Wait, we need a [correct type] session first"

**Session taking too long**:
→ Check if scope is too large (iterations should be 1-3 hours)

**Not sure which session type**:
→ Ask Claude: "What type of session do we need for [goal]?"

---

## Quick Commands by Session Type

```bash
# First Session
"Analyze this project directory"

# Requirements Review
"Review this requirements document critically"

# Implementation (TDD)
"Continue from session N. Implement UC-XXX"

# Implementation Analysis
"Analyze this reference implementation. Read CLAUDE.md"

# Research
"Help me research [topic] before implementing"

# Architecture Decision
"Let's decide on [choice] and create an ADR"

# Refactoring
"Refactor [component] - tests pass but code needs improvement"

# Continuation
"Continue from session N. Read planning/session-state.md"

# Service Extraction
"Extract services from use cases. Follow service extraction protocol"

# Service Optimization
"Benchmark [ServiceName] implementations. Compare [Strategy A] vs [Strategy B]"
```

---

**Remember**: Each session type has its protocol. Follow the protocol for consistent, high-quality results.