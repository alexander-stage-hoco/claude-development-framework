# Agent Library - Claude Development Framework v2.1

**Version**: 2.1
**Last Updated**: 2025-10-02
**Total Agents**: 18 (12 core development + 6 service-oriented)
**Status**: Production-ready

---

## Overview

### What Are Agents?

Agents are specialized automation tools within the Claude Development Framework that handle specific development tasks:
- **Test generation** from specifications
- **Code quality** checking
- **Specification** creation and validation
- **Git workflow** automation
- **Documentation** generation
- **Service architecture** design

Each agent is a focused expert that follows framework rules and produces consistent, high-quality output.

### How Agents Work

**Invocation Methods:**
1. **Trigger Keywords**: Use specific phrases that activate agents
   - "generate tests for UC-001" → `test-writer`
   - "check tech debt" → `tech-debt-detector`
   - "create branch for iteration 2" → `git-workflow-helper`

2. **Direct Request**: Ask Claude to use a specific agent
   - "Use the spec-validator to check UC-003"
   - "Run iteration-planner for this use case"

3. **Proactive**: Some agents activate automatically when appropriate
   - `git-workflow-helper` at session start (Phase 1)
   - `session-summarizer` at session end (Phase 8)

**Agent Execution:**
1. Agent receives input (spec file, code files, user requirements)
2. Agent processes using specialized tools (Read, Grep, Bash, etc.)
3. Agent generates output (tests, documentation, reports, files)
4. User reviews and approves output
5. Agent executes final action (write files, commit, etc.)

### When to Use Agents

**Use Agents For:**
- ✅ Repetitive tasks (test generation, quality checks)
- ✅ Complex analysis (service extraction, dependency analysis)
- ✅ Consistency enforcement (spec validation, code quality)
- ✅ Time-consuming work (documentation generation, refactoring analysis)

**Do NOT Use Agents For:**
- ❌ Simple, one-off tasks
- ❌ Tasks requiring human judgment/creativity
- ❌ Exploratory work without clear specifications

---

## Quick Reference Table

| # | Agent | Tier | Purpose | Triggers | Rules | File |
|---|-------|------|---------|----------|-------|------|
| **Core Development Agents** |
| 1 | test-writer | 1 | Test generation from specs | "write tests", "generate tests" | #2 | test-writer.md |
| 2 | bdd-scenario-writer | 1 | Gherkin scenario generation | "write BDD", "generate scenarios" | #8 | bdd-scenario-writer.md |
| 3 | code-quality-checker | 1 | Quality validation | "check quality", "validate code" | #9 | code-quality-checker.md |
| 4 | refactoring-analyzer | 1 | Refactoring suggestions | "suggest refactoring", "analyze code" | #12 | refactoring-analyzer.md |
| 5 | uc-writer | 1 | Use case spec creation | "create UC", "write use case" | #1 | uc-writer.md |
| 6 | adr-manager | 1 | ADR creation/compliance | "create ADR", "check ADR" | #7 | adr-manager.md |
| 7 | iteration-planner | 2 | Iteration planning | "plan iteration", "break down UC" | #3, #5 | iteration-planner.md |
| 8 | spec-validator | 2 | Spec quality enforcement | "validate spec", "check specification" | #1 | spec-validator.md |
| 9 | git-workflow-helper | 2 | Git automation | "create branch", "generate commit" | #11 | git-workflow-helper.md |
| 10 | session-summarizer | 2 | Session documentation | "end session", "generate summary" | #10 | session-summarizer.md |
| 11 | tech-debt-detector | 3 | Tech debt detection | "check tech debt", "scan for issues" | #6 | tech-debt-detector.md |
| 12 | doc-generator | 3 | API documentation | "generate docs", "create README" | - | doc-generator.md |
| **Service-Oriented Agents** |
| 13 | service-extractor | SO | Extract services from UCs | "extract services" | #1 | service-extractor.md |
| 14 | service-designer | SO | Design service interfaces | "design services" | #1 | service-designer.md |
| 15 | service-dependency-analyzer | SO | Dependency validation | "check dependencies" | #1 | service-dependency-analyzer.md |
| 16 | service-optimizer | SO | Performance optimization | "optimize service" | - | service-optimizer.md |
| 17 | service-library-finder | SO | Library evaluation | "find library", "evaluate libs" | #4 | service-library-finder.md |
| 18 | uc-service-tracer | SO | Traceability validation | "check traceability" | #1 | uc-service-tracer.md |

