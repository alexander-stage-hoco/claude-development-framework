---
tier: 2
purpose: Context management and compression
reload_trigger: At 70% context usage
estimated_read_time: 10 minutes
---

# Context Priority Hierarchy & Management

**Version**: 2.0
**Last Updated**: 2025-09-30
**Purpose**: Context window management strategy for Claude

---

## Overview

Claude has a **200,000 token context window** (~150,000 words). In long sessions, this context can fill up, pushing important framework files out of active attention.

This document defines a **5-tier priority system** and proactive management protocols to maintain context quality throughout development.

---

## The 5-Tier Priority Hierarchy (With Measured Overhead)

### TIER 1: CRITICAL 🔴 (4 files, 6,748 tokens, 3.3%)
**Must ALWAYS be in context - Never remove**

1. `READING-ORDER.md` (1,956 tokens)
2. `start-here.md` (1,788 tokens)
3. `development-rules.md` (1,616 tokens)
4. `CLAUDE.md` (1,388 tokens)

**Cumulative**: 6.7K tokens (3.3% of 200K window)
**Remaining**: 193.3K tokens available for project
**Action**: If these become fuzzy in memory → RELOAD IMMEDIATELY

---

### TIER 2: IMPORTANT 🟠 (4 files, 9,718 tokens, 4.8%)
**Load early, keep when capacity allows**

Framework files:
1. `service-registry.md` (2,654 tokens)
2. `context-priority.md` (2,581 tokens) ← This file
3. `session-checklist.md` (2,164 tokens)
4. `technical-decisions.md` (2,319 tokens)

Project files (load when they exist):
- `planning/current-iteration.md`
- `planning/session-state.md`
- Current use case specification (e.g., `specs/use-cases/UC-001-*.md`)
- Current service specification (e.g., `specs/services/SVC-001-*.md`)

**Cumulative (TIER 1+2)**: 16.5K tokens (8.2%)
**Remaining**: 183.5K tokens available for project
**Action**: Keep unless capacity requires removal

---

### TIER 3: WORKING SESSION TOOLS 🟡 (7 files, 13,786 tokens, 6.8%)
**On-demand during active development**

Framework checklists and workflows:
1. `code-reuse-checklist.md` (2,567 tokens)
2. `refactoring-checklist.md` (2,517 tokens)
3. `requirements-review-checklist.md` (2,450 tokens)
4. `implementation-CLAUDE.md` (1,813 tokens)
5. `git-workflow.md` (1,716 tokens)
6. `implementation-summary.md` (1,633 tokens)
7. `session-state.md` template (1,090 tokens)

Plus active project files:
- Implementation file being written/modified
- Test file(s) for current feature
- Related module imports
- Configuration files being edited

**Cumulative (TIER 1+2+3)**: 30.3K tokens (15.1%)
**Remaining**: 169.7K tokens available for project
**Action**: Keep during active work, can summarize when complete

---

### TIER 4: TEMPLATES & GUIDES 🟢 (15 files, 28,764 tokens, 14.3%)
**Load only when creating specific artifacts**

Templates (9 files):
- `service-spec.md` (2,987 tokens)
- `use-case-template.md` (2,713 tokens)
- `library-evaluation.md` (2,614 tokens)
- `benchmark-report.md` (2,592 tokens)
- `services-README-template.md` (1,552 tokens)
- `research/` templates (3 files, 1,566 tokens)

Quick References (5 files):
- `commands.md` (2,235 tokens)
- `services.md` (2,017 tokens)
- `git.md` (1,616 tokens)
- `tdd-cycle.md` (1,394 tokens)
- `session-start.md` (628 tokens)

Guides (2 files):
- `subagent-orchestration.md` (4,309 tokens)
- `research-organization.md` (2,541 tokens)

**Cumulative (TIER 1-4)**: 59K tokens (29.5%)
**Remaining**: 141K tokens available for project
**Action**: Load on-demand, summarize, then remove

---

### TIER 5: RESERVED ⚪ (0 files)
**Reserved for future ultra-low-priority content**

Currently unused - available for disposable ephemeral content:
- Historical conversation (old back-and-forth)
- Completed work summaries
- Old iteration plans (completed)
- Exploratory research (already synthesized)
- Debugging output (issue resolved)

