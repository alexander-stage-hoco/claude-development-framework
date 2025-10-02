# Example Sessions: Claude Development Framework v2.1

**Purpose**: Real-world examples demonstrating the Claude Development Framework in action

**Last Updated**: 2025-10-02

---

## Quick Navigation

### By Use Case

| I Want To... | Example | Duration |
|-------------|---------|----------|
| Generate tests from specs | [Test Generation](#11-test-generation-with-test-writer) | 5-10 min |
| Create BDD scenarios | [BDD Scenarios](#12-bdd-scenarios-with-bdd-scenario-writer) | 5-10 min |
| Validate code quality | [Quality Validation](#13-quality-validation-with-code-quality-checker) | 5-10 min |
| Find refactoring opportunities | [Refactoring](#14-refactoring-with-refactoring-analyzer) | 10-15 min |
| Create use case specifications | [Spec Creation](#15-specification-creation-with-uc-writer) | 15-20 min |
| Document technical decisions | [ADR Documentation](#16-adr-documentation-with-adr-manager) | 10-15 min |
| Plan iterations | [Iteration Planning](#17-iteration-planning-with-iteration-planner) | 15-20 min |
| Validate specifications | [Spec Validation](#18-spec-validation-with-spec-validator) | 5-10 min |
| Automate git workflow | [Git Workflow](#19-git-workflow-with-git-workflow-helper) | 3-5 min |
| Document session work | [Session Summary](#20-session-documentation-with-session-summarizer) | 5-10 min |
| Extract services from use cases | [Service Extraction](#1-service-extraction) | 30 min |
| Find and evaluate libraries | [Library Evaluation](#2-library-evaluation) | 20 min |
| Optimize service performance | [Performance Optimization](#3-performance-optimization) | 45 min |
| Validate architecture dependencies | [Dependency Analysis](#4-dependency-analysis) | 10 min |
| Ensure UC-Service traceability | [Traceability Validation](#5-traceability-validation) | 15 min |
| Automate entire service layer creation | [Multi-Agent Orchestration](#6-multi-agent-orchestration) | 90 min |
| Fix circular dependencies | [Circular Dependency Fix](#7-circular-dependency-fix) | 60 min |
| Handle changing requirements | [Specification Evolution](#8-specification-evolution) | 45 min |
| Fix production performance crisis | [Production Crisis](#9-production-performance-crisis) | 2 hours |
| Manage large project context | [Context Window Management](#10-context-window-management) | 30 min |

### By Complexity

**Simple** (< 10 minutes):
- Test Generation
- BDD Scenarios
- Quality Validation
- Git Workflow
- Session Summary
- Spec Validation
- Dependency Analysis
- Traceability Validation

**Medium** (10-30 minutes):
- Refactoring Analysis
- Spec Creation
- ADR Documentation
- Iteration Planning
- Service Extraction
- Library Evaluation
- Specification Evolution
- Context Window Management

**Complex** (30+ minutes):
- Performance Optimization
- Multi-Agent Orchestration
- Circular Dependency Fix
- Production Crisis

### By Framework Feature

**Subagent Workflows**:
- [Service Extraction](#1-service-extraction)
- [Library Evaluation](#2-library-evaluation)
- [Performance Optimization](#3-performance-optimization)
- [Dependency Analysis](#4-dependency-analysis)
- [Traceability Validation](#5-traceability-validation)
- [Multi-Agent Orchestration](#6-multi-agent-orchestration)

**Real-World Scenarios**:
- [Circular Dependency Fix](#7-circular-dependency-fix)
- [Specification Evolution](#8-specification-evolution)
- [Production Crisis](#9-production-performance-crisis)
- [Context Window Management](#10-context-window-management)

---

## Examples

### 1. Service Extraction

**File**: `subagent-service-extraction.md`

**Scenario**: User has completed 5 use case specifications and requests service extraction

**Demonstrates**:
- service-extractor subagent in action
- Analyzing UCs for capabilities
- Grouping by domain (Single Responsibility Principle)
- Creating service specifications
- UC-Service traceability setup
- Layered architecture validation

**Outcome**:
- 6 services extracted from 5 UCs
- Clean 3-layer architecture
- 100% UC-Service traceability
- ~1,430 lines of specs created
- **Time**: 8 minutes (vs. 2+ hours manual)

**Key Quote**:
> "I'll use the service-extractor subagent to analyze your use cases and identify reusable services following service-oriented architecture principles."

---

### 2. Library Evaluation

**File**: `subagent-library-evaluation.md`

**Scenario**: Evaluate authentication libraries for AuthService before implementing

**Demonstrates**:
- service-library-finder subagent
- PyPI and GitHub search
- Decision matrix with weighted scoring (9 criteria)
- Feature coverage analysis (must-have vs. nice-to-have)
- Quality assessment (stars, downloads, maintenance)
- Cost analysis (library vs. custom)

**Outcome**:
- **Recommendation**: PyJWT + Passlib (91.5% score)
- **vs. Authlib**: 84% (more features but OAuth2 overhead)
- **vs. Custom**: 78.5% (4 days development, not worth it)
- **Cost Saved**: $2,100 (avoided custom development)
- **Time**: 12 minutes research

**Key Quote**:
> "PyJWT + Passlib provide 100% must-have feature coverage, industry-standard quality, and save $2,100 vs. custom implementation."

---

### 3. Performance Optimization

**File**: `subagent-performance-optimization.md`

**Scenario**: ProductService slow with 50,000+ products, needs optimization

**Demonstrates**:
- service-optimizer subagent
- Implementing 4 alternative strategies
- Benchmarking (p50, p95, p99, throughput, memory)
- Trade-off analysis (speed vs. cost vs. complexity)
- Decision matrix proving optimal choice
- TDD throughout (tests never skipped)

**Outcome**:
- **Performance**: 1225ms → 12ms p99 (99.2x faster!)
- **Strategy**: PostgreSQL Full-Text Search (vs. ElasticSearch)
- **Cost**: $0 additional (vs. $2,300/year for ElasticSearch)
- **Quality**: All 47 tests still pass
- **Time**: 45 minutes (vs. days trial-and-error)

**Key Quote**:
> "Strategy 3 provides 99.2x speedup while costing $0 additional. ElasticSearch is only 1.3x faster for $2,300/year—not worth 3ms improvement."

---

### 4. Dependency Analysis

**File**: `subagent-dependency-analysis.md`

**Scenario**: Validate service dependencies before implementation

**Demonstrates**:
- service-dependency-analyzer subagent
- Building dependency graph
- Cycle detection algorithm (DFS)
- Topological sort for layer assignment
- Dependency limit validation (≤3 per service)

**Outcome**:
- **Architecture**: Clean ✅
- **Circular Dependencies**: 0
- **Max Dependencies**: 2 (well below limit of 3)
- **Layers**: 3 (clean layered architecture)
- **Time**: 10 minutes (vs. 1-2 hours manual analysis)

**Key Quote**:
> "Architecture is production-ready. No circular dependencies, all services ≤2 dependencies, clean 3-layer architecture."

---

### 5. Traceability Validation

**File**: `subagent-traceability-validation.md`

**Scenario**: After implementation, validate UC-Service traceability

**Demonstrates**:
- uc-service-tracer subagent
- Bidirectional traceability checking
- Detecting missing service references
- Finding orphan services
- Method mismatch detection

**Outcome**:
- **Issues Found**: 2 (missing UC-004 services, SVC-002 mismatch)
- **Coverage**: 80% → 100% after fixes
- **Orphan Services**: 0
- **Time**: 15 minutes (vs. hours debugging integration)

**Key Quote**:
> "UC-004 is missing service references and UserService spec doesn't list UC-002. I cannot proceed with implementation until these are fixed."

---

### 6. Multi-Agent Orchestration

**File**: `subagent-multi-agent-orchestration.md`

**Scenario**: Complete service layer development using 5 subagents sequentially

**Demonstrates**:
- Orchestrating multiple subagents
- Sequential execution with checkpoints
- Data flow between subagents
- User approval gates
- End-to-end service layer creation

**Workflow**:
1. service-extractor → 12 services identified
2. service-library-finder → 3 libraries evaluated
3. service-designer → 12 interfaces designed
4. service-dependency-analyzer → Architecture validated
5. uc-service-tracer → Traceability verified

**Outcome**:
- **Services**: 12 services fully specified
- **Files Created**: 38 files (~6,000 lines)
- **Time**: 55 minutes (vs. 2-3 days manual)
- **Time Saved**: 97%

**Key Quote**:
> "Multi-agent workflow complete! 12 services extracted, evaluated, designed, validated, and traced in 55 minutes."

---

### 7. Circular Dependency Fix

**File**: `scenario-circular-dependency-fix.md`

**Scenario**: Dependency analyzer detects circular dependency needing refactoring

**Demonstrates**:
- Detecting cycles with service-dependency-analyzer
- Root cause analysis
- Two refactoring options (events vs. extraction)
- Event-based decoupling implementation
- Re-validation after fix

**Problem**:
```
PaymentService → OrderService → InventoryService → PaymentService ❌
```

**Solution**:
```
Layer 1: EventBus
Layer 2: PaymentService, OrderService, InventoryService (independent) ✅
```

**Outcome**:
- **Cycle**: Broken using event bus
- **Architecture**: Clean layers restored
- **Quality**: All tests pass, specs updated
- **Time**: 60 minutes

**Key Quote**:
> "Circular dependency detected. I cannot proceed with implementation. Two refactoring options: event-based decoupling (recommended) or extract shared logic."

---

### 8. Specification Evolution

**File**: `scenario-specification-evolution.md`

**Scenario**: User changes requirements mid-iteration (add task priorities)

**Demonstrates**:
- Refusing to code without spec update (Rule #1)
- Presenting impact analysis options
- Updating specifications first
- Backward compatibility testing
- No regression (old tests still pass)

**User Request**: "Actually, I want to add task priorities (high, medium, low)"

**Claude's Response**: Present two options with impact analysis

**Outcome**:
- **Option Chosen**: Finish current UC, add priorities as new UC-006
- **Timeline**: 2h 15min (vs. 3+ hours ad-hoc)
- **Quality**: Backward compatible, no regression
- **Tests**: All pass (including 5 new priority tests)

**Key Quote**:
> "This adds scope to the current iteration. I cannot add this feature without updating the specification first (Rule #1)."

---

### 9. Production Performance Crisis

**File**: `scenario-production-performance-crisis.md`

**Scenario**: Production API degraded, urgent fix needed while maintaining quality

**Demonstrates**:
- Emergency hotfix protocol
- Root cause analysis under pressure
- TDD even in emergencies (tests never skipped!)
- Benchmarking improvement
- Post-mortem and lessons learned

**Crisis**: API p99 latency 3000ms (SLA: 200ms), losing $500/min

**Timeline**:
- 02:00: Alert received
- 02:05: Root cause identified (N+1 queries)
- 02:15: Fix implemented and tested
- 02:20: Deployed to production
- 02:25: Metrics confirmed resolution
- **Total**: 25 minutes

**Outcome**:
- **Performance**: 2800ms → 8ms (350x faster)
- **Tests**: All 49 tests pass (even in emergency!)
- **Revenue Saved**: ~$12,500
- **Quality Debt**: ZERO

**Key Quote**:
> "🚨 Production emergency detected. I will NOT skip tests even in emergency (Rule #6: Never Compromise Tests)."

---

### 10. Context Window Management

**File**: `scenario-context-window-management.md`

**Scenario**: Large project approaching context limits, need compression

**Demonstrates**:
- Context monitoring (warns at 70%)
- Compression protocol (summarize + archive + reload)
- Session-state.md for continuity
- TIER 1 file protection
- Seamless work resumption

**Problem**: Context at 72% (144K / 200K tokens)

**Solution**:
1. Summarize conversation history (94K → 3K tokens)
2. Archive completed work
3. Reload TIER 1 files (verify rules)
4. Resume work

**Outcome**:
- **Context**: 72% → 23% (68% freed)
- **TIER 1 Files**: Protected and reloaded
- **Work Continuity**: Seamless (no focus loss)
- **Framework Enforcement**: Fully restored

**Key Quote**:
> "Context at 72%. Compressing now to protect TIER 1 files. Estimated recovery: 72% → 25%."

---

## Tier 1 & Tier 2 Core Agent Examples

These examples complement the existing service-oriented agent examples, demonstrating the 12 core development agents.

### 11. Test Generation with test-writer

**Scenario**: Generate tests for UC-001 user registration
**Demonstrates**: test-writer agent, RED phase automation, test-first development
**Outcome**: 12 tests generated in 5 minutes vs. 45 minutes manual
**Time**: 5-10 minutes

**Key Learnings**:
- test-writer reads UC acceptance criteria
- Generates unit tests, integration tests, edge cases
- Tests fail initially (RED phase - correct!)
- Implementation follows tests (GREEN phase)

**Process**:
1. User creates UC-001 specification (8 acceptance criteria)
2. User: "generate tests for UC-001"
3. test-writer extracts criteria, generates 12 test cases
4. Output: tests/test_user_registration.py (180 lines)
5. Tests run: 12 failing (expected - no implementation yet)

**Value**: 40 minutes saved, 100% AC coverage, consistent test structure

---

### 12. BDD Scenarios with bdd-scenario-writer

**Scenario**: Create Gherkin scenarios for authentication flow
**Demonstrates**: bdd-scenario-writer, acceptance criteria automation, Rule #8
**Outcome**: 8 scenarios generated, 100% UC criteria coverage
**Time**: 5-10 minutes

**Key Learnings**:
- Converts UC acceptance criteria to Given-When-Then format
- Creates scenario outlines for data variations
- Executable with behave/cucumber frameworks
- Stakeholder-readable specifications

**Process**:
1. User provides UC-002 (User Login) specification
2. User: "write BDD scenarios for UC-002"
3. bdd-scenario-writer converts ACs to Gherkin format
4. Output: features/user_login.feature (85 lines, 8 scenarios)
5. Scenarios include: success cases, error cases, edge cases

**Value**: Executable specs, stakeholder communication, automated acceptance testing

---

### 13. Quality Validation with code-quality-checker

**Scenario**: Pre-commit quality validation catches 15 issues
**Demonstrates**: code-quality-checker, Rule #9 enforcement, quality gates
**Outcome**: 15 issues found and fixed before commit, prevented broken build
**Time**: 5-10 minutes

**Key Learnings**:
- Checks type hints, docstrings, complexity, linting
- Blocks commits with quality violations
- Provides file:line references for fixes
- Scores 0-100 (threshold: 80)

**Process**:
1. User completes implementation of user_service.py
2. User: "check code quality in user_service.py"
3. code-quality-checker analyzes code
4. Output: Score 72/100 (FAIL) - 15 issues found
5. User fixes issues, re-checks: Score 94/100 (PASS)
6. Commit proceeds

**Value**: Quality gates enforced, issues caught early, no broken builds

---

### 14. Refactoring with refactoring-analyzer

**Scenario**: Analyze user_service.py for code improvements
**Demonstrates**: refactoring-analyzer, Rule #12, REFACTOR phase automation
**Outcome**: 5 refactoring suggestions, code complexity reduced 40%
**Time**: 10-15 minutes

**Key Learnings**:
- Detects code smells (long functions, duplication)
- Suggests specific refactorings with examples
- Estimates effort vs. benefit for each suggestion
- Prioritizes high-impact improvements

**Process**:
1. User completes implementation (tests passing - GREEN phase)
2. User: "suggest refactoring for user_service.py"
3. refactoring-analyzer finds 5 opportunities
4. User implements top 2 suggestions (extract method, remove duplication)
5. Complexity reduced from 12 → 7
6. All tests still pass ✓

**Value**: Cleaner code, reduced complexity, maintainability improved

---

### 15. Specification Creation with uc-writer

**Scenario**: Create UC-006 task prioritization from requirements
**Demonstrates**: uc-writer, Rule #1, spec-first development
**Outcome**: Complete 500-line UC spec in 15 minutes vs. 2+ hours manual
**Time**: 15-20 minutes

**Key Learnings**:
- Interviews user for requirements (interactive)
- Generates complete 16-section UC template
- Includes acceptance criteria, edge cases, error scenarios
- Ready for validation and implementation

**Process**:
1. User: "We need a feature to let users prioritize their tasks"
2. uc-writer asks clarifying questions (priority levels, who can set, UI)
3. User provides answers
4. uc-writer generates complete UC-006 specification
5. Output: specs/use-cases/UC-006-task-prioritization.md (500 lines)
6. Includes 8 ACs, 4 edge cases, 3 error scenarios

**Value**: 1.75 hours saved, consistent structure, comprehensive specification

---

### 16. ADR Documentation with adr-manager

**Scenario**: Document decision to use JWT authentication
**Demonstrates**: adr-manager, Rule #7, technical decision documentation
**Outcome**: ADR-004 created with alternatives analysis and rationale
**Time**: 10-15 minutes

**Key Learnings**:
- Documents technical decisions permanently
- Includes alternatives considered and why rejected
- Captures consequences (positive and negative)
- Provides compliance checklist

**Process**:
1. Team decides to use JWT for authentication
2. User: "create ADR for JWT authentication"
3. adr-manager interviews for decision details
4. User provides: options considered, rationale, trade-offs
5. adr-manager generates ADR-004
6. Output: planning/adrs/ADR-004-jwt-authentication.md (120 lines)

**Value**: Decisions documented, no rehashing debates, new team members understand context

---

### 17. Iteration Planning with iteration-planner

**Scenario**: Break UC-001 into 3 iterations
**Demonstrates**: iteration-planner, Rule #3 & #5, strategic + tactical planning
**Outcome**: UC broken into 3 manageable iterations (each <3 hours)
**Time**: 15-20 minutes

**Key Learnings**:
- Analyzes UC complexity (ACs, dependencies, effort)
- Breaks into iterations (max 3 hours each)
- Creates detailed iteration plans with scope, tests, duration
- Ensures incremental delivery

**Process**:
1. User has UC-001 (User Registration) - 12 ACs, ~8 hours effort
2. User: "plan iterations for UC-001"
3. iteration-planner analyzes and breaks down
4. Output: 3 iteration files
   - Iteration 1: Basic registration (AC1-4, 2h 30min)
   - Iteration 2: Email verification (AC5-8, 2h 45min)
   - Iteration 3: Password security (AC9-12, 2h 15min)

**Value**: Manageable chunks, clear scope, realistic estimates

---

### 18. Spec Validation with spec-validator

**Scenario**: Validate UC-003 completeness before implementation
**Demonstrates**: spec-validator, Rule #1, quality enforcement
**Outcome**: Score 68/100 (FAIL), 8 issues found and fixed, re-validated: 92/100 (PASS)
**Time**: 5-10 minutes

**Key Learnings**:
- Checks 16 required sections for completeness
- Validates content quality (ACs, edge cases, dependencies)
- Blocks implementation if spec invalid (<80/100)
- Provides actionable fix recommendations

**Process**:
1. User creates UC-003 (User Logout) specification
2. User: "validate UC-003"
3. spec-validator analyzes spec
4. Output: Score 68/100 (FAIL)
   - Missing: Edge Cases section
   - Only 3 ACs (min 5 recommended)
   - Missing: Service Dependencies
5. User fixes 8 issues
6. Re-validate: Score 92/100 (PASS)
7. Implementation approved

**Value**: Quality specs, no missing requirements, implementation blockers caught early

---

### 19. Git Workflow with git-workflow-helper

**Scenario**: Branch creation and commit message generation for iteration 2
**Demonstrates**: git-workflow-helper, Rule #11, git automation
**Outcome**: Branch created, commit message generated with spec refs and test counts
**Time**: 3-5 minutes

**Key Learnings**:
- Automates branch creation (follows naming convention)
- Generates commit messages (conventional commits format)
- Pre-commit validation (tests passing, no TODOs, no debug code)
- Enforces git workflow discipline

**Process**:
1. User ready to start iteration 2
2. User: "create branch for iteration 2"
3. git-workflow-helper creates: iteration-002-email-verification
4. [User implements feature]
5. User: "generate commit message"
6. git-workflow-helper analyzes changes, generates message:
   ```
   feat: email verification (iteration 2)

   Implemented UC-001 iteration 2: email verification.
   Tests: 24 passing / 24 total

   Specification: UC-001 iteration 2
   ```

**Value**: Consistent git workflow, professional commit messages, automated validation

---

### 20. Session Documentation with session-summarizer

**Scenario**: End session and generate session-state.md
**Demonstrates**: session-summarizer, Rule #10, session continuity
**Outcome**: Comprehensive session-state.md with work completed, decisions, next steps
**Time**: 5-10 minutes

**Key Learnings**:
- Analyzes conversation for work completed, decisions made, blockers
- Checks git history for commits and file changes
- Extracts test counts and coverage metrics
- Provides detailed next steps for session resumption

**Process**:
1. User completes iteration 2 work (2h 15min session)
2. User: "end session"
3. session-summarizer analyzes:
   - Conversation history
   - Git commits (git log -10)
   - Files changed (git diff --name-status)
   - Current iteration status
4. Output: session-state.md (350 lines)
   - Work completed (specific features implemented)
   - Decisions made (ADRs, technical choices)
   - Files modified (with line counts)
   - Next steps (exact commands to resume)

**Value**: Seamless session continuity, no context loss, easy resume next time

---

**Note**: Detailed walkthroughs for these agents are available in:
- [agent-guide.md](../agent-guide.md) - Practical usage guide
- [agent-integration-patterns.md](../agent-integration-patterns.md) - Orchestration workflows

---

## How to Use These Examples

### For Learning

1. **Start with Simple Examples**:
   - Dependency Analysis (10 min)
   - Traceability Validation (15 min)

2. **Progress to Medium**:
   - Service Extraction (30 min)
   - Library Evaluation (20 min)

3. **Study Complex Workflows**:
   - Multi-Agent Orchestration (90 min)
   - Production Crisis (2 hours)

### For Reference

**Quick Lookup**:
- Need to optimize performance? → Performance Optimization
- Circular dependency? → Circular Dependency Fix
- Requirements changed? → Specification Evolution
- Context filling up? → Context Window Management

### For Teaching

**Show New Users**:
1. Service Extraction (shows framework value)
2. Multi-Agent Orchestration (shows automation)
3. Production Crisis (shows quality under pressure)

---

## Common Patterns Across Examples

### Framework Enforcement

Every example demonstrates:
- ✅ **Spec-First**: No code without specification
- ✅ **Test-First**: Tests written before implementation
- ✅ **Quality Gates**: Validation before proceeding
- ✅ **Documentation**: ADRs, specs, reports created

### Subagent Value

Subagent examples show:
- **Automation**: Hours saved (55 min vs. 2-3 days)
- **Consistency**: Template compliance, no human error
- **Validation**: Automatic quality checks
- **Reports**: Detailed analysis and recommendations

### Real-World Challenges

Scenario examples show:
- **Resilience**: Framework handles emergencies
- **Flexibility**: Spec evolution supported
- **Scale**: Large projects manageable
- **Quality**: Never compromised, even under pressure

---

## Example Statistics

**Total Examples**: 20 (6 service-oriented + 4 real-world scenarios + 10 core agents)
**Total Content**: ~9,000+ lines (existing examples + new summaries)
**Time Ranges**: 3 min - 2 hours
**Agent Coverage**: 16/18 agents (89%) - all 12 core + 4 of 6 service-oriented
**Framework Features**: 30+ features shown

**Complexity Distribution**:
- Simple (8): 40% (5-10 min examples)
- Medium (8): 40% (10-30 min examples)
- Complex (4): 20% (30+ min examples)

**Time Savings Demonstrated**:
- Service extraction: 2+ hours saved
- Library evaluation: 2-3 hours saved
- Performance optimization: 2-3 days saved
- Multi-agent workflow: 15-23 hours saved
- Test generation: 40 min saved per UC
- Spec creation: 1.75 hours saved per UC
- Quality validation: Prevents hours of debugging
- **Total**: ~60+ hours saved across examples

---

## Next Steps

**After Reading Examples**:

1. **Try the Framework**:
   - Run `./init-project.sh my-project`
   - Follow Quick Start Guide
   - Reference examples as needed

2. **Customize for Your Domain**:
   - Adapt use case templates
   - Modify service patterns
   - Add domain-specific ADRs

3. **Share Your Examples**:
   - Document your own sessions
   - Contribute back to framework
   - Help others learn

---

## Related Documentation

**Framework Core**:
- `docs/claude-development-framework.md` - Main framework guide
- `docs/service-architecture.md` - Service-oriented architecture
- `docs/session-types.md` - 10 session type patterns

**Quick References**:
- `.claude/quick-ref/session-start.md` - Session startup checklist
- `.claude/quick-ref/tdd-cycle.md` - Test-driven development
- `.claude/quick-ref/services.md` - Service patterns

**Templates**:
- `.claude/templates/` - All templates (use cases, services, iterations)

**Troubleshooting**:
- `docs/troubleshooting.md` - Common problems and solutions

---

**Framework Version**: Claude Development Framework v2.1
**Examples Version**: 2.0
**Last Updated**: 2025-10-02

**Contributors**: Knowledge Graph Builder project learnings

---

**Ready to Start?** Choose an example that matches your current need! 🚀
