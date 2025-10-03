---
tier: 3
purpose: Git branching and commit strategy
reload_trigger: When committing or branching
estimated_read_time: 10 minutes
---

# Git Workflow Guide

**Version**: 2.1
**Last Updated**: 2025-09-30
**Purpose**: Git branching and commit strategy for disciplined development

---

## Overview

This framework enforces structured git workflow ensuring:
- Every piece of work on dedicated branch
- Code never committed in broken state
- Commit history traces to specifications
- Easy rollback and review

---

## Branch Strategy

### Branch Types

| Type | Pattern | Purpose | Example |
|------|---------|---------|---------|
| `main` | - | Production-ready, always deployable | `main` |
| `iteration-XXX-name` | iteration-### | Feature iterations | `iteration-001-user-auth` |
| `uc-XXX-name` | uc-### | Use case implementations | `uc-001-registration` |
| `bugfix-name` | bugfix- | Bug fixes | `bugfix-login-validation` |
| `spike-name` | spike- | Research/exploration | `spike-graphql-api` |

---

## Quick Workflows

### Start New Iteration
```bash
git checkout main && git pull && git checkout -b iteration-XXX-description
```

### Complete Iteration (Tests Pass)
```bash
git add specs/ implementation/ planning/ .claude/
git commit -m "[message with spec reference]"
git push -u origin iteration-XXX-description
```

### Refactor (Separate Commit)
```bash
# After implementation commit, refactor code
git add .
git commit -m "refactor: [description]

Tests: X passing / X total (no behavior change)"
git push
```

### Merge to Main
```bash
git checkout main && git merge iteration-XXX && git push
```

**Detailed workflows**: See `.claude/examples/git/workflows.md`

---

## Commit Message Format

### Standard Template

```
[type]: Brief description (50 chars max)

Specification: UC-XXX / SVC-XXX / ITERATION-XXX
Tests: [X passing / Y total]

Details:
- What was implemented
- What tests were added

ADR References: ADR-XXX (if applicable)

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Commit Types

| Type | Use When | Example |
|------|----------|---------|
| `feat` | New feature | `feat: Add user registration` |
| `fix` | Bug fix | `fix: Correct validation logic` |
| `refactor` | Code improvement | `refactor: Extract helpers` |
| `test` | Add/update tests | `test: Add edge cases` |
| `docs` | Documentation | `docs: Update API docs` |
| `chore` | Maintenance | `chore: Update dependencies` |

**Detailed examples**: See `.claude/examples/git/commit-messages.md`

---

## Commit Checklist

Before committing, verify:
- [ ] All tests passing
- [ ] No TODO comments
- [ ] No debug code
- [ ] Spec references in docstrings
- [ ] User approved implementation
- [ ] On feature branch (not main)

---

## When to Commit

### ✅ Commit When:
- Iteration complete with all tests passing
- Significant refactoring complete (separate commit)
- Use case fully implemented and validated
- Bugfix complete with tests

### ❌ DO NOT Commit:
- Failing tests
- Incomplete iteration
- TODO comments
- Debug code
- Work in progress on main branch

---

## Branch Workflow Rules

### Rule 1: Create Branch First
**Before starting work**:
```bash
git checkout main
git pull origin main
git checkout -b iteration-XXX-name
```

### Rule 2: Work on Branch
- Write tests (RED)
- Implement (GREEN)
- Refactor (REFACTOR)
- DO NOT commit until complete

### Rule 3: Commit When Complete
- All tests pass
- Follow commit message format
- Include spec references

### Rule 4: Separate Refactoring Commits
- Implementation: `feat:` or `fix:`
- Refactoring: `refactor:`
- Two commits, clear history

---

## Common Scenarios

### Scenario 1: Hotfix
```bash
git checkout main && git pull
git checkout -b hotfix-description
# Fix, test, commit
git push -u origin hotfix-description
git checkout main && git merge hotfix-description
```

### Scenario 2: Experimental Work
```bash
git checkout -b spike-description
# Experiment freely
# If keeping: commit and merge
# If discarding: git checkout main && git branch -D spike-description
```

### Scenario 3: Multiple Related Iterations
```bash
# Complete iteration 1
git checkout iteration-001 && git add . && git commit && git push
git checkout main && git merge iteration-001

# NOW start iteration 2
git checkout -b iteration-002
```

**More scenarios**: See `.claude/examples/git/workflows.md`

---

## Troubleshooting

### Quick Fixes

| Problem | Solution |
|---------|----------|
| On wrong branch | `git checkout -b correct-branch` |
| Uncommitted changes | `git stash` or `git commit` |
| Undo last commit | `git reset --soft HEAD~1` |
| Merge conflict | Edit files, `git add .`, `git commit` |
| Branch diverged | `git pull --rebase` |

**Complete troubleshooting**: See `.claude/quick-ref/git.md`

---

## Claude's Git Responsibilities

### At Session Start
- [ ] Check `git status`
- [ ] Verify current branch
- [ ] Report to user: "On branch [name], working tree [clean/has changes]"

### Before Starting Iteration
- [ ] Ensure on main: `git checkout main && git pull`
- [ ] Create feature branch: `git checkout -b iteration-XXX`
- [ ] Report: "Created branch [name]"

### At Iteration Complete
- [ ] Verify all tests pass
- [ ] Generate commit message (with spec references)
- [ ] Show message to user for approval
- [ ] Execute commit and push
- [ ] Report: "Committed to [branch] and pushed"

### When User Asks to Skip Git
**Response**:
"Git workflow is Rule #11 - ensures traceability and quality. Creating branch takes 5 seconds. Should I proceed?"

---

## Integration with Development Rules

**Rule #11**: Git Workflow Discipline
- Branch per iteration/use case
- Commit only when complete with passing tests
- Proper commit messages with spec references
- See: `.claude/templates/development-rules.md`

**Session Protocol**: Phase 1, 3, 9
- Phase 1: Check git status
- Phase 3: Create branch
- Phase 9: Commit with proper message
- See: `.claude/templates/session-checklist.md`

---

## Quick Reference

**Essential Commands**:
```bash
# Start work
git checkout main && git pull && git checkout -b iteration-XXX-name

# Check status
git status

# Commit
git add . && git commit -m "message"

# Push
git push -u origin [branch]

# Merge
git checkout main && git merge [branch]
```

---

## Additional Resources

**Quick Reference**:
- `.claude/quick-ref/git.md` - Complete git reference with workflows, commit messages, and troubleshooting

**Related Guides**:
- `development-rules.md` - Rule 11: Git Workflow Discipline
- `session-checklist.md` - Git steps in phases 1, 3, 9

---

**Remember**: Every iteration on dedicated branch. Commit only when complete with passing tests. Clean git history enables easy rollback and review.
---

**Template Version**: 1.0
**Framework**: Claude Development Framework v2.2
**Last Updated**: 2025-10-01
**Compatibility**: Framework v2.2+