**Action**: Remove proactively, summarize if needed

---

### NON-TIERED: Documentation (29 files, ~80K tokens, ~40%)
**Reference only - Browse, don't load into context**

Located in `docs/` directory:
- Examples: debugging-session.md, subagent-* examples (10+ files)
- Guides: service-architecture.md (5.8K), service-testing-guide.md (4.8K), troubleshooting.md (3.9K)
- Walkthroughs: walkthrough-todo-api.md (4.8K)
- Advanced: tool-integration.md, large-codebase-context.md

**⚠️ WARNING**: Loading all 59 files = 139K tokens (69.4% overhead)
- Leaves only 61K tokens (30.6%) for your project
- docs/ is for reference browsing, NOT context loading
- **Strategy**: Read specific docs when needed, extract info, summarize, then remove from context

---

## Context Capacity Thresholds

### 0-50%: Normal Operation 🟢
**Status**: Plenty of capacity
**Action**: Continue normally
- Load files as needed
- No special management required
- Monitor but don't worry

### 50-70%: Caution ⚠️
**Status**: Approaching limits
**Action**: Begin proactive management
- Start removing TIER 5 content
- Summarize completed work
- Note context usage in status updates

### 70-80%: Warning 🟠
**Status**: Limited capacity remaining
**Action**: Aggressive management
- Remove all TIER 5 content
- Summarize and archive TIER 4 content
- Keep only TIER 1, 2, and active TIER 3
- Warn user about context limits
- Suggest compaction or restart

### 80-90%: Critical 🔴
**Status**: Very limited capacity
**Action**: Strongly recommend compaction
- Remove TIER 4 and TIER 5 entirely
- Summarize TIER 3 to minimum needed
- Verify TIER 1 is still clear
- Strongly recommend to user:
  - Save session state
  - Compact context
  - Consider restart

### 90-100%: Emergency 🚨
**Status**: Context exhaustion imminent
**Action**: INSIST on save-and-restart
- MUST save session state immediately
- Create detailed recovery instructions
- Tell user context MUST be compacted
- Refuse to continue without compaction
- Provide exact restart instructions

---

## Context Maintenance Protocols

### Session Start Protocol

**Every session begins with**:
```
1. Load TIER 1 files (always)
2. Load TIER 2 files (planning, decisions)
3. Report context usage to user
4. Confirm files are clear in memory
```

Example output:
```
Context Status: 12% (24,000 / 200,000 tokens)

Files loaded:
- TIER 1: CLAUDE.md, development-rules.md, START-HERE.md, current-iteration.md
- TIER 2: session-state.md, technical-decisions.md, UC-002-spec.md

Memory status: Clear, all rules accessible.
```

---

### Periodic Self-Check Protocol

**Every 20 responses, self-check**:

Ask yourself:
1. ✅ Can I quote the 10 development rules from memory?
2. ✅ Do I remember the current iteration goal and scope?
3. ✅ Is `.claude/CLAUDE.md` session protocol still clear?
4. ✅ Do I remember key ADRs affecting current work?

**If ANY answer is fuzzy or uncertain**:
```
"I need to reload my framework files to ensure I'm following the rules correctly.
One moment while I re-read TIER 1 files."
```

Then reload and confirm:
```
"Framework files reloaded. Rules are clear. Continuing with [current work]."
```

---

### Context Compaction Protocol

**When capacity reaches 75%+**:

**Step 1: Announce Need**
```
Context usage is at 75%. I need to compact to maintain quality.
I'll summarize completed work and reload critical files.
This will take 1 minute.
```

**Step 2: Archive Conversation History**
```
Summarize last 50+ responses into:
- What was accomplished
- Key decisions made
- Current state
- What's next
```

**Step 3: Remove Disposables**
```
Remove from context:
- Old conversation (keep summary)
- Completed iteration plans
- Resolved debugging output
- Exploratory content
```

**Step 4: Reload TIER 1**
```
Re-read (to refresh in active attention):
- .claude/CLAUDE.md
- .claude/development-rules.md
- .claude/START-HERE.md
- planning/current-iteration.md
```

