# Framework Gap Analysis - Agent Coverage vs Features

**Date**: 2025-10-01
**Version**: v2.1
**Purpose**: Identify where new agents would add value to the framework

---

## Executive Summary

**Current State**: 6 service-oriented agents covering service lifecycle + 1 Tier 1 agent implemented
**Finding**: **Major gaps** in 8 out of 12 framework rules and 7 out of 9 session phases
**Recommendation**: 12-15 new agents needed for comprehensive coverage
**Priority**: 6 high-priority agents address 80% of manual effort
**Progress**: ✅ 1/6 Tier 1 agents complete (test-writer)

---

## Part 1: Framework Feature Inventory

### The 12 Development Rules (Coverage Analysis)

| Rule | Description | Manual Effort | Agent Coverage | Gap |
|------|-------------|---------------|----------------|-----|
| **#1** | Specifications Are Law | HIGH | ❌ None | **CRITICAL** - No spec writing/validation |
| **#2** | Tests Define Correctness | HIGH | ✅ test-writer | Partial - Test generation automated |
| **#3** | Incremental Above All | MEDIUM | ❌ None | **HIGH** - No iteration planning automation |
| **#4** | Research Informs Implementation | MEDIUM | ❌ None | **MEDIUM** - No research organization automation |
| **#5** | Two-Level Planning | HIGH | ❌ None | **HIGH** - No planning assistance |
| **#6** | No Shortcuts | LOW | ❌ None | **MEDIUM** - No TODO/tech-debt detection |
| **#7** | Technical Decisions Are Binding | MEDIUM | ❌ None | **HIGH** - No ADR creation/compliance checking |
| **#8** | BDD for User-Facing Features | HIGH | ❌ None | **CRITICAL** - No Gherkin writing/validation |
| **#9** | Code Quality Standards | HIGH | ❌ None | **CRITICAL** - No quality checking automation |
| **#10** | Session Discipline | LOW | ❌ None | **LOW** - Mostly protocol, hard to automate |
| **#11** | Git Workflow Discipline | MEDIUM | ❌ None | **MEDIUM** - No git automation |
| **#12** | Mandatory Refactoring | HIGH | ❌ None | **CRITICAL** - No refactoring analysis |

