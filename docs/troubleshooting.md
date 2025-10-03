# Troubleshooting Guide: When Things Go Wrong

**Purpose**: Concrete solutions to common problems when using the Claude Development Framework

**Last Updated**: 2025-09-30

---

## How to Use This Guide

When you encounter a problem:
1. Find the scenario that matches your situation
2. Follow the "Immediate Recovery" steps
3. Apply the "Prevention" measures to avoid recurrence

---

## Scenario 1: Claude Writes Code Without Tests

### Symptom
```
Claude: "I'll implement the entity extractor:
         [shows implementation code]"
```

### What Went Wrong
Violated Rule 2 (Tests Define Correctness) - Claude skipped test-first approach

### Immediate Recovery

**User says**:
```
"STOP. Check development-rules.md Rule 2. Tests first."
```

**Expected Claude Response**:
```
"You're absolutely right. I apologize for violating the rules.
 Let me write the tests FIRST:

 tests/unit/test_entity_extractor.py:
 - test_extract_person_entities()
 - test_extract_organization_entities()
 - test_confidence_scoring()

 These tests will fail with 'Module not found'.
 May I run them to verify they fail correctly before implementing?"
```

### Root Cause Prevention

Add to `.claude/CLAUDE.md`:
```markdown
## IMPLEMENTATION GATE
Before ANY implementation code:
1. STOP and verify test file exists
2. STOP and verify tests are written
3. STOP and verify tests are failing correctly
4. Request user approval
5. ONLY THEN write implementation code
```

### Quick Recovery Commands
- `"Check development rules"`
- `"Tests first, then implementation"`
- `"Show me the failing tests"`

---

## Scenario 2: Tests Fail and Claude Wants to Weaken Them

### Symptom
```
Claude: "The test expects exact match, but that's too strict.
         Let's change assert x == 'exact' to assert 'partial' in x"
```

### What Went Wrong
Attempting to weaken tests instead of fixing the system (violates Rule 6)

### Immediate Recovery

**User says**:
```
"NO. This violates Rule 6. The test is correct.
 The system is wrong. Analyze WHY it's failing."
```

**Expected Claude Response**:
```
"You're correct. Let me analyze the root cause:

 Test Failure Analysis:
 - Test expects: 'John Smith'
 - System returns: 'john smith'
 - Root Cause: Entity extractor not preserving original capitalization
 - Fix: Update EntityExtractor.extract() to preserve case
 - Spec alignment: UC-003 says 'preserve original formatting'

 The specification is correct, the test is correct,
 the implementation needs fixing."
```

### Prevention Template

Create `.claude/test-failure-analysis.md`:
```markdown
# Test Failure Analysis Protocol

When test fails:

## Step 1: State Facts
- **Failing Test**: [test name]
- **Error Message**: [exact error]
- **Expected**: [what test expects]
- **Actual**: [what system does]

## Step 2: Check Specification
- **Spec Says**: [quote from spec]
- **Spec Location**: specs/use-cases/UC-XXX.md#section
- **Is Spec Clear?**: Yes/No

## Step 3: Identify Root Cause
- **Where**: [which component/function]
- **Why**: [underlying issue]
- **Type**: Logic Error | Data Issue | Integration Problem

## Step 4: Determine Fix
- [ ] Option A: Fix implementation (PREFERRED)
- [ ] Option B: Spec is unclear → Update spec, then update test
- [ ] Option C: Test has bug → Fix test (RARE)

## Step 5: Validate Fix
- [ ] Fix addresses root cause
- [ ] No other tests broken
- [ ] Spec still aligned

**NEVER** weaken test to make it pass without this analysis.
```

### Quick Recovery Commands
- `"Analyze root cause, don't change the test"`
- `"What does the specification say?"`
- `"The test is correct, fix the system"`

---

## Scenario 3: Iteration Scope Creep

### Symptom
```
User: "Actually, we need to add feature X to this iteration."
```

### What Goes Wrong
Scope creep - iteration grows from 2 hours to 6 hours

### Correct Claude Response

