---
tier: 2
purpose: Architecture decision records template
reload_trigger: When making/reviewing ADRs
estimated_read_time: 5 minutes
---

# Technical Decisions (ADRs)

**Project**: [PROJECT_NAME]
**Status**: Active
**Last Updated**: [DATE]
**Framework**: Claude Development Framework v2.1

---

## About This Document

This file contains **Architecture Decision Records (ADRs)** - a log of all significant technical decisions made during the project.

### Why ADRs Matter

ADRs are **binding**. Once a decision is recorded here:
- ✅ Claude will follow it in all future work
- ✅ All code must align with recorded decisions
- ✅ Deviations require explicit discussion and new ADR
- ❌ Claude will refuse to silently violate ADRs

### What Qualifies as an ADR

Document these types of decisions:
- Technology/framework choices (language, database, libraries)
- Architectural patterns (microservices vs monolith, event-driven, etc.)
- Data storage approaches (SQL vs NoSQL, schema design)
- API design standards (REST, GraphQL, conventions)
- Security approaches (authentication, authorization)
- Testing strategies (unit/integration mix, coverage targets)
- Deployment approaches (containers, cloud platform)
- Code organization principles (folder structure, naming conventions)

### What Doesn't Need an ADR

- Implementation details within existing patterns
- Bug fixes
- Refactoring that doesn't change architecture
- Routine dependency updates

---

## ADR Format

Each decision uses this standard format:

### ADR-XXX: [Decision Title]
**Date**: YYYY-MM-DD
**Status**: Proposed | Accepted | Deprecated | Superseded by ADR-YYY
**Deciders**: [Who made this decision]
**Context**: What is the issue motivating this decision?
**Decision**: What did we decide to do?
**Consequences**: What becomes easier or harder as a result?
**Alternatives Considered**: What other options were evaluated?

---

## Example ADRs

