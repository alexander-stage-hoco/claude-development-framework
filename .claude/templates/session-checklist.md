---
tier: 2
purpose: Session start/end procedures
reload_trigger: At session start
estimated_read_time: 5 minutes
---

# Session Checklist - 9 Phases

**Version**: 2.0
**Last Updated**: 2025-09-30
**Purpose**: Per-session verification checklist for every interaction

---

## Phase 1: Orientation ⚙️

**Every session starts here:**

- [ ] Read `.claude/CLAUDE.md`
- [ ] Read `.claude/development-rules.md`
- [ ] Read `.claude/start-here.md` (refresh understanding)
- [ ] Read `planning/current-iteration.md`
- [ ] Read `planning/session-state.md` (if exists)
- [ ] **Check git status**: Run `git status` and report branch and working tree state
- [ ] **Verify branch**: Confirm on correct branch or on main (ready to create feature branch)
- [ ] Report context usage percentage to user
- [ ] Confirm current focus with user

**Output**: Clear understanding of current state, git status, and what to work on.

---

## Phase 2: Research 📚

**If work requires learning something new:**

- [ ] Identify knowledge gaps (e.g., new library, pattern, algorithm)
- [ ] Search for relevant documentation, papers, or articles
- [ ] Read and understand key concepts
- [ ] Document findings in `research/learnings/[topic]-summary.md`
- [ ] Create ADR if technical decision is needed
- [ ] Get user confirmation on approach

**Output**: Research documented, approach validated.

**Skip if**: No new learning required for current work.

---

## Phase 3: Planning 📋

**Before any implementation work:**

- [ ] Review current iteration plan OR create new iteration
- [ ] Verify iteration scope is 1-3 hours max
- [ ] Verify specification exists for all planned work
- [ ] List specific tests needed (test names, scenarios)
- [ ] Confirm iteration is fully planned
- [ ] **Create git branch**: If starting new iteration/UC, create feature branch
  - `git checkout main && git pull origin main`
  - `git checkout -b iteration-XXX-description` (or `uc-XXX-description`)
  - Report to user: "Created branch [branch-name]"
- [ ] Get user approval to proceed

**Output**: Clear iteration plan with test list, on dedicated feature branch.

---

## Phase 4: Test-First 🔴

**For each test in the iteration:**

- [ ] Write test BEFORE implementation
- [ ] Test should fail (RED)
- [ ] Run test to verify it fails correctly
- [ ] Verify test failure message is clear
- [ ] Show failing test to user
- [ ] Get approval to implement

**Output**: Failing test that defines correctness.

**CRITICAL**: NEVER skip to implementation without failing test.

---

## Phase 5: Implement ✅

**Make the test pass:**

- [ ] Write minimal code to make test pass (GREEN)
- [ ] Run test to verify it passes
- [ ] Run ALL tests to verify nothing broke
- [ ] Check code quality (type hints, docstrings, SRP)
- [ ] Add spec reference to code comments/docstrings
- [ ] Show passing tests to user

**Output**: Working code with all tests green.

---

## Phase 6: Refactor 🔧

**Improve code quality (REFACTOR step of TDD):**

- [ ] Review code against refactoring checklist
- [ ] Check for code duplication → Extract to functions
- [ ] Check function complexity → Split if > 20-30 lines or multiple responsibilities
- [ ] Check naming quality → Rename for clarity
- [ ] Check for magic numbers → Extract to constants
- [ ] Simplify conditional logic → Use guard clauses, extract conditions
- [ ] Review type hints and docstrings → Add if missing
- [ ] Apply design patterns where appropriate
- [ ] Run tests after EACH refactoring → Verify behavior unchanged
- [ ] Commit refactoring separately with `refactor:` type

**Output**: Clean, maintainable code with all tests still passing.

**CRITICAL**: NEVER skip refactoring. RED → GREEN → **REFACTOR** is the full TDD cycle.

See `.claude/templates/refactoring-checklist.md` for comprehensive refactoring guidance.

---

## Phase 7: Validate ✓

**Before considering work complete:**

- [ ] ALL tests pass (unit, integration, BDD)
- [ ] No test output warnings or errors
- [ ] Code quality checks pass (linting, type checking)
- [ ] Spec alignment verified (code matches spec)
- [ ] No TODO comments added
- [ ] No skipped error handling
- [ ] Coverage maintained or improved

**Output**: High-quality, verified code.

---

## Phase 8: Document 📝

**Record what was done:**