```
"I understand the new requirement is important.
 However, adding it mid-iteration violates our incremental approach.

 Current Situation:
 - Iteration 007: 60% complete (tests written, half implemented)
 - New feature: Would add 3-4 hours
 - Risk: Incomplete iteration, untested code

 Recommended Approach:

 Option 1 (Recommended): Complete Current, New Next
 - Finish iteration 007 (1 hour remaining)
 - Create iteration 008 for new feature
 - Estimated: 2 hours for feature
 Total time: Same, but cleaner

 Option 2: Pause and Reprioritize
 - Commit current progress
 - Create urgent iteration 007b for new feature
 - Resume 007 afterward
 - Risk: Context switching overhead

 Option 3: Spec Update + Replan
 - Update UC-003 specification with new requirement
 - Abandon iteration 007
 - Create new iteration with full scope
 - Risk: Waste 1 hour of work

 Which approach do you prefer?"
```

### Change Request Protocol

Create `specs/change-requests/CR-XXX-change-request.md`:
```markdown
# Change Request: CR-007

**Date**: YYYY-MM-DD
**Requested By**: [Name]
**Priority**: High | Medium | Low

## Current Behavior
[What exists now]

## Requested Behavior
[What is being requested]

## Business Justification
[Why this is needed now]

## Impact Analysis

**Specifications Affected**:
- [ ] specs/use-cases/UC-XXX.md (section X.Y)
- [ ] specs/services/SVC-XXX.md

**Iterations Affected**:
- Iteration XXX: [status] → needs [action]

**Tests Affected**:
- N existing tests need updates
- N new tests required

**Estimated Additional Effort**: X hours

## Decision
- [ ] Approved - Update specs and proceed
- [ ] Rejected - Reason: [why]
- [ ] Deferred - Reason: [why] When: [iteration]

## If Approved
1. Update relevant specifications
2. Create new/updated iteration plan
3. Archive current progress if needed
4. Start with updated scope
```

### Quick Recovery Commands
- `"Let's complete the current iteration first"`
- `"Can this wait for the next iteration?"`
- `"Show me the impact analysis"`

---

## Scenario 4: Iteration Taking Much Longer Than Planned

### Symptom
Planned 2 hours, now at 4 hours and not done

### Common Causes

**Cause 1: Underestimated Complexity**
```
Original plan: "Add confidence threshold parameter" (2h)

Reality:
- Parameter validation needed
- Backward compatibility required
- Three filtering strategies, not one
- Integration with caching layer

Fix: Add research/design phase before complex iterations
```

**Cause 2: Unclear Specification**
```
Iteration failed because:
- Spec says "filter low confidence entities"
- Doesn't define "low confidence"
- Spent 2 hours clarifying with stakeholder

Fix: Specification review checklist before iteration
```

**Cause 3: Hidden Dependencies**
```
Started entity extraction, discovered:
- Need chunking service (not ready)
- Need database schema (doesn't exist)
- Need NLP model (not downloaded)

Fix: Dependency analysis in iteration planning
```

### Prevention Checklist

Add to iteration template:
```markdown
## Iteration Complexity Assessment

### Complexity Signals (If ANY are true, add buffer or split):
- [ ] Touching >5 files
- [ ] New external dependency
- [ ] Specification has ambiguity
- [ ] Team hasn't done similar work before
- [ ] Requires coordination with other systems

### If Complex:
- [ ] Add 50% time buffer
- OR
- [ ] Split into 2 smaller iterations
- [ ] Add research/spike phase first

### Dependency Check:
- [ ] All required services exist
- [ ] All required data structures defined
- [ ] All required external resources available
- [ ] No blocking issues
```

### Quick Recovery Actions
1. **Stop and assess**: How much more work remains?
2. **Split iteration**: Complete what's done, plan new iteration for rest
3. **Update estimates**: Learn from this for future planning
4. **Document learnings**: Add to iteration "Lessons Learned"

---

## Scenario 5: Context Window Degradation

### Symptom
Claude starts violating rules or forgetting critical information

### What Went Wrong
Long session pushed critical files (CLAUDE.md, development-rules.md) out of active context