### ADR-001: Use Python 3.11+ with Type Hints
**Date**: 2025-09-30
**Status**: Accepted
**Deciders**: Project Team
**Context**: Need to choose primary development language and version for this project. Team has Python experience, project requires rapid development with maintainability.
**Decision**: Use Python 3.11 or later with full type hints (enforced by mypy) for all production code.
**Consequences**:
- ✅ **Easier**: IDE autocomplete, early error detection, self-documenting code
- ✅ **Easier**: Python's extensive library ecosystem
- ❌ **Harder**: Slightly more verbose code, type hint learning curve
- ❌ **Harder**: Some dynamic Python patterns require more thought
**Alternatives Considered**:
- Python 3.9 (rejected: missing some type system features)
- TypeScript/Node.js (rejected: team more familiar with Python)
- Go (rejected: preference for Python's expressiveness)

---

### ADR-002: Use pytest for Testing
**Date**: 2025-09-30
**Status**: Accepted
**Deciders**: Project Team
**Context**: Need consistent testing framework. Project uses TDD, requires strong fixture support and readable test output.
**Decision**: Use pytest as primary testing framework with pytest-cov for coverage reporting.
**Consequences**:
- ✅ **Easier**: Simple assert statements, excellent fixture system
- ✅ **Easier**: Great plugin ecosystem (coverage, BDD, parametrize)
- ✅ **Easier**: Clear test failure output
- ❌ **Harder**: Different from stdlib unittest (but worth it)
**Alternatives Considered**:
- unittest (stdlib, but more verbose)
- nose2 (less actively maintained)

---

### ADR-003: Repository Pattern for Data Access
**Date**: 2025-09-30
**Status**: Accepted
**Deciders**: Project Team
**Context**: Need clean separation between business logic and data storage. Want testability and ability to swap storage implementations.
**Decision**: Implement Repository pattern for all data access. Each domain aggregate gets a repository interface.
**Consequences**:
- ✅ **Easier**: Business logic testing (can mock repositories)
- ✅ **Easier**: Changing storage technology later
- ✅ **Easier**: Clear boundary between layers
- ❌ **Harder**: More abstraction layers
- ❌ **Harder**: Initial setup overhead
**Alternatives Considered**:
- Direct ORM access (rejected: tight coupling)
- Generic DAO pattern (rejected: less domain-focused)
- Active Record (rejected: mixes concerns)

---

## Active ADRs

[New ADRs are added here as technical decisions are made during development]

---

## Deprecated/Superseded ADRs

[Old ADRs that have been replaced are moved here for history]

---

## Guidelines for Creating ADRs

### When to Create an ADR

Create an ADR when:
- Making a choice that impacts multiple parts of the system
- Choosing between multiple viable options
- Decision will be hard to change later
- Future developers will wonder "why did we do it this way?"
- User or Claude proposes a significant technical approach

### How to Write a Good ADR

**Good Context**:
> "We need to persist user data. Current mock storage won't scale. Need 100+ QPS read performance, ACID transactions for user updates."

**Bad Context**:
> "We need a database."

**Good Decision**:
> "Use PostgreSQL 15+ as primary datastore. Use SQLAlchemy ORM with repository pattern. Connection pooling with 20 connections max."

**Bad Decision**:
> "Use Postgres."

**Good Consequences**:
> "Easier: Strong consistency, ACID. Harder: Need to manage Postgres instance, more complex than SQLite for testing."

**Bad Consequences**:
> "It's good."

### ADR Numbering

- Number sequentially: ADR-001, ADR-002, etc.
- Never reuse numbers (even if deprecated)
- Pad with zeros for sorting (ADR-001, not ADR-1)

### ADR Status Lifecycle

```
Proposed → Accepted → (Deprecated or Superseded)
```

- **Proposed**: Under discussion, not yet binding
- **Accepted**: Decided, now binding on all code
- **Deprecated**: No longer recommended, but existing usage OK
- **Superseded**: Replaced by newer ADR (note which ADR)

---

## How Claude Uses ADRs

### When Writing Code

Claude will:
1. Read `.claude/technical-decisions.md` at session start
2. Check relevant ADRs before proposing approaches
3. Follow ADR guidance in all implementations
4. Reference ADR number in code comments

Example:
```python
# ADR-003: Using repository pattern for data access
class UserRepository:
    """
    Repository for User aggregate.
    Specification: specs/services/SVC-002-user-management.md
    Architecture: ADR-003 (Repository Pattern)
    """
```

### When User Proposes Conflicting Approach

**User**: "Let's just use direct database access here"

**Claude**:
```
That would violate ADR-003 (Repository Pattern for Data Access).

ADR-003 decided we use repositories for all data access to maintain:
- Testability (can mock repositories)
- Clean architecture boundaries
- Ability to swap storage later

If you want to change this approach, we should:
1. Discuss why repository pattern isn't working
2. Create ADR-XXX superseding ADR-003
3. Then refactor to new approach

Would you like to create a new ADR, or shall we implement with repositories?
```

### When Creating New ADRs

If user and Claude agree on new decision:

**Claude**:
```
Let me document this as ADR-004:

### ADR-004: [Title]
**Date**: [Today]
**Status**: Accepted
**Context**: [Explain issue]
**Decision**: [What we decided]
**Consequences**: [Pros and cons]
**Alternatives**: [What else we considered]

I've added this to .claude/technical-decisions.md. This is now binding
on all future work.
```

---

## Modifying Existing ADRs

### To Deprecate an ADR

Change status and add note:

```markdown
### ADR-003: Repository Pattern for Data Access
**Date**: 2025-09-30
**Status**: Deprecated (see ADR-015)
**Deprecated Date**: 2025-12-15
**Reason**: Moved to event sourcing pattern

[Original content...]
```

### To Supersede an ADR

Create new ADR referencing old:

```markdown
### ADR-015: Event Sourcing for Data Persistence
**Date**: 2025-12-15
**Status**: Accepted
**Supersedes**: ADR-003
**Context**: Repository pattern worked well, but we need full audit trail
and time-travel capabilities. Event sourcing provides this.
**Decision**: Use event sourcing pattern with event store...
```

---

## ADR Review Checklist

Before marking ADR as "Accepted":

- [ ] Context clearly explains the problem/need
- [ ] Decision is specific and actionable
- [ ] Consequences list both pros and cons
- [ ] At least 2 alternatives were considered
- [ ] Status is correct (Proposed vs Accepted)
- [ ] Date is recorded
- [ ] Number is sequential and unique
- [ ] Title is descriptive

---

## Quick Reference

| You Want To... | Do This... |
|----------------|-----------|
| Make a tech choice | Create ADR before implementing |
| Implement feature | Check ADRs for relevant decisions |
| Deviate from ADR | Discuss and create superseding ADR |
| Remember past decision | Search ADRs by keyword |
| Explain architecture | Reference ADR numbers |

---

**Remember**: ADRs are **living documentation** of your architecture. They capture **why**, not just **what**. When maintained well, they're invaluable for onboarding and decision-making.

---

**Version**: 2.0
**Template by**: Claude Development Framework
---

**Template Version**: 1.0
**Framework**: Claude Development Framework v2.1
**Last Updated**: 2025-10-01
**Compatibility**: Framework v2.1+
