# Quick Ref: Session Start Checklist

**Purpose**: Essential steps to start every Claude development session

---

## 1. Read Framework Files (ALWAYS)

```
✓ .claude/CLAUDE.md
✓ .claude/templates/development-rules.md
✓ planning/current-iteration.md
✓ planning/session-state.md (if exists)
```

---

## 2. Check Git Status

```bash
git status
git branch
```

**Report to user**: "On branch [name], working tree [clean/has changes]"

**If uncommitted changes**:
- Ask: "Found uncommitted changes. Commit or stash them?"
- Get user decision before proceeding

---

## 3. Verify Current Context

- [ ] What are we working on? (Check current-iteration.md)
- [ ] What's the current phase? (Spec / Test / Implement / Refactor)
- [ ] What's blocked/waiting? (Check session-state.md)

---

## 4. Report Context Usage

"Context usage: [X]% - [status: clear/moderate/high]"

**At 70%+**: Warn user about context limits

---

## 5. Ask User for Direction

**If continuation**: "Ready to continue [current work]. Shall I proceed?"
**If new work**: "What would you like to work on today?"

---

## Quick Branch Check

**NOT on a feature branch?** → Create immediately:
```bash
git checkout -b iteration-XXX-description
```

---

## Common Session Start Scenarios

### Scenario: First Session (New Project)
1. Read framework files
2. Ask discovery questions (problem, users, features, constraints)
3. Create project overview and use case specs
4. Save session state
5. **NO CODE YET** (specs first!)

### Scenario: Continuation Session
1. Read framework files
2. Read session-state.md
3. Report: "Last session: [summary]. Current focus: [task]"
4. Continue from stopping point

### Scenario: Context Low (Reload Needed)
1. Say: "Context usage high ([X]%). Need to reload key files."
2. Re-read TIER 1 files (CLAUDE.md, development-rules.md, current-iteration.md)
3. Re-read relevant specs
4. Confirm: "Context refreshed. Ready to continue."

---

## Red Flags at Session Start

❌ **No current-iteration.md**: "Project not initialized. Start with first session protocol?"
❌ **Uncommitted changes**: "Working tree not clean. What should I do with these changes?"
❌ **On main branch**: "Not on feature branch. Should I create one?"
❌ **Can't quote rules**: "Context degraded. Need to reload framework files."

---

**Remember**: Session start discipline ensures continuity and prevents context loss.