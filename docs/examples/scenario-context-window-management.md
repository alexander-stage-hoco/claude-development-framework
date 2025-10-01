# Scenario: Context Window Management

**Scenario**: Large project approaching context limits, need compression
**Complexity**: Medium
**Duration**: ~30 minutes
**Problem**: Context at 72%, framework files at risk of being pushed out
**Solution**: Context compression and session-state management

---

## Context

**Project**: Large Microservices Platform
**Session**: 45 (long-running session)
**Project Size**: 30 services, 50 use cases, 200+ files
**Context Usage**: 72% (144,000 / 200,000 tokens)
**Warning**: Approaching TIER 1 file eviction threshold (75%)

---

## Session Transcript

### Claude's Context Warning

```
Claude: ⚠️ **Context Window Warning**

**Current Usage**: 72% (144,000 / 200,000 tokens)
**Status**: Approaching critical threshold

**Risk**:
- At 75%: TIER 1 files (CLAUDE.md, development-rules.md) may be evicted
- Framework enforcement could degrade
- Development rules may be forgotten

**Context Distribution**:
- TIER 1 (Critical): 8,000 tokens (6%)
- TIER 2 (Important): 12,000 tokens (8%)
- TIER 3-5 (Working): 30,000 tokens (21%)
- Conversation history: 94,000 tokens (65%) ⚠️

**Recommendation**: Perform context compression now (before 75% threshold)

**Compression Protocol** (from context-priority.md):
1. Summarize conversation history (95K → 10K tokens)
2. Archive completed work to session-state.md
3. Unload non-essential files (TIER 4-5)
4. Reload TIER 1 files (verify enforcement)
5. Resume work

**Estimated Recovery**: 72% → 25% usage

May I proceed with compression?
```

---

### User Response

```
User: "Yes, compress context. I want to keep working on UserService."
```

---

### Context Compression Process

```
Claude: **Context Compression Starting...**

**Step 1: Summarize Conversation History** (2 min)

Analyzing last 40 interactions...

Summary created:
```markdown
# Session Summary (Interactions 1-40)

**Work Completed**:
- Sessions 1-10: Created 15 use cases
- Sessions 11-20: Extracted 12 services
- Sessions 21-30: Implemented AuthService, ProductService, OrderService
- Sessions 31-40: Working on UserService (60% complete)

**Current Focus**:
- UserService implementation
- Tests: 8/12 passing
- Next: Implement update_user() method

**Key Decisions**:
- ADR-008: Use PostgreSQL for persistence
- ADR-011: PyJWT for authentication
- ADR-015: Event bus for service decoupling
```

Saved to: `planning/session-state.md`

**Tokens Saved**: 94,000 → 3,000 (91K tokens freed) ✅

**Step 2: Archive Completed Work**

Files to unload (TIER 4-5):
- Completed service specs (AuthService, ProductService, OrderService)
- Completed use cases (UC-001 through UC-040)
- Old iteration plans (iteration-001 through iteration-030)

**Note**: Work is saved in git, can reload if needed

**Tokens Saved**: 25,000 tokens freed ✅

**Step 3: Keep Active Files** (TIER 1-3)

Retained:
- .claude/CLAUDE.md ✅
- .claude/development-rules.md ✅
- .claude/technical-decisions.md ✅
- services/user-service/ (active work) ✅
- planning/current-iteration.md ✅
- planning/session-state.md ✅

**Step 4: Reload TIER 1 Files** (Verify Enforcement)

Re-reading critical files...
- .claude/CLAUDE.md ✅
- .claude/development-rules.md (all 12 rules) ✅

**Self-Check**:
✅ Can I quote Rule #2? "Tests Define Correctness - tests written BEFORE implementation"
✅ Can I quote Rule #6? "Never Compromise Tests - fix system, not tests"
✅ Do I remember current iteration? "UserService implementation, 60% complete"

**Result**: Framework enforcement fully restored ✅

**Step 5: Final Status**

**Context Usage After Compression**:
- Before: 72% (144,000 tokens)
- After: 23% (46,000 tokens)
- **Freed**: 98,000 tokens (68%) ✅

**Context Distribution**:
- TIER 1 (Critical): 8,000 tokens (17%)
- TIER 2 (Important): 10,000 tokens (22%)
- TIER 3 (Working): 18,000 tokens (39%)
- Conversation summary: 3,000 tokens (7%)
- Headroom: 162,000 tokens (70%) ✅

✅ **Compression Complete!**

**Recovery Capability**:
If you need any archived files, I can reload them from git.
For example: "Load OrderService spec" → I'll git show the file

**Ready to Resume**: UserService implementation

Where were we? Ah yes, implementing update_user() method...
```

