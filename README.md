# Claude Development Framework - Template

**Version**: 2.2 (Agent Ecosystem + Comprehensive Test Suite)
**Last Updated**: 2025-10-03
**Based On**: Learnings from Knowledge Graph Builder project

---

## What This Is

A disciplined, spec-driven, incremental development framework designed for AI-assisted software development with Claude.

This template provides a complete methodology for building high-quality software with Claude as a **disciplined development partner** that enforces quality standards, not just generates code.

---

## Philosophy

> **"Slow is smooth, smooth is fast."**
>
> Incremental, disciplined development produces better results than rushing.

**Core Principles**:
1. Specification-First (no code without specs)
2. Test-Driven Development (tests before implementation)
3. Incremental Progress (1-3 hour iterations)
4. Never Compromise Tests (fix system, not tests)
5. Document Technical Decisions (ADRs are binding)

---

## Structure

### Main Framework Document
- **docs/claude-development-framework.md** (615 lines) - Core framework "constitution"
  - Quick Start (15 minutes)
  - Core Principles
  - Project Structure
  - Context Window Management
  - Development Workflow
  - Enforcement Mechanisms

### User Documentation (`docs/`)

Comprehensive guides for human developers:

| Guide | Size | Purpose |
|-------|------|---------|
| **troubleshooting.md** | 544 lines | Common problems & recovery procedures |
| **walkthrough-todo-api.md** | 774 lines | Complete 5-session example project |
| **example-first-session.md** | 261 lines | Example transcript of perfect first session |
| **session-types.md** | 350 lines | Reference guide for different session patterns |
| **advanced/tool-integration.md** | 594 lines | Git hooks, CI/CD, IDE setup |
| **advanced/large-codebase-context.md** | 475 lines | Advanced strategies for 50K+ LOC |

### Claude Context Files (`.claude/`)