**Legend:**
- **Tier 1**: CRITICAL (80% effort coverage)
- **Tier 2**: HIGH (15% effort coverage)
- **Tier 3**: MEDIUM (5% effort coverage)
- **SO**: Service-Oriented (specialized)

---

## Tier 1: CRITICAL Agents (6)

### 1. test-writer

**Purpose**: Automated test generation from use case specifications

**Model**: opus (complex test logic generation)
**Tools**: Read, Write, Bash
**File**: `.claude/subagents/test-writer.md`

**When to Use:**
- After creating UC specification
- Before implementation (RED phase of TDD)
- When spec changes require new tests

**Triggers:**
- "generate tests for UC-001"
- "write tests for user registration"
- "create test file for UC-XXX"

**Capabilities:**
- Generates unit tests (pytest, jest, etc.)
- Creates integration tests
- Produces BDD-compatible test structure
- Includes edge cases and error scenarios
- Follows spec acceptance criteria exactly

**Example Usage:**
```
User: "Generate tests for UC-001 user registration"

Agent:
1. Reads specs/use-cases/UC-001-user-registration.md
2. Extracts acceptance criteria
3. Generates test file: tests/test_user_registration.py
4. Creates 12 tests covering happy path, edge cases, errors
5. Shows preview, gets approval, writes file
```

**Output**: Test file with RED tests (all failing, ready for implementation)

**Rule Coverage**: Rule #2 (Tests Define Correctness)

---

### 2. bdd-scenario-writer

**Purpose**: Generate Gherkin (Given-When-Then) BDD scenarios from UC acceptance criteria

**Model**: sonnet (structured scenario generation)
**Tools**: Read, Write
**File**: `.claude/subagents/bdd-scenario-writer.md`

**When to Use:**
- After creating UC specification
- For user-facing features requiring BDD
- When acceptance criteria need executable scenarios

**Triggers:**
- "write BDD scenarios for UC-002"
- "generate Gherkin for authentication"
- "create BDD feature file"

**Capabilities:**
- Converts acceptance criteria to Gherkin format
- Creates Given-When-Then scenarios
- Generates feature files (*.feature)
- Includes scenario outlines for data variations
- Matches UC acceptance criteria 1:1

**Example Usage:**
```
User: "Generate BDD scenarios for UC-002 authentication"

Agent:
1. Reads UC-002 acceptance criteria
2. Converts each criteria to Gherkin scenario
3. Creates features/authentication.feature
4. Generates 8 scenarios (happy path, invalid password, locked account, etc.)
```

**Output**: Gherkin feature file ready for BDD framework (behave, cucumber, etc.)

**Rule Coverage**: Rule #8 (BDD for User-Facing Features)

---

### 3. code-quality-checker

**Purpose**: Validate code quality before commits (type hints, docstrings, complexity, linting)

**Model**: sonnet (rule-based validation)
**Tools**: Read, Bash, Grep
**File**: `.claude/subagents/code-quality-checker.md`

**When to Use:**
- Before committing code (Phase 9)
- During code review
- Before merging to main

**Triggers:**
- "check code quality"
- "validate quality standards"
- "run quality checks on implementation/"

**Capabilities:**
- Checks type hints presence
- Validates docstrings (with Specification: references)
- Runs linting (pylint, eslint, etc.)
- Checks cyclomatic complexity
- Validates function length, parameter count
- Ensures SRP (Single Responsibility Principle)

**Example Usage:**
```
User: "Check code quality before commit"

Agent:
1. Scans implementation/ directory
2. Runs pylint, checks type hints, validates docstrings
3. Finds 3 issues: missing type hints, docstring without spec ref, function too long
4. Reports issues with file:line references
5. Blocks commit until fixed
```

**Output**: Quality report (PASS/FAIL) with actionable fixes