---

### Resumed Work (No Interruption)

```
Claude: **Resuming UserService Implementation**

From session-state.md:
- Current: update_user() method
- Tests: 8/12 passing (4 tests waiting for update_user)
- Next: Implement update_user() with validation

**Step 1: Tests (RED)**

```python
def test_update_user_email():
    user = user_service.update_user(
        user_id=123,
        email="newemail@example.com"
    )
    assert user.email == "newemail@example.com"
```

Run: ❌ FAILS (not implemented)

**Step 2: Implement** (GREEN)

```python
def update_user(
    self,
    user_id: int,
    email: Optional[str] = None,
    name: Optional[str] = None,
) -> Result[User, UserError]:
    # Implementation...
```

Run: ✅ PASSES

---

[Work continues normally, no context issues]
```

---

## Context Management Best Practices Demonstrated

**When to Compress**:
- ⚠️ 70%: Start planning compression
- ⚠️ 75%: Compress immediately
- 🚨 80%: Emergency compression (TIER 1 at risk)

**What to Archive**:
- ✅ Conversation history (biggest win: ~60% of context)
- ✅ Completed work (specs, implementations)
- ✅ Old iterations

**What to Keep**:
- ✅ TIER 1 files (CLAUDE.md, development-rules.md)
- ✅ Active work files
- ✅ Current iteration plan
- ✅ Session state summary

**Session-State.md Format**:

```markdown
# Session State

**Last Updated**: 2024-09-30 15:45
**Session**: 45
**Context Usage**: 23% (after compression)

## Current Focus

**Active Work**: UserService implementation
**Progress**: 60% complete (8/12 tests passing)
**Next Steps**:
1. Implement update_user() method
2. Implement delete_user() method
3. Integration tests

## Work Completed (Sessions 1-44)

- ✅ 50 use cases specified
- ✅ 30 services extracted
- ✅ 12 services implemented (AuthService, ProductService, OrderService, ...)
- ✅ 8 services in progress

## Key Decisions

**ADRs**:
- ADR-008: PostgreSQL for persistence
- ADR-011: PyJWT for authentication
- ADR-015: Event bus for decoupling

## Files to Reload If Needed

**Completed Services**:
- services/auth-service/service-spec.md
- services/product-service/service-spec.md
- services/order-service/service-spec.md

**Command**: `git show HEAD:services/auth-service/service-spec.md`

## Next Session Instructions

**For Claude**:
1. Read this file (session-state.md)
2. Read .claude/CLAUDE.md
3. Read .claude/development-rules.md
4. Load services/user-service/ (active work)
5. Continue with update_user() implementation

**Context should be**: ~25% after loading
```

---

## Outcome

✅ **Context Managed Successfully**

**Metrics**:
- Context reduced: 72% → 23% (68% freed)
- TIER 1 files: Protected and reloaded
- Work continuity: Seamless (no loss of focus)
- Session recovery: Complete (can resume next session)

**Quality Maintained**:
- ✅ Framework rules still enforced
- ✅ Current work unaffected
- ✅ All active tests still pass
- ✅ No information lost (saved in session-state.md)

---

## Key Takeaways

**Framework Enforcement**: Context priority system prevents rule degradation
**Proactive Monitoring**: Warns at 70%, acts at 75%
**Session Continuity**: session-state.md enables perfect resumption
**No Quality Loss**: Compression is lossless (git + summaries)

---

## Context Management Lifecycle

```
Session Start (0%):
↓
Work Progresses (0% → 70%):
↓
⚠️ Warning Issued (70%):
↓
Continue Working (70% → 75%):
↓
🚨 Compression Triggered (75%):
↓
Compress + Archive (75% → 25%):
↓
Resume Work (25%):
↓
Session End:
- Update session-state.md
- Commit work
- Next session starts at ~10%
```

---

## Files Created/Modified

**Created**:
- `planning/session-state.md` (session summary + recovery instructions)

**Modified**:
- `planning/current-iteration.md` (updated with compression timestamp)

---

**Session End**: Context optimized, work continues seamlessly ✅