**Service-Oriented** (Rule #1 Extension):
- ✅ **COVERED** by 6 existing agents

**Coverage**: 1/12 rules (8.3%) - **Service architecture only**

---

### 9-Phase Session Checklist (Coverage Analysis)

| Phase | Activities | Manual Effort | Agent Coverage | Gap |
|-------|-----------|---------------|----------------|-----|
| **1. Orientation** | Read files, git status, context check | LOW | ❌ None | Context management could be semi-automated |
| **2. Research** | Find docs, read, document, create ADRs | HIGH | ❌ None | **CRITICAL** - Fully manual |
| **3. Planning** | Create iteration plan, scope check, branch | HIGH | ❌ None | **CRITICAL** - Fully manual |
| **4. Test-First** | Write tests before implementation | HIGH | ❌ None | **CRITICAL** - Fully manual |
| **5. Implement** | Write code, pass tests, add docs | HIGH | ✅ service-* | **PARTIAL** - Only service design |
| **6. Refactor** | Improve quality, run checks | HIGH | ❌ None | **CRITICAL** - Fully manual |
| **7. Validate** | Run all tests, linting, coverage | MEDIUM | ❌ None | **HIGH** - Fully manual |
| **8. Document** | Update plans, session state, learnings | MEDIUM | ❌ None | **MEDIUM** - Could automate summaries |
| **9. Close** | Commit, push, summarize | MEDIUM | ❌ None | **MEDIUM** - Git workflow automation |

**Coverage**: 0.5/9 phases (5.6%) - **Partial coverage of implementation only**

---

### Development Lifecycle (Coverage Analysis)

```
Research → Plan → Specify → Design → Test → Implement → Refactor → Validate → Document → Commit
```

| Stage | Current Coverage | Gap |
|-------|-----------------|-----|
| **Research** | ❌ None | Need research-organizer agent |
| **Plan** | ❌ None | Need iteration-planner agent |
| **Specify** | ❌ None | Need spec-writer, uc-writer agents |
| **Design** | ✅ service-designer, service-extractor | **COVERED** (services only) |
| **Test** | ❌ None | Need test-writer, bdd-scenario-writer agents |
| **Implement** | ✅ (manual with service guidance) | Mostly manual |
| **Refactor** | ❌ None | Need refactoring-analyzer agent |
| **Validate** | ✅ service-optimizer, uc-service-tracer | **PARTIAL** (services only) |
| **Document** | ❌ None | Need doc-generator agent |
| **Commit** | ❌ None | Need git-workflow-helper agent |

**Coverage**: 2.5/10 stages (25%) - **Service design and validation only**

---

## Part 2: Current Agent Coverage (6 Agents)

### Service-Oriented Architecture Agents

| Agent | Focus | Rule Coverage | Phase Coverage | Notes |
|-------|-------|---------------|----------------|-------|
| **service-extractor** | Extract services from UCs | Rule #1 (partial) | Phase 5 (partial) | Scoped to services only |
| **service-designer** | Design Protocol interfaces | Rule #1 (partial) | Phase 5 (partial) | Scoped to services only |
| **service-dependency-analyzer** | Validate dependencies, detect cycles | Rule #1 (partial) | Phase 7 (partial) | Scoped to services only |
| **service-optimizer** | Benchmark implementations | Rule #4 (partial) | Phase 6 (partial) | Scoped to performance only |
| **service-library-finder** | Evaluate external libraries | Rule #4 (partial) | Phase 2 (partial) | Scoped to library research only |
| **uc-service-tracer** | Validate UC-Service traceability | Rule #1 (partial) | Phase 7 (partial) | Scoped to traceability only |

**Strengths**:
- ✅ Comprehensive service lifecycle coverage
- ✅ Strong service design and validation
- ✅ Good traceability checking

**Limitations**:
- ❌ No general UC/spec writing
- ❌ No test generation
- ❌ No code quality checking
- ❌ No refactoring analysis
- ❌ No general planning assistance

---

## Part 3: Gap Identification

### CRITICAL Gaps (High Impact, High Frequency)

#### 1. **Specification Writing** (Rule #1)
**Current**: Fully manual
**Problem**: Most time-consuming activity, no automation
**Need**: Agents to help write UCs, service specs, acceptance criteria

#### 2. **Test Writing** (Rule #2)
**Current**: Fully manual
**Problem**: Every feature needs tests, no assistance
**Need**: Agents for unit tests, BDD scenarios, integration tests

#### 3. **Code Quality Checking** (Rule #9)
**Current**: Manual linting/review
**Problem**: Inconsistent application, easy to miss
**Need**: Agent for type hints, docstrings, complexity analysis

#### 4. **Refactoring Analysis** (Rule #12)
**Current**: Manual checklist
**Problem**: Mandatory but subjective, needs systematic approach
**Need**: Agent to analyze code smells, suggest improvements

#### 5. **BDD Scenario Validation** (Rule #8)
**Current**: Manual Gherkin writing
**Problem**: Every UC needs scenarios, alignment with criteria
**Need**: Agent to generate/validate Gherkin scenarios

---

### HIGH Gaps (Medium-High Impact, Medium Frequency)

#### 6. **ADR Creation & Compliance** (Rule #7)
**Current**: Manual ADR writing, manual compliance checking
**Problem**: Technical decisions drift without enforcement
**Need**: Agent for ADR generation, compliance verification

#### 7. **Iteration Planning** (Rule #3, #5)
**Current**: Manual scope estimation, task breakdown
**Problem**: Planning takes significant time, scope creep common
**Need**: Agent to break down work, estimate time, validate scope

#### 8. **Use Case Writing** (Rule #1)
**Current**: Fully manual
**Problem**: Foundation of all work, needs consistency
**Need**: Agent to help write well-structured UCs

---

### MEDIUM Gaps (Medium Impact, Low-Medium Frequency)

#### 9. **Git Workflow Automation** (Rule #11)
**Current**: Manual branching, manual commit messages
**Problem**: Repetitive, format errors common
**Need**: Agent for branch creation, commit message generation

#### 10. **Documentation Generation** (Phase 8)
**Current**: Manual session state, manual summaries
**Problem**: Tedious documentation work
**Need**: Agent to generate session summaries, update state

#### 11. **Research Organization** (Rule #4)
**Current**: Manual research, manual ADR creation
**Problem**: Research scattered, not systematically captured
**Need**: Agent to organize research, suggest ADRs (already exists as guide, could be agent)

#### 12. **Technical Debt Detection** (Rule #6)
**Current**: Manual code review
**Problem**: TODOs slip through, technical debt accumulates
**Need**: Agent to detect TODOs, skipped error handling, incomplete code

---

### LOW Gaps (Lower Impact or Hard to Automate)

#### 13. **Context Management** (Rule #10, Phase 1)
**Current**: Manual file loading, manual compaction
**Problem**: Context degradation in long sessions
**Difficulty**: Requires Claude's self-awareness, hard to delegate to agent

#### 14. **Session Protocol** (Rule #10)
**Current**: Manual checklist following
**Problem**: Easy to forget steps
**Difficulty**: Enforcement is protocol, not task-based

---

## Part 4: Recommended New Agents (Prioritized)

### Tier 1: CRITICAL Priority (6 agents) - Address 80% of manual effort

#### 1. **uc-writer** 🔴 CRITICAL
**Purpose**: Help write well-structured use case specifications
**Triggers**: "create use case", "write UC", UC file creation
**Input**: User requirements, business problem description
**Process**:
1. Interview user for UC details (actor, goal, preconditions, etc.)
2. Extract acceptance criteria
3. Identify required services
4. Generate UC specification from template
5. Validate completeness (all sections filled)
**Output**: Complete UC specification file
**Tools**: [Read, Write, WebSearch (for domain research)]
**Model**: opus (complex reasoning for requirements gathering)
**Impact**: HIGH - UCs are foundation of all work
**Frequency**: HIGH - Every new feature starts with UC

---

#### 2. **test-writer** ✅ IMPLEMENTED
**Purpose**: Generate unit tests from specifications and implementation
**Triggers**: "write tests", "create tests", MUST BE USED before implementation
**Input**: Specification file, implementation signatures (if exist)
**Process**:
1. Parse specification for requirements
2. Identify test scenarios (happy path, edge cases, errors)
3. Generate test structure using pytest/unittest
4. Create fixtures and mocks as needed
5. Ensure tests fail initially (RED state)
6. Add docstrings with spec references
**Output**: Complete test file with failing tests
**Tools**: [Read, Write, Bash, Glob, Grep]
**Model**: opus (complex test scenario design)
**Impact**: CRITICAL - Rule #2 enforcement, every feature needs tests
**Frequency**: VERY HIGH - Every implementation task
**Status**: ✅ Implemented in `.claude/subagents/test-writer.md` (v1.0)

---

#### 3. **bdd-scenario-writer** 🔴 CRITICAL
**Purpose**: Generate Gherkin scenarios from UC acceptance criteria
**Triggers**: "write BDD scenarios", "create Gherkin", UC has acceptance criteria
**Input**: Use case specification with acceptance criteria
**Process**:
1. Extract acceptance criteria from UC
2. Convert each criterion to Given-When-Then scenario
3. Identify scenario outline opportunities (examples table)
4. Generate .feature file with all scenarios
5. Validate scenario completeness vs. acceptance criteria
**Output**: Complete .feature file with Gherkin scenarios
**Tools**: [Read, Write]
**Model**: sonnet (structured transformation)
**Impact**: HIGH - Rule #8 requirement, every UC needs BDD
**Frequency**: HIGH - Every user-facing feature

---

#### 4. **code-quality-checker** 🔴 CRITICAL
**Purpose**: Validate code quality standards before commit
**Triggers**: MUST BE USED before commit, "check code quality"
**Input**: Implementation files (Python)
**Process**:
1. Check type hints (all params, all returns)
2. Check docstrings (all functions, spec references)
3. Check complexity (cyclomatic complexity <10)
4. Check SRP violations (functions >50 lines)
5. Run pylint/flake8/mypy
6. Generate quality report with violations
**Output**: Quality report with pass/fail and specific violations
**Tools**: [Read, Bash (run linters)]
**Model**: sonnet (rule-based checking)
**Impact**: CRITICAL - Rule #9 enforcement
**Frequency**: VERY HIGH - Every implementation

---

#### 5. **refactoring-analyzer** 🔴 CRITICAL
**Purpose**: Analyze code for refactoring opportunities after GREEN phase
**Triggers**: MUST BE USED after implementation passes, "analyze refactoring"
**Input**: Implementation files with passing tests
**Process**:
1. Detect code duplication (>3 lines repeated)
2. Identify complex functions (complexity >10, >30 lines)
3. Find magic numbers/strings (extract to constants)
4. Detect poor naming (single letters, abbreviations)
5. Identify missing abstractions (similar patterns)
6. Generate prioritized refactoring recommendations
**Output**: Refactoring report with specific suggestions and code examples
**Tools**: [Read, Bash (run complexity analyzers)]
**Model**: opus (pattern recognition, design suggestions)
**Impact**: CRITICAL - Rule #12 enforcement (mandatory refactoring)
**Frequency**: VERY HIGH - After every GREEN phase

---

#### 6. **adr-manager** 🔴 HIGH
**Purpose**: Create ADRs for technical decisions and check compliance
**Triggers**: "create ADR", "check ADR compliance", major technical decision made
**Input**: Technical decision description OR implementation to check
**Process**:
- **Creation Mode**:
  1. Interview user for decision context
  2. Document options considered
  3. Record decision rationale
  4. Note consequences and trade-offs
  5. Generate ADR file with unique ID
- **Compliance Mode**:
  1. Read all existing ADRs
  2. Parse current implementation
  3. Check for ADR violations
  4. Report violations with evidence (file:line)
**Output**: ADR file OR compliance report
**Tools**: [Read, Write, Grep, Glob]
**Model**: opus (complex reasoning for decisions)
**Impact**: HIGH - Rule #7 enforcement, prevents architectural drift
**Frequency**: MEDIUM - Major decisions, periodic compliance checks

---

### Tier 2: HIGH Priority (4 agents) - Address next 15% of effort

#### 7. **iteration-planner** 🟠 HIGH
**Purpose**: Help plan iterations with scope validation
**Triggers**: "plan iteration", "create iteration", start of new work
**Input**: Use case or feature description
**Process**:
1. Break down UC into implementation tasks
2. Estimate time for each task (aim for 1-3 hours total)
3. Identify test scenarios needed
4. List specifications required
5. Check scope (warn if >3 hours)
6. Generate iteration plan file
**Output**: Iteration plan with tasks, tests, time estimate
**Tools**: [Read, Write]
**Model**: opus (complex planning and estimation)
**Impact**: HIGH - Rule #3 & #5 enforcement
**Frequency**: MEDIUM - Every new iteration/UC

---

#### 8. **spec-validator** 🟠 HIGH
**Purpose**: Validate specification completeness and consistency
**Triggers**: "validate spec", "check specification", spec file modified
**Input**: Specification file (UC or service spec)
**Process**:
1. Check all required sections present
2. Validate acceptance criteria are testable
3. Check service references (specs exist)
4. Verify traceability (UC ↔ Service references consistent)
5. Check for ambiguous language ("should", "might", etc.)
6. Generate validation report
**Output**: Validation report with issues and recommendations
**Tools**: [Read, Grep, Glob]
**Model**: sonnet (rule-based validation)
**Impact**: HIGH - Prevents downstream issues from bad specs
**Frequency**: MEDIUM - After spec creation/modification

---

#### 9. **git-workflow-helper** 🟠 MEDIUM
**Purpose**: Automate git workflow (branching, commit messages)
**Triggers**: "create branch", "generate commit message", start/end of work
**Input**: Current git state, work completed description
**Process**:
- **Branch Creation**:
  1. Determine branch type (iteration-XXX, uc-XXX, fix-XXX)
  2. Generate branch name from UC/iteration ID
  3. Check if on main, pull latest
  4. Create and switch to branch
- **Commit Message**:
  1. Analyze staged changes
  2. Determine commit type (feat/fix/refactor/etc.)
  3. Extract spec references from code
  4. Count tests passing
  5. Generate formatted commit message
**Output**: Branch created OR commit message
**Tools**: [Bash (git commands), Read]
**Model**: sonnet (structured text generation)
**Impact**: MEDIUM - Rule #11 enforcement, saves time
**Frequency**: MEDIUM-HIGH - Every iteration start/end

---

#### 10. **session-summarizer** 🟠 MEDIUM
**Purpose**: Generate session state and summaries automatically
**Triggers**: "end session", "generate summary", session end
**Input**: Conversation history, files modified, git commits
**Process**:
1. Summarize work completed
2. Extract key decisions made
3. Identify blockers encountered
4. List files modified
5. Note next steps
6. Generate session-state.md
**Output**: session-state.md file for next session pickup
**Tools**: [Read, Write, Bash (git log)]
**Model**: sonnet (summarization)
**Impact**: MEDIUM - Phase 8 automation, improves continuity
**Frequency**: HIGH - Every session end

---

### Tier 3: MEDIUM Priority (2 agents) - Nice-to-have

#### 11. **tech-debt-detector** 🟡 MEDIUM
**Purpose**: Detect technical debt (TODOs, skipped error handling)
**Triggers**: "check tech debt", before commit
**Input**: Codebase files
**Process**:
1. Search for TODO/FIXME comments
2. Detect functions without error handling
3. Find missing type hints
4. Identify print() debugging statements
5. Check for broad exception catches (except Exception)
6. Generate tech debt report
**Output**: Tech debt report with file:line references
**Tools**: [Grep, Glob, Read]
**Model**: sonnet (pattern matching)
**Impact**: MEDIUM - Rule #6 enforcement
**Frequency**: MEDIUM - Before commits, periodic audits

---

#### 12. **doc-generator** 🟡 LOW-MEDIUM
**Purpose**: Generate API documentation, README files automatically
**Triggers**: "generate docs", service/module completed
**Input**: Implementation files with docstrings
**Process**:
1. Extract docstrings from code
2. Generate API reference (functions, classes)
3. Create usage examples
4. Build table of contents
5. Generate README or API.md
**Output**: Documentation markdown files
**Tools**: [Read, Write, Bash (run doc generators)]
**Model**: sonnet (structured doc generation)
**Impact**: LOW-MEDIUM - Helps with documentation
**Frequency**: LOW - Post-implementation

---

## Part 5: Coverage Improvement Projection

### With Tier 1 Agents (6 new agents)

**12 Rules Coverage**:
| Rule | Before | After T1 | Improvement |
|------|--------|----------|-------------|
| #1 | 8% | 50% | +42% (uc-writer, spec-validator) |
| #2 | 0% | 90% | +90% (test-writer, code-quality-checker) |
| #8 | 0% | 90% | +90% (bdd-scenario-writer) |
| #9 | 0% | 90% | +90% (code-quality-checker) |
| #12 | 0% | 90% | +90% (refactoring-analyzer) |
| #7 | 0% | 70% | +70% (adr-manager) |

**Overall**: 8% → 48% (+40 percentage points)

---

### With All Tiers (12 new agents)

**12 Rules Coverage**:
- Rule #1-12: ~60-70% coverage
- **Overall**: 8% → 65% (+57 percentage points)

**9 Phases Coverage**:
- Phase 1-9: ~50-60% coverage
- **Overall**: 5.6% → 58% (+52 percentage points)

---

## Part 6: Implementation Roadmap

### Phase 1: Foundation (Tier 1 - 6 agents)
**Goal**: Cover critical manual effort (80%)
**Time**: 2-3 weeks
**Progress**: 1/6 complete (16.7%)
**Agents**:
1. ✅ test-writer (COMPLETE - v1.0)
2. ⏳ bdd-scenario-writer (PENDING)
3. ⏳ code-quality-checker (PENDING)
4. ⏳ refactoring-analyzer (PENDING)
5. ⏳ uc-writer (PENDING)
6. ⏳ adr-manager (PENDING)

**Validation**: Test on real project, measure time savings

---

### Phase 2: Enhancement (Tier 2 - 4 agents)
**Goal**: Cover planning and workflow automation (15%)
**Time**: 1-2 weeks
**Agents**:
7. iteration-planner
8. spec-validator
9. git-workflow-helper
10. session-summarizer

**Validation**: Gather user feedback, refine

---

### Phase 3: Polish (Tier 3 - 2 agents)
**Goal**: Nice-to-have automation (5%)
**Time**: 1 week
**Agents**:
11. tech-debt-detector
12. doc-generator

**Validation**: Final integration testing

---

## Part 7: Success Metrics

### Quantitative Metrics
- **Coverage**: 8% → 65% (8x improvement)
- **Time Savings**: Estimate 40-60% reduction in manual effort
- **Quality**: 90% automated enforcement of Rules #2, #8, #9, #12

### Qualitative Metrics
- User no longer needs to manually write tests
- Refactoring becomes systematic, not ad-hoc
- ADR compliance is enforced, not hoped for
- BDD scenarios always match acceptance criteria

---

## Conclusion

**Finding**: Current 6 agents cover only **8% of framework features** (service architecture only)

**Recommendation**: Add **12 new agents** in 3 tiers to achieve **65% coverage**

**Priority**: Start with **Tier 1 (6 agents)** to address **80% of manual effort**:
1. ✅ test-writer (COMPLETE - v1.0)
2. ⏳ bdd-scenario-writer (NEXT)
3. ⏳ code-quality-checker
4. ⏳ refactoring-analyzer
5. ⏳ uc-writer
6. ⏳ adr-manager

**Impact**: Transform framework from service-focused tooling to comprehensive development automation

**Progress**: 1/6 Tier 1 agents implemented (16.7% complete)

---

**Document Version**: 1.1
**Date**: 2025-10-01
**Last Updated**: 2025-10-01 (test-writer implemented)
**Next Steps**: Implement bdd-scenario-writer (Tier 1 #2)
