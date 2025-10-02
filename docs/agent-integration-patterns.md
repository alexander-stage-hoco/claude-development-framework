# Agent Integration Patterns

**Framework**: Claude Development Framework v2.1
**Last Updated**: 2025-10-02
**Purpose**: Orchestration patterns and complex workflows for multi-agent systems

---

## Table of Contents

1. [Introduction](#introduction)
2. [Pattern 1: Spec-to-Implementation Pipeline](#pattern-1-spec-to-implementation-pipeline)
3. [Pattern 2: Session Lifecycle Workflow](#pattern-2-session-lifecycle-workflow)
4. [Pattern 3: Quality Gate Pipeline](#pattern-3-quality-gate-pipeline)
5. [Pattern 4: Service Architecture Workflow](#pattern-4-service-architecture-workflow)
6. [Pattern 5: Documentation Pipeline](#pattern-5-documentation-pipeline)
7. [Pattern 6: Emergency Hotfix](#pattern-6-emergency-hotfix)
8. [Custom Orchestration](#custom-orchestration)
9. [Performance Considerations](#performance-considerations)
10. [Workflow Decision Tree](#workflow-decision-tree)
11. [Error Handling](#error-handling)

---

## Introduction

### Agent Orchestration Concepts

**Orchestration** = coordinating multiple agents to accomplish complex tasks

**Key Concepts**:
- **Sequential Execution**: Agent B waits for Agent A output
- **Parallel Execution**: Multiple agents run independently
- **Data Flow**: Output of Agent A → Input of Agent B
- **Checkpoints**: User approval gates between agents
- **Error Handling**: What happens when agent fails

### Sequential vs. Parallel Execution

**Sequential** (Agent B depends on Agent A):
```
uc-writer → spec-validator → iteration-planner → test-writer
   ↓            ↓                 ↓                  ↓
  spec    validates spec    creates plan      generates tests
```

**Parallel** (Agents independent):
```
   code-quality-checker ──┐
                          ├──→ [All complete] → commit
   tech-debt-detector ────┘
```

### Data Flow Between Agents

**Example Flow**: UC Creation → Implementation
```
1. uc-writer creates:     specs/use-cases/UC-001.md
                          ↓
2. spec-validator reads:  UC-001.md → validates → score 92/100
                          ↓
3. iteration-planner reads: UC-001.md → splits → 3 iteration files
                          ↓
4. test-writer reads:     iteration-01.md → generates → tests/test_*.py
                          ↓
5. [Manual implementation]
                          ↓
6. code-quality-checker reads: implementation/*.py → validates → score 88/100
```

### Error Handling in Workflows

**Failure Modes**:
1. **Agent blocks**: spec-validator score <80 → STOP workflow, fix spec
2. **Agent warns**: refactoring-analyzer finds issues → CONTINUE, but note
3. **Agent fails**: git-workflow-helper can't create branch → DEBUG, retry

**Recovery Strategy**:
- Fix root cause (not bypass agent)
- Re-run from failed agent
- Document issue in session-state

---

## Pattern 1: Spec-to-Implementation Pipeline

### Overview

**Purpose**: Complete feature development from requirements to tested code
**Agents**: 8 agents (uc-writer → spec-validator → iteration-planner → test-writer → bdd-scenario-writer → code-quality-checker → refactoring-analyzer → adr-manager)
**Duration**: 60-90 minutes (vs. 4-6 hours manual)
**Automation**: 75%

### Workflow Diagram

```
Requirements
    ↓
[uc-writer] → Use Case Spec (specs/use-cases/UC-006.md)
    ↓
[spec-validator] → Validation Report (score 92/100 ✓)
    ↓
[iteration-planner] → 3 Iterations (planning/iterations/UC-006/)
    ↓
[test-writer] → Tests (tests/test_uc006_it01.py) [RED PHASE]
    ↓
[bdd-scenario-writer] → BDD Scenarios (features/task_priority.feature)
    ↓
[MANUAL IMPLEMENTATION] → Code (implementation/services/task_service.py) [GREEN PHASE]
    ↓
[code-quality-checker] → Quality Report (score 88/100 ✓)
    ↓
[refactoring-analyzer] → Refactoring Suggestions (5 opportunities) [REFACTOR PHASE]
    ↓
[adr-manager] → Technical Decisions (planning/adrs/ADR-006.md)
    ↓
Production-Ready Feature ✓
```

### Detailed Steps

#### Step 1: uc-writer (15 minutes)

**Input**: User requirement (verbal or written)
```
You: "We need a feature to let users prioritize their tasks (high, medium, low)"
```

**Agent Process**:
```
1. Interview user:
   - How many priority levels? (3: high/medium/low)
   - Who can set priority? (task owner + managers)
   - UI requirements? (dropdown selector)

2. Generate UC spec from template

3. Write to: specs/use-cases/UC-006-task-prioritization.md
```

**Output**: Complete 500-line UC specification
- 16 required sections
- 8 acceptance criteria
- 4 edge cases
- 3 error scenarios
- Service dependencies mapped

**Checkpoint**: Review UC spec (does it match requirements?)

---

#### Step 2: spec-validator (3 minutes)

**Input**: UC-006 file path
```
You: "validate UC-006"
```

**Agent Process**:
```
1. Read specs/use-cases/UC-006-task-prioritization.md

2. Check 16 sections (all present?)

3. Validate content quality:
   - Acceptance criteria ≥5 ✓ (has 8)
   - Edge cases documented ✓ (has 4)
   - Service dependencies listed ✓
   - Traceability complete ✓

4. Score: 92/100 (PASS - threshold 80)
```

**Output**: Validation report
```
Specification Validation: UC-006

Score: 92/100 ✓ (PASS)

Section Completeness: 16/16 ✓
Content Quality: Excellent

Minor Issues (2):
⚠ Non-Functional Requirements: Missing performance targets (add "Priority update <200ms")
⚠ Traceability: No iteration assigned yet (expected - will be added in planning)

✅ Specification VALID. Ready for implementation planning.
```

**Checkpoint**: Score ≥80? → YES, proceed

---

#### Step 3: iteration-planner (15 minutes)

**Input**: UC-006 spec
```
You: "plan iterations for UC-006"
```

**Agent Process**:
```
1. Analyze complexity:
   - 8 acceptance criteria
   - Estimated effort: 7 hours

2. Break into iterations (max 3 hours each):
   Iteration 1: Basic priority (AC1-3) - 2h 15min
   Iteration 2: Priority logic (AC4-6) - 2h 30min
   Iteration 3: Advanced features (AC7-8) - 2h 15min

3. Create iteration files
```

**Output**: 3 iteration plan files
```
planning/iterations/UC-006-task-prioritization/
├── iteration-01-basic-priority.md
├── iteration-02-priority-logic.md
└── iteration-03-advanced-features.md
```

**Checkpoint**: Review iteration breakdown (reasonable scope?)

---

#### Step 4: test-writer (5 minutes)

**Input**: Iteration 1 plan
```
You: "generate tests for UC-006 iteration 1"
```

**Agent Process**:
```
1. Read iteration-01-basic-priority.md

2. Extract acceptance criteria (AC1-3)

3. Generate test cases:
   - test_user_can_set_priority_high()
   - test_user_can_set_priority_medium()
   - test_user_can_set_priority_low()
   - test_priority_visible_in_task_list()
   - test_invalid_priority_rejected()
   ...

4. Write test file
```

**Output**: tests/test_task_priority_basic.py
- 8 tests (RED phase - all failing)
- Docstrings with UC/AC references
- Test data fixtures

**Checkpoint**: Tests should FAIL (no implementation yet - TDD!)

---

#### Step 5: bdd-scenario-writer (5 minutes)

**Input**: UC-006 acceptance criteria
```
You: "write BDD scenarios for UC-006"
```

**Agent Process**:
```
1. Read UC-006 acceptance criteria

2. Convert to Given-When-Then format

3. Create scenario outlines
```

**Output**: features/task_priority.feature
```gherkin
Feature: Task Prioritization
  Scenario: User sets task priority to High
    Given I have a task "Complete report"
    When I set priority to "High"
    Then the task should show priority "High"
    And the task should appear at top of list

  Scenario Outline: Valid priority values
    Given I have a task "<task>"
    When I set priority to "<priority>"
    Then the task priority should be "<priority>"

    Examples:
      | task          | priority |
      | Task 1        | High     |
      | Task 2        | Medium   |
      | Task 3        | Low      |
```

**Checkpoint**: Review scenarios (readable by stakeholders?)

---

#### Step 6: Manual Implementation (60-90 minutes)

**Your Work** (agents assist, but you implement):
```python
# implementation/services/task_service.py

class TaskService:
    VALID_PRIORITIES = ['High', 'Medium', 'Low']

    def set_task_priority(self, task_id: int, priority: str) -> Task:
        """Set task priority (UC-006 AC1-3)"""
        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Invalid priority: {priority}")

        task = self.task_repo.get_by_id(task_id)
        task.priority = priority
        task.updated_at = datetime.now()

        self.task_repo.save(task)
        return task
```

**TDD Cycle**:
1. Run tests: `pytest tests/test_task_priority_basic.py` → 8 failing
2. Implement minimal code
3. Run tests again → 6 failing, 2 passing
4. Implement more
5. Repeat until: → 8 passing ✓ (GREEN phase)

---

#### Step 7: code-quality-checker (5 minutes)

**Input**: Implementation files
```
You: "check code quality in implementation/services/task_service.py"
```

**Agent Process**:
```
1. Analyze:
   - Type hints coverage: 95% ✓
   - Docstrings: 100% ✓
   - Complexity: max 6 (threshold 10) ✓
   - Linting: 0 issues ✓

2. Score: 88/100 (PASS - threshold 80)
```

**Output**: Quality Report
```
Code Quality: task_service.py

Score: 88/100 ✓ (PASS)

Strengths:
✓ Full type hints coverage
✓ All functions documented
✓ Low complexity (max 6)
✓ No linting issues

Minor Issues (2):
⚠ Line 45: Consider extracting constant VALID_PRIORITIES to config
⚠ Line 67: Add error logging for invalid priority

✅ Quality check PASSED. Ready to commit.
```

**Checkpoint**: Score ≥80? → YES, proceed

---

#### Step 8: refactoring-analyzer (10 minutes)

**Input**: Implementation code
```
You: "suggest refactoring for task_service.py"
```

**Agent Process**:
```
1. Analyze code smells (none found - code is clean!)

2. Find improvement opportunities:
   - Extract priority validation to separate method
   - Add caching for frequently accessed tasks
   - Consider strategy pattern for priority rules
```

**Output**: Refactoring Report
```
Refactoring Analysis: task_service.py

Code Quality: Excellent (no smells detected)

Enhancement Opportunities (5):

1. Extract Priority Validation (LOW PRIORITY)
   - Current: Inline check in set_task_priority()
   - Suggestion: _validate_priority(priority: str) method
   - Benefit: Reusable in other methods
   - Effort: 10 min

2. Add Priority Change Logging (MEDIUM PRIORITY)
   - Current: Silent priority updates
   - Suggestion: Log priority changes for audit trail
   - Benefit: Better observability
   - Effort: 15 min

[... 3 more suggestions]

Recommendation: Implement #2 (priority change logging) in iteration 2.
Others are optional enhancements.
```

**Checkpoint**: Implement critical refactorings now, defer others

---

#### Step 9: adr-manager (10 minutes)

**Input**: Technical decision (e.g., priority value format)
```
You: "create ADR for task priority values"
```

**Agent Process**:
```
1. Interview for decision details:
   - What options considered? (numeric 1-10, high/medium/low, custom labels)
   - Why chosen option? (simplicity, user-friendly)
   - What rejected? (numeric too abstract)

2. Generate ADR from template
```

**Output**: planning/adrs/ADR-006-task-priority-values.md
```markdown
# ADR-006: Task Priority Values (High/Medium/Low)

**Status**: Accepted
**Date**: 2025-10-02

## Decision
Use **3-level text priority** (High, Medium, Low) for task prioritization.

## Alternatives Considered
1. Numeric 1-10: Too granular, users confused
2. Custom labels: Too flexible, inconsistent usage

## Consequences
✅ Simple, user-friendly
✅ Industry standard (Jira, Asana use similar)
❌ Less granular than numeric (acceptable trade-off)
```

---

### Example Session Transcript

```
You: We need a feature to let users prioritize their tasks

Claude: I'll use the uc-writer agent to create a use case specification.
[uc-writer activates]
→ Created: specs/use-cases/UC-006-task-prioritization.md

You: Validate the spec

Claude: I'll use spec-validator to check quality.
[spec-validator activates]
→ Score: 92/100 ✓ (PASS)

You: Plan iterations

Claude: I'll use iteration-planner to break this down.
[iteration-planner activates]
→ Created 3 iterations (2h 15min, 2h 30min, 2h 15min)

You: Generate tests for iteration 1

Claude: I'll use test-writer to generate tests.
[test-writer activates]
→ Created: tests/test_task_priority_basic.py (8 tests, all failing - RED phase)

You: [implements feature over 90 minutes]

You: Check code quality

Claude: I'll use code-quality-checker to validate.
[code-quality-checker activates]
→ Score: 88/100 ✓ (PASS)

You: Any refactoring suggestions?

Claude: I'll use refactoring-analyzer to find improvements.
[refactoring-analyzer activates]
→ Found 5 opportunities (2 high-impact, 3 optional)

You: Document the decision to use High/Medium/Low priority

Claude: I'll use adr-manager to create an ADR.
[adr-manager activates]
→ Created: ADR-006-task-priority-values.md

You: Commit the work

Claude: I'll use git-workflow-helper to generate commit message.
[git-workflow-helper activates]
→ Commit created with spec references
```

**Total Time**: ~2 hours (vs. 4-6 hours manual)

---

### Outcomes & Metrics

**Files Created**: 8 files
- 1 UC spec (500 lines)
- 3 iteration plans (150 lines each)
- 1 test file (180 lines)
- 1 BDD feature (60 lines)
- 1 implementation (120 lines)
- 1 ADR (80 lines)

**Quality Metrics**:
- Spec validation: 92/100
- Code quality: 88/100
- Test coverage: 100% (iteration 1 scope)
- All tests passing: 8/8

**Time Savings**:
- Manual approach: 4-6 hours
- With agents: 2 hours
- **Savings**: 50-67%

---

## Pattern 2: Session Lifecycle Workflow

### Overview

**Purpose**: Manage session start, work, and end with continuity
**Agents**: 3 agents (git-workflow-helper → [work] → session-summarizer → git-workflow-helper)
**Duration**: 10-15 minutes (overhead for 2-3 hour session)
**Automation**: 90%

### Workflow Diagram

```
Session Start (Phase 1)
    ↓
[git-workflow-helper] → Git status check + branch verification
    ↓
[WORK: Phases 2-7] → Development (2-3 hours)
    ↓
Session End (Phase 8)
    ↓
[session-summarizer] → session-state.md (continuity documentation)
    ↓
Commit & Close (Phase 9)
    ↓
[git-workflow-helper] → Commit generation + push
    ↓
Session Complete ✓
```

### Phase 1: Session Start (5 minutes)

**Trigger**: "check git status" or "start session"

**git-workflow-helper Mode 1**:
```bash
1. git status --porcelain=v2
2. git log -5 --oneline
3. git branch --show-current
4. Check for uncommitted changes
```

**Output**:
```
Git Status Report:

Current Branch: iteration-002-email-verification
Status: Clean (no uncommitted changes)

Recent Commits:
- abc1234 feat: basic registration (iteration 1)
- def5678 docs: UC-001 specification
- ghi9012 chore: project setup

Untracked Files: None

Recommendations:
✓ Ready to continue iteration 2
✓ All previous work committed
✓ No merge conflicts
```

**Next**: Review planning/current-iteration.md, begin work

---

### Phase 8: Session End (5 minutes)

**Trigger**: "end session" or "generate session summary"

**session-summarizer**:
```
1. Analyze conversation (work completed, decisions, blockers)
2. Check git: git log -10, git diff --name-status
3. Check tests: pytest --collect-only (count tests)
4. Read current iteration plan
5. Determine next steps
6. Generate session-state.md (NO PLACEHOLDERS!)
```

**Output**: session-state.md (see Agent Guide example for full content)

---

### Phase 9: Commit & Close (5 minutes)

**Trigger**: "generate commit message" or "commit and push"

**git-workflow-helper Mode 3**:
```bash
1. Analyze changes: git diff --name-status
2. Count tests: grep -r "def test_" tests/
3. Find spec refs: grep -r "UC-" specs/
4. Generate commit message (conventional commits format)
5. Pre-commit validation:
   - Tests passing?
   - No TODOs?
   - No debug code?
```

**Output**:
```
feat: email verification (iteration 2 complete)

Implemented UC-001 iteration 2: email verification workflow.

Changes:
- Email verification token generation (24h expiry)
- Verification email template (HTML + text)
- verify_email() endpoint with validation
- Token expiry handling

Tests: 24 passing / 24 total
Coverage: 94%

Specification: UC-001 iteration 2
Framework: Claude Development Framework v2.1

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>

---

Commit and push? (yes/no)
```

---

### Example Session Timeline

**09:00 - Session Start**
```
You: check git status
→ Git clean, on iteration-002 branch, ready to work
```

**09:05-11:20 - Development Work** (2h 15min)
- Implement email verification
- Write tests (TDD cycle)
- Fix bugs, refactor

**11:20 - Session End**
```
You: end session
→ session-state.md created with complete summary
```

**11:25 - Commit & Push**
```
You: generate commit message
→ Commit created and pushed to origin

You: Session complete! See you next time.
```

**Total Overhead**: 15 minutes for session management (in 2h 30min session = 10%)

---

## Pattern 3: Quality Gate Pipeline

### Overview

**Purpose**: Validate code quality before merge/release
**Agents**: 4 agents (code-quality-checker → refactoring-analyzer → tech-debt-detector → spec-validator)
**Duration**: 15-20 minutes
**Use Cases**: Before merge to main, before release, periodic audits

### Workflow Diagram

```
Code Ready for Merge?
    ↓
[code-quality-checker] → Score ≥80? → NO → BLOCK merge
    ↓ YES
[refactoring-analyzer] → Critical issues? → YES → BLOCK merge
    ↓ NO
[tech-debt-detector] → CRITICAL debt? → YES → BLOCK merge
    ↓ NO
[spec-validator] → All specs valid? → NO → BLOCK merge
    ↓ YES
✅ Quality Gate PASSED → Merge Approved
```

### Gate 1: Code Quality (5 minutes)

**Trigger**: "check code quality in implementation/"

**code-quality-checker**:
```
Scans:
- Type hints coverage (≥90%)
- Docstring presence (≥80%)
- Cyclomatic complexity (≤10)
- Linting (0 errors)
- Security issues

Threshold: ≥80/100 to pass
```

**Pass**: Score 88/100 → Proceed
**Fail**: Score 72/100 → BLOCK, fix issues

---

### Gate 2: Refactoring (5 minutes)

**Trigger**: "analyze code for refactoring"

**refactoring-analyzer**:
```
Checks:
- Code smells (long functions, duplication)
- Complexity (cyclomatic, cognitive)
- Design patterns (violations)
- SOLID principles

Blocker: Critical smells (god class, feature envy)
```

**Pass**: No critical smells → Proceed
**Fail**: 2 god classes found → BLOCK, refactor

---

### Gate 3: Tech Debt (5 minutes)

**Trigger**: "check tech debt"

**tech-debt-detector**:
```
Scans:
- TODOs/FIXMEs (HIGH severity)
- Debug code (CRITICAL)
- Hardcoded secrets (CRITICAL)
- Missing error handling (MEDIUM)

Blocker: Any CRITICAL issues
```

**Pass**: Score 85/100, 0 CRITICAL → Proceed
**Fail**: 2 CRITICAL (debug code) → BLOCK, remove

---

### Gate 4: Spec Validation (5 minutes)

**Trigger**: "validate all specs"

**spec-validator**:
```
Validates:
- All UC specs (≥80/100)
- All service specs (≥80/100)
- Traceability complete

Blocker: Any spec <80/100
```

**Pass**: All specs ≥80 → Proceed
**Fail**: UC-003 score 68/100 → BLOCK, fix spec

---

### Decision Logic

```
if code_quality < 80:
    BLOCK("Code quality below threshold")
elif refactoring_critical_smells > 0:
    BLOCK("Critical code smells found")
elif tech_debt_critical > 0:
    BLOCK("Critical tech debt present")
elif any_spec_score < 80:
    BLOCK("Invalid specifications")
else:
    APPROVE("All quality gates passed")
```

---

## Pattern 4: Service Architecture Workflow

### Overview

**Purpose**: Design complete service layer from use cases
**Agents**: 6 service-oriented agents (sequential pipeline)
**Duration**: 45-60 minutes (vs. 4+ hours manual)
**Use Cases**: New project, architecture refactoring

### Workflow Diagram

```
Use Cases (5 UCs)
    ↓
[service-extractor] → Identify services (12 services)
    ↓
[service-designer] → Design interfaces (12 service specs)
    ↓
[service-dependency-analyzer] → Validate dependencies (check cycles)
    ↓
[uc-service-tracer] → Verify traceability (UC ↔ Service)
    ↓
[service-library-finder] → Evaluate libraries (3 libraries)
    ↓
[service-optimizer] → Performance strategies (caching, indexing)
    ↓
Complete Service Architecture ✓
```

### Step 1: service-extractor (10 min)

**Input**: 5 use case specs
```
You: "extract services from all UCs"
```

**Process**:
```
1. Read all UC specs (UC-001 to UC-005)
2. Identify capabilities:
   - UC-001: user registration, email verification
   - UC-002: authentication, token generation
   - UC-003: task CRUD operations
   - UC-004: task prioritization
   - UC-005: task assignment

3. Group by domain (SRP):
   - UserService: registration, profiles
   - AuthService: authentication, tokens
   - TaskService: task operations
   - NotificationService: emails, alerts
   - ...

4. Create service specs
```

**Output**: 12 service specifications
```
specs/services/
├── SVC-001-user-service.md
├── SVC-002-auth-service.md
├── SVC-003-task-service.md
├── SVC-004-notification-service.md
├── SVC-005-email-service.md
└── ...
```

---

### Step 2: service-designer (15 min)

**Input**: 12 service specs
```
You: "design interfaces for all services"
```

**Process**:
```
For each service:
1. Define interface (public methods)
2. Specify method signatures (params, returns)
3. Document contracts (preconditions, postconditions)
4. List dependencies (which services needed)
```

**Output**: Updated service specs with interfaces
```markdown
# SVC-003: TaskService

## Interface

### create_task
```python
def create_task(
    user_id: int,
    title: str,
    description: str,
    priority: str = 'Medium'
) -> Task
```

**Preconditions**:
- user_id exists
- title not empty
- priority in ['High', 'Medium', 'Low']

**Postconditions**:
- Task created in database
- Owner assigned to user_id
- Created event published

**Dependencies**:
- UserService.get_user(user_id)
- NotificationService.notify_task_created()
```

---

### Step 3: service-dependency-analyzer (5 min)

**Input**: All service specs
```
You: "check service dependencies"
```

**Process**:
```
1. Build dependency graph:
   TaskService → UserService, NotificationService
   NotificationService → EmailService
   EmailService → (none)

2. Detect cycles (DFS algorithm)

3. Topological sort (layer assignment)

4. Validate limits (≤3 dependencies per service)
```

**Output**: Dependency Report
```
Service Dependency Analysis:

Dependency Graph:
Layer 1 (Foundation):
- UserService (0 dependencies)
- EmailService (0 dependencies)

Layer 2 (Core):
- AuthService (depends: UserService)
- NotificationService (depends: EmailService)

Layer 3 (Business):
- TaskService (depends: UserService, NotificationService)

---

Validation Results:
✓ No circular dependencies
✓ Max dependencies: 2 (limit: 3)
✓ Clean 3-layer architecture

✅ Architecture is production-ready
```

---

### Step 4: uc-service-tracer (5 min)

**Input**: UCs + Service specs
```
You: "check UC-Service traceability"
```

**Process**:
```
1. For each UC:
   - Check "Service Dependencies" section
   - Verify services exist

2. For each Service:
   - Check "Used By" section
   - Verify UCs exist

3. Detect mismatches:
   - UC references missing service
   - Service not referenced by any UC (orphan)
```

**Output**: Traceability Report
```
UC-Service Traceability:

Coverage: 100% (5/5 UCs traced)

UC → Service Mapping:
✓ UC-001 → UserService, EmailService
✓ UC-002 → AuthService, UserService
✓ UC-003 → TaskService
✓ UC-004 → TaskService, NotificationService
✓ UC-005 → TaskService, UserService

Service → UC Mapping:
✓ UserService ← UC-001, UC-002, UC-005
✓ AuthService ← UC-002
✓ TaskService ← UC-003, UC-004, UC-005
✓ EmailService ← UC-001
✓ NotificationService ← UC-004

Orphan Services: 0

✅ Complete traceability verified
```

---

### Step 5: service-library-finder (15 min)

**Input**: Service requirements
```
You: "find libraries for AuthService"
```

**Process**:
```
1. Identify needs:
   - JWT token generation
   - Password hashing
   - OAuth2 (future)

2. Search PyPI, GitHub

3. Evaluate candidates:
   - PyJWT vs. Authlib vs. Custom
   - Score by: features, quality, maintenance

4. Recommend best option
```

**Output**: Library Evaluation Report
```
Library Evaluation: AuthService

Candidates:
1. PyJWT + Passlib: 91.5/100 ⭐ RECOMMENDED
   - Lightweight, focused
   - JWT + hashing only
   - 50M+ downloads, actively maintained

2. Authlib: 84/100
   - Full OAuth2/OIDC
   - Overkill for current needs
   - Heavier dependency

3. Custom Implementation: 78.5/100
   - Full control
   - 4 days effort, security risks

Decision: Use PyJWT + Passlib (save $2,100 vs. custom)
```

---

### Step 6: service-optimizer (10 min)

**Input**: Service specs
```
You: "optimize TaskService for performance"
```

**Process**:
```
1. Identify bottlenecks:
   - get_tasks() scans all tasks (slow with 50K+)

2. Suggest strategies:
   - Database indexing (priority, user_id)
   - Caching (Redis for hot tasks)
   - Pagination (limit results)

3. Benchmark options

4. Recommend best approach
```

**Output**: Optimization Report
```
Performance Optimization: TaskService

Bottleneck: get_tasks() - 1200ms with 50K tasks

Strategies:
1. Database Indexing: 1200ms → 45ms (96% faster, $0 cost)
2. Redis Caching: 1200ms → 8ms (99% faster, $50/mo cost)
3. Pagination: 1200ms → 120ms (90% faster, $0 cost)

Recommendation:
- Implement #1 (indexing) immediately
- Add #3 (pagination) for UX
- Defer #2 (caching) until >100K tasks

ROI: 96% performance gain, $0 additional cost
```

---

### Complete Architecture Output

**Deliverables** (60 minutes work):
- 12 service specifications (~3,000 lines)
- Dependency graph (validated, no cycles)
- Traceability matrix (100% coverage)
- 3 library evaluations (best options chosen)
- Performance optimization plan (96% faster queries)

**vs. Manual** (4+ hours):
- Inconsistent specs
- Likely circular dependencies
- Manual traceability tracking
- Ad-hoc library choices
- No performance analysis

**Time Savings**: 75%

---

## Pattern 5: Documentation Pipeline

### Overview

**Purpose**: Generate complete documentation set
**Agents**: 3 agents (doc-generator → session-summarizer → git-workflow-helper)
**Duration**: 30-45 minutes
**Output**: API docs, session history, commit

### Workflow

```
Codebase
    ↓
[doc-generator] → API Documentation (docs/api/*.md)
    ↓
[session-summarizer] → Session Summary (what was documented)
    ↓
[git-workflow-helper] → Commit "docs: API documentation"
    ↓
Documentation Complete ✓
```

**Example**:
```
You: "generate API docs for all services"
→ doc-generator creates 12 API docs (15 min)

You: "end session"
→ session-summarizer documents what was generated (5 min)

You: "commit documentation"
→ git-workflow-helper creates commit (2 min)

Total: 22 minutes (vs. 2+ hours manual)
```

---

## Pattern 6: Emergency Hotfix

### Overview

**Purpose**: Fix production bug while maintaining quality
**Agents**: Minimal (2 agents - git-workflow-helper + tech-debt-detector)
**Duration**: 20-30 minutes (for hotfix + validation)
**Constraint**: Tests REQUIRED even in emergency (Rule #2: Never Compromise Tests)

### Workflow

```
🚨 Production Bug Alert
    ↓
[git-workflow-helper] → Create hotfix branch (bugfix-XXX)
    ↓
[MANUAL] → Write test reproducing bug (RED phase)
    ↓
[MANUAL] → Implement minimal fix (GREEN phase)
    ↓
[tech-debt-detector] → Scan for CRITICAL issues only
    ↓
[git-workflow-helper] → Generate commit + push
    ↓
Hotfix Deployed ✓
```

### Example: API Timeout Bug

**Alert** (02:00 AM): API p99 latency 3000ms (SLA: 200ms)

**Step 1: Create Branch** (1 min)
```
You: "create branch for bugfix: API timeout"
→ git checkout -b bugfix-api-timeout
```

**Step 2: Reproduce Bug** (5 min)
```python
def test_api_timeout_bug():
    """Reproduce: API times out with N+1 queries"""
    response = api.get_tasks(user_id=1)

    # Currently: 2800ms (BUG!)
    # Expected: <200ms
    assert response.elapsed < 200  # FAILS (reproduces bug)
```

**Step 3: Fix Bug** (10 min)
```python
# OLD (N+1 queries):
tasks = Task.objects.filter(user_id=user_id)  # 1 query
for task in tasks:
    task.owner  # N queries! (BUG)

# NEW (1 query):
tasks = Task.objects.filter(user_id=user_id).select_related('owner')  # 1 query
```

**Step 4: Verify Fix** (2 min)
```
pytest tests/test_api_timeout_bug.py
→ PASS (8ms response time)
```

**Step 5: Scan for Issues** (2 min)
```
You: "check tech debt for CRITICAL issues only"

tech-debt-detector (fast scan):
→ 0 CRITICAL issues (debug code, secrets)
→ 2 HIGH issues (TODOs - acceptable for hotfix)

✅ No blockers
```

**Step 6: Commit & Deploy** (3 min)
```
You: "generate commit for hotfix"

git-workflow-helper:
→ Commit message:
  fix: resolve API timeout (N+1 query bug)

  Bug: API p99 latency 3000ms (SLA: 200ms)
  Root Cause: N+1 queries in get_tasks()
  Fix: Added select_related('owner')

  Performance:
  - Before: 2800ms avg
  - After: 8ms avg (350x faster)

  Tests: 1 new test (reproduces + verifies fix)

  🚨 Production Hotfix
```

**Total Time**: 23 minutes (alert → deployed)

**Quality Maintained**:
- ✅ Test written (even in emergency!)
- ✅ Root cause identified
- ✅ No CRITICAL tech debt introduced
- ✅ Performance verified (350x faster)

---

## Custom Orchestration

### Building Your Own Workflows

**5-Step Process**:

#### 1. Identify Task Sequence
```
Example: "I want to add a new feature"

Tasks:
1. Write specification
2. Validate spec quality
3. Plan iterations
4. Generate tests
5. Implement
6. Check quality
7. Commit
```

#### 2. Map Tasks to Agents
```
1. Write spec        → uc-writer
2. Validate spec     → spec-validator
3. Plan iterations   → iteration-planner
4. Generate tests    → test-writer
5. Implement         → MANUAL
6. Check quality     → code-quality-checker, tech-debt-detector
7. Commit            → git-workflow-helper
```

#### 3. Define Data Flow
```
uc-writer output (spec file)
    ↓
spec-validator input (reads spec file)
    ↓
spec-validator output (validation report)
    ↓
[User decision: if valid, proceed]
    ↓
iteration-planner input (reads spec file)
    ↓
...
```

#### 4. Add Checkpoints (User Approval Gates)
```
After uc-writer:
  → Review spec (does it match intent?)

After spec-validator:
  → If score <80, fix spec, re-validate

After iteration-planner:
  → Review iteration breakdown (reasonable?)

After test-writer:
  → Review tests (cover all cases?)
```

#### 5. Handle Errors/Branches
```
IF spec-validator FAILS (score <80):
  → STOP workflow
  → Fix spec issues
  → Re-run spec-validator
  → Resume from iteration-planner

IF code-quality-checker FAILS (score <80):
  → STOP workflow
  → Fix quality issues
  → Re-run code-quality-checker
  → Resume from commit
```

### Example: Custom CI/CD Pipeline

**Goal**: Automated quality checks on every commit

```yaml
# .github/workflows/quality-gate.yml

on: [push]

jobs:
  quality-gate:
    steps:
      - name: Code Quality Check
        run: claude-agent code-quality-checker --threshold 80

      - name: Tech Debt Scan
        run: claude-agent tech-debt-detector --critical-only

      - name: Spec Validation
        run: claude-agent spec-validator --all-specs

      - name: Traceability Check
        run: claude-agent uc-service-tracer

      # If all pass → deploy
      # If any fail → block deployment
```

---

## Performance Considerations

### Sequential vs. Parallel Execution

**Sequential** (data dependency):
```
✅ USE WHEN: Agent B needs Agent A output

Example:
uc-writer (creates spec) → spec-validator (reads spec)
└─ Must wait for spec file to exist
```

**Parallel** (independent agents):
```
✅ USE WHEN: Agents don't depend on each other

Example:
code-quality-checker ─┐
                      ├─→ [Both can run simultaneously]
tech-debt-detector ───┘

Speedup: 2x (10 min → 5 min)
```

### Optimization Strategies

#### 1. Scope Reduction
```
❌ Slow: "check tech debt in entire codebase" (2 min)
✅ Fast: "check tech debt in implementation/services/" (20 sec)

4x faster by limiting scope
```

#### 2. Targeted Scans
```
❌ Slow: "analyze all code for refactoring" (5 min)
✅ Fast: "analyze UserService for refactoring" (30 sec)

10x faster with specific target
```

#### 3. Incremental Validation
```
❌ Slow: "validate all 20 specs" (10 min)
✅ Fast: "validate only changed specs (UC-003, UC-005)" (1 min)

10x faster with incremental approach
```

#### 4. Caching
```
spec-validator caches results:
- First run: 3 min (reads all specs)
- Second run: 10 sec (only changed specs)

18x faster with caching
```

---

## Workflow Decision Tree

### ASCII Decision Tree

```
Starting new work?
├─ Yes: New Feature?
│  ├─ Yes: New UC?
│  │  ├─ Yes → Use Pattern 1 (Spec-to-Implementation)
│  │  └─ No → Use Pattern 2 (Session Lifecycle) + test-writer
│  └─ No: Bug Fix?
│     ├─ Production? → Use Pattern 6 (Emergency Hotfix)
│     └─ Development? → Write test + fix + quality check
│
└─ No: Ongoing work?
   ├─ Yes: Session start?
   │  └─ Yes → Use Pattern 2 (Session Lifecycle)
   │
   ├─ No: Ready to commit?
   │  ├─ Yes: Before merge?
   │  │  ├─ Yes → Use Pattern 3 (Quality Gate)
   │  │  └─ No → git-workflow-helper + tech-debt-detector
   │  │
   │  └─ No: Architecture design?
   │     ├─ Yes → Use Pattern 4 (Service Architecture)
   │     └─ No: Documentation?
   │        └─ Yes → Use Pattern 5 (Documentation Pipeline)
```

### Decision Table

| Scenario | Pattern | Agents | Duration |
|----------|---------|--------|----------|
| New feature (with UC) | Pattern 1 | 8 agents | 60-90 min |
| New feature (no UC) | Custom | 3-4 agents | 30-45 min |
| Session start | Pattern 2 | 1 agent | 5 min |
| Session end | Pattern 2 | 2 agents | 10 min |
| Before merge | Pattern 3 | 4 agents | 15-20 min |
| Service design | Pattern 4 | 6 agents | 45-60 min |
| Documentation | Pattern 5 | 3 agents | 30-45 min |
| Production bug | Pattern 6 | 2 agents | 20-30 min |
| Code review | Custom | 3 agents | 10-15 min |
| Refactoring | Custom | 2 agents | 15-30 min |

---

## Error Handling

### Common Failure Scenarios

#### 1. Agent Blocks Workflow (Validation Fails)

**Scenario**: spec-validator score <80, blocks implementation

**Error Handling**:
```
1. STOP workflow immediately
2. Review validation report (what's missing?)
3. Fix spec issues incrementally
4. Re-run spec-validator
5. Once valid (≥80), resume workflow from next agent
```

**Example**:
```
You: "plan iterations for UC-003"

Claude: Spec validation required first. Running spec-validator...
→ Score: 68/100 (FAIL)
→ Issues: Missing edge cases, only 3 ACs (min 5)

Claude: ❌ Cannot proceed with planning. Fix spec first.

You: [adds 3 more ACs, documents edge cases]

You: "validate UC-003 again"
→ Score: 88/100 (PASS)

You: "now plan iterations"
→ Proceeds successfully
```

---

#### 2. Agent Execution Fails (Technical Error)

**Scenario**: git-workflow-helper can't create branch (uncommitted changes)

**Error Handling**:
```
1. Agent reports error with diagnostic info
2. User fixes root cause
3. Retry agent operation
```

**Example**:
```
You: "create branch for iteration 2"

git-workflow-helper:
→ ❌ Error: Uncommitted changes in working directory
→ Files: implementation/user_service.py (modified)

git-workflow-helper:
→ Fix: Commit or stash changes first

You: [commits changes]

You: "create branch for iteration 2"
→ ✅ Branch created: iteration-002-email-verification
```

---

#### 3. Data Flow Broken (Missing Input)

**Scenario**: test-writer can't find spec file

**Error Handling**:
```
1. Agent reports missing dependency
2. User provides correct input
3. Retry agent
```

**Example**:
```
You: "generate tests for UC-007"

test-writer:
→ ❌ Error: Spec file not found
→ Expected: specs/use-cases/UC-007-*.md
→ Found: None

test-writer:
→ Fix: Create UC-007 spec first using uc-writer

You: "create use case for notifications"
→ uc-writer creates UC-007

You: "generate tests for UC-007"
→ ✅ Tests created successfully
```

---

### Recovery Strategies

#### Strategy 1: Restart from Failed Agent
```
Workflow: A → B → C → D
           ✓   ✓   ✗

Recovery:
1. Fix issue that caused C to fail
2. Re-run C
3. Continue to D
```

#### Strategy 2: Rollback and Retry
```
Workflow: A → B → C
           ✓   ✓   ✗ (B's output invalid)

Recovery:
1. Fix B's input
2. Re-run B (overwrites previous output)
3. Run C with corrected input
```

#### Strategy 3: Manual Override (Last Resort)
```
Workflow: A → B (stuck)

Recovery:
1. Complete B's task manually
2. Continue workflow from C
3. Document why manual override needed
```

---

## Related Documentation

- **Agent Library**: [.claude/AGENTS.md](../.claude/AGENTS.md) - Complete agent reference
- **Usage Guide**: [agent-guide.md](./agent-guide.md) - Practical agent usage
- **Examples**: [examples/README.md](./examples/README.md) - Real-world scenarios
- **Framework Core**: [claude-development-framework.md](./claude-development-framework.md) - Core principles

---

**Framework**: Claude Development Framework v2.1
**Version**: 1.0
**Last Updated**: 2025-10-02

Master agent orchestration for maximum productivity! 🚀
