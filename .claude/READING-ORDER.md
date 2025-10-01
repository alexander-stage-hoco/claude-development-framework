---
tier: 1
purpose: Canonical file reading sequence
reload_trigger: When reading order unclear
estimated_read_time: 10 minutes
---

# File Reading Order - Claude Development Framework

**Purpose**: Single source of truth for which files to read and when

**Context**: Framework has 33+ files. This is your roadmap.

---

## Session Start (Read These FIRST)

### TIER 1 (Critical - ALWAYS load)

1. **start-here.md** (5 min)
   - Framework orientation
   - Your role as Claude
   - Why this matters
   - **Location**: `.claude/start-here.md`

2. **CLAUDE.md** (10 min)
   - Session protocols (start/end procedures)
   - Implementation gates
   - Anti-patterns to reject
   - Emergency procedures
   - **Location**: `.claude/CLAUDE.md`

3. **development-rules.md** (15 min)
   - The 12 non-negotiable rules
   - Enforcement actions
   - Quick reference table
   - **Location**: `.claude/development-rules.md`

### TIER 2 (Important - Load early)

4. **planning/current-iteration.md** (2 min)
   - What's being worked on NOW
   - Current focus
   - Next steps

5. **planning/session-state.md** (2 min, if exists)
   - Context from last session
   - Where to resume
   - Work completed summary

6. **specs/00-project-overview.md** (5 min)
   - Project vision
   - Business problem
   - Scope boundaries

**Total Time to Full Context**: ~39 minutes

---

## As-Needed References (Read When Relevant)

### Service Work
7. **service-registry.md** - Service catalog and traceability
8. **quick-ref/services.md** - Service patterns and FAQs
9. **docs/service-architecture.md** - SOA deep dive

### Planning & Decisions
10. **technical-decisions.md** - ADRs (Architecture Decision Records)
11. **session-checklist.md** - Session start/end protocols

### Quality Gates
12. **refactoring-checklist.md** - RED-GREEN-REFACTOR cycle
13. **requirements-review-checklist.md** - Spec review process
14. **code-reuse-checklist.md** - Before writing new code

### Context Management
15. **context-priority.md** - TIER system details and compression protocol
16. **session-state.md** (template) - Session continuity format

### Git Workflow
17. **git-workflow.md** - Branch strategy, commit format, merge process
18. **quick-ref/git.md** - Git command quick reference

### Templates (Use When Creating)
19. **use-case-template.md** - UC specification format
20. **service-spec.md** - Service specification format
21. **benchmark-report.md** - Performance testing results
22. **library-evaluation.md** - Third-party library analysis

---

## Reading Order By Session Type

### First Session
**Read**: 1-3 (TIER 1), then 6 (project overview)

**Purpose**: Understand framework and project vision

**Time**: ~35 minutes

---

### Continuation Session
**Read**: 1-2 (refresh rules), 4-5 (current state), 10 (recent ADRs)

**Purpose**: Resume work from previous session

**Time**: ~15 minutes

---

### Service Extraction Session
**Read**: 1-2 (refresh), 7-8 (service references), 19-20 (UC & service templates)

**Purpose**: Extract services from use cases

**Time**: ~20 minutes

---

### Implementation Session
**Read**: 1-4 (context), 10 (ADRs), 12 (refactoring checklist), 17-18 (git workflow)

**Purpose**: Implement feature with TDD

**Time**: ~25 minutes

---

### Architecture Review Session
**Read**: 1-2 (refresh), 9 (service architecture), 10 (existing ADRs), 13 (review checklist)

**Purpose**: Make architectural decisions

**Time**: ~30 minutes

---

### Refactoring Session
**Read**: 1-2 (refresh), 4 (current work), 12 (refactoring checklist), 14 (code reuse)

**Purpose**: Improve code quality

**Time**: ~20 minutes

---

## Reload Triggers

### At 70% Context Usage
**Action**: Re-read TIER 1 files (1-3)

**Verify**: Can you quote Rule #2?

**Time**: 30 minutes

---