**Rule Coverage**: Rule #9 (Code Quality Standards)

---

### 4. refactoring-analyzer

**Purpose**: Suggest refactorings after GREEN phase (mandatory REFACTOR step)

**Model**: opus (complex code analysis)
**Tools**: Read, Grep, Glob
**File**: `.claude/subagents/refactoring-analyzer.md`

**When to Use:**
- After implementation passes tests (GREEN → REFACTOR)
- During code review
- Before finalizing feature

**Triggers:**
- "suggest refactoring for user_service.py"
- "analyze code for refactoring"
- "what refactorings are needed?"

**Capabilities:**
- Detects code duplication
- Identifies complex functions (>20 lines, >10 complexity)
- Suggests function extraction
- Recommends design patterns
- Finds magic numbers/strings
- Checks naming quality

**Example Usage:**
```
User: "Suggest refactoring for implementation/auth/user_service.py"

Agent:
1. Reads user_service.py
2. Analyzes code structure
3. Finds: password validation duplicated 3 times, function too complex
4. Suggests: Extract _validate_password helper, split register_user into 3 functions
5. Provides refactored code example
```

**Output**: Refactoring report with prioritized suggestions

**Rule Coverage**: Rule #12 (Mandatory Refactoring)

---

### 5. uc-writer

**Purpose**: Create use case specifications from user requirements

**Model**: opus (complex specification writing)
**Tools**: Read, Write, Bash
**File**: `.claude/subagents/uc-writer.md`

**When to Use:**
- Starting new feature
- Converting requirements to formal specs
- Creating UC from user stories

**Triggers:**
- "create UC for task management"
- "write use case for user authentication"
- "generate UC-006 specification"

**Capabilities:**
- Interviews user for requirements
- Generates complete UC specification (16 sections)
- Creates Gherkin acceptance criteria
- Identifies services needed
- Suggests implementation plan
- Follows UC template exactly

**Example Usage:**
```
User: "Create UC for password reset functionality"

Agent:
1. Interviews user (actors, flows, acceptance criteria)
2. Generates specs/use-cases/UC-007-password-reset.md
3. Includes: objective, actors, flows, acceptance criteria, services, implementation plan
4. Shows preview, gets approval, writes file
```

**Output**: Complete UC specification file (400-600 lines)

**Rule Coverage**: Rule #1 (Specifications Are Law)

---

### 6. adr-manager

**Purpose**: Create and manage Architecture Decision Records (ADRs)

**Model**: opus (complex decision documentation)
**Tools**: Read, Write, Bash, Grep
**File**: `.claude/subagents/adr-manager.md`

**When to Use:**
- Making technical decision (library, pattern, architecture)
- Documenting decision rationale
- Checking ADR compliance

**Triggers:**
- "create ADR for authentication approach"
- "document decision to use JWT"
- "check ADR compliance"

**Capabilities:**
- Creates ADR files (ADR-XXX format)
- Documents context, decision, consequences
- Checks existing ADRs before new decisions
- Validates ADR compliance in code
- Updates ADR status (proposed, accepted, superseded)

**Example Usage:**
```
User: "Create ADR for choosing bcrypt for password hashing"

Agent:
1. Interviews user (why bcrypt? alternatives considered?)
2. Researches alternatives (scrypt, argon2, pbkdf2)
3. Documents decision rationale
4. Creates planning/ADR-005-password-hashing-bcrypt.md
5. Includes: context, decision, consequences, alternatives rejected
```

**Output**: ADR file following ADR template

**Rule Coverage**: Rule #7 (Technical Decisions Are Binding)

---

## Tier 2: HIGH Priority Agents (4)

### 7. iteration-planner

**Purpose**: Break use cases into 1-3 hour iterations with detailed task lists

**Model**: opus (complex planning)
**Tools**: Read, Write, Glob, Grep
**File**: `.claude/subagents/iteration-planner.md`

**When to Use:**
- Starting new UC implementation
- Breaking large feature into manageable chunks
- Validating iteration scope (≤3 hours)

**Triggers:**
- "plan iteration for UC-001"
- "break down this use case"
- "create iteration plan"

