# Agent Usage Guide

**Framework**: Claude Development Framework v2.1
**Last Updated**: 2025-10-02
**Purpose**: Practical guide to using the 18 specialized agents effectively

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started: Your First Agent](#getting-started-your-first-agent)
3. [Tier 1 Agents in Practice](#tier-1-agents-in-practice)
4. [Tier 2 Agents in Practice](#tier-2-agents-in-practice)
5. [Tier 3 Agents in Practice](#tier-3-agents-in-practice)
6. [Common Workflows](#common-workflows)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

---

## Introduction

### What Agents Do For You

Agents are specialized automation tools that handle repetitive, time-consuming development tasks:

**They automate**:
- ✅ Test generation from specifications (5 min vs. 45 min manual)
- ✅ Quality validation before commits (catches issues early)
- ✅ Git workflow (branch creation, commit messages)
- ✅ Documentation generation (API docs, session summaries)
- ✅ Architecture validation (dependencies, traceability)

**They enforce**:
- ✅ Framework rules (12 non-negotiables)
- ✅ Consistent patterns (templates, formats)
- ✅ Quality gates (no shortcuts, no tech debt)

### When to Use Agents vs. Manual Work

**Use Agents For**:
- Repetitive tasks (test generation, quality checks)
- Complex analysis (service extraction, dependency validation)
- Time-consuming work (documentation, refactoring analysis)
- Consistency enforcement (spec validation, code quality)

**Manual Work For**:
- Creative problem-solving
- Architectural decisions
- Business logic implementation
- One-off exploratory tasks

### How to Invoke Agents

**Method 1: Trigger Keywords** (Recommended)
```
You: "generate tests for UC-001"
→ Activates: test-writer agent
```

**Method 2: Direct Request**
```
You: "Use the spec-validator to check UC-003"
→ Activates: spec-validator agent
```

**Method 3: Proactive Activation**
- Some agents activate automatically when appropriate
- `git-workflow-helper` at session start (Phase 1)
- `session-summarizer` at session end (Phase 8)

---

## Getting Started: Your First Agent

### Example: Using test-writer

**Scenario**: You've written UC-001 (User Registration) and need tests.

**Step 1: Create UC Specification**
```bash
# File: specs/use-cases/UC-001-user-registration.md
# Contains: Acceptance Criteria section with 8 criteria
```

**Step 2: Invoke test-writer**
```
You: "generate tests for UC-001"
```

**Step 3: Agent Process** (what happens behind the scenes)
1. Reads `specs/use-cases/UC-001-user-registration.md`
2. Extracts 8 acceptance criteria
3. Generates test cases for each criterion
4. Adds edge cases and error scenarios
5. Shows preview: "I'll create 12 tests covering all criteria"

**Step 4: You Review**
```
Claude: "I'll create tests/test_user_registration.py with:
- 8 acceptance criteria tests
- 3 edge case tests
- 1 error handling test

Total: 12 tests. Approve?"
```

**Step 5: You Approve**
```
You: "yes, proceed"
```

**Step 6: Agent Executes**
- Writes `tests/test_user_registration.py`
- Uses template from `.claude/templates/test-template.md`
- Includes docstrings with UC references

**Outcome**:
- ✅ 12 tests created in **5 minutes** (vs. 45 minutes manual)
- ✅ 100% UC criteria coverage
- ✅ Consistent test structure
- ✅ Ready for RED phase (tests fail until implementation)

---

## Tier 1 Agents in Practice

### 1. test-writer: Generating Tests from Specs

**When to use**: After writing UC spec, before implementation (TDD RED phase)

**Trigger Keywords**: "generate tests", "write tests for UC-XXX", "create test file"

**Example Workflow**:

**Input**: UC-001 User Registration spec
```markdown
## Acceptance Criteria
1. User can register with email and password
2. Email must be unique
3. Password must be ≥8 characters
4. User receives confirmation email
5. User account is inactive until email verified
...
```

**Agent Process**:
```
1. Read spec file
2. Extract 8 acceptance criteria
3. Generate test cases:
   - test_user_can_register_with_valid_credentials()
   - test_email_must_be_unique()
   - test_password_minimum_length()
   - test_confirmation_email_sent()
   - test_account_inactive_until_verified()
   ...
4. Add edge cases (empty fields, SQL injection, XSS)
5. Add error scenarios (duplicate email, weak password)
```

**Output**: `tests/test_user_registration.py`
```python
"""
Tests for UC-001: User Registration
Specification: specs/use-cases/UC-001-user-registration.md
"""

def test_user_can_register_with_valid_credentials():
    """AC1: User can register with email and password"""
    # Arrange
    email = "test@example.com"
    password = "SecurePass123"

    # Act
    user = register_user(email, password)

    # Assert
    assert user.email == email
    assert user.password_hash != password  # Hashed

# ... 11 more tests
```

**Tips**:
- ✅ Review test data (realistic values)
- ✅ Check edge cases (agent might miss domain-specific ones)
- ✅ Verify UC references in docstrings
- ✅ Run tests (should fail initially - RED phase)

---

### 2. bdd-scenario-writer: Creating Gherkin Scenarios

**When to use**: For user-facing features needing acceptance tests (Rule #8)

**Trigger Keywords**: "write BDD scenarios", "generate Gherkin for UC-XXX", "create feature file"

**Example Workflow**:

**Input**: UC-002 User Login spec

**Agent Process**:
```
1. Read UC acceptance criteria
2. Convert to Given-When-Then format
3. Create scenario outlines for data variations
4. Add background steps (common setup)
```

**Output**: `features/user_login.feature`
```gherkin
Feature: User Login
  As a registered user
  I want to log in with my credentials
  So that I can access my account

  Background:
    Given the system is running
    And a user exists with email "test@example.com" and password "SecurePass123"

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter email "test@example.com"
    And I enter password "SecurePass123"
    And I click "Login"
    Then I should be redirected to the dashboard
    And I should see "Welcome back"

  Scenario Outline: Login fails with invalid credentials
    Given I am on the login page
    When I enter email "<email>"
    And I enter password "<password>"
    And I click "Login"
    Then I should see error "<error_message>"
    And I should remain on the login page

    Examples:
      | email              | password       | error_message          |
      | wrong@example.com  | SecurePass123  | Invalid email          |
      | test@example.com   | wrongpass      | Invalid password       |
      | invalid-email      | SecurePass123  | Invalid email format   |
      | test@example.com   | short          | Password too short     |
```

**Tips**:
- ✅ Executable with behave (Python) or cucumber (Ruby/JS)
- ✅ Scenario outlines for data-driven testing
- ✅ Clear, non-technical language (readable by stakeholders)

---

### 3. code-quality-checker: Validating Before Commit

**When to use**: Before git commit (Phase 9), during code review

**Trigger Keywords**: "check code quality", "validate quality", "run quality check"

**Example Workflow**:

**Input**: You've implemented user_service.py and want to commit

**Agent Process**:
```
1. Analyze code:
   - Type hints coverage
   - Docstring presence
   - Cyclomatic complexity
   - Linting (flake8/pylint)
   - Security issues

2. Score: 0-100 (passing ≥80)

3. Report findings with file:line references
```

**Output**: Quality Report
```
Code Quality Report: user_service.py

Score: 72/100 (FAIL - below 80 threshold)

Issues Found (15):

CRITICAL (3):
- Line 42: Missing type hint for return value
- Line 67: SQL query vulnerable to injection
- Line 89: Password stored in plain text

HIGH (5):
- Line 23: Missing docstring for register_user()
- Line 45: Cyclomatic complexity 12 (max 10)
- Line 78: Broad exception catch (except Exception)

MEDIUM (7):
- Line 12: Variable name 'x' not descriptive
- Line 34: Magic number 8 (extract to constant)
...

❌ Quality check FAILED. Fix issues before committing.
```

**Outcome**:
- Agent **BLOCKS commit** until issues fixed
- You fix 15 issues
- Re-run: Score 94/100 (PASS ✅)
- Commit proceeds

**Tips**:
- ✅ Run proactively (don't wait for commit)
- ✅ Fix issues incrementally (not all at once)
- ✅ Use file:line references for quick fixes
- ✅ Set up pre-commit hook for automation

---

### 4. refactoring-analyzer: Finding Improvements

**When to use**: After GREEN phase (tests passing), REFACTOR phase, before release

**Trigger Keywords**: "suggest refactoring", "analyze code for improvements", "find refactoring opportunities"

**Example Workflow**:

**Input**: Working code in user_service.py (tests passing)

**Agent Process**:
```
1. Analyze code smells:
   - Long functions (>50 lines)
   - Code duplication
   - Complex conditionals
   - God classes
   - Feature envy

2. Suggest refactorings with examples

3. Estimate impact (effort vs. benefit)
```

**Output**: Refactoring Report
```
Refactoring Analysis: user_service.py

Found 5 refactoring opportunities:

1. Extract Method (HIGH PRIORITY)
   Location: register_user() lines 45-78
   Issue: 34-line email validation logic embedded
   Suggestion:
     def validate_email(email: str) -> bool:
         # Extract lines 45-78 here

   Benefits:
   - Reusable in reset_password()
   - Testable independently
   - Complexity: 12 → 6
   Effort: 15 min

2. Replace Conditional with Polymorphism (MEDIUM)
   Location: authenticate_user() lines 89-112
   Issue: if/elif chain for auth methods (password, OAuth, SSO)
   Suggestion: Strategy pattern with AuthMethod interface
   Benefits:
   - Extensible (add new auth methods)
   - Complies with Open/Closed Principle
   Effort: 45 min

3. Remove Code Duplication (HIGH PRIORITY)
   Location: Lines 23-28, 67-72, 134-139
   Issue: Email format validation duplicated 3 times
   Suggestion: Use extracted validate_email() from #1
   Benefits:
   - DRY principle
   - Single source of truth
   Effort: 10 min

...

Priority Queue:
1. Extract validate_email() (15 min, high impact)
2. Remove duplication (10 min, high impact)
3. Strategy pattern for auth (45 min, medium impact)
```

**Tips**:
- ✅ Refactor incrementally (one at a time)
- ✅ Tests must still pass after each refactoring
- ✅ Prioritize high-impact, low-effort changes
- ✅ Update specs if behavior changes

---

### 5. uc-writer: Creating Specifications

**When to use**: At project start, when adding new features (Rule #1: Spec-First)

**Trigger Keywords**: "create use case for [feature]", "write UC spec", "generate use case"

**Example Workflow**:

**Input**: User requirement (verbal or written)
```
You: "We need a feature to let users prioritize their tasks"
```

**Agent Process**:
```
1. Interview user for requirements:
   - What task properties? (high/medium/low, numeric 1-10?)
   - Who can prioritize? (task owner only, or managers?)
   - UI requirements? (drag-and-drop, dropdown?)

2. Generate UC template with 16 sections:
   - Use Case ID
   - Title
   - Actors
   - Preconditions
   - Main Flow
   - Acceptance Criteria (8+)
   - Edge Cases
   - Error Scenarios
   ...

3. Populate from interview responses
```

**Output**: `specs/use-cases/UC-006-task-prioritization.md` (500 lines)
```markdown
# UC-006: Task Prioritization

## Use Case ID
UC-006

## Title
Allow users to set priority levels for tasks

## Actors
- Primary: Task Owner (user who created task)
- Secondary: Project Manager (can override priorities)

## Preconditions
- User is authenticated
- User has at least one task
- User has permission to edit task

## Main Flow
1. User navigates to task list
2. System displays tasks with current priorities
3. User selects task to prioritize
4. System shows priority dropdown (High/Medium/Low)
5. User selects priority
6. System updates task priority
7. System re-sorts task list by priority
8. System shows confirmation

## Acceptance Criteria
1. User can set priority to High/Medium/Low
2. Priority is visible in task list
3. Tasks are sorted by priority (High → Medium → Low)
4. Managers can override user-set priorities
5. Priority changes are logged in task history
6. Default priority is Medium for new tasks
7. Task priority affects due date calculations
8. Priority filter available in task search

## Edge Cases
- EC1: User sets priority while another user editing same task
  → Last write wins, show conflict warning
...

## Service Dependencies
- TaskService.update_task_priority()
- TaskService.get_tasks_by_priority()
- NotificationService.notify_priority_change()

## Traceability
- Iteration: TBD (assign in iteration planning)
- Tests: tests/test_task_prioritization.py (TBD)
- ADRs: TBD
```

**Tips**:
- ✅ Review for completeness (use spec-validator)
- ✅ Validate with stakeholders
- ✅ Add to iteration plan
- ✅ Generate tests before implementation

---

### 6. adr-manager: Documenting Decisions

**When to use**: When making technical decisions (Rule #7: Decisions Are Binding)

**Trigger Keywords**: "create ADR for [decision]", "document decision", "check ADR compliance"

**Example Workflow**:

**Scenario**: Choosing authentication library

**Input**:
```
You: "create ADR for using JWT for authentication"
```

**Agent Process**:
```
1. Create ADR file (ADR-004)
2. Populate template:
   - Status: Proposed/Accepted/Deprecated
   - Context: Why decision needed
   - Decision: What was chosen
   - Alternatives: What was considered
   - Consequences: Pros/cons
   - Compliance: How to verify

3. Link related UCs and services
```

**Output**: `planning/adrs/ADR-004-jwt-authentication.md`
```markdown
# ADR-004: Use JWT for Authentication

**Status**: Accepted
**Date**: 2025-10-02
**Deciders**: Tech Lead, Security Team

## Context
UC-002 (User Login) requires stateless authentication for API.
Need secure, scalable solution for 10,000+ concurrent users.

## Decision
Use **JSON Web Tokens (JWT)** with PyJWT library.

**Implementation**:
- Access tokens: 15-minute expiry
- Refresh tokens: 7-day expiry
- HS256 algorithm (symmetric)
- Claims: user_id, role, exp

## Alternatives Considered

### 1. Session-based Auth (Cookie)
**Pros**: Simple, built-in Django support
**Cons**: Stateful (requires Redis), not API-friendly
**Rejected**: Doesn't support mobile clients

### 2. OAuth2 (Authlib)
**Pros**: Industry standard, supports SSO
**Cons**: Complex, overkill for MVP
**Rejected**: Too much overhead for current needs

### 3. Custom Token System
**Pros**: Full control
**Cons**: Security risks, 3+ days development
**Rejected**: Reinventing wheel, security risk

## Consequences

**Positive**:
- ✅ Stateless (scales horizontally)
- ✅ Works with web + mobile + API
- ✅ Mature library (PyJWT 50M+ downloads)
- ✅ Small tokens (~200 bytes)

**Negative**:
- ❌ Cannot revoke tokens (until expiry)
- ❌ Requires refresh token mechanism
- ❌ Need secure key management

**Mitigations**:
- Short access token expiry (15 min)
- Refresh token rotation
- Store secrets in environment variables

## Compliance Check
- [ ] All auth endpoints use JWT validation
- [ ] Tokens expire in 15 minutes
- [ ] Refresh tokens stored securely (hashed)
- [ ] Unit tests for token generation/validation

## Related
- **UC-002**: User Login
- **UC-003**: User Logout
- **Services**: AuthService, TokenService
- **Tests**: tests/test_jwt_auth.py
```

**Tips**:
- ✅ Create ADR **before** implementation
- ✅ Include alternatives (shows due diligence)
- ✅ Update status when deprecated
- ✅ Use agent to check ADR compliance

---

## Tier 2 Agents in Practice

### 7. iteration-planner: Breaking Down Work

**When to use**: After UC created, before implementation (Rule #3, #5: Two-Level Planning)

**Trigger Keywords**: "plan iteration for UC-XXX", "break down use case", "create iteration plan"

**Example Workflow**:

**Input**: UC-001 User Registration (too large for single iteration)

**Agent Process**:
```
1. Analyze UC complexity:
   - 12 acceptance criteria
   - 3 service dependencies
   - Estimated effort: 8 hours

2. Break into iterations (max 3 hours each):
   - Iteration 1: Basic registration (email + password)
   - Iteration 2: Email verification
   - Iteration 3: Password strength + security

3. Generate iteration specs with:
   - Scope (which ACs)
   - Tests (which test files)
   - Duration estimate
   - Dependencies
   - Success criteria
```

**Output**: `planning/iterations/UC-001-user-registration/`
```
iteration-01-basic-registration.md  (scope: AC1-4, est: 2h 30min)
iteration-02-email-verification.md  (scope: AC5-8, est: 2h 45min)
iteration-03-security-hardening.md  (scope: AC9-12, est: 2h 15min)
```

**iteration-01-basic-registration.md**:
```markdown
# Iteration 1: Basic Registration

## Iteration ID
UC-001-IT-001

## Parent Use Case
UC-001: User Registration

## Scope
**Acceptance Criteria**: AC1-4
- AC1: User can register with email + password
- AC2: Email must be unique
- AC3: Password must be ≥8 characters
- AC4: User receives confirmation email

## Out of Scope (Future Iterations)
- Email verification (Iteration 2)
- Password strength meter (Iteration 3)
- Social auth (Future UC)

## Estimated Duration
2 hours 30 minutes

## Tasks
1. [30 min] Write tests (test_basic_registration.py) - 8 tests
2. [45 min] Implement UserService.register()
3. [30 min] Implement email uniqueness check
4. [25 min] Integrate EmailService for confirmation
5. [20 min] Run tests, fix bugs

## Tests
- tests/test_basic_registration.py (8 tests)
- Expected: 8 failing → 8 passing

## Dependencies
- Services: UserService, EmailService
- Infrastructure: Database, email server

## Success Criteria
- [ ] All 8 tests passing
- [ ] No TODOs in code
- [ ] Code quality score ≥80
- [ ] Commit with spec reference
```

**Tips**:
- ✅ Keep iterations **under 3 hours**
- ✅ Each iteration independently testable
- ✅ Clear scope (what's IN, what's OUT)
- ✅ Estimate conservatively (add 25% buffer)

---

### 8. spec-validator: Checking Quality

**When to use**: After creating/updating UC or service spec (Rule #1 enforcement)

**Trigger Keywords**: "validate spec", "check UC-XXX", "verify specification quality"

**Example Workflow**:

**Input**: UC-003 spec (user wants to validate before implementation)

**Agent Process**:
```
1. Check 16 required sections:
   - Use Case ID ✓
   - Title ✓
   - Actors ✓
   - Preconditions ✓
   - Main Flow ✓
   - Acceptance Criteria ✓
   - ...

2. Validate content quality:
   - Acceptance criteria count (min 5)
   - Edge cases documented
   - Error scenarios defined
   - Service dependencies listed
   - Traceability complete

3. Score: 0-100 (passing ≥80)
```

**Output**: Validation Report
```
Specification Validation: UC-003-user-logout.md

Score: 68/100 (FAIL - below 80 threshold)

Section Completeness: 14/16 sections ✓

Issues Found (8):

CRITICAL (2):
✗ Missing: Edge Cases section
✗ Missing: Service Dependencies

HIGH (3):
⚠ Acceptance Criteria: Only 3 criteria (min 5 recommended)
⚠ Main Flow: Step 4 unclear ("System does stuff")
⚠ Traceability: No iteration assigned

MEDIUM (3):
⚠ Error Scenarios: Generic ("System shows error")
⚠ Preconditions: Missing "User must be logged in"
⚠ Non-Functional: No performance requirements

---

Recommendations:

1. Add Edge Cases section:
   - What if user has multiple sessions?
   - What if logout happens during active request?
   - What if network fails during logout?

2. Add Service Dependencies:
   - Which services handle logout?
   - Token invalidation service?
   - Session cleanup service?

3. Expand Acceptance Criteria (3 → 8):
   - User can logout from web
   - User can logout from mobile
   - All tokens invalidated
   - Session removed from database
   - Redirect to login page
   ...

4. Clarify Main Flow step 4:
   Current: "System does stuff"
   Better: "System invalidates access token and removes session"

---

❌ Specification INVALID. Cannot proceed with implementation.
```

**Outcome**:
- Agent **BLOCKS implementation** until spec valid
- User fixes 8 issues
- Re-validate: Score 92/100 (PASS ✅)
- Implementation can proceed

**Tips**:
- ✅ Validate **before** iteration planning
- ✅ Fix issues immediately (don't defer)
- ✅ Use validation checklist (in agent output)
- ✅ Re-validate after major spec changes

---

### 9. git-workflow-helper: Automating Git

**When to use**: Session start (Phase 1), before work (Phase 3), session end (Phase 9)

**Trigger Keywords**: "create branch for iteration X", "generate commit message", "check git status"

**4 Operating Modes**:

#### Mode 1: Git Status Check (Session Start - Phase 1)
```
You: "check git status"

Output:
Git Status Report:

Current Branch: main
Status: Clean (no uncommitted changes)

Recent Commits (last 5):
- eae3562 (2 hours ago) docs: AGENTS.md (Phase 2.1)
- 70ee345 (3 hours ago) feat: tech-debt-detector + doc-generator
- 6507239 (4 hours ago) feat: session-summarizer (Tier 2 #4/4)

Untracked Files: None

Recommendation:
✓ Ready to start work
✓ Create feature branch for new iteration
```

#### Mode 2: Branch Creation (Before Work - Phase 3)
```
You: "create branch for iteration 2"

Agent Process:
1. Verify on main branch
2. Pull latest: git pull origin main
3. Determine branch name: iteration-002-email-verification
4. Create branch: git checkout -b iteration-002-email-verification

Output:
Branch created: iteration-002-email-verification

Branch naming follows Rule #11:
- iteration-XXX: For planned iterations
- uc-XXX: For entire use case
- bugfix-XXX: For bug fixes
- spike-XXX: For exploratory work

You're now on: iteration-002-email-verification
Ready to start TDD cycle.
```

#### Mode 3: Commit Message Generation (Session End - Phase 9)
```
You: "generate commit message"

Agent Process:
1. Run git diff (analyze changes)
2. Count tests: grep "def test_" tests/
3. Identify specification: grep "UC-" specs/
4. Check test status: pytest --tb=short

Output:
Generated Commit Message:

feat: email verification workflow (iteration 2)

Implemented UC-001 iteration 2: email verification.

Changes:
- Email verification token generation (UserService)
- Verification email template (EmailService)
- verify_email() endpoint (AuthController)
- Token expiry logic (24 hours)

Tests: 12 passing / 12 total
Coverage: 94% (target: 90%)

Specification: UC-001-user-registration (iteration 2)
Framework: Claude Development Framework v2.1

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>

---

Commit? (yes/no)
```

#### Mode 4: Pre-Commit Validation
```
Agent checks before commit:
✓ All tests passing (12/12)
✓ No TODO comments
✓ No debug code (print, console.log)
✓ On feature branch (not main)
✓ Spec references present

Result: ✅ Ready to commit
```

**Tips**:
- ✅ Always use branch naming convention
- ✅ Validate before commit (catches issues)
- ✅ Let agent generate commit messages (consistent format)
- ✅ Never commit directly to main

---

### 10. session-summarizer: Documenting Sessions

**When to use**: Session end (Phase 8), when context filling up, before long break

**Trigger Keywords**: "end session", "generate session summary", "create session state"

**Example Workflow**:

**Scenario**: Completed iteration 2, need to end session

**Input**:
```
You: "end session and generate summary"
```

**Agent Process**:
```
1. Analyze conversation:
   - Work completed
   - Decisions made
   - Blockers encountered
   - Questions raised

2. Check git history:
   - Commits made this session
   - Files changed
   - Test count changes

3. Determine current state:
   - Active iteration
   - Next steps
   - Pending tasks

4. Generate session-state.md (NO PLACEHOLDERS!)
```

**Output**: `session-state.md`
```markdown
# Session State

**Date**: 2025-10-02 14:30
**Duration**: 2h 15min
**Framework**: v2.1

---

## Work Completed (This Session)

**Iteration 2**: Email Verification (UC-001)

**Implemented**:
- Email verification token generation (UserService.create_verification_token)
  - 24-hour expiry
  - Cryptographically secure random tokens
  - Stored in database with user_id linkage

- Verification email template (EmailService)
  - HTML + plain text versions
  - Click-to-verify link with token
  - Resend verification option

- verify_email() endpoint (AuthController)
  - Token validation
  - Account activation
  - Error handling (expired, invalid, already verified)

**Tests**: 12 passing / 12 total
- test_create_verification_token() ✓
- test_verification_email_sent() ✓
- test_verify_with_valid_token() ✓
- test_verify_with_expired_token() ✓
- test_verify_already_verified() ✓
- ... (7 more)

**Coverage**: 94% (target: 90% ✓)

---

## Decisions Made

**ADR-005**: Email verification token expiry
- **Decision**: 24-hour expiry for verification tokens
- **Rationale**: Balance security (short-lived) vs. UX (not too short)
- **Alternatives**: 1 hour (too short), 7 days (security risk)

**Technical Choice**: Use secrets.token_urlsafe(32) for tokens
- Cryptographically secure
- URL-safe (no encoding needed)
- 32 bytes = 256 bits entropy

---

## Blockers Encountered

**NONE** this session

---

## Questions Raised

1. **Q**: Should verification emails be rate-limited?
   **A**: Yes - added to UC-001 iteration 3 scope (max 3 emails/hour)

2. **Q**: What if user changes email before verifying?
   **A**: Invalidate old token, send new one - added to edge cases

---

## Files Modified

**Implementation** (3 files):
- implementation/services/user_service.py (+45 lines)
- implementation/services/email_service.py (+32 lines)
- implementation/controllers/auth_controller.py (+28 lines)

**Tests** (1 file):
- tests/test_email_verification.py (NEW, 210 lines, 12 tests)

**Specs** (1 file):
- specs/use-cases/UC-001-user-registration.md (updated edge cases)

---

## Current Iteration Status

**Iteration 2** (UC-001): Email Verification
**Status**: ✅ COMPLETE

**Acceptance Criteria**: 4/4 complete
- AC5: User receives verification email ✓
- AC6: User can verify via link ✓
- AC7: Account inactive until verified ✓
- AC8: Verification token expires (24h) ✓

**Duration**: 2h 15min (estimated: 2h 45min - **30min under!**)

---

## Next Steps

1. **Iteration 3** (UC-001): Password strength + security
   - Estimated: 2h 15min
   - Scope: AC9-12 (strength meter, breach check, lockout)
   - Branch: iteration-003-password-security

2. **Before Next Session**:
   - Review ADR-005 (verify 24h expiry acceptable)
   - Consider rate limiting design (ADR needed?)

3. **Technical Debt**: None

---

## Context

**Active Use Cases**: UC-001 (2/3 iterations complete)
**Tests**: 24 total (24 passing)
**Coverage**: 94%
**Current Branch**: iteration-002-email-verification (ready to merge)

---

## Session Metrics

**Lines of Code**: +315 (implementation + tests)
**Tests Added**: 12
**Bugs Found**: 0
**Refactorings**: 0
**Time Saved**: Agent automation ~45 min (test generation, commit messages)

---

## Recovery Information

**To Resume**:
1. Read this session-state.md
2. Checkout iteration-002-email-verification
3. Run tests: `pytest tests/` (should be 24/24 passing)
4. Review UC-001 spec: `specs/use-cases/UC-001-user-registration.md`
5. Start iteration 3: "create branch for iteration 3"

**Key Files**:
- Current iteration: planning/iterations/UC-001/iteration-02-email-verification.md
- Next iteration: planning/iterations/UC-001/iteration-03-password-security.md
```

**Tips**:
- ✅ Generate summary **every session** (even short ones)
- ✅ Include specific details (no "implemented some features")
- ✅ Document decisions (even small ones)
- ✅ List exact next steps (makes resume easy)

---

## Tier 3 Agents in Practice

### 11. tech-debt-detector: Finding Issues

**When to use**: Before commits (Phase 9), before release, periodic scans

**Trigger Keywords**: "check tech debt", "scan for issues", "find TODOs"

**Example Workflow**:

**Scenario**: Before committing, check for tech debt

**Input**:
```
You: "check tech debt in implementation/"
```

**Agent Process**:
```
1. Scan for patterns:
   - TODO/FIXME comments
   - Debug code (print, console.log, debugger)
   - Hardcoded secrets
   - Broad exception handlers
   - Missing error handling
   - Missing type hints

2. Categorize by severity:
   - CRITICAL: Blocks commit
   - HIGH: Should fix
   - MEDIUM: Consider fixing
   - LOW: Nice to have

3. Calculate tech debt score (0-100)
```

**Output**: Tech Debt Report
```
Tech Debt Scan: implementation/ (recursive)

Tech Debt Score: 45/100 (HIGH DEBT - refactoring recommended)

Issues Found (23):

CRITICAL (3) - 🚨 BLOCKS COMMIT:
✗ user_service.py:67 - Hardcoded API key
  → api_key = "sk_live_1234567890abcdef"
  Fix: Move to environment variable

✗ auth_controller.py:89 - SQL injection vulnerability
  → query = f"SELECT * FROM users WHERE email='{email}'"
  Fix: Use parameterized query

✗ email_service.py:45 - Debug print() statement
  → print(f"DEBUG: Sending email to {user.email}")
  Fix: Remove or replace with logging

HIGH (8) - Should fix before commit:
⚠ user_service.py:23 - TODO: Add password hashing
⚠ user_service.py:45 - TODO: Validate email format
⚠ user_service.py:78 - Broad exception: except Exception
⚠ auth_controller.py:34 - Missing error handling
⚠ email_service.py:12 - NotImplementedError in send_verification()
... (3 more)

MEDIUM (7) - Consider fixing:
⚠ user_service.py:12 - Missing type hint for 'email' parameter
⚠ user_service.py:28 - Missing docstring
⚠ email_service.py:56 - Magic number: 3600 (extract to constant)
... (4 more)

LOW (5) - Nice to have:
• user_service.py:89 - Variable name 'x' not descriptive
• auth_controller.py:23 - Function too long (78 lines, max 50)
... (3 more)

---

Breakdown by Category:
- Security Issues: 2 (CRITICAL)
- Debug Code: 1 (CRITICAL)
- TODOs: 5 (HIGH)
- Error Handling: 3 (HIGH)
- Code Quality: 12 (MEDIUM/LOW)

---

Priority Fix Queue:
1. Remove hardcoded API key (CRITICAL, 2 min)
2. Fix SQL injection (CRITICAL, 5 min)
3. Remove debug print (CRITICAL, 1 min)
4. Implement password hashing (HIGH, 15 min)
5. Add email validation (HIGH, 10 min)

---

❌ COMMIT BLOCKED due to 3 CRITICAL issues.
Fix critical issues, then re-scan.
```

**Outcome**:
- Agent **BLOCKS commit** (CRITICAL issues present)
- User fixes 3 critical issues (18 min)
- Re-scan: Score 78/100 (MEDIUM debt - commit allowed)
- User continues to fix HIGH issues

**Tips**:
- ✅ Run scan **before every commit**
- ✅ Fix CRITICAL issues immediately (non-negotiable)
- ✅ Track HIGH issues (address in next iteration)
- ✅ Set up pre-commit hook for automation

---

### 12. doc-generator: Creating Documentation

**When to use**: After feature completion, before release, for public APIs

**Trigger Keywords**: "generate API docs", "create README", "document service interface"

**Example Workflow**:

**Scenario**: Generate API documentation for UserService

**Input**:
```
You: "generate API docs for UserService"
```

**Agent Process**:
```
1. Find service file: implementation/services/user_service.py
2. Extract:
   - Class definition
   - Method signatures
   - Docstrings (Google/NumPy style)
   - Type hints
   - Parameters, returns, raises

3. Generate markdown tables and examples
```

**Output**: `docs/api/UserService.md`
```markdown
# UserService API Documentation

**Module**: `implementation.services.user_service`
**Version**: 1.0
**Last Updated**: 2025-10-02

---

## Overview

UserService handles user account management including registration, authentication, and profile updates.

**Responsibilities**:
- User registration and email verification
- Password hashing and validation
- User account lifecycle (activate, deactivate, delete)
- Profile management

**Dependencies**:
- EmailService (email verification)
- TokenService (JWT generation)
- Database (user persistence)

---

## Class: UserService

### Methods

#### register_user

```python
def register_user(email: str, password: str) -> User
```

Register a new user with email and password.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| email | str | Yes | User email address (must be unique) |
| password | str | Yes | User password (min 8 chars) |

**Returns**:
| Type | Description |
|------|-------------|
| User | Newly created user object (inactive until email verified) |

**Raises**:
| Exception | When |
|-----------|------|
| ValueError | Email already exists |
| ValueError | Password too short (<8 chars) |
| ValueError | Invalid email format |

**Example**:
```python
from services.user_service import UserService

user_service = UserService()

# Register new user
user = user_service.register_user(
    email="alice@example.com",
    password="SecurePass123"
)

# User is created but inactive
assert user.email == "alice@example.com"
assert user.is_active == False
assert user.id is not None
```

**Related**:
- Use Case: UC-001 (User Registration)
- Tests: tests/test_user_registration.py
- ADR: ADR-003 (Password hashing with bcrypt)

---

#### verify_email

```python
def verify_email(token: str) -> User
```

Verify user email with verification token.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| token | str | Yes | Email verification token (from email link) |

**Returns**:
| Type | Description |
|------|-------------|
| User | Verified and activated user object |

**Raises**:
| Exception | When |
|-----------|------|
| ValueError | Token invalid or expired |
| ValueError | User already verified |

**Example**:
```python
# User clicks verification link with token
token = "abc123xyz789..."

user = user_service.verify_email(token)

# User is now active
assert user.is_active == True
assert user.email_verified_at is not None
```

---

[Continue for all methods...]

---

## Usage Patterns

### Complete Registration Flow
```python
# 1. Register user
user = user_service.register_user("bob@example.com", "SecurePass123")

# 2. Verification email sent automatically (via EmailService)

# 3. User clicks link, verify email
verified_user = user_service.verify_email(user.verification_token)

# 4. User can now login
authenticated = user_service.authenticate("bob@example.com", "SecurePass123")
```

### Error Handling
```python
try:
    user = user_service.register_user(email, password)
except ValueError as e:
    if "already exists" in str(e):
        # Email duplicate - show error
        flash("Email already registered")
    elif "too short" in str(e):
        # Password weak - show error
        flash("Password must be ≥8 characters")
```

---

## Testing

**Test Coverage**: 94%
**Test File**: tests/test_user_service.py
**Total Tests**: 18

**Key Test Cases**:
- Registration with valid credentials
- Registration with duplicate email (fails)
- Registration with weak password (fails)
- Email verification with valid token
- Email verification with expired token (fails)
- Password update with current password validation

---

## Configuration

**Environment Variables**:
- `PASSWORD_MIN_LENGTH`: Minimum password length (default: 8)
- `VERIFICATION_TOKEN_EXPIRY`: Token expiry in seconds (default: 86400 = 24h)

**Database Tables**:
- `users`: User accounts
- `verification_tokens`: Email verification tokens

---

**Framework**: Claude Development Framework v2.1
**Generated**: 2025-10-02
```

**Tips**:
- ✅ Keep docs in sync with code (regenerate after changes)
- ✅ Include examples (copy-paste ready)
- ✅ Document error scenarios (not just happy path)
- ✅ Link to related specs, tests, ADRs

---

## Common Workflows

### Workflow 1: Starting New Use Case
**Duration**: 60-90 minutes
**Agents**: 4

```
1. uc-writer: Create use case specification (15 min)
   You: "create use case for task prioritization"
   → specs/use-cases/UC-006-task-prioritization.md

2. spec-validator: Validate specification (5 min)
   You: "validate UC-006"
   → Score: 92/100 ✓ (valid)

3. iteration-planner: Break into iterations (15 min)
   You: "plan iterations for UC-006"
   → 3 iterations (2h each)

4. test-writer: Generate tests for iteration 1 (5 min)
   You: "generate tests for UC-006 iteration 1"
   → tests/test_task_priority_basic.py (8 tests)

→ Ready to implement! (Total: 40 min setup vs. 3+ hours manual)
```

### Workflow 2: Completing Feature
**Duration**: 15-20 minutes
**Agents**: 5

```
1. code-quality-checker: Validate quality (5 min)
   You: "check code quality"
   → Score: 88/100 ✓

2. refactoring-analyzer: Find improvements (3 min)
   You: "suggest refactoring"
   → 2 minor suggestions (optional)

3. tech-debt-detector: Scan for issues (3 min)
   You: "check tech debt"
   → Score: 85/100 ✓ (no critical issues)

4. git-workflow-helper: Generate commit (2 min)
   You: "generate commit message"
   → Commit created with spec refs

5. session-summarizer: Document work (5 min)
   You: "end session"
   → session-state.md created

→ Feature complete with quality! (Total: 18 min vs. 1+ hour manual)
```

### Workflow 3: Service Architecture Design
**Duration**: 45-60 minutes
**Agents**: 5 (service-oriented)

```
1. service-extractor: Extract services from UCs (10 min)
2. service-designer: Design interfaces (15 min)
3. service-dependency-analyzer: Validate architecture (5 min)
4. uc-service-tracer: Check traceability (5 min)
5. service-library-finder: Evaluate libraries (15 min)

→ Complete service layer designed! (Total: 50 min vs. 4+ hours manual)
```

### Workflow 4: Quality Gate (Before Merge)
**Duration**: 10-15 minutes
**Agents**: 3

```
1. code-quality-checker: "check quality" → Score ≥80
2. tech-debt-detector: "check tech debt" → No CRITICAL issues
3. spec-validator: "validate all specs" → All specs valid

→ Merge approved!
```

### Workflow 5: Emergency Hotfix
**Duration**: 20-30 minutes
**Agents**: Minimal (2)

```
1. git-workflow-helper: "create branch for bugfix"
2. [Manual fix + tests]
3. tech-debt-detector: "check tech debt" (CRITICAL only)
4. git-workflow-helper: "generate commit"

→ Hotfix deployed (tests still required, even in emergency!)
```

### Workflow 6: Documentation Sprint
**Duration**: 30-45 minutes
**Agents**: 2

```
1. doc-generator: "generate API docs for all services"
   → docs/api/*.md (one per service)

2. session-summarizer: "generate summary"
   → session-state.md (what was documented)

→ Complete API documentation!
```

### Workflow 7: Refactoring Session
**Duration**: 60-90 minutes
**Agents**: 3

```
1. refactoring-analyzer: "analyze codebase" (15 min)
   → 10 refactoring opportunities

2. [Implement top 3 refactorings] (45 min)
   → Tests must still pass after each!

3. code-quality-checker: "check quality" (5 min)
   → Verify improvements (score increased)

→ Cleaner code, same functionality
```

### Workflow 8: Iteration Execution (TDD)
**Duration**: 2-3 hours
**Agents**: 4

```
1. git-workflow-helper: "create branch for iteration X"

2. test-writer: "generate tests for iteration X"
   → RED phase (tests fail)

3. [Implement until tests pass]
   → GREEN phase (tests pass)

4. refactoring-analyzer: "suggest refactoring"
   → REFACTOR phase (improve code)

5. git-workflow-helper: "generate commit"

→ One iteration complete!
```

### Workflow 9: BDD Feature Development
**Duration**: 1-2 hours
**Agents**: 3

```
1. bdd-scenario-writer: "write BDD for UC-XXX" (10 min)
   → features/feature_name.feature

2. test-writer: "generate step definitions" (15 min)
   → tests/steps/step_definitions.py

3. [Implement feature] (60 min)

→ Executable specification!
```

### Workflow 10: Project Setup
**Duration**: 30-45 minutes
**Agents**: 3

```
1. uc-writer: "create use cases for all features" (20 min)
   → 5 use case specs

2. service-extractor: "extract services from all UCs" (10 min)
   → 8 service specs

3. iteration-planner: "plan iterations for all UCs" (15 min)
   → 20 iterations (roadmap complete)

→ Project planned!
```

---

## Troubleshooting

### Problem 1: Agent Doesn't Respond
**Symptoms**: You use trigger keyword, agent doesn't activate

**Solutions**:
1. **Be more specific**:
   - ❌ "check this"
   - ✅ "check code quality in user_service.py"

2. **Use direct request**:
   - "Use the test-writer agent to generate tests for UC-001"

3. **Check file paths**:
   - Agent needs correct spec file path
   - "generate tests for specs/use-cases/UC-001-user-registration.md"

### Problem 2: Agent Output Wrong
**Symptoms**: Generated tests don't match spec, wrong assumptions

**Solutions**:
1. **Review input spec**:
   - Agent works from spec content
   - Validate spec first: "validate UC-001"

2. **Provide more context**:
   - "generate tests for UC-001, focus on edge cases"
   - "use pytest fixtures for database setup"

3. **Iterate**:
   - Review agent output
   - "regenerate with [specific changes]"

### Problem 3: Quality Check Fails
**Symptoms**: code-quality-checker score <80, blocks commit

**Solutions**:
1. **Fix issues incrementally**:
   - Start with CRITICAL (required)
   - Then HIGH (important)
   - Then MEDIUM (nice to have)

2. **Use file:line references**:
   - Agent provides exact locations
   - Fix one at a time, re-check

3. **Adjust standards** (if needed):
   - Modify `.claude/templates/code-quality-template.md`
   - Update thresholds (use sparingly!)

### Problem 4: Spec Validation Fails
**Symptoms**: spec-validator score <80, blocks implementation

**Solutions**:
1. **Follow checklist**:
   - Agent lists missing sections
   - Add each section one by one

2. **Use templates**:
   - `.claude/templates/use-case-template.md`
   - `.claude/templates/service-spec-template.md`

3. **Expand content**:
   - "Acceptance Criteria: Only 3 (min 5)"
   - Add 2 more criteria, re-validate

### Problem 5: Tests Generated Incorrectly
**Symptoms**: test-writer creates tests that don't match UC

**Solutions**:
1. **Check AC section**:
   - Agent extracts from "Acceptance Criteria"
   - Ensure ACs are clear, specific

2. **Specify test framework**:
   - "generate pytest tests for UC-001"
   - "use unittest for UC-002"

3. **Review and adjust**:
   - Agent provides preview
   - Request changes before execution

### Problem 6: Commit Blocked (Tech Debt)
**Symptoms**: tech-debt-detector finds CRITICAL issues, blocks commit

**Solutions**:
1. **Fix CRITICAL immediately**:
   - Security issues (hardcoded secrets, SQL injection)
   - Debug code (print, console.log)
   - Cannot defer these!

2. **Create tech debt tasks**:
   - HIGH issues → next iteration tasks
   - MEDIUM issues → backlog
   - LOW issues → optional

### Problem 7: Git Workflow Errors
**Symptoms**: git-workflow-helper fails to create branch

**Solutions**:
1. **Check current state**:
   - "check git status"
   - Ensure on main, no uncommitted changes

2. **Pull latest**:
   - "git pull origin main"
   - Then create branch

3. **Use correct naming**:
   - iteration-XXX (planned work)
   - bugfix-XXX (bug fixes)
   - spike-XXX (exploration)

### Problem 8: Agent Takes Too Long
**Symptoms**: Agent processing for 2+ minutes

**Solutions**:
1. **Scope down**:
   - ❌ "analyze entire codebase"
   - ✅ "analyze implementation/services/"

2. **Use targeted scans**:
   - tech-debt-detector: scan specific files
   - refactoring-analyzer: focus on one service

3. **Check file sizes**:
   - Large files (>1000 lines) slow agents
   - Refactor into smaller modules

### Problem 9: Documentation Out of Sync
**Symptoms**: doc-generator creates docs that don't match code

**Solutions**:
1. **Update docstrings first**:
   - Agent extracts from docstrings
   - Ensure docstrings current

2. **Regenerate after changes**:
   - "regenerate API docs for UserService"
   - Delete old docs first

3. **Version docs**:
   - Add "Last Updated" timestamps
   - Track which code version docs match

### Problem 10: Session Summary Too Generic
**Symptoms**: session-summarizer creates vague summary

**Solutions**:
1. **Provide context**:
   - Mention specific work completed
   - "I completed iteration 2, email verification"

2. **Check git history**:
   - Agent analyzes commits
   - Ensure commits have good messages

3. **Be specific in conversation**:
   - Agent summarizes from chat
   - Describe what you did clearly

---

## Best Practices

### 1. Use Agents Proactively
Don't wait to be asked. Agents work best when invoked at the right time:
- **Session start**: "check git status"
- **Before implementation**: "generate tests"
- **Before commit**: "check tech debt"
- **Session end**: "end session"

### 2. Chain Agent Outputs
Use one agent's output as next agent's input:
```
uc-writer → spec-validator → iteration-planner → test-writer
```

### 3. Review Before Approving
Agents assist, you decide:
- Read generated tests (do they match intent?)
- Check quality reports (are scores fair?)
- Validate commit messages (accurate?)

### 4. Update Specs First
Agents work from specifications:
- Spec changes → Regenerate tests
- New requirements → Update UC → Re-validate

### 5. Trust But Verify
Agents are reliable but not perfect:
- Check critical outputs (security, data integrity)
- Run tests after agent changes
- Code review agent-generated code

### 6. Use Validation Gates
Prevent issues early:
- spec-validator before implementation
- code-quality-checker before commit
- tech-debt-detector before merge

### 7. Leverage Patterns
Agents implement framework patterns:
- Use case structure (16 sections)
- Test structure (Arrange-Act-Assert)
- Commit format (conventional commits)

### 8. Iterate on Agent Outputs
Not perfect first time? Refine:
- "regenerate with more edge cases"
- "check quality again after fixes"
- "validate spec with stricter criteria"

### 9. Combine Manual + Agent Work
Hybrid approach works best:
- Agents for repetitive tasks
- You for creative problem-solving
- Agents for validation
- You for decisions

### 10. Document Agent Usage
Track which agents used when:
- In session-state.md
- In commit messages
- Helps debug issues

### 11. Keep Agents Updated
Templates evolve:
- Review `.claude/subagents/` periodically
- Update agent prompts for your domain
- Share improvements with team

### 12. Use Appropriate Tiers
Not every task needs every agent:
- **Quick fix**: Tier 1 only (test-writer, quality-checker)
- **Feature**: Tier 1+2 (add planner, git-helper)
- **Release**: All tiers (add tech-debt, doc-gen)

### 13. Monitor Agent Performance
Track time savings:
- Manual: 45 min test writing
- Agent: 5 min
- **Saved**: 40 min (89%)

### 14. Learn Agent Capabilities
Read agent files (`.claude/subagents/`):
- What they can do
- What they can't do
- When to use each

### 15. Handle Agent Failures Gracefully
Agent blocked by issue?
- Fix root cause (not agent)
- Invalid spec → Fix spec
- Tech debt → Fix debt

### 16. Use Agents for Learning
New to framework? Let agents guide:
- uc-writer shows UC structure
- test-writer shows test patterns
- git-workflow-helper shows workflow

### 17. Respect Agent Boundaries
Agents enforce rules (by design):
- spec-validator blocks bad specs → Fix spec
- tech-debt-detector blocks commits → Fix debt
- Don't fight the agents, fix the issues

### 18. Optimize Agent Workflows
Find your rhythm:
- Morning: Planning agents (uc-writer, iteration-planner)
- Development: Test/quality agents (test-writer, quality-checker)
- End of day: Summary agents (session-summarizer)

### 19. Share Agent Best Practices
Team using framework? Document patterns:
- Which agents for which tasks
- Common workflows (see section above)
- Team-specific customizations

### 20. Measure Agent ROI
Track benefits:
- Time saved (40-60% estimated)
- Bugs prevented (quality gates)
- Consistency improved (templates)
- Onboarding faster (agents teach framework)

---

## Quick Reference Card

### Agent Invocation Cheat Sheet

| I Want To... | Say This... | Agent Activates |
|--------------|-------------|-----------------|
| Start session | "check git status" | git-workflow-helper |
| Create UC | "create use case for [feature]" | uc-writer |
| Validate UC | "validate UC-XXX" | spec-validator |
| Plan iterations | "plan iterations for UC-XXX" | iteration-planner |
| Generate tests | "generate tests for UC-XXX" | test-writer |
| Write BDD | "write BDD scenarios for UC-XXX" | bdd-scenario-writer |
| Create branch | "create branch for iteration X" | git-workflow-helper |
| Check quality | "check code quality" | code-quality-checker |
| Find improvements | "suggest refactoring" | refactoring-analyzer |
| Check debt | "check tech debt" | tech-debt-detector |
| Generate docs | "generate API docs for [service]" | doc-generator |
| Document decision | "create ADR for [decision]" | adr-manager |
| Create commit | "generate commit message" | git-workflow-helper |
| End session | "end session" | session-summarizer |

### Agent Quality Gates

| Gate | Agent | Threshold | Action if Fail |
|------|-------|-----------|---------------|
| Spec Valid | spec-validator | ≥80/100 | Block implementation |
| Code Quality | code-quality-checker | ≥80/100 | Block commit |
| Tech Debt | tech-debt-detector | 0 CRITICAL | Block commit |
| Tests Passing | git-workflow-helper | 100% pass | Block commit |

---

## Related Documentation

- **Agent Library**: [.claude/AGENTS.md](../.claude/AGENTS.md) - Complete agent reference
- **Integration Patterns**: [agent-integration-patterns.md](./agent-integration-patterns.md) - Complex workflows
- **Examples**: [examples/README.md](./examples/README.md) - Real-world examples
- **Framework Core**: [claude-development-framework.md](./claude-development-framework.md) - Core principles
- **Troubleshooting**: [troubleshooting.md](./troubleshooting.md) - General framework issues

---

**Framework**: Claude Development Framework v2.1
**Version**: 1.0
**Last Updated**: 2025-10-02

Ready to automate your development workflow! 🚀