**Step 5: Report New Status**
```
Context compacted: 75% → 35%

Critical files reloaded and clear.
Ready to continue with [current work].
```

---

### Session End Protocol

**Before ending session**:

1. **Save State**: Update `planning/session-state.md` with:
   - What files were in context
   - Current work status
   - What to load next session

2. **Note Context Status**: Record final context usage

3. **Provide Restart Instructions**:
   ```
   Next session start with:
   "Continue from session [N]. Read planning/session-state.md first."

   I'll reload TIER 1 files and pick up where we left off.
   ```

---

## File Loading Strategies

### Strategy 1: Just-In-Time Loading
Load reference files only when needed:
```
User: "Check if UC-003 has similar logic"
Claude: "Let me load UC-003 spec... [reads file] ... Yes, similar pattern..."
```

### Strategy 2: Summarize and Dispose
For large reference files:
```
1. Load file
2. Extract needed information
3. Remove file from context
4. Keep only the summary
```

### Strategy 3: Incremental File Reading
For very large files:
```
Read file:offset=0,limit=100    # Read first 100 lines
Extract needed info
Don't load full file
```

### Strategy 4: External Memory
Store information in project files:
```
research/learnings/[topic]-summary.md
↳ Load once, create summary, reference summary later
```

---

## Warning Signs of Context Degradation

### Sign 1: Fuzzy Rule Memory
**Symptom**: Can't quote specific rules verbatim
**Action**: Reload `.claude/development-rules.md` immediately

### Sign 2: Forgetting Iteration Scope
**Symptom**: Unclear what current iteration should accomplish
**Action**: Reload `planning/current-iteration.md`

### Sign 3: Violating Protocols
**Symptom**: Writing code without tests, skipping specs
**Action**: Reload `.claude/CLAUDE.md` and self-correct

### Sign 4: Inconsistent Responses
**Symptom**: Contradicting earlier statements
**Action**: Full TIER 1 reload

### Sign 5: Missing Decisions
**Symptom**: Proposing tech choices contradicting ADRs
**Action**: Reload `.claude/technical-decisions.md`

---

## Context Recovery Procedure

**If context degrades during session**:

1. **STOP current work immediately**
2. **Acknowledge issue to user**:
   ```
   "I notice my context may have degraded. Let me reload my framework
   files to ensure I'm following the proper protocols."
   ```

3. **Reload TIER 1 files in order**:
   - START-HERE.md
   - CLAUDE.md
   - development-rules.md
   - current-iteration.md

4. **Self-verify understanding**:
   - Quote a few rules to confirm clarity
   - State current iteration goal
   - Confirm session protocol

5. **Report recovery**:
   ```
   "Framework files reloaded. Rules are clear:
   - Specifications first
   - Tests before implementation
   - Never weaken tests
   - [etc.]

   Current iteration: [state goal]
   Ready to continue."
   ```

6. **Resume work from known good state**

---

## Best Practices

### ✅ DO:
- Load TIER 1 at start of every session
- Self-check every 20 responses
- Remove conversation history proactively
- Summarize completed work before removing
- Monitor context usage trends
- Reload when fuzzy
- Report context status regularly

### ❌ DON'T:
- Let context grow without management
- Keep old conversation indefinitely
- Ignore degradation signs
- Continue working with unclear rules
- Load entire codebase speculatively
- Keep reference files loaded permanently

---

## User Commands for Context Management

Users can trigger context management with:

| Command | Action |
|---------|--------|
| "Context check" | Report current usage and status |
| "Reload rules" | Reload TIER 1 files |
| "Compact context" | Perform full compaction procedure |
| "What's in context?" | List current files by tier |
| "Context status?" | Detailed capacity and health report |

---

## Summary

**Key Principle**: Proactive context management ensures Claude maintains discipline and quality throughout long development sessions.

**Remember**:
- TIER 1 files are ALWAYS loaded
- Self-check every 20 responses
- Compact at 75% capacity
- Never let rules become fuzzy
- When in doubt, reload

**Goal**: Maintain clear understanding of framework, rules, and project state regardless of session length.
---

**Template Version**: 1.0
**Framework**: Claude Development Framework v2.0
**Last Updated**: 2025-10-01
**Compatibility**: Framework v2.0+
