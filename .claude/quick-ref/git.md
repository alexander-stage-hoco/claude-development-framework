---
tier: 4
purpose: Git commands quick reference
reload_trigger: When using git (quick ref)
estimated_read_time: 3 minutes
---

# Quick Ref: Git Workflow

**Purpose**: Complete git reference for the framework

---

## Branch Workflow

### Start New Iteration
```bash
git checkout main && git pull && git checkout -b iteration-XXX-description
```

### During Work
```bash
git status          # Check what changed
git diff            # See changes
# DON'T commit until iteration complete with tests passing!
```

### When Complete (Tests Pass)
```bash
git add specs/ implementation/ planning/ .claude/
git commit -m "[message]"  # See format below
git push -u origin iteration-XXX-description
```

### Merge to Main
```bash
git checkout main && git merge iteration-XXX-description && git push
```

---

## Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Iteration | `iteration-XXX-description` | `iteration-001-user-auth` |
| Use Case | `uc-XXX-description` | `uc-002-authentication` |
| Bugfix | `bugfix-description` | `bugfix-login-validation` |
| Spike | `spike-description` | `spike-graphql-api` |

---

## Commit Message Format

```
[type]: Brief description (50 chars max)

Specification: UC-XXX / SVC-XXX / ITERATION-XXX
Tests: [X passing / Y total]

Details:
- What was implemented
- What tests were added
- Technical decisions made

ADR References: ADR-XXX (if applicable)

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Commit Types
- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code improvement (no behavior change)
- `test` - Add/update tests
- `docs` - Documentation
- `chore` - Maintenance

### Example Commits

**Feature**:
```
feat: Implement user registration endpoint

Specification: UC-001, SVC-001
Tests: 12 passing / 12 total

Details:
- POST /users endpoint with validation
- User model with password hashing (bcrypt)
- Repository pattern for data access
- BDD scenarios for happy path and errors

ADR References: ADR-001 (Python), ADR-003 (Repository)

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Refactor**:
```
refactor: Extract user processing into separate functions

Improves code organization:
- Extract _register_new_user function
- Extract _update_existing_user function
- Standardize response formats
- Add type hints

Tests: 12 passing / 12 total (no behavior change)

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Using HEREDOC for multiline**:
```bash
git commit -m "$(cat <<'EOF'
feat: Implement user registration

Specification: UC-001
Tests: 8 passing / 8 total

Details:
- User registration endpoint
- Email validation
- Password hashing

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Commit Requirements

**Before committing**:
- [ ] All tests passing
- [ ] No TODO comments
- [ ] No debug code
- [ ] Spec references in docstrings
- [ ] User approved implementation
- [ ] On feature branch (not main)

**DON'T commit**:
- ❌ Failing tests
- ❌ TODO comments
- ❌ Debug code
- ❌ Work on main branch

---

## Common Workflows

### Hotfix
```bash
git checkout main && git pull
git checkout -b hotfix-description
# Fix, test, commit
git push -u origin hotfix-description
git checkout main && git merge hotfix-description && git push
```

### Spike (Experimental)
```bash
git checkout -b spike-description
# Experiment freely
# Keep: commit and merge
# Discard: git checkout main && git branch -D spike-description
```

### Multiple Iterations
```bash
# Complete iteration 1
git checkout iteration-001 && git commit && git push
git checkout main && git merge iteration-001

# Start iteration 2
git checkout -b iteration-002
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| On wrong branch | `git checkout -b correct-branch` |
| Uncommitted changes blocking checkout | `git stash` then checkout, then `git stash pop` |
| Want to undo last commit (keep changes) | `git reset --soft HEAD~1` |
| Want to undo last commit (discard) | `git reset --hard HEAD~1` ⚠️ |
| Forgot to create branch before committing | `git branch new-branch && git reset --hard origin/main && git checkout new-branch` |
| Main branch diverged | `git checkout main && git pull && git checkout feature && git rebase main` |
| Merge conflict | Edit files, remove `<<<<<<<` markers, `git add .`, `git commit` |
| Push rejected (non-fast-forward) | `git pull --rebase origin branch-name` then `git push` |
| Accidentally deleted branch | `git reflog` find commit, `git checkout -b branch-name <commit-hash>` |
| Working tree not clean | `git stash` or `git add . && git commit` or `git checkout .` ⚠️ |

⚠️ = Can lose work, use carefully!

---

## Viewing History

```bash
git log --oneline -10              # Recent commits
git log -1                         # Last commit details
git show HEAD                      # Changes in last commit
git log --oneline --graph --all    # Visual branch history
```

---

## Stashing

```bash
git stash push -m "WIP message"    # Save changes
git stash list                     # List stashes
git stash apply                    # Apply most recent (keep in list)
git stash pop                      # Apply and remove from list
git stash drop stash@{0}           # Delete stash
```

---

## Remote Operations

```bash
git remote -v                      # Check remotes
git fetch origin                   # Fetch without merging
git pull origin main               # Fetch and merge
git push                           # Push current branch
git push -u origin branch-name     # Push with upstream tracking
git push origin --delete branch    # Delete remote branch
```

---

## Branch Management

```bash
git branch -a                      # List all branches
git branch -d branch-name          # Delete merged branch
git branch -D branch-name          # Force delete unmerged ⚠️
git branch -m new-name             # Rename current branch
git checkout branch-name           # Switch branch
git checkout -b new-branch         # Create and switch
```

---

## Emergency Commands ⚠️

```bash
git merge --abort                  # Abort merge
git rebase --abort                 # Abort rebase
git reset --hard HEAD              # Discard ALL changes ⚠️
git push --force                   # Force push ⚠️ (NEVER to main!)
```

---

**Remember**: Branch per iteration, commit when complete with passing tests!
