# Large Codebase Context Management

**Purpose**: Advanced strategies for using the framework with 50K+ line codebases

**Last Updated**: 2025-09-30

---

## The Challenge

**Problem**: Claude's context window (200K tokens) can't hold an entire large codebase.

**Reality**:
- 50K lines of code ≈ 150K tokens
- Specifications ≈ 20K tokens
- Conversation history ≈ 30K tokens
- **Total**: 200K tokens (at capacity)

**Solution**: Hierarchical context loading with intelligent prioritization.

---

## Strategy 1: Modular Architecture

### Principle
Structure code so Claude only needs to see relevant modules.

### Implementation

**Directory Structure**:
```
src/
├── core/           # Shared models (always load)
├── auth/           # Auth module (load when working on auth)
├── api/            # API layer (load when working on endpoints)
├── processing/     # Processing module (load when working on processing)
└── storage/        # Storage module (load when working on storage)
```

**Context Loading Rules**:
```markdown
## Working on auth feature:
LOAD:
- .claude/ (critical files)
- specs/use-cases/UC-auth*.md
- src/core/ (dependencies)
- src/auth/ (current work)
- tests/unit/auth/
- tests/integration/auth/

SKIP:
- src/processing/
- src/storage/
- src/api/ (unless integration needed)
```

### Benefits
- Claude sees 20% of codebase, not 100%
- Faster context loading
- More room for specifications

---

## Strategy 2: Context Layers

### Three-Tier Loading Strategy

#### Tier 1: Skeleton (Always Load - ~10K tokens)
```
.claude/CLAUDE.md
.claude/development-rules.md
.claude/technical-decisions.md (summary only)
planning/current-iteration.md
specs/00-project-overview.md (executive summary)
src/core/models.py (data models only)
```

**Purpose**: Orientation - Where am I? What am I doing?

#### Tier 2: Current Work (Load on Demand - ~50K tokens)
```
specs/use-cases/UC-current.md
specs/services/SVC-current.md
planning/iterations/iteration-current.md
src/[current_module]/
tests/[current_module]/
```

**Purpose**: Implementation - What am I building right now?

#### Tier 3: Reference (Load When Needed - ~40K tokens)
```
research/learnings/[relevant-topic].md
src/[related_module]/ (if integrating)
specs/architecture/[relevant-doc].md
```

**Purpose**: Understanding - How does this fit together?

### Context Loading Protocol

**Session Start**:
```
User: "Initialize session for UC-015 iteration 023"

Claude loads:
1. Tier 1 (skeleton)
2. UC-015 spec
3. Iteration 023 plan
4. Relevant module code

Reports: "Context: 35% (70K tokens). Ready."
```

**Mid-Session**:
```
User: "Need to integrate with storage module"

Claude loads:
- src/storage/storage_interface.py (interface only)
- specs/services/SVC-storage.md (contract)

Reports: "Context: 45% (90K tokens). Storage interface loaded."
```

---

## Strategy 3: Specification Summaries

### Problem
Full specifications can be 2K-5K tokens each. 10 specs = 50K tokens.

### Solution
Create specification summaries.

**Full Spec** (`specs/use-cases/UC-015-full.md`): 3,000 tokens
```markdown
# UC-015: Entity Extraction
[Detailed 50-section specification...]
```

**Summary** (`specs/use-cases/UC-015-summary.md`): 300 tokens
```markdown
# UC-015: Entity Extraction (Summary)

**Purpose**: Extract named entities from text

**Input**: Text string
**Output**: List of entities with type, value, confidence

**Key Rules**:
- Confidence threshold: 0.7
- Supported types: PERSON, ORG, LOCATION, DATE
- Max 1000 entities per document

**Integration Points**:
- Requires: Chunking service (UC-003)
- Provides: Entities to graph service (UC-005)

**See**: specs/use-cases/UC-015-full.md for complete details
```

### When to Use
- **Summary**: Initial planning, context loading, general understanding
- **Full Spec**: Detailed implementation, edge cases, validation rules

### Creating Summaries

Add to specs after writing full spec:

```bash
# scripts/create-spec-summary.sh
#!/bin/bash
# Extract key sections from full spec to create summary

UC_FILE=$1
SUMMARY_FILE="${UC_FILE%.md}-summary.md"

{
    grep "^# UC-" "$UC_FILE"
    echo
    grep "^##Purpose" -A 2 "$UC_FILE"
    echo
    grep "^## Key Rules" -A 5 "$UC_FILE"
    echo
    echo "**See**: $UC_FILE for complete details"
} > "$SUMMARY_FILE"

echo "Created summary: $SUMMARY_FILE"
```

---

## Strategy 4: Code Reference System

### Problem
Loading 1,000-line file = 3,000 tokens. Loading 10 files = 30,000 tokens.

### Solution
Reference code by location instead of loading entire files.

**Instead of loading full file**:
```python
# src/services/extraction/entity_extractor.py (1,000 lines)
[entire file content]
```

**Use references**:
```markdown
## Current Implementation

**File**: src/services/extraction/entity_extractor.py

**Key Components**:
- Lines 45-78: EntityExtractor.extract() method
- Lines 120-145: Confidence filtering logic
- Lines 200-250: Entity deduplication

**Relevant Tests**:
- tests/unit/services/test_entity_extractor.py:42 (test_extract_with_confidence)

**To see implementation**: Read src/services/extraction/entity_extractor.py:45-78
```

### Selective Loading

**Load only what's needed**:
```
User: "Show me the confidence filtering logic"

Claude reads:
- src/services/extraction/entity_extractor.py (lines 120-145 only)

Not loading:
- Rest of file
- Related but not immediately relevant code
```

---