- [ ] Update `planning/current-iteration.md` with progress
- [ ] Record any new technical decisions as ADRs
- [ ] **Generate session state** (automated):
  - [ ] Run: `./scripts/generate-session-state.sh`
  - [ ] Review generated `planning/session-state.md`
  - [ ] Fill in placeholders (work completed, next steps, blockers)
  - [ ] Edit context notes as needed
- [ ] Note any learnings or insights
- [ ] Document any blockers or issues
- [ ] Update use case status if iteration completed

**Output**: Current state documented for continuity.

**Tip**: The `generate-session-state.sh` script creates a template automatically. Just fill in the details!

---

## Phase 9: Close 🏁

**End of session:**

- [ ] **Pre-commit verification** (iteration must be complete):
  - [ ] All tests passing
  - [ ] No TODO comments
  - [ ] No debug code
  - [ ] Spec references in docstrings
- [ ] **Git commit workflow**:
  - [ ] Stage files: `git add specs/ implementation/ planning/ .claude/`
  - [ ] Generate commit message with format:
    ```
    [type]: Brief description

    Specification: UC-XXX / ITERATION-XXX
    Tests: [X passing / Y total]

    Details:
    - What was implemented
    - Tests added

    🤖 Generated with Claude Code
    Co-Authored-By: Claude <noreply@anthropic.com>
    ```
  - [ ] Show commit message to user for approval
  - [ ] Execute: `git commit -m "message"`
  - [ ] Push: `git push -u origin [branch-name]`
  - [ ] Report: "Committed and pushed to branch [branch-name]"
- [ ] Summarize accomplishments for user
- [ ] Note what should happen next session
- [ ] Suggest specific next steps
- [ ] Confirm session-state.md is ready for pickup

**Output**: Clean session closure with work committed to feature branch and clear handoff.

**IMPORTANT**: Only commit when iteration/UC is complete. If incomplete, document stopping point in `planning/current-iteration.md` and tell user work remains on branch uncommitted.

---

## Red Flags 🚩

**STOP IMMEDIATELY if you catch yourself:**

❌ Writing code without a test → Go to Phase 4
❌ Weakening a test to make it pass → Root cause analysis required
❌ No specification exists → Go to Phase 3, create spec first
❌ Scope creeping beyond iteration → Replan or defer
❌ Skipping error handling → Implement properly now
❌ Adding TODO comments → Create iteration or issue instead
❌ Context above 80% → Compact before proceeding
❌ Working on main branch → Create feature branch immediately
❌ Committing with failing tests → Fix tests first
❌ Committing incomplete iteration → Wait until complete or document stopping point
❌ Skipping refactoring step → Always RED → GREEN → **REFACTOR**

---

## Quick Phase Reference

| Phase | Key Question | Go/No-Go |
|-------|--------------|----------|
| 1. Orientation | Do I know what to work on? | Must pass |
| 2. Research | Do I know how to build this? | Skip if known |
| 3. Planning | Is there a clear iteration plan? | Must pass |
| 4. Test-First | Is there a failing test? | Must pass |
| 5. Implement | Does test pass now? | Must pass |
| 6. Refactor | Is code clean and maintainable? | Must pass |
| 7. Validate | Is everything green and quality? | Must pass |
| 8. Document | Is state recorded for next session? | Must pass |
| 9. Close | Is work committed and summarized? | Must pass |

---

## Self-Check Questions

### At Start of Session:
- ✅ Have I read TIER 1 files?
- ✅ Do I know current iteration?
- ✅ Is context usage acceptable?

### During Development:
- ✅ Am I following test-first?
- ✅ Am I enforcing the rules?
- ✅ Is quality maintained?

### Before Closing:
- ✅ All tests green?
- ✅ State documented?
- ✅ User knows next steps?

---

## Emergency Procedures

### If You Skip Ahead
**Caught writing code without test?**
1. STOP immediately
2. Delete or comment out code
3. Go to Phase 4: Write test first
4. Then return to Phase 5 properly

### If Test Fails Unexpectedly
1. Do NOT weaken test
2. Analyze root cause
3. Fix system, not test
4. If spec is wrong, update spec first

### If Context Degraded
1. STOP work
2. Save session state
3. Reload TIER 1 files
4. Resume from current phase

---

**Remember**: These phases are NOT optional. Follow them in order every session for consistent, high-quality results.
---

**Template Version**: 1.0
**Framework**: Claude Development Framework v2.1
**Last Updated**: 2025-10-01
**Compatibility**: Framework v2.1+
