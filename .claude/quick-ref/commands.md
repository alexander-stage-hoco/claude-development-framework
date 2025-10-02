---
tier: 4
purpose: Common commands quick reference
reload_trigger: When need command reminder
estimated_read_time: 3 minutes
---

# Quick Command Reference

**Purpose**: One-page reference for common commands and prompts

---

## Framework Scripts

### Initialize Project
```bash
./init-project.sh my-project
./init-project.sh ../projects/my-project  # Outside template
./init-project.sh /absolute/path/my-project
```

### Validate Framework
```bash
./validate-template.sh
```

### Validate Traceability
```bash
# Check UC-Service traceability
python3 scripts/validate-traceability.py

# Check spec-code alignment (BDD scenarios vs acceptance criteria)
./scripts/check-alignment.py --verbose
```

---

## Git Commands

**See `quick-ref/git.md` for complete details**

### Start New Iteration
```bash
git checkout main && git pull
git checkout -b iteration-007-entity-extraction
```

### Commit When Tests Pass
```bash
git add .
git commit -m "feat: implement entity extraction

Specification: UC-003
Tests: 12 passing / 12 total
Services: EntityService
Iteration: 007

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Merge to Main
```bash
git checkout main
git merge iteration-007-entity-extraction
git push origin main
```

---

## Common Claude Prompts

### Session Start
```
Continue from last session. Read planning/session-state.md first.
```

```
Start new session. Check planning/current-iteration.md for current work.
```

### Context Management
```
Context check - what's your current usage?
```

```
Can you quote Rule #2 from development-rules.md?
```

```
Reload TIER 1 files (.claude/CLAUDE.md, development-rules.md)
```

```
Context 75% full - compress now
```

### Framework Enforcement
```
STOP. Check development-rules.md Rule #2 - tests first.
```

```
This violates Rule #6 (Never Compromise Tests) - analyze root cause.
```

```
What does the specification say about this?
```

```
Tests first, then implementation.
```

### Status Checks
```
What's the current iteration status?
```

```
Show me planning/current-iteration.md
```

```
List all use cases in specs/use-cases/
```

```
What use cases are spec'd but not implemented?
```

### Service Work
```
Extract services from use cases UC-001 through UC-005
```

```
Validate service dependencies - check for circular dependencies
```

```
Update .claude/service-registry.md with new services
```

```
Show me the service dependency graph
```

### Specification Work
```
Create use case specification for [feature description]
```

```
Review specs/use-cases/UC-003.md for completeness
```

```
Does UC-004 reference all required services?
```

### Implementation
```
Implement UC-003 following TDD cycle
```

```
Show me the failing tests first
```

```
All tests passing - commit this iteration
```

### Troubleshooting
```
Why is this test failing? Analyze root cause.
```

```
The implementation doesn't match the spec - which should we update?
```

```
Show me the spec-code alignment for UC-003
```

---

## File Locations Quick Reference

| Need | Location |
|------|----------|
| Current work | `planning/current-iteration.md` |
| Session continuity | `planning/session-state.md` |
| Project vision | `specs/00-project-overview.md` |
| Use cases | `specs/use-cases/UC-*.md` |
| Services | `services/*/service-spec.md` |
| Service catalog | `.claude/service-registry.md` |
| Technical decisions | `.claude/technical-decisions.md` |
| Implementation | `implementation/src/` |
| Tests | `implementation/tests/` |
| Research | `research/` |

---

## Validation Checklists

### Before Committing
- [ ] All tests passing
- [ ] No TODO comments
- [ ] Spec references in docstrings
- [ ] User approved implementation
- [ ] Iteration complete

### Before New Iteration
- [ ] Previous iteration complete
- [ ] Spec exists for new work
- [ ] Dependencies available
- [ ] New branch created
- [ ] Iteration plan documented

### Before Implementation
- [ ] Specification file exists
- [ ] Tests file created
- [ ] Tests written and failing
- [ ] User approval received

---

## Quick Fixes

| Problem | Command/Prompt |
|---------|----------------|
| Framework not validating | `./validate-template.sh` |
| Traceability broken | `python3 scripts/validate-traceability.py` |
| Spec-code drift | `./scripts/check-alignment.py --verbose` |
| Git branch confusion | `git branch --show-current` |
| Context overload | `"Context check"` |
| Lost current work | `cat planning/current-iteration.md` |
| Claude violating rules | `"Check development-rules.md Rule #N"` |
| Tests weakened | `"NO - analyze root cause, fix system not test"` |
| Scope creep | `"Complete current iteration first"` |

---

## Session Start Commands

### First Session (New Project)
```
Analyze this project directory. Read .claude/start-here.md first.
```

### Continuation Session
```
Continue from session N. Read these files:
1. planning/session-state.md (context)
2. planning/current-iteration.md (current work)
3. .claude/development-rules.md (rules refresh)
```

### After Long Break
```
Context reset needed. Re-read:
1. .claude/CLAUDE.md
2. .claude/development-rules.md
3. planning/current-iteration.md
Then report current context.
```

---

## Emergency Commands

### Production Hotfix
```
PRODUCTION EMERGENCY. Need hotfix mode.
Create branch: hotfix/YYYY-MM-DD-issue-description
Minimal fix only - no refactoring.
```

### Context Emergency (80%+)
```
STOP work. Context at 80%+. Compress immediately:
1. Summarize conversation
2. Archive completed work
3. Reload TIER 1 files
4. Resume work
```

### Rules Forgotten
```
Context degradation detected. You cannot quote the rules correctly.
Re-read .claude/CLAUDE.md and development-rules.md NOW.
```

---

## Claude Self-Check Commands

### Every 20 Interactions
```
Self-check:
- Can I quote Rule #2? [test yourself]
- Do I remember current iteration? [verify]
- Can I recall recent ADRs? [check]
```

### At 70% Context
```
Context usage check:
- Current: X%
- TIER 1 files loaded? [verify]
- Recommend: [action if needed]
```

---

## Subagent Commands

### Launch Service Extractor
```
Use service-extractor subagent to analyze UC-001 through UC-005
and extract reusable services.
```

### Launch Library Finder
```
Use service-library-finder subagent to evaluate authentication
libraries for AuthService implementation.
```

### Launch Performance Optimizer
```
Use service-optimizer subagent to benchmark 3 caching strategies
for ProductService and recommend optimal approach.
```

### Launch Dependency Analyzer
```
Use service-dependency-analyzer subagent to validate architecture
and detect circular dependencies.
```

### Launch Traceability Validator
```
Use uc-service-tracer subagent to verify bidirectional
UC-Service traceability is 100%.
```

---

## Testing Commands

### Run Tests
```bash
pytest tests/unit/
pytest tests/integration/
pytest tests/bdd/
pytest  # All tests
```

### Run Specific Test
```bash
pytest tests/unit/test_entity_extractor.py::test_extract_person
```

### Run With Coverage
```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

---

## Common Bash Commands

### Find Files
```bash
find specs/use-cases -name "UC-*.md"
find implementation -name "test_*.py"
```

### Search Content
```bash
grep -r "EntityService" specs/
grep -r "TODO" implementation/src/
```

### Count Lines
```bash
wc -l specs/use-cases/*.md
find implementation -name "*.py" | xargs wc -l
```

### Tree View
```bash
tree -L 2 specs/
tree -L 3 -I '__pycache__|*.pyc'
```

---

## Python Environment

### Setup
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Run Application
```bash
python -m src.main
python implementation/src/app.py
```

---

## Documentation Commands

### Generate Docs
```bash
sphinx-build -b html docs/ docs/_build/
mkdocs build
```

### View Docs Locally
```bash
python -m http.server 8000 --directory docs/_build/
open http://localhost:8000
```

---

## Quick Reference Cards

For more details, see these quick reference files:

- **`quick-ref/session-start.md`** - Session start checklist
- **`quick-ref/tdd-cycle.md`** - Test-driven development cycle
- **`quick-ref/git.md`** - Complete git workflow
- **`quick-ref/services.md`** - Service patterns and FAQs

---

## Mnemonics

### The 12 Rules (First Letter)
**S**pecs, **T**ests, **I**ncremental, **R**esearch, (Two-Level) **P**lanning, **N**o Shortcuts, (Technical) **D**ecisions, **B**DD, (Code) **Q**uality, **S**ession Discipline, **G**it Workflow, (Mandatory) **R**efactoring

**STIR PDNBQSGR** (Not catchy, just read the rules!)

### TDD Cycle
**R**ed → **G**reen → **R**efactor (RGB like colors)

### Git Workflow
**B**ranch → **T**est → **I**mplement → **C**ommit → **M**erge (BTICM)

---

**Quick Reference Version**: 1.0
**Framework**: Claude Development Framework v2.1
**Last Updated**: 2025-10-01
