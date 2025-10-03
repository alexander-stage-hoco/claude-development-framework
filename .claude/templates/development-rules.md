---
tier: 1
purpose: The 12 non-negotiable rules
reload_trigger: Always at session start, at 70% context
estimated_read_time: 15 minutes
---

# The 12 Non-Negotiable Development Rules

**Project**: [PROJECT_NAME]
**Status**: ⚠️ **AUTHORITATIVE SOURCE** - Do not duplicate these rules elsewhere
**Last Updated**: [DATE]
**Referenced By**: CLAUDE.md, start-here.md, READING-ORDER.md
**Sync Policy**: Other files must reference this file, not copy rules

---

## Important

This file is the **single source of truth** for the 12 development rules.

**DO NOT**:
- Copy these rules to other files (creates drift)
- Summarize rules differently elsewhere (creates confusion)
- Skip reading this file (rules are mandatory)

**DO**:
- Reference this file from other framework files
- Re-read when rules seem fuzzy
- Quote specific rules by number when enforcing

---

## The Rules (Quick Reference)

| # | Rule | Core Requirement | Claude's Enforcement |
|---|------|------------------|---------------------|
| **1** | **Specifications Are Law** | No code without spec. **Use cases must reference services.** Spec updated first. Docstrings reference specs: `Specification: specs/file.md#section` | Refuses to code without spec or service reference |
| **2** | **Tests Define Correctness** | Write test first (RED), implement (GREEN), refactor (REFACTOR). Never weaken tests—fix system. | Refuses to implement before test |
| **3** | **Incremental Above All** | Max 3-hour iterations. Break large features. Complete current before next. | Stops if scope grows |
| **4** | **Research Informs Implementation** | Read papers/articles first. Document in `research/learnings/`. Create ADRs. | Requires research before novel features |
| **5** | **Two-Level Planning** | Strategic (UC → milestones) + Tactical (iterations → 1-3 hours, tests listed) | Enforces planning before implementation |
| **6** | **No Shortcuts** | No TODOs (create issues). No skipped error handling. Document debt explicitly. | Rejects TODOs and incomplete code |
| **7** | **Technical Decisions Are Binding** | Create ADRs for major choices. Follow existing ADRs. Update via new ADR, never silently deviate. | Follows ADRs strictly |
| **8** | **BDD for User-Facing Features** | Use cases have Gherkin scenarios matching acceptance criteria. BDD tests verify scenarios. | Ensures Gherkin exists for UCs |
| **9** | **Code Quality Standards** | Type hints, docstrings with spec refs, SRP, no pylint warnings | Maintains quality bar |
| **10** | **Session Discipline** | Start: Read CLAUDE.md, development-rules.md, current-iteration.md. End: Update planning, commit, summarize. | Follows protocol |
| **11** | **Git Workflow Discipline** | Branch per iteration (`iteration-XXX`) or UC (`uc-XXX`). Commit only when tests pass. Format: `[type]: desc\nSpec: UC-XXX\nTests: N passing` | Creates branches, refuses broken commits |
| **12** | **Mandatory Refactoring** | After GREEN, ALWAYS refactor. Check: duplication, complexity, naming, magic numbers, SRP. Separate `refactor:` commits. | Proposes refactoring after every feature |

---

## TDD Cycle (Rule #2 + #12)

```
┌──────────┐
│   RED    │ Write failing test → Verify failure → Get approval
└────┬─────┘
     ▼
┌──────────┐
│  GREEN   │ Write minimal code → Test passes
└────┬─────┘
     ▼
┌──────────┐
│ REFACTOR │ Improve quality (MANDATORY) → Tests still pass → Commit
└──────────┘
```

**See**: `.claude/quick-ref/tdd-cycle.md` for detailed cycle

---

## Git Workflow (Rule #11)

**Branch**:
```bash
git checkout -b iteration-XXX-description  # or uc-XXX-description
```

**Commit** (when complete + tests pass):
```
[type]: Brief description

Specification: UC-XXX / SVC-XXX
Tests: X passing / Y total

Details:
- What was implemented
- Technical decisions

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types**: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

**See**: `.claude/quick-ref/git.md` for complete workflow

---

## Refactoring Checklist (Rule #12)

After implementation passes:
- [ ] **Duplication?** Extract to functions
- [ ] **Complexity > 10?** Split functions (SRP)
- [ ] **Names clear?** Improve clarity
- [ ] **Magic numbers?** Extract to constants
- [ ] **Type hints?** Add if missing
- [ ] **Docstrings?** Add spec references

**See**: `.claude/templates/refactoring-checklist.md` for detailed guidance

---

## Enforcement

**Claude will refuse to**:
- Code without specification
- Implement before tests
- Weaken tests to make them pass
- Commit broken code or failing tests
- Skip refactoring step
- Violate ADRs

**When rules are violated**, Claude stops work and reminds user.

**User intervention**: If Claude violates rules, say:
- "Check development rules"
- "Show me the specification"
- "Tests first, then implementation"

---

## Anti-Patterns to Reject

| User Says | Claude Responds |
|-----------|-----------------|
| "Let's skip the spec for now" | "Spec must exist first (Rule #1)" |
| "This test is too strict" | "Let's analyze root cause, not weaken test (Rule #2)" |
| "We'll refactor later" | "Refactoring is mandatory after GREEN (Rule #12)" |
| "Let's build multiple features" | "One iteration at a time (Rule #3)" |
| "Just commit to main" | "Branch per iteration required (Rule #11)" |

---

## Service-Oriented Architecture Requirements

**Rule #1 Extension**: Use cases must reference services

**Service Requirements**:
- Services are extracted from use cases (not invented ad-hoc)
- Services have clear interfaces (Protocols with type hints)
- Services are testable in isolation (dependency injection, mocks)
- Services minimize dependencies on other services
- Use cases document which services they use (`## Services Used` section)
- Serviceless use cases must be challenged ("Is this really a UC or just UI?")

**Service Design**:
- Single Responsibility Principle (one service, one purpose)
- Stateless preferred, stateful justified
- Implementation strategies benchmarked when performance critical
- Existing libraries used when suitable (evaluate before building)

**See**: `.claude/service-registry.md` for service catalog and `services/` for specifications

---

**These rules ensure**: Quality · Traceability · Maintainability · Discipline · Version Control · Clean Code · Service-Driven Architecture
---

**Template Version**: 1.0
**Framework**: Claude Development Framework v2.2
**Last Updated**: 2025-10-01
**Compatibility**: Framework v2.2+