**Capabilities:**
- Strategic planning: UC → multiple iterations
- Tactical planning: Detailed iteration with tasks, tests, steps
- Scope validation: Warns if >3 hours
- Complexity detection: Flags risky iterations
- Time estimation: Estimates per task and total

**Example Usage:**
```
User: "Plan iterations for UC-001 user registration"

Agent:
1. Reads UC-001 specification
2. Breaks into 2 iterations:
   - Iteration 1: Basic registration (email, password) - 2.5 hours
   - Iteration 2: Email verification - 2 hours
3. Creates detailed plan for iteration 1 (tasks, tests, DoD)
4. Writes planning/iteration-001-basic-registration.md
```

**Output**: Iteration plan file with tasks, tests, estimates

**Rule Coverage**: Rule #3 (Incremental Above All), Rule #5 (Two-Level Planning)

---

### 8. spec-validator

**Purpose**: Validate UC and service spec completeness and quality

**Model**: sonnet (rule-based validation)
**Tools**: Read, Grep, Glob
**File**: `.claude/subagents/spec-validator.md`

**When to Use:**
- After creating spec (before implementation)
- Before starting iteration
- During spec review

**Triggers:**
- "validate UC-003 specification"
- "check spec quality"
- "is this spec complete?"

**Capabilities:**
- Checks all 16 UC sections present
- Validates Gherkin format in acceptance criteria
- Ensures service references exist
- Detects ambiguous language ("should", "might", "TBD")
- Scores spec 0-100 (≥80 = pass)
- Provides actionable fix suggestions

**Example Usage:**
```
User: "Validate UC-003 task creation spec"

Agent:
1. Reads specs/use-cases/UC-003-task-creation.md
2. Checks 16 required sections
3. Finds issues: Services Used empty, Main Flow <3 steps, non-Gherkin AC
4. Scores: 68/100 (FAIL)
5. Provides priority fixes (CRITICAL, HIGH, MEDIUM)
```

**Output**: Validation report with score and fixes

**Rule Coverage**: Rule #1 (Specifications Are Law)

---

### 9. git-workflow-helper

**Purpose**: Automate git branching, commit message generation, pre-commit validation

**Model**: sonnet (structured text generation)
**Tools**: Bash, Read
**File**: `.claude/subagents/git-workflow-helper.md`

**When to Use:**
- Session start (Phase 1) - git status check
- Before new work (Phase 3) - branch creation
- Session end (Phase 9) - commit generation

**Triggers:**
- "create branch for iteration 2"
- "generate commit message"
- "check git status"
- Proactively at session start/end

**Capabilities:**
- Git status reporting
- Branch creation with naming conventions (iteration-XXX, uc-XXX)
- Commit message generation (with spec refs, test counts)
- Pre-commit validation (tests passing, no TODOs, no debug code)
- Blocks commits with critical violations

**Example Usage:**
```
User: "Create branch for iteration 2"

Agent:
1. Checks current branch (on main)
2. Pulls latest: git pull origin main
3. Creates branch: git checkout -b iteration-002-task-management
4. Reports: "✅ Created branch: iteration-002-task-management"
```

**Output**: Git operations executed, status reported

**Rule Coverage**: Rule #11 (Git Workflow Discipline)

---

### 10. session-summarizer

**Purpose**: Generate session-state.md for session continuity

**Model**: sonnet (summarization)
**Tools**: Read, Write, Bash
**File**: `.claude/subagents/session-summarizer.md`

**When to Use:**
- Session end (Phase 8)
- Mid-session progress check
- After major work completion

**Triggers:**
- "end session"
- "generate summary"
- "what have we done so far?"
- Proactively at session end

**Capabilities:**
- Analyzes conversation for work completed
- Parses git log for commits
- Extracts decisions (ADRs, technical choices)
- Identifies blockers and open questions
- Determines next steps from current-iteration.md
- Generates session-state.md with real content (no placeholders)

**Example Usage:**
```
User: "End session and generate summary"

Agent:
1. Analyzes conversation history
2. Runs git log, git diff
3. Extracts: Implemented user registration, 8 tests passing, created ADR-004
4. Identifies: No blockers
5. Next steps: Implement email verification
6. Writes planning/session-state.md
```