### Every 20 Interactions
**Self-Check**:
- Can I quote the 12 rules?
- Do I remember current iteration details?
- Can I recall recent ADRs?

**If Fuzzy**: Reload TIER 1 (files 1-3)

---

### When Confused About Rules
**Action**: Re-read TIER 1 files (1-3)

**Focus**: development-rules.md for specific rule details

**Time**: 30 minutes

---

### When Confused About Project
**Action**: Re-read TIER 2 files (4-6)

**Focus**: current-iteration.md for immediate focus

**Time**: 10 minutes

---

## Priority System

### TIER 1 (Must Have)
Files 1-3: Critical for framework enforcement
- Load at EVERY session start
- Reload at 70% context
- Never drop from context

### TIER 2 (Important)
Files 4-6: Essential project context
- Load early in session
- Keep in active context
- Reload if dropped

### TIER 3 (Useful)
Files 7-18: Working references
- Load when needed for specific tasks
- OK to drop if context tight
- Quick to reload

### TIER 4 (Optional)
Files 19-22: Templates
- Load only when creating new files
- Can always drop from context
- Templates copied when needed

### TIER 5 (On-Demand)
Subagents, examples, advanced guides
- Load only when explicitly requested
- Drop immediately after use
- Not part of normal workflow

---

## Context Management Strategy

### Session Start (0% Context)
Load TIER 1 → TIER 2 → Current work files

**Target**: 25-30% context usage

---

### Active Work (30-70% Context)
Keep TIER 1-2 loaded, cycle TIER 3-4 as needed

**Monitor**: Check every 20 interactions

---

### Approaching Limit (70-75% Context)
**Warning**: Issue proactive warning to user

**Action**: Prepare for compression

**Keep**: TIER 1 files protected

---

### Critical Threshold (75-80% Context)
**Action**: Compress immediately

**Steps**:
1. Summarize conversation history
2. Archive completed work
3. Unload TIER 3-5 files
4. Reload TIER 1 files (verify enforcement)
5. Resume work

**Target**: Drop to 25-30% context

---

### Emergency (80%+ Context)
**Action**: Stop work, compress now

**Risk**: TIER 1 files may be evicted (framework degradation)

---

## File Dependencies

**start-here.md** references:
- CLAUDE.md
- development-rules.md
- READING-ORDER.md (this file)

**CLAUDE.md** references:
- development-rules.md
- session-checklist.md
- git-workflow.md
- context-priority.md
- READING-ORDER.md (this file)

**development-rules.md** references:
- None (authoritative source)

**Templates** reference:
- Parent specifications
- Other templates (cross-references)

---

## Quick Commands

### Check What's Loaded
```
"What files do you currently have in context?"
"Can you quote Rule #2 from development-rules.md?"
```

### Reload Critical Files
```
"Reload TIER 1 files now"
"Re-read .claude/CLAUDE.md and development-rules.md"
```

### Load Specific File
```
"Read planning/current-iteration.md"
"Load .claude/technical-decisions.md"
```

### Context Check
```
"Context check - what's your usage percentage?"
"Do you have all TIER 1 files loaded?"
```

---

## For New Projects

**First Session Reading Order**:
1. start-here.md (framework orientation)
2. CLAUDE.md (session protocol)
3. development-rules.md (the 12 rules)
4. specs/00-project-overview.md (project vision - usually empty initially)

**After User Interview**:
5. Newly created use case specifications
6. Newly created project overview

**Before Implementation**:
7. technical-decisions.md (ADRs made)
8. service-registry.md (services extracted)
9. current-iteration.md (current focus)

---

## Maintenance Notes

**This File**:
- **Status**: Canonical reading order (single source of truth)
- **Referenced By**: start-here.md, CLAUDE.md
- **Update When**: New critical files added to framework
- **Sync Check**: Quarterly review with framework updates

**Consistency**:
- start-here.md should reference this file, not duplicate
- CLAUDE.md should reference this file, not duplicate
- No other files should define reading order

---

**File Version**: 1.0
**Framework**: Claude Development Framework v2.0
**Last Updated**: 2025-10-01
**Next Review**: 2026-01-01