### Immediate Recovery

**User says**:
```
"Context check. Can you quote Rule 2 from development-rules.md?"
```

**If Claude can't quote accurately**:
```
"Reload .claude/CLAUDE.md and .claude/development-rules.md immediately."
```

### Prevention

**Check context every 20 interactions**:
```
User: "Context check"

Claude should respond:
"Context Status: 65% (130K/200K tokens)
 TIER 1 files:
 - ✅ CLAUDE.md: Rules clear
 - ✅ development-rules.md: All 10 rules clear
 - ✅ current-iteration.md: Clear
 Recommendation: Healthy, continue working"
```

**At 75%+ usage, compact**:
```
User: "Context 75% full. Compact now."

Claude:
1. Summarizes conversation history
2. Archives completed work references
3. Reloads TIER 1 critical files
4. Reports new usage percentage
```

### Quick Recovery Commands
- `"Context check"`
- `"Reload CLAUDE.md"`
- `"Compact context"`
- `"What are the 10 development rules?"` (verification)

---

## Scenario 6: Specification-Code Drift

### Symptom
Code and specifications no longer match after several iterations

### What Went Wrong
Changes were made to code without updating specs, or vice versa

### Immediate Recovery

**Run automated alignment check**:
```bash
./scripts/check-alignment.py --verbose
```

This script automatically verifies:
1. Every use case has a corresponding BDD feature file
2. BDD scenario counts match acceptance criteria counts
3. No orphaned features (tests without specs)
4. No broken references between UCs and BDD files

**Example output**:
```
🔍 Parsing use case specifications...
   Found 5 use cases

🔍 Parsing BDD feature files...
   Found 4 features

⚠️  ALIGNMENT ISSUES FOUND: 2

🚨 ERRORS (must fix):
  ❌ UC-005 has no corresponding BDD feature file
     UC: UC-005

⚠️  WARNINGS (review recommended):
  ⚠️  UC-003: 4 acceptance criteria but 3 BDD scenarios in 'List TODOs'
     UC: UC-003
     Feature: List TODOs
```

**Manual audit**:
1. Pick one use case (e.g., UC-003)
2. Read the specification
3. Trace to implementation
4. Verify tests match acceptance criteria
5. Find mismatches

### Fixing Alignment Issues

**Issue: missing_bdd (ERROR)**
- Problem: Use case has acceptance criteria but no BDD feature file
- Fix: Create BDD feature file in `tests/bdd/` with scenarios matching criteria
```bash
# Create feature file
touch tests/bdd/features/uc-005-example.feature

# Add UC reference to spec
echo "**BDD File**: \`features/uc-005-example.feature\`" >> specs/use-cases/UC-005-example.md
```

**Issue: count_mismatch (WARNING)**
- Problem: Number of BDD scenarios doesn't match acceptance criteria count
- Fix: Add missing scenarios or update criteria to match
```bash
# Check current counts
./scripts/check-alignment.py --verbose

# Option 1: Add missing scenario to BDD file
# Option 2: Update acceptance criteria in spec
# Option 3: Merge/split scenarios to align
```

**Issue: orphaned_feature (WARNING)**
- Problem: BDD feature file exists but doesn't reference any use case
- Fix: Add UC reference to feature file comments
```gherkin
# Feature: Example Feature
# Use Case: UC-003
# Spec: specs/use-cases/UC-003-example.md
```

**Issue: broken_bdd_ref (ERROR)**
- Problem: Use case references a BDD file that doesn't exist
- Fix: Create the referenced file or update the reference
```bash
# Find broken reference
grep "BDD File:" specs/use-cases/UC-*.md

# Create missing file or fix reference
```

**Get detailed explanations**:
```bash
./scripts/check-alignment.py --explain
```

### Prevention

**After every iteration**:
- [ ] Update `planning/current-iteration.md` with actual results
- [ ] If spec changed, update spec file AND commit message
- [ ] If implementation deviated, update spec OR fix implementation
- [ ] Run alignment check: `./scripts/check-alignment.py`