**Output**: session-state.md for next session pickup

**Rule Coverage**: Rule #10 (Session Discipline)

---

## Tier 3: MEDIUM Priority Agents (2)

### 11. tech-debt-detector

**Purpose**: Detect technical debt (TODOs, debug code, missing error handling)

**Model**: sonnet (pattern matching)
**Tools**: Grep, Glob, Read
**File**: `.claude/subagents/tech-debt-detector.md`

**When to Use:**
- Before commits (pre-commit check)
- Periodic code audits
- Before releases

**Triggers:**
- "check tech debt"
- "scan for issues"
- "find TODOs"
- Proactively before commits

**Capabilities:**
- Scans for TODO/FIXME/HACK comments
- Detects debug code (print, console.log, debugger)
- Finds missing error handling
- Checks for hardcoded secrets
- Validates type hints presence
- Scores tech debt 0-100
- Blocks commits with critical violations

**Example Usage:**
```
User: "Check tech debt before commit"

Agent:
1. Scans staged files
2. Finds: 1 TODO comment, 2 print() statements
3. Severity: HIGH (TODO) + CRITICAL (debug code)
4. Blocks commit
5. Reports: "Fix 2 CRITICAL issues before committing"
```

**Output**: Tech debt report (PASS/BLOCK)

**Rule Coverage**: Rule #6 (No Shortcuts)

---

### 12. doc-generator

**Purpose**: Generate API documentation, READMEs, service docs from docstrings

**Model**: sonnet (structured doc generation)
**Tools**: Read, Write, Bash
**File**: `.claude/subagents/doc-generator.md`

**When to Use:**
- After feature completion
- Before releases
- When documentation outdated

**Triggers:**
- "generate API docs for implementation/auth/"
- "create README for this module"
- "document UserService"

**Capabilities:**
- Extracts docstrings from code
- Parses function signatures and type hints
- Generates API reference (classes, functions, parameters)
- Creates README files with usage examples
- Validates documentation completeness
- Suggests missing docstring templates

**Example Usage:**
```
User: "Generate API docs for implementation/auth/"

Agent:
1. Scans implementation/auth/ for *.py files
2. Extracts docstrings from UserService, helpers
3. Parses function signatures
4. Generates docs/api/auth.md with formatted API reference
5. Reports: "✅ 8 functions documented, 100% coverage"
```

**Output**: API documentation markdown files

**Integration**: Complements code-quality-checker (documentation requirement)

---

## Service-Oriented Agents (6)

### 13-18. service-* Agents

**Purpose**: Complete service architecture lifecycle automation

**Agents:**
1. **service-extractor**: Extract reusable services from use cases
2. **service-designer**: Design service interfaces (protocols, methods)
3. **service-dependency-analyzer**: Validate dependencies, detect cycles
4. **service-optimizer**: Performance optimization strategies
5. **service-library-finder**: Library evaluation and recommendations
6. **uc-service-tracer**: UC-Service traceability validation

**Files**: `.claude/subagents/service-*.md`

**When to Use:**
- After creating multiple UCs (extract services)
- Designing service layer
- Validating service architecture
- Optimizing performance
- Choosing libraries

**Example Workflow:**
```
service-extractor → service-designer → service-dependency-analyzer →
service-optimizer → service-library-finder → uc-service-tracer
```

**See**: `docs/examples/` for detailed service agent examples

---

## Agent Orchestration

### Sequential Workflows

**Pattern**: Agent A → Agent B → Agent C

**Use When**: Output of A is input for B

**Example: Spec-to-Implementation**
```
uc-writer → spec-validator → iteration-planner → test-writer → [implementation]
```

**Benefits:**
- Enforces proper sequence
- Validates at each step
- Catches issues early

---

### Parallel Execution

**Pattern**: Run multiple agents simultaneously

**Use When**: Agents are independent

**Example: Quality Gate**
```
code-quality-checker + refactoring-analyzer + tech-debt-detector
(run all 3 in parallel, collect results)
```

**Benefits:**
- Faster execution
- Comprehensive validation

---

### Conditional Workflows

