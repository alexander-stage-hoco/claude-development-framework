# Claude-Optimized Development Framework
**A Disciplined, Spec-Driven, Incremental Approach to Software Development with AI Assistance**

**Version**: 2.3 (Template Quality + Validation)
**Date**: 2025-10-04
**Based on**: Learnings from Knowledge Graph Builder project

---

## Table of Contents
1. [Quick Start](#quick-start)
2. [Core Principles](#core-principles)
3. [Project Structure](#project-structure)
4. [The Claude Directory](#the-claude-directory)
5. [Essential Files](#essential-files)
6. [Context Window Management](#context-window-management)
7. [Development Workflow](#development-workflow)
8. [Enforcement Mechanisms](#enforcement-mechanisms)
9. [Where to Get Help](#where-to-get-help)

---

## Quick Start: Get Running in 15 Minutes

### Step 1: Initialize Project Structure (2 minutes)

```bash
mkdir -p my-project/{.claude/guides,specs/{use-cases,services,apis,data-models,architecture},research/{papers,articles,implementations,learnings,decisions},planning/{milestones,iterations},implementation/{src,tests/{unit,integration,bdd,system}}}
cd my-project
```

### Step 2: Create Core Claude Files (5 minutes)

Copy and customize these 3 essential files from `.claude/templates/` folder:

1. **`.claude/CLAUDE.md`** - Session protocol and mandatory rules
2. **`.claude/development-rules.md`** - The 12 non-negotiable rules
3. **`.claude/session-checklist.md`** - Per-session verification steps

**See**: `.claude/templates/` folder for complete templates

### Step 3: First Session (8 minutes)

```
User: "I want to build [X]. The business problem is [Y].
       Please read .claude/CLAUDE.md first."

Claude: "I'll start with research and specifications—no code yet."
```

**Typical progression**: Specs (1-2 sessions) → Research (1) → Planning (1) → Test-first implementation (ongoing)

---

## Core Principles

| # | Principle | Requirement |
|---|-----------|-------------|
| **1** | **Highly Incremental** | 1-3 hour iterations max. Small steps compound into large systems. |
| **2** | **Specification-First** | Every line of code traces to documented specification. No exceptions. |
| **3** | **Learn Before Building** | Research papers/articles inform decisions. Document learnings. |
| **4** | **Use Case Driven** | All work delivers business value tied to a use case. |
| **5** | **Test-Driven/BDD** | Tests written BEFORE implementation. Tests define correctness. |
| **6** | **Never Compromise Tests** | Failing tests reveal system issues. Fix system, never weaken tests. |
| **7** | **Two-Level Planning** | Strategic (use case level) + Tactical (iteration level). |
| **8** | **Document Decisions** | Architecture Decision Records (ADRs) are binding. No deviation without updates. |

---

## Project Structure

```
project-root/
├── .claude/                          # Claude-specific enforcement files
│   ├── CLAUDE.md                     # Main Claude instructions
│   ├── development-rules.md          # The 12 non-negotiable rules
│   ├── service-registry.md           # Service catalog and traceability
│   ├── session-checklist.md          # Per-interaction checklist
│   ├── technical-decisions.md        # ADRs (Architecture Decision Records)
│   ├── context-priority.md           # Context management rules
│   ├── subagents/                    # Subagent configurations (6 service-oriented agents)
│   ├── templates/                    # Template files for Claude reference
│   ├── quick-ref/                    # Quick reference cards
│   └── guides/                       # Claude operational guides
│       └── research-organization.md  # How to organize research
│
├── docs/                             # User documentation
│   ├── claude-development-framework.md
│   ├── troubleshooting.md
│   ├── walkthrough-todo-api.md
│   ├── example-first-session.md      # Example session transcript
│   ├── session-types.md              # Session pattern reference
│   └── advanced/                     # Advanced guides
│       ├── tool-integration.md
│       └── large-codebase-context.md
│
├── specs/                            # Authoritative specifications
│   ├── 00-project-overview.md        # Vision, scope, constraints
│   ├── use-cases/                    # Business-driven requirements
│   │   ├── UC-001-[name].md
│   │   └── ...
│   ├── apis/                         # API contracts (OpenAPI/AsyncAPI)
│   ├── data-models/                  # Canonical data structures
│   └── architecture/                 # System design documents
│
├── services/                         # Service layer (created in new projects)
│   ├── README.md                     # Project-specific service guide (from template)
│   ├── [service-name]/
│   │   ├── service-spec.md           # Service specification
│   │   ├── interface.py              # Protocol (abstract interface)
│   │   ├── implementation.py         # Concrete implementation
│   │   ├── tests/                    # Unit, integration, contract tests
│   │   ├── benchmarks/               # Performance benchmarks
│   │   └── library-evaluation.md     # Library selection (if applicable)
│   └── ...
│
│   NOTE: services/ directory is NOT in template root, only in created projects
│
├── research/                         # Learning materials (READ FIRST)
│   ├── papers/                       # Academic papers
│   ├── articles/                     # Industry articles
│   ├── learnings/                    # Extracted insights
│   │   └── [topic]-summary.md
│   └── decisions/                    # Research-based decisions
│
├── planning/                         # Two-level planning artifacts
│   ├── roadmap.md                    # High-level use case roadmap
│   ├── session-state.md              # Session continuity file
│   ├── current-iteration.md          # Active work tracking
│   ├── milestones/                   # Use case implementation plans
│   └── iterations/                   # Tactical implementation plans
│       ├── iteration-001-[task].md
│       └── ...
│
├── implementation/                   # Source code
│   ├── src/
│   │   ├── core/                     # Shared domain models
│   │   ├── services/                 # Business logic
│   │   ├── repositories/             # Data access
│   │   └── api/                      # External interfaces
│   ├── tests/
│   │   ├── unit/                     # Unit tests (TDD)
│   │   ├── integration/              # Integration tests
│   │   ├── bdd/features/             # BDD scenarios (Gherkin)
│   │   └── system/                   # End-to-end tests
│   └── README.md
│
├── docs/                             # Generated documentation
└── README.md
```

---

## The .claude/ Directory

Contains enforcement mechanisms that ensure Claude follows the disciplined approach.

| File | Purpose |
|------|---------|
| **CLAUDE.md** | Primary instructions: session protocol, implementation gate, anti-patterns |
| **development-rules.md** | The 12 non-negotiable rules + service requirements + enforcement statements |
| **service-registry.md** | Service catalog, dependencies, UC-Service traceability |
| **session-checklist.md** | 8-phase checklist: Orient → Research → Plan → Test → Implement → Validate → Document → Close |
| **technical-decisions.md** | Architecture Decision Records (ADRs) - binding on all work |
| **context-priority.md** | 5-tier hierarchy + context maintenance thresholds |
| **subagents/** | 6 specialized agents for service-oriented architecture |
| **templates/** | Copy-paste ready templates for all file types (including service templates) |
| **quick-ref/** | Single-page reference cards (session-start, tdd-cycle, git, services) |
| **guides/** | Operational guides (research-organization) |

---

## Essential Files

**All templates in**: `.claude/templates/` folder

| Template | Contents |
|----------|----------|
| **Use Case** | Business requirements + Gherkin acceptance criteria + Services Used |
| **Service Specification** | Interface (Protocol), data models, dependencies, implementation strategies |
| **Benchmark Report** | Performance comparison, optimal strategy recommendation |
| **Library Evaluation** | Library comparison, feature coverage, recommendation |
| **Iteration Plan** | Test-first approach, implementation steps, DoD |
| **ADR** | Context, decision, consequences, alternatives |
| **Session State** | Current work, files in context, next session instructions |

**Principle**: Copy templates → Fill project details → Never start from scratch

---

## Context Window Management

### Understanding Context Windows

**Capacity**: Claude has a 200,000 token context window (~150,000 words)

**Problem**: Long sessions can push critical files (CLAUDE.md, development-rules.md) out of active attention.

**Solution**: Proactive context management with regular maintenance.

### Context Priority Hierarchy

**TIER 1: CRITICAL** (Must ALWAYS be in context)
- `.claude/CLAUDE.md`
- `.claude/development-rules.md`
- `.claude/technical-decisions.md`
- `planning/current-iteration.md`

**TIER 2: IMPORTANT** (Keep if capacity allows)
- Current use case specification
- Current service specification
- `planning/session-state.md`
- Current iteration plan

**TIER 3-5**: Working files, reference materials, conversation history

### Session Protocols

| When | Action |
|------|--------|
| **Session Start** | Read: CLAUDE.md → development-rules.md → session-state.md → current-iteration.md. Report context usage. |
| **Every 20 interactions** | Context check: Report usage %, verify TIER 1 clear, recommend action |
| **At 75%+ usage** | Compact: Summarize history, archive completed work, reload TIER 1 |
| **Session End** | Update session-state.md, summarize work, create recovery instructions |

---

## Development Workflow

### The Tactical Loop (Every Session)

1. **Orientation** → Read rules, decisions, status
2. **Check** → Failing tests? Fix first
3. **Plan** → Next iteration (if current complete)
4. **Test** → Write tests first (RED)
5. **Implement** → Make tests pass (GREEN)
6. **Validate** → All tests green, quality checks
7. **Document** → Update status, record decisions
8. **Close** → Commit, prepare next

### Session Patterns

| Session | Focus | Activities |
|---------|-------|------------|
| **1: Init** | Specifications | Create specs (NO CODE) · Identify use cases · Create ADRs · Set up structure |
| **2: Research** | Learning | Research best practices · Document learnings · Identify dependencies |
| **3: Planning** | Breakdown | Break UC into milestones · Create iteration plans · Identify tests |
| **4: Service Extraction** | Services | Extract services from UCs · Design interfaces · Validate dependencies |
| **5+: Loop** | Implementation | Write tests (RED) → Implement (GREEN) → Refactor → Optimize → Repeat |

**Example**: See `docs/walkthrough-todo-api.md` for complete 5-session TODO API project.

---

## Enforcement Mechanisms

### 1. Claude Self-Checks

Embedded in `.claude/CLAUDE.md` and `.claude/development-rules.md`:
- ✅ Read rules at session start
- ✅ Refuse to skip tests or compromise quality
- ✅ Verify specifications exist before coding

### 2. User Intervention Phrases

If Claude deviates, say:
- "Check development rules"
- "Tests first, then implementation"
- "What does the specification say?"

### 3. Automated Tools

**See**: `docs/advanced/tool-integration.md` for complete setup

- **Git Hooks**: Pre-commit test verification, commit-msg spec references
- **CI/CD**: GitHub Actions enforce standards
- **IDE Integration**: Auto-run tests, linting, type checking

---

## Additional Documentation (v2.0)

### Service-Oriented Architecture

- **Service Architecture Guide**: `docs/service-architecture.md` - Complete 900+ line guide to SOA
- **Service Quick Reference**: `.claude/quick-ref/services.md` - Patterns, checklists, FAQs
- **Service Registry**: `.claude/templates/service-registry.md` - Central service catalog template
- **Services README Template**: `.claude/templates/services-README-template.md` - Template for created projects
- **Session Types**: `docs/session-types.md` - Includes Session 9 (Service Extraction) and Session 10 (Service Optimization)

**Note**: `services/` directory does NOT exist in template root. It is created in new projects by `init-project.sh`.

### Specialized Subagents

Six service-oriented architecture subagents automate complex service development tasks:

- **service-extractor** (`.claude/subagents/service-extractor.md`) - Extract services from use cases
- **service-designer** (`.claude/subagents/service-designer.md`) - Design detailed Protocol-based interfaces
- **service-dependency-analyzer** (`.claude/subagents/service-dependency-analyzer.md`) - Analyze dependencies, detect cycles
- **service-optimizer** (`.claude/subagents/service-optimizer.md`) - Benchmark implementations, recommend optimal strategy
- **service-library-finder** (`.claude/subagents/service-library-finder.md`) - Search and evaluate external libraries
- **uc-service-tracer** (`.claude/subagents/uc-service-tracer.md`) - Validate UC-Service traceability

**Usage**: These agents are invoked automatically by Claude when appropriate, or manually via specialized prompts.

**See Examples**: `docs/examples/` - 10 real-world examples showing subagents in action

---

## Example Sessions

**NEW in v2.0**: 10 comprehensive example sessions demonstrating framework and subagents

**Location**: `docs/examples/` directory

### Subagent Examples (6)

1. **Service Extraction** (`subagent-service-extraction.md`) - Extract 6 services from 5 UCs in 8 minutes
2. **Library Evaluation** (`subagent-library-evaluation.md`) - Evaluate auth libraries, save $2,100
3. **Performance Optimization** (`subagent-performance-optimization.md`) - 99.2x speedup with benchmarking
4. **Dependency Analysis** (`subagent-dependency-analysis.md`) - Validate architecture in 10 minutes
5. **Traceability Validation** (`subagent-traceability-validation.md`) - Ensure 100% UC-Service traceability
6. **Multi-Agent Orchestration** (`subagent-multi-agent-orchestration.md`) - Complete service layer in 55 min

### Real-World Scenarios (4)

7. **Circular Dependency Fix** (`scenario-circular-dependency-fix.md`) - Fix cycles with event-based decoupling
8. **Specification Evolution** (`scenario-specification-evolution.md`) - Handle changing requirements cleanly
9. **Production Performance Crisis** (`scenario-production-performance-crisis.md`) - Emergency fix in 25 min
10. **Context Window Management** (`scenario-context-window-management.md`) - Compress 72% → 23% context

**Index**: See `docs/examples/README.md` for complete catalog with quick navigation

**Total Content**: ~6,000 lines across 10 examples
**Time Savings Shown**: 40+ hours saved across examples

---

## Where to Get Help

### When You Have a Problem

**First**: Check `docs/troubleshooting.md`

**Common Scenarios**:
1. Claude writes code without tests → Recovery steps
2. Claude wants to weaken tests → Root cause analysis protocol
3. Iteration scope creep → Change request protocol
4. Taking longer than planned → Complexity assessment
5. Context window degradation → Reload procedures
6. Spec-code drift → Alignment audit
7. Production emergency → Hotfix protocol

### When You Want to Learn

**Read**: `docs/walkthrough-todo-api.md`

Complete 5-session example showing:
- Spec creation
- Research documentation
- Iteration planning
- Test-first implementation
- Quality maintenance

Shows framework in action from start to finish.

### When You Need Templates

**Use**: `.claude/templates/` folder

Copy-paste ready templates for:
- `.claude/CLAUDE.md`
- `.claude/development-rules.md`
- Use case specifications
- Iteration plans
- Architecture Decision Records (ADRs)
- Session state files

### When Setting Up Tools

**Follow**: `docs/advanced/tool-integration.md`

Setup instructions for:
- Git hooks (pre-commit, commit-msg)
- Pre-commit framework
- GitHub Actions CI/CD
- VS Code / PyCharm configuration
- pytest configuration
- Makefile for common commands

### When Working with Large Codebases

**Apply**: `docs/advanced/large-codebase-context.md`

Advanced strategies for 50K+ line projects:
- Modular architecture
- Three-tier context loading
- Specification summaries
- Code reference system
- Dynamic module loading

---

## Benefits & Success Metrics

### Key Benefits
- **Confidence**: Every step documented and traceable
- **Consistency**: Claude follows same rules every session
- **Quality**: Tests ensure correctness, no shortcuts
- **Velocity**: Disciplined development is faster long-term
- **Maintainability**: Anyone can pick up work anytime

### Success Metrics

**After 3 Months**: 100% test coverage · Every feature traces to spec · Zero TODOs · Seamless session continuity

**After 6 Months**: Reusable research knowledge base · ADRs prevent rehashing decisions · Higher iteration velocity · Bugs trace to spec gaps, not implementation

---

## How to Adapt This Framework

### For Your Next Project

1. **Copy Structure**: Use directory layout as-is
2. **Customize Templates**: Adjust to your domain
3. **Set Research Topics**: Identify relevant papers/articles upfront
4. **Define First UCs**: Start with 3-5 core use cases
5. **Initialize Claude**: Point to `.claude/CLAUDE.md` in first session
6. **Iterate**: Follow tactical loop session after session

### Domain-Specific Adaptations

**Data Science Projects**:
- Add `research/datasets/` for dataset documentation
- Add `notebooks/` for exploratory analysis
- Modify UC template for model performance criteria

**API-First Projects**:
- Expand `specs/apis/` with OpenAPI specs
- Add contract testing
- Modify iteration template for API compatibility checks

**Embedded Systems**:
- Add `specs/hardware/` for hardware specs
- Add resource usage validation to iterations
- Include constraints (memory, power) in NFRs

---

## Anti-Pattern Recognition

### What This Framework PREVENTS

| Anti-Pattern | Framework Approach |
|--------------|-------------------|
| ❌ "Move Fast and Break Things" | ✅ Move Steadily and Build Correctly |
| ❌ "We'll Document It Later" | ✅ Specification-First Development |
| ❌ "Just Get It Working" | ✅ Test-First Development |
| ❌ "The Test Is Wrong" | ✅ Tests Reveal System Issues |
| ❌ "Build It All At Once" | ✅ Incremental Integration |

---

## Philosophy

> **"Slow is smooth, smooth is fast."**
>
> Incremental, disciplined development produces better results than rushing.

This framework turns Claude into a **disciplined development partner** that enforces quality, not just generates code.

**The Result**: A codebase that's maintainable, testable, traceable, and understandable—with Claude as an **enforcer of quality**, not just a code generator.

---

## Quick Reference Card

### Every Session Must:
☑ Claude reads `.claude/CLAUDE.md`
☑ Reviews `planning/current-iteration.md`
☑ Writes tests BEFORE code
☑ All tests green before proceeding
☑ Updates status documents

### When Claude Deviates:
- Say: "Check development rules"
- Say: "Tests first, then implementation"
- Say: "What does the specification say?"

### Files to Read for Help:
- **Problem?** → `docs/troubleshooting.md`
- **Learning?** → `docs/walkthrough-todo-api.md`
- **Template?** → `.claude/templates/` folder
- **Tools?** → `docs/advanced/tool-integration.md`
- **Large codebase?** → `docs/advanced/large-codebase-context.md`

---

## When to Use This Framework

**✅ Use this framework when**:
- Starting a new project from scratch
- Replatforming/rewriting an existing system
- Building systems with long-term maintenance requirements
- Working with distributed teams or across sessions
- Need to ensure AI-assisted development maintains quality

**❌ Do NOT use this framework when**:
- Building quick prototypes for exploration
- Working on one-off scripts or utilities
- Contributing to projects with established processes
- Time constraints require pragmatic shortcuts (acknowledge tech debt explicitly)

---

**Document Version**: 2.0 (Constitution + Guides)
**Last Updated**: 2025-09-30
**Maintained By**: [Your Name/Team]
**Based On**: Knowledge Graph Builder project learnings

**Next Steps**:
1. Copy this framework to your new project root
2. Customize templates for your domain (see `.claude/templates/` folder)
3. Point Claude to `.claude/CLAUDE.md` in first session
4. Start with research and specifications
5. Build incrementally with discipline

**Need help?** All guides are in `.claude/guides/` directory.

Good luck with your next project! 🚀