What Claude reads at session start:
- **templates/** - 23 ready-to-use template files (CLAUDE.md, development-rules.md, etc.)
- **guides/** - 1 essential guide (research-organization.md)
- **quick-ref/** - 3 single-page reference cards (session-start.md, tdd-cycle.md, git.md)

### Setup Tools

- **init-project.sh** - Automated project initialization script
- **.gitignore** - Python project gitignore template

---

## Context Window Efficiency

The framework uses **incremental context loading** for maximum efficiency:

| Strategy | Overhead | Available Context | Use Case |
|----------|----------|------------------|----------|
| **TIER 1 only** | 3.3% (6.7K) | 96.7% (193K) | ✅ Recommended for most sessions |
| **TIER 1+2** | 8.2% (16.5K) | 91.8% (184K) | Active development |
| **TIER 1+2+3** | 15.1% (30.3K) | 84.9% (170K) | Quality gates active |
| **All tiered (1-4)** | 29.5% (59K) | 70.5% (141K) | Template creation |
| **All 59 files** | 69.4% (139K) | 30.6% (61K) | ⚠️ Learning only |

**Key Insight**: Load TIER 1 (4 files, 3.3%) at session start, then load additional files on-demand. The `docs/` directory (29 files, ~40% overhead) is for reference browsing, not context loading.

**Estimate usage anytime**: `./scripts/estimate-context.sh`

---

## Quick Start

⚡ **Want to start FAST?** See [`docs/10-minute-start.md`](./docs/10-minute-start.md) - Get to your first Claude session in 10 minutes!

📘 **Want more details?** See [`quick-start-guide.md`](./quick-start-guide.md) for a complete walkthrough.

### Option 1: Automated Setup (Recommended)

Use the initialization script to set up a new project in 30 seconds:

```bash
# From this template directory
./init-project.sh my-new-project

# Then start working
cd my-new-project
```

The script creates the complete directory structure, copies all framework files, and sets up initial placeholder files.

### Option 2: Manual Setup

1. **Read the Framework** (20 minutes)
   Start here: [`docs/claude-development-framework.md`](./docs/claude-development-framework.md)

2. **Understand the Approach**
   - Specifications come FIRST (before any code)
   - Tests define correctness (written before implementation)
   - Work in small iterations (max 3 hours each)
   - Document all technical decisions (ADRs)

3. **See It In Action**
   Read the complete example: [`docs/walkthrough-todo-api.md`](./docs/walkthrough-todo-api.md)

   Shows 5 sessions building a TODO API from scratch using the framework.

---

## Using This Template

### Option 1: Copy to New Project

```bash
# Copy entire framework to your project
cp -r /path/to/2025-09-Claude-Development-Approach/.claude your-project/
cp -r /path/to/2025-09-Claude-Development-Approach/docs your-project/

# Create project-specific .claude/CLAUDE.md from template
cp your-project/.claude/templates/CLAUDE.md your-project/.claude/CLAUDE.md
# Then customize with project name and date
```

### Option 2: Use as Reference

Keep this template separate and reference it when:
- Starting new projects
- Training team members
- Resolving methodology questions
- Updating development practices
- Need troubleshooting help

### Option 3: Customize for Your Domain

See "How to Adapt This Framework" in main document for:
- Data Science projects
- API-First projects
- Embedded Systems
- Other domains

---

## What This Framework Prevents

| Anti-Pattern | Framework Approach |
|--------------|-------------------|
| ❌ "Move Fast and Break Things" | ✅ Move Steadily and Build Correctly |
| ❌ "We'll Document It Later" | ✅ Specification-First Development |
| ❌ "Just Get It Working" | ✅ Test-First Development |
| ❌ "The Test Is Wrong" | ✅ Tests Reveal System Issues |
| ❌ "Build It All At Once" | ✅ Incremental Integration |

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
- Time constraints require pragmatic shortcuts

---

## Key Features

### 1. Enforcement Mechanisms
- Claude self-checks before every response
- User intervention phrases for course correction
- Automated tools (Git hooks, CI/CD)
- Spec alignment verification

### 2. Context Window Management
- Proactive monitoring and maintenance
- 5-tier priority hierarchy
- Session continuity protocols
- Context compaction procedures

### 3. Two-Level Planning
- **Strategic**: Use case breakdown into milestones
- **Tactical**: Milestones into 1-3 hour iterations

### 4. Complete Templates
Ready-to-use templates for:
- Use case specifications
- Service specifications
- Iteration plans
- Architecture Decision Records (ADRs)
- Session state files

---

## Agent Ecosystem 🤖

The framework includes **18 specialized agents** that automate critical development tasks:

### Core Development Agents (12)

**Tier 1: CRITICAL** (6 agents - 80% effort coverage)
- **test-writer** - Automated test generation from specs (Rule #2)
- **bdd-scenario-writer** - Gherkin scenario generation (Rule #8)
- **code-quality-checker** - Quality validation before commit (Rule #9)
- **refactoring-analyzer** - Refactoring recommendations (Rule #12)
- **uc-writer** - Use case specification generation (Rule #1)
- **adr-manager** - ADR creation and compliance checking (Rule #7)

**Tier 2: HIGH** (4 agents - 15% effort coverage)
- **iteration-planner** - Strategic & tactical planning (Rule #3, #5)
- **spec-validator** - UC/service spec quality enforcement (Rule #1)
- **git-workflow-helper** - Branch creation, commit generation (Rule #11)
- **session-summarizer** - Session continuity and documentation (Rule #10)

**Tier 3: MEDIUM** (2 agents - 5% effort coverage)
- **tech-debt-detector** - Tech debt detection and prevention (Rule #6)
- **doc-generator** - API documentation generation

### Service-Oriented Agents (6)

Specialized agents for service architecture lifecycle:
- **service-extractor** - Extract services from use cases
- **service-designer** - Design service interfaces
- **service-dependency-analyzer** - Validate dependencies, detect cycles
- **service-optimizer** - Performance optimization strategies
- **service-library-finder** - Library evaluation and recommendations
- **uc-service-tracer** - UC-Service traceability validation

### Using Agents

**Quick Start:**
Agents work through trigger keywords or proactive invocation:
- "generate tests for UC-001" → test-writer
- "create branch for iteration 2" → git-workflow-helper
- "check tech debt" → tech-debt-detector

**Complete Reference:** See [.claude/AGENTS.md](./.claude/AGENTS.md) for full agent library

**Usage Guide:** See [docs/agent-guide.md](./docs/agent-guide.md) for practical examples

**Integration Patterns:** See [docs/agent-integration-patterns.md](./docs/agent-integration-patterns.md) for workflows

### Agent Statistics

- **Total Agents**: 18 (12 core + 6 service-oriented)
- **Total Code**: ~10,000 lines
- **Rule Coverage**: 10/12 rules (83%)
- **Phase Coverage**: 4/9 phases (partial automation)
- **Time Savings**: 40-60% reduction in manual effort (estimated)

**Version**: All agents v1.0, Framework v2.2

---

### Agent Test Suite ✅

**Status**: Complete (v1.0 - October 2025)

The framework includes a **comprehensive test suite** validating all 18 agents:

**Test Coverage**:
- **794 total tests** across 7 phases
- Metadata validation (131 tests)
- Structure validation (309 tests)
- Behavioral tests for Tier 1 agents (209 tests)
- Integration workflows (48 tests)
- E2E development workflows (35 tests)
- Performance & consistency (62 tests)

**Test Organization**:
```
tests/agents/
├── unit/           # Metadata, structure, behavioral (Phases 1-4)
├── integration/    # Agent chains & workflows (Phase 5)
├── e2e/            # Complete development workflows (Phase 6)
├── performance/    # Efficiency & consistency (Phase 7)
└── fixtures/       # Shared test utilities
```

**Quick Start**:
```bash
# Run all tests
pytest tests/agents/ -v

# Run specific phase
pytest tests/agents/e2e/ -v

# With coverage
pytest tests/agents/ --cov=tests
```

**Documentation**: See [`tests/README.md`](./tests/README.md) for complete guide

**Benefits**:
- ✅ Confidence in agent reliability
- ✅ Catch regressions early
- ✅ Document expected behaviors
- ✅ Enable safe agent evolution
- ✅ <1 second runtime (fast feedback)

---

## Success Metrics

**After 3 Months**:
- ✅ 100% test coverage on core logic
- ✅ Every feature traces to a specification
- ✅ Zero "TODO" comments in codebase
- ✅ Claude picks up work across sessions seamlessly

**After 6 Months**:
- ✅ Research becomes reusable knowledge base
- ✅ ADRs prevent rehashing old decisions
- ✅ Iteration velocity increases
- ✅ Production bugs trace to spec gaps, not implementation bugs

---

## Getting Help

The framework includes comprehensive guides for common scenarios:

### Have a Problem?
→ [`docs/troubleshooting.md`](./docs/troubleshooting.md)
- Claude writes code without tests
- Claude wants to weaken tests
- Iteration scope creep
- Context window degradation
- And more...

### Want to Learn?
→ [`docs/walkthrough-todo-api.md`](./docs/walkthrough-todo-api.md)
- Complete 5-session example
- Shows every principle in practice

### Need a Template?
→ `.claude/templates/` folder
- 23 copy-paste ready templates
- All essential file formats
- Use case specifications, ADRs, session state, etc.

### Setting Up Tools?
→ [`docs/advanced/tool-integration.md`](./docs/advanced/tool-integration.md)
- Git hooks
- CI/CD workflows
- IDE configuration

### Large Codebase?
→ [`docs/advanced/large-codebase-context.md`](./docs/advanced/large-codebase-context.md)
- Strategies for 50K+ lines
- Context management techniques

---

## Project History

This framework was developed based on learnings from the **Knowledge Graph Builder** project (September 2025), which successfully implemented:
- 6 use cases (UC01-UC05, UC08, UC15)
- 93 test files with 1,176 test functions
- 100% test coverage on core logic
- Complete spec-to-implementation traceability
- Neo4j knowledge graph with entity extraction pipeline

The framework crystallizes the lessons learned from that project into a reusable template.

---

## Development Status

**Current Version**: 2.0 (Constitution + Guides Model)

**What's Included**:
- ✅ Complete framework documentation
- ✅ 5 comprehensive guides
- ✅ Working example (TODO API)
- ✅ Copy-paste templates
- ✅ Tool integration instructions

**What's Next**:
- Use this template in new projects
- Gather feedback and iterate
- Refine based on real-world usage
- Potentially add more examples

---

## Contributing

This is a personal development framework template. However, if you:
- Find issues or gaps
- Have suggestions for improvements
- Want to share your experience using it
- Have examples to contribute

Feel free to evolve this template for your own use.

---

## License

This framework is based on learnings from practical software development experience. Use freely, adapt as needed, share your improvements.

---

## Quick Reference

**The 10 Non-Negotiable Rules**:
1. Specifications Are Law
2. Tests Define Correctness
3. Incremental Above All
4. Research Informs Implementation
5. Two-Level Planning
6. No Shortcuts
7. Technical Decisions Are Binding
8. BDD for User-Facing Features
9. Code Quality Standards
10. Session Discipline

**Every Session Must**:
- ☑ Claude reads `.claude/CLAUDE.md`
- ☑ Reviews `planning/current-iteration.md`
- ☑ Writes tests BEFORE code
- ☑ All tests green before proceeding
- ☑ Updates status documents

**When Claude Deviates**:
- Say: "Check development rules"
- Say: "Tests first, then implementation"
- Say: "What does the specification say?"

---

**Last Updated**: 2025-10-03
**Version**: 2.2 (Agent Ecosystem + Comprehensive Test Suite)
**Claude Context**: ~16,200 lines (framework + agents)
**User Documentation**: ~5,000 lines in separate /docs folder
**Agent Library**: 18 agents (~10,000 lines)
**Test Suite**: 794 tests (~4,000 lines)

Ready to build with discipline! 🚀