## Strategy 5: Session State Compression

### Problem
Long sessions accumulate conversation history (50K+ tokens).

### Solution
Periodic summarization.

**Every 50 interactions**:
```markdown
## Session History Summary

**Duration**: 2 hours
**Work Completed**:
- Iteration 020: Complete (entity extraction)
- Iteration 021: Complete (confidence filtering)
- Iteration 022: 60% complete (deduplication)

**Key Decisions**:
- ADR-025: Use spaCy for NER
- Confidence threshold: 0.7 (from research)

**Current State**:
- 23 tests, all passing
- Working on deduplication algorithm

**Next**: Complete iteration 022

[Full conversation archived to planning/session-archive-2025-09-30.md]
```

**Benefits**:
- Conversation history: 50K tokens → 500 tokens
- Frees 49.5K tokens for other files
- Preserves continuity

---

## Strategy 6: Dynamic Module Loading

### Use Case
"I'm working on API module, but need to understand how storage works."

### Implementation

**Create**: `.claude/module-map.md`

```markdown
# Module Dependency Map

## Core Module
**Files**: src/core/
**Purpose**: Shared data models
**Loaded**: Always (TIER 1)

## Auth Module
**Files**: src/auth/
**Purpose**: Authentication & authorization
**Depends On**: core
**Interface**: src/auth/auth_interface.py (200 lines)
**Load when**: Working on auth OR integrating with auth

## API Module
**Files**: src/api/
**Purpose**: REST API endpoints
**Depends On**: core, auth, processing, storage
**Interface**: src/api/endpoints/ (FastAPI routers)
**Load when**: Working on API OR adding endpoints

## Processing Module
**Files**: src/processing/
**Purpose**: Document processing pipeline
**Depends On**: core, storage
**Interface**: src/processing/processor_interface.py (150 lines)
**Load when**: Working on processing OR integrating with pipeline

## Storage Module
**Files**: src/storage/
**Purpose**: Database and persistence
**Depends On**: core
**Interface**: src/storage/storage_interface.py (180 lines)
**Load when**: Working on storage OR doing data operations
```

**Claude Protocol**:
```
When user says: "I need to integrate with storage"

Claude:
1. Checks .claude/module-map.md
2. Loads storage interface only (180 lines, not full module)
3. Reports: "Storage interface loaded. Full module available if needed."
```

---

## Strategy 7: Test Reference, Not Full Tests

### Problem
Test files can be 500-1000 lines. Loading 10 test files = 30K tokens.

### Solution
Reference tests, don't load them unless implementing.

**Test Summary** (`tests/unit/services/test_summary.md`):

```markdown
# Test Summary: Entity Extraction Service

**File**: tests/unit/services/test_entity_extractor.py
**Tests**: 42 total (all passing)

**Coverage**:
- Entity extraction: 15 tests
- Confidence filtering: 8 tests
- Deduplication: 12 tests
- Error handling: 7 tests

**Key Tests**:
- test_extract_person_entities (line 42)
- test_confidence_threshold_filtering (line 156)
- test_deduplicate_identical_entities (line 298)

**Load full file when**: Writing new tests, debugging failures
```

---

## Strategy 8: Documentation Generation

### Problem
Documentation adds to codebase size.

### Solution
Generate docs from docstrings. Keep only source.

```bash
# Generate API docs from docstrings
sphinx-apidoc -o docs/api src/
sphinx-build docs/ docs/_build/

# Result: Documentation lives outside codebase
# Claude reads source docstrings, not generated docs
```

---

## Complete Large Codebase Workflow

### Session 1: Initial Context (Day 1, Morning)
```
User: "Initialize for UC-050"

Claude loads:
1. Tier 1: Skeleton (10K tokens)
2. UC-050 spec summary (500 tokens)
3. Module map (1K tokens)
4. Current module interface only (5K tokens)

Context: 20% (40K tokens)
Ready to work.
```

### Session 2: Deep Dive (Day 1, Afternoon)
```
User: "Implement iteration 105"

Claude loads (additional):
1. Iteration 105 plan (2K tokens)
2. Full UC-050 spec (4K tokens)
3. Current module implementation (10K tokens)
4. Related tests (8K tokens)

Context: 45% (90K tokens)
Implementing...
```

### Session 3: Integration (Day 2)
```
User: "Integrate with storage"

Claude loads (additional):
1. Storage interface (5K tokens)
2. SVC-storage spec summary (1K tokens)
3. Integration tests (3K tokens)

Context: 55% (110K tokens)
Integration work...
```

### Session 4: Maintenance (Day 2, End)
```
User: "Context check"

Claude: "Context 72% (144K tokens). Recommend compaction."

User: "Compact"

Claude:
1. Summarizes session history (50K → 1K tokens)
2. Archives completed iteration plans
3. Reloads TIER 1 files

Context: 48% (96K tokens)
Healthy, ready to continue.
```

---

## Quick Reference

| Codebase Size | Strategy |
|---------------|----------|
| < 10K lines | Load everything, no special handling |
| 10K-50K lines | Use Tier 1-2 loading, summarize old sessions |
| 50K-100K lines | Add spec summaries, code references |
| 100K+ lines | Full strategy: modules, summaries, dynamic loading |

---

## Checklist for Large Codebases

- [ ] Modular directory structure
- [ ] `.claude/module-map.md` created
- [ ] Specification summaries for all UCs
- [ ] Test summary documents
- [ ] Code reference system in place
- [ ] Session state compression protocol
- [ ] Context checks every 20 interactions
- [ ] Compaction at 75% usage

---

**Document Version**: 1.0
**Part of**: Claude Development Framework
**See also**: `.claude/CLAUDE.md` (Context Window Management Protocol)