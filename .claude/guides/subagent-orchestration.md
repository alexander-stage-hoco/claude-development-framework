---
tier: 4
purpose: Multi-agent workflow patterns and orchestration
reload_trigger: When planning multi-agent workflows
estimated_read_time: 15 minutes
---

# Subagent Orchestration Guide

**Purpose**: How to use multiple subagents together for complex workflows

**When to Use**: Tasks requiring multiple specialized capabilities in sequence or parallel

---

## Table of Contents

1. [When to Orchestrate Multiple Subagents](#when-to-orchestrate-multiple-subagents)
2. [Orchestration Patterns](#orchestration-patterns)
3. [Data Passing](#data-passing)
4. [User Approval Gates](#user-approval-gates)
5. [Error Handling](#error-handling)
6. [Common Workflows](#common-workflows)
7. [Best Practices](#best-practices)

---

## When to Orchestrate Multiple Subagents

### Use Single Subagent When:
✅ Task is self-contained (e.g., "extract services from these 5 UCs")
✅ No dependencies on other subagent outputs
✅ User can review and approve result immediately
✅ Total time < 30 minutes

**Example**: Use service-extractor alone to analyze UCs and create service specs

---

### Use Multiple Subagents When:
✅ Task requires multiple specialized steps
✅ Each step produces output needed by next step
✅ Validation needed between steps
✅ Total workflow > 30 minutes but < 2 hours

**Example**: Extract services → Evaluate libraries → Design interfaces → Validate architecture

---

## Orchestration Patterns

### Pattern 1: Sequential Pipeline

**Structure**: A → B → C → D (each uses previous output)

**When**: Steps must happen in order, each depends on previous

**Example**: Complete Service Layer Creation
```
1. service-extractor (UCs → service list)
      ↓
2. service-library-finder (service list → library recommendations)
      ↓
3. service-designer (service list + libraries → detailed specs)
      ↓
4. service-dependency-analyzer (specs → dependency validation)
      ↓
5. uc-service-tracer (UCs + specs → traceability verification)
```

**Execution**:
```markdown
User: "Create complete service layer for UC-001 through UC-005"

Claude:
Step 1: Launching service-extractor subagent...
[subagent runs]
Result: 12 services identified

⏸️  CHECKPOINT: Review 12 services. Approve to continue? [User: Yes]

Step 2: Launching service-library-finder for AuthService, EmailService...
[subagent runs]
Result: 3 library recommendations

⏸️  CHECKPOINT: Review library choices. Approve to continue? [User: Yes]

Step 3: Launching service-designer for all 12 services...
[subagent runs]
Result: 12 complete service specifications created

⏸️  CHECKPOINT: Review specs. Approve to continue? [User: Yes]

Step 4: Launching service-dependency-analyzer...
[subagent runs]
Result: Architecture validated, no cycles, clean layers

⏸️  CHECKPOINT: Architecture OK. Approve to continue? [User: Yes]

Step 5: Launching uc-service-tracer...
[subagent runs]
Result: 100% bidirectional traceability verified

✅ Complete! 12 services designed, validated, and traced in 55 minutes.
```

---

### Pattern 2: Parallel Fan-Out → Merge

**Structure**:
```
       ┌─ B1 ─┐
   A ──├─ B2 ─┤── C
       └─ B3 ─┘
```

**When**: Multiple independent analyses needed, then combined

**Example**: Evaluate Multiple Libraries in Parallel
```
1. service-extractor → identifies AuthService needed
      ↓
2. Launch 3 parallel library-finder subagents:
   - Evaluate JWT libraries
   - Evaluate OAuth libraries
   - Evaluate password hashing libraries
      ↓
3. Merge results → Recommend best combination
```

**Execution**:
```markdown
User: "Evaluate authentication solution options"

Claude:
Step 1: Launching service-extractor...
Result: AuthService needs JWT, OAuth2, password hashing

Step 2: Launching 3 library evaluators in parallel...

⚠️  Note: Running 3 subagents concurrently (2-3 min each)

[After ~3 minutes]

Results:
- JWT: PyJWT (score: 9.5/10)
- OAuth2: Authlib (score: 9/10)
- Hashing: Passlib (score: 9.8/10)

Step 3: Analyzing combination compatibility...
Recommendation: PyJWT + Authlib + Passlib (combined score: 9.4/10)

⏸️  CHECKPOINT: Approve this stack? [User: Yes]
```

**Note**: Parallel execution not yet supported by Task tool, but pattern documents intent

---

### Pattern 3: Conditional Branching

**Structure**:
```
   A → decision?
        ├─ Yes → B
        └─ No  → C
```

**When**: Next step depends on validation result

**Example**: Architecture Validation with Fix Loop
```
1. service-dependency-analyzer checks for cycles
      ↓
2. If cycles found:
     → service-designer suggests refactoring
     → Apply fix
     → Re-run analyzer (loop)
   If no cycles:
     → Proceed to traceability validation
```

**Execution**:
```markdown
User: "Validate and fix service architecture"

Claude:
Step 1: Launching service-dependency-analyzer...
Result: ❌ Circular dependency detected: PaymentService → OrderService → InventoryService → PaymentService

Step 2: Cycle detected! Launching service-designer for refactoring options...
Result: 2 options: (1) Event-based decoupling, (2) Extract shared logic

⏸️  CHECKPOINT: Choose option? [User: Option 1 - events]

Step 3: Applying event-based refactoring...
Result: Services decoupled using EventBus

Step 4: Re-running service-dependency-analyzer...
Result: ✅ No cycles, clean 3-layer architecture

Step 5: Launching uc-service-tracer...
Result: ✅ 100% traceability maintained after refactoring

✅ Complete! Architecture fixed and validated.
```

---

### Pattern 4: Iterative Refinement

**Structure**: A → B → Validate → (if not OK) → A → B → Validate (loop)

**When**: Output quality needs multiple refinement passes

**Example**: Performance Optimization with Multiple Strategies
```
1. service-optimizer implements Strategy 1
      ↓
2. Benchmark
      ↓
3. If not meeting SLA:
     → Implement Strategy 2
     → Benchmark
     → Repeat until SLA met or strategies exhausted
```

**Execution**:
```markdown
User: "Optimize ProductService to meet <50ms p99 latency"

Claude:
Iteration 1:
- Strategy: In-memory caching
- Result: 120ms p99 ❌ (not meeting SLA)

Iteration 2:
- Strategy: PostgreSQL full-text search
- Result: 45ms p99 ✅ (meeting SLA!)

⏸️  CHECKPOINT: SLA met! Deploy Strategy 2? [User: Yes]

✅ Optimization complete in 2 iterations.
```

---

## Data Passing

### Between Subagents

**Method 1: File-Based** (Recommended)
```markdown
Subagent A writes: services/service-list.md
Subagent B reads: services/service-list.md
```

**Pros**: Persistent, reviewable, versionable
**Cons**: Requires file I/O

**Example**:
```markdown
service-extractor creates:
  - services/extracted-services.md (list of services)
  - specs/services-summary.md (summary)

service-designer reads:
  - services/extracted-services.md
  - Creates: services/*/service-spec.md
```

---

**Method 2: Context-Based** (For small data)
```markdown
Subagent A returns summary in response
User provides summary to Subagent B in prompt
```

**Pros**: Simple, no files
**Cons**: Limited size, not persistent

**Example**:
```markdown
Claude: service-extractor identified 12 services:
[AuthService, UserService, EmailService, ...]

User: "Now run service-designer on these 12 services"
```

---

**Method 3: Structured Output** (For complex data)
```markdown
Subagent A writes JSON/YAML:
  services-extracted.json

Subagent B parses:
  json = read(services-extracted.json)
```

**Pros**: Machine-readable, structured
**Cons**: Requires parsing

---

### Data Flow Example: Complete Pipeline

```
Step 1: service-extractor
Input: specs/use-cases/UC-*.md
Output: services/extracted-services.md (list), services/*/service-spec.md (skeleton)

Step 2: service-library-finder
Input: services/extracted-services.md (which services need libraries)
Output: services/library-evaluation.md (recommendations)

Step 3: service-designer
Input: services/extracted-services.md, services/library-evaluation.md
Output: services/*/service-spec.md (complete specs with library choices)

Step 4: service-dependency-analyzer
Input: services/*/service-spec.md (reads all specs)
Output: services/dependency-graph.md (analysis)

Step 5: uc-service-tracer
Input: specs/use-cases/UC-*.md, services/*/service-spec.md
Output: services/traceability-report.md (validation)
```

**All outputs are files** → Reviewable, committable, traceable

---

## User Approval Gates

### Why Approval Gates?

✅ Prevents cascading errors (bad input → bad output × 5 subagents)
✅ Allows course correction mid-workflow
✅ Maintains user control
✅ Documents decision points

### When to Add Gates

**Always** between major phases:
- After analysis (before design)
- After design (before implementation)
- After implementation (before optimization)
- After validation (before deploy)

**Optional** within phases:
- After each service designed (if many services)
- After each optimization iteration

---

### Gate Patterns

**Pattern A: Review and Approve**
```markdown
⏸️  CHECKPOINT: Service Extraction Complete

Results:
- 12 services identified
- 3-layer architecture
- Dependencies: max 2 per service

📄 Review: services/extracted-services.md

❓ Approve these services to proceed with library evaluation?
   [User: Yes / No / Modify]
```

**Pattern B: Choose Option**
```markdown
⏸️  DECISION NEEDED: Circular Dependency Fix

Options:
1. Event-based decoupling (recommended)
   - Pros: Clean separation, scalable
   - Cons: More complex, requires event bus
   - Effort: 2-3 hours

2. Extract shared logic
   - Pros: Simpler, no new infrastructure
   - Cons: Creates utility service (potential god object)
   - Effort: 1-2 hours

❓ Which approach? [User: Option 1]
```

**Pattern C: Iterative Feedback**
```markdown
⏸️  ITERATION 1 COMPLETE: Performance Optimization

Strategy: In-memory caching
Result: 120ms p99 (SLA: <50ms) ❌

Next Strategies Available:
- Strategy 2: Redis caching (estimated: 30ms p99)
- Strategy 3: PostgreSQL full-text (estimated: 45ms p99)

❓ Try Strategy 2? Or different approach? [User: Try Strategy 2]
```

---

## Error Handling

### Subagent Failure Scenarios

**Scenario 1: Subagent Can't Complete Task**
```markdown
Step 3: Launching service-designer...

❌ ERROR: service-designer unable to design AuthService
Reason: Missing specification for password policy

🛑 WORKFLOW PAUSED

Required: Define password policy in specs/security-policy.md

❓ Action: Create policy now or skip AuthService? [User: Create policy]
```

**Recovery**:
1. Address blocker
2. Re-run failed subagent
3. Continue workflow

---

**Scenario 2: Invalid Input**
```markdown
Step 2: Launching service-library-finder...

❌ ERROR: No services specified
Reason: service-extractor output file not found

🛑 WORKFLOW PAUSED

❓ Action: Re-run service-extractor or provide service list manually? [User: Re-run]
```

**Recovery**:
1. Go back to previous step
2. Fix issue
3. Resume from failed step

---

**Scenario 3: Validation Fails**
```markdown
Step 5: Launching uc-service-tracer...

❌ ERROR: Traceability validation failed
Issues:
- UC-004 missing service references
- ServiceB not used by any UC (orphan)

🛑 WORKFLOW INCOMPLETE

Required Fixes:
1. Update UC-004 with service references
2. Either use ServiceB or remove it

❓ Fix now or complete workflow with known issues? [User: Fix now]
```

**Recovery**:
1. User fixes issues manually
2. Re-run validation subagent
3. Confirm success

---

### Error Prevention

**Strategy 1: Validate Early**
```markdown
Before launching multi-agent workflow:
1. Check all UCs have service references (uc-service-tracer)
2. Check architecture has no cycles (service-dependency-analyzer)
3. THEN proceed with changes
```

**Strategy 2: Checkpoint State**
```markdown
After each subagent:
1. Save output files
2. Commit to git: `git commit -m "checkpoint: service extraction complete"`
3. If later step fails, can roll back to checkpoint
```

**Strategy 3: Dry-Run Mode**
```markdown
User: "Preview complete service layer creation (don't create files)"

Claude: [Runs read-only analysis]
Result: Would create 12 services, 45 files, estimated 55 minutes

❓ Proceed with actual creation? [User: Yes]
```

---

## Common Workflows

### Workflow 1: Complete Service Layer (Sequential)

**Goal**: From UCs to validated, traceable services

**Steps**:
1. **service-extractor**: UC-001 through UC-010 → 15 services identified
2. **Gate**: Review services, approve list
3. **service-library-finder**: Evaluate auth, email, payment libraries
4. **Gate**: Approve library choices
5. **service-designer**: Create 15 complete service specifications
6. **Gate**: Review specs, adjust as needed
7. **service-dependency-analyzer**: Validate architecture, check for cycles
8. **Gate**: Confirm architecture clean
9. **uc-service-tracer**: Verify 100% bidirectional traceability
10. **Gate**: Final approval, ready for implementation

**Time**: ~90 minutes
**Output**: 15 services fully specified, validated, traced

---

### Workflow 2: Performance Crisis (Conditional)

**Goal**: Optimize underperforming service to meet SLA

**Steps**:
1. **service-optimizer**: Analyze current performance, identify bottleneck
2. **Gate**: Confirm root cause analysis
3. **service-optimizer**: Implement Strategy 1 (cached queries)
4. **Benchmark**: Test performance
5. **Decision**: SLA met?
   - Yes → Done
   - No → Strategy 2
6. **service-optimizer**: Implement Strategy 2 (indexed search)
7. **Benchmark**: Test performance
8. **Decision**: SLA met?
   - Yes → Done
   - No → Strategy 3
9. **Continue until SLA met or strategies exhausted**

**Time**: 45-120 minutes (depends on iterations)
**Output**: Optimized service meeting SLA with benchmark proof

---

### Workflow 3: Specification Evolution (Branch + Merge)

**Goal**: Major spec changes affecting multiple services

**Steps**:
1. **uc-service-tracer**: Baseline - current traceability state
2. **Gate**: Confirm current state documented
3. **User**: Updates UC specifications (add requirements)
4. **service-extractor**: Re-analyze UCs, identify new service needs
5. **Gate**: Review changes (new services? modified services?)
6. **Parallel**:
   - Branch A: **service-designer** updates existing service specs
   - Branch B: **service-library-finder** evaluates libraries for new needs
7. **Merge**: Combine updated specs + new library choices
8. **service-dependency-analyzer**: Re-validate architecture
9. **uc-service-tracer**: Verify traceability still 100%
10. **Gate**: Approve changes, ready to implement

**Time**: ~60 minutes
**Output**: Specifications evolved, services updated, traceability maintained

---

## Best Practices

### DO ✅

1. **Plan the Pipeline**
   - List all subagents needed
   - Identify data dependencies
   - Mark approval gates

2. **One Subagent at a Time**
   - Launch sequentially (not parallel, current limitation)
   - Wait for completion before next
   - Review outputs between steps

3. **Checkpoint Frequently**
   - Commit after each major subagent
   - Enable rollback if later step fails

4. **Validate Between Steps**
   - Don't assume subagent output is perfect
   - User reviews prevent cascading errors

5. **Document Decisions**
   - Create ADRs for major choices
   - Record why options were chosen

6. **Handle Errors Gracefully**
   - Pause workflow on error
   - Fix root cause
   - Resume from checkpoint

---

### DON'T ❌

1. **Don't Chain Blindly**
   - ❌ "Run all 5 subagents automatically"
   - ✅ "Run subagent 1, review, then run subagent 2 if approved"

2. **Don't Skip Gates**
   - ❌ Proceeding without user review
   - ✅ Wait for explicit approval at each gate

3. **Don't Ignore Failures**
   - ❌ Continuing workflow after subagent error
   - ✅ Pause, fix, resume

4. **Don't Lose Context**
   - ❌ Forgetting what previous subagent produced
   - ✅ Reference output files explicitly

5. **Don't Overcomplicate**
   - ❌ Using 6 subagents for simple task
   - ✅ Use minimum subagents needed

---

## Orchestration Template

**Use this template when planning multi-agent workflows:**

```markdown
## Multi-Agent Workflow: [Workflow Name]

**Goal**: [What are we trying to achieve?]

**Estimated Time**: [X minutes/hours]

### Pipeline

1. **Subagent**: [name]
   - **Input**: [files/data]
   - **Output**: [files/data created]
   - **Purpose**: [what this step does]
   - **⏸️  Gate**: [what user reviews/approves]

2. **Subagent**: [name]
   - **Input**: [uses output from step 1]
   - **Output**: [files/data created]
   - **Purpose**: [what this step does]
   - **⏸️  Gate**: [what user reviews/approves]

[...continue for all steps...]

### Success Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] All gates passed
- [ ] Output validated

### Error Recovery Plan

**If Step X fails**:
1. [Recovery action 1]
2. [Recovery action 2]
3. Resume from Step X

### Estimated Output

- [N files created]
- [M services designed / UCs analyzed / etc.]
- [Traceability report / Architecture validation / etc.]
```

---

## Examples

**See docs/examples/** for complete orchestration examples:

- `subagent-multi-agent-orchestration.md` - Complete 5-subagent workflow
- `scenario-circular-dependency-fix.md` - Conditional branching with fix loop
- `scenario-production-performance-crisis.md` - Iterative optimization

---

**Guide Version**: 1.0
**Framework**: Claude Development Framework v2.0
**Last Updated**: 2025-10-01