**Pattern**: If X then agent Y, else agent Z

**Example: Branch Selection**
```
If (new feature) → uc-writer
Else if (bug fix) → just test-writer
```

---

## Integration with Framework

### 9-Phase Session Checklist Coverage

| Phase | Agents Used | Automation Level |
|-------|-------------|------------------|
| 1. Orientation | git-workflow-helper | Partial (git status) |
| 2. Research | service-library-finder | Partial (library research) |
| 3. Planning | iteration-planner, git-workflow-helper | High (planning + branch) |
| 4. Test-First | test-writer, bdd-scenario-writer | High (test generation) |
| 5. Implement | (manual) | Low |
| 6. Refactor | refactoring-analyzer | Partial (suggestions) |
| 7. Validate | code-quality-checker, spec-validator | High (quality validation) |
| 8. Document | session-summarizer, doc-generator | High (documentation) |
| 9. Close | git-workflow-helper, tech-debt-detector | High (commit + validation) |

**Coverage**: 4/9 phases with high automation (44%)

---

## Creating Custom Agents

### Agent Template Structure

```markdown
---
name: agent-name
description: Expert in X. Masters Y. Use when Z.
tools: [Read, Write, Bash, Grep, Glob]
model: opus | sonnet
---

You are an expert [domain] agent...

## Responsibilities
1. [Responsibility 1]
...

## [Domain] Checklist
### Category 1
- [ ] Item 1
...

## Process
1. [Step 1]
...

## Examples
### Example 1: [Scenario]
[Input → Process → Output]

## Quality Checks
- [ ] Check 1
...

## Anti-Patterns
❌ Pattern 1 → Correct approach
...
```

### Requirements

**YAML Frontmatter:**
- `name`: Agent identifier (lowercase-hyphen-separated)
- `description`: What agent does, when to use (include "Use PROACTIVELY" if applicable)
- `tools`: List of tools agent needs
- `model`: opus (complex reasoning) or sonnet (rule-based/structured)

**Content Sections:**
- **Responsibilities**: 6-8 core responsibilities
- **Checklist**: 7 categories, 60-70 items total
- **Process**: 18-step process (detailed workflow)
- **Examples**: 3-5 real-world examples with input/output
- **Quality Checks**: 15-18 validation items
- **Anti-Patterns**: 8-10 patterns to reject

### Best Practices

1. **Focused Scope**: One agent, one domain (SRP)
2. **Clear Triggers**: Explicit trigger keywords in description
3. **Structured Output**: Templates, checklists, consistent format
4. **User Approval**: Show preview before final action
5. **Error Handling**: Detect invalid inputs, provide clear errors
6. **Rule Coverage**: Tie agent to framework rules

---

## Statistics

**Agent Count**: 18 (12 core + 6 service-oriented)
**Total Code**: ~10,000 lines (agent implementations)
**Rule Coverage**: 10/12 rules (83%)
**Phase Coverage**: 4/9 phases (44% high automation)
**Time Savings**: 40-60% reduction in manual effort (estimated)

**Version**: All agents v1.0
**Framework**: Claude Development Framework v2.1
**Status**: Production-ready

---

## Quick Start

**Using Your First Agent:**

1. **Choose Agent**: Browse table above
2. **Trigger**: Use trigger keyword or ask directly
3. **Provide Input**: Spec file, code path, requirements
4. **Review**: Check agent output
5. **Approve**: Confirm action
6. **Execute**: Agent completes task

**Example:**
```
"Generate tests for UC-001"
→ test-writer activates
→ Reads UC-001 spec
→ Shows test preview
→ You approve
→ Writes test file
```

---

## Additional Resources

**Usage Guide**: `docs/agent-guide.md` - Practical examples and workflows
**Integration Patterns**: `docs/agent-integration-patterns.md` - Agent orchestration
**Examples**: `docs/examples/` - 20 detailed agent usage examples
**Agent Files**: `.claude/subagents/` - All 18 agent implementations

---

**Last Updated**: 2025-10-02
**Framework Version**: 2.1
**Maintained By**: Claude Development Framework Team

**Ready to automate your development workflow!** 🚀