**Weekly automated audit** (2 minutes):
```bash
# Run comprehensive alignment check
./scripts/check-alignment.py --verbose

# Check traceability
./scripts/validate-traceability.py

# Both should exit with 0 (no issues)
echo $?
```

**Weekly manual audit** (15 minutes):
```markdown
## Spec-Code Alignment Audit

### UC-001: Create TODO
- [ ] Spec exists: ✅ specs/use-cases/UC-001-create-todo.md
- [ ] Implementation exists: ✅ src/api/routes/todos.py
- [ ] Tests exist: ✅ tests/integration/api/test_create_todo.py
- [ ] BDD feature: ✅ tests/bdd/features/UC-001-create-todo.feature
- [ ] Alignment: ✅ Code matches spec

### UC-002: List TODOs
[repeat audit]
```

### Quick Recovery Commands
- `"Audit UC-003 for spec-code alignment"`
- `"Show me what changed in this iteration"`
- `"Does the implementation match the specification?"`

---

## Scenario 7: Dependencies Between Iterations

### Symptom
Can't start iteration 008 because iteration 007 isn't fully complete

### What Went Wrong
Iteration dependencies not explicitly documented

### Prevention

In iteration plan, add:
```markdown
## Dependencies

**This iteration requires**:
- [ ] Iteration 007 complete (entity extraction service)
- [ ] Database schema v2 deployed
- [ ] NLP model downloaded (~500MB)

**This iteration blocks**:
- Iteration 009 (needs confidence filtering from this iteration)
- Iteration 010 (needs same)

**Can proceed in parallel with**:
- Iteration 011 (different use case)
- Iteration 012 (different service)
```

### Quick Recovery
1. Document the blocker explicitly
2. Find parallel work (different use case/service)
3. Update roadmap to reflect dependency chain

---

## Emergency: Production Hotfix Needed

### When to Use
- Production system down
- Need fix in < 1 hour
- Can't follow full process

### Emergency Protocol

```markdown
## EMERGENCY HOTFIX MODE

User: "PRODUCTION EMERGENCY. Need hotfix mode."
Claude: "Emergency protocol activated. Documenting technical debt."

### Step 1: Create Emergency Branch
git checkout -b hotfix/YYYY-MM-DD-issue-description

### Step 2: Minimal Fix ONLY
- Fix ONLY the specific bug
- Add ONLY regression test for the bug
- NO refactoring
- NO "while I'm here" changes

### Step 3: Emergency Commit
git commit -m "HOTFIX: [Brief description]

Emergency: Production down
Root Cause: [Specific technical issue]
Fix: [What code changed]
Test: [Regression test added]

Technical Debt Created:
- TD-007: No full specification exists
- TD-008: Only regression test, no comprehensive tests

Follow-up: Create proper implementation in iteration XXX"

### Step 4: Deploy Immediately

### Step 5: Technical Debt Payback (Within 1 Week)
- Schedule iteration to create specification
- Schedule iteration to implement properly
- Schedule iteration to add comprehensive tests
```

**Key Principle**: Emergency hotfix is TEMPORARY. Proper solution REQUIRED within 1 week.

---

## Summary: Quick Reference

| Problem | Quick Command |
|---------|---------------|
| Claude skips tests | `"Tests first, then implementation"` |
| Claude weakens tests | `"Analyze root cause, don't change the test"` |
| Scope creep | `"Complete current iteration first"` |
| Over time estimate | Stop, split, document |
| Context degradation | `"Context check"` |
| Spec drift | Run weekly alignment audit |
| Dependency blocker | Document explicitly, find parallel work |
| Production emergency | `"EMERGENCY HOTFIX MODE"` |

---

## When to Modify the Framework

If you encounter the same problem 3+ times and these solutions don't work:
1. Document the new problem in `planning/framework-issues.md`
2. Propose a new rule or process
3. Add to `.claude/development-rules.md` if approved
4. Update this troubleshooting guide

**The framework should evolve based on real problems.**

---

**Document Version**: 1.0
**Part of**: Claude Development Framework
**See also**: `.claude/CLAUDE.md`, `.claude/development-rules.md`
