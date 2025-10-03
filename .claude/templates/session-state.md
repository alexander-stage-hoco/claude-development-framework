---
tier: 3
purpose: Session continuity template
reload_trigger: At session end
estimated_read_time: 5 minutes
---

# Session State

**Session #**: [NUMBER]
**Date**: [YYYY-MM-DD]
**Duration**: [HOURS]
**Framework**: Claude Development Framework v2.2

---

## Work Completed This Session

[List what was accomplished - be specific]

Example:
- Created UC-002 specification for user authentication
- Wrote 5 tests for login functionality (all passing)
- Implemented UserRepository with in-memory storage
- Documented ADR-004 for authentication approach

---

## Current Status

### Active Iteration
- **Iteration**: [ITERATION-XXX] - [Name]
- **Status**: [Not Started | In Progress | Completed]
- **Progress**: [X of Y tasks complete]

### Tests Status
- **Total Tests**: [NUMBER]
- **Passing**: [NUMBER]
- **Failing**: [NUMBER] (if any, list them)
- **Coverage**: [PERCENTAGE]%

### Blockers
[None | List any blockers]

Example:
- Waiting for API key for external service
- Need clarification on UC-003 acceptance criteria

---

## Files in Context (By Tier)

### TIER 1 (Critical - Always loaded)
- `.claude/CLAUDE.md`
- `.claude/development-rules.md`
- `.claude/START-HERE.md`
- `planning/current-iteration.md`

### TIER 2 (Important - Current work)
- `specs/use-cases/UC-002-user-authentication.md`
- `specs/services/SVC-003-auth-service.md`
- `.claude/technical-decisions.md`

### TIER 3 (Working - Files being modified)
- `implementation/src/auth/user_repository.py`
- `implementation/tests/unit/test_user_repository.py`

---

## Context Status

- **Usage at Session End**: [PERCENTAGE]%
- **Compaction Needed**: [Yes/No]
- **Framework Files Clear**: [Yes/No]

---

## Decisions Made This Session

### Technical Decisions
[List any new ADRs or significant choices]

Example:
- **ADR-004**: Use JWT for authentication tokens
- **ADR-005**: Use bcrypt for password hashing

### Specification Updates
[List any spec changes or new specs created]

Example:
- Updated UC-002 acceptance criteria to include "remember me" functionality
- Created SVC-003 specification for authentication service

---

## Next Session Instructions

### For Claude

**Start Next Session With**:
```
Continue from session [N]. Read planning/session-state.md first.
```

**What to Do Next**:
1. Read this file (session-state.md)
2. Read `planning/current-iteration.md`
3. Continue with [SPECIFIC NEXT TASK]

**Context to Load**:
- TIER 1 files (always)
- TIER 2 files (listed above)
- [SPECIFIC FILE] if continuing [SPECIFIC WORK]

**Current Focus**:
[What should be worked on next]

Example:
- Continue iteration-003: Implement password reset flow
- Next step: Write tests for reset token generation
- Then: Implement token generation logic

---

### For User

**Your Next Steps**:
[Specific actions user might need to take]

Example:
- Review the login flow implementation
- Provide feedback on UC-003 specification
- Decide: Should we implement 2FA now or later?

**Ready to Continue**:
[Yes/No - if no, what's blocking]

---

## Learnings & Insights

[Document anything learned this session]

Example:
- Discovered pytest-mock simplifies repository testing
- Pattern: Repository tests don't need real database
- Note: Keep auth logic separate from HTTP layer (ADR-004)

---

## Open Questions

[List any unresolved questions]

Example:
1. Should password reset tokens expire after 1 hour or 24 hours?
2. Do we need email verification before allowing login?
3. What's the max failed login attempts before lockout?

---

## Session Notes

[Any other context Claude needs for next session]

Example:
- User prefers shorter sessions (~2 hours)
- User likes seeing test output before implementation
- Project target: MVP in 6 weeks

---

## Recovery Instructions

**If This Session State Is Lost**:

You can recover by:
1. Reading `planning/current-iteration.md` for current work
2. Running tests: `pytest` to see what's passing
3. Checking git log: `git log --oneline -10` for recent work
4. Reading most recent specs in `specs/use-cases/`

---

## File Checksums (Optional)

**Key Files at Session End**:
[Helps detect if files changed between sessions]

- `planning/current-iteration.md`: [HASH or last modified date]
- `.claude/technical-decisions.md`: [HASH or last modified date]

---

**Session Ended**: [TIME]
**Next Session**: [PLANNED DATE if known]
**Template Version**: 2.0
