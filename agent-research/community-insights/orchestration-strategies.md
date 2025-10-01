# Orchestration Strategies - Multi-Agent Coordination

**Purpose**: Patterns for coordinating multiple subagents effectively
**Sources**: wshobson/agents, VoltAgent/awesome-claude-code-subagents, Official Anthropic guidance
**Last Updated**: 2025-10-01

---

## What is Agent Orchestration?

**Agent orchestration** is the process of coordinating multiple specialized subagents to complete complex tasks that require diverse expertise.

**Key principle from Anthropic**:
> "Use subagents for complex problems, especially early in a task to preserve context availability in the main session."

---

## Why Orchestrate Multiple Agents?

### Benefits

1. **Context Preservation**: Each agent operates in isolated context
2. **Specialized Expertise**: Domain experts handle specific tasks
3. **Parallel Work**: Multiple agents can work concurrently
4. **Clarity**: Clear separation of responsibilities
5. **Scalability**: Add agents as complexity grows

### When to Use Multi-Agent Systems

✅ **Use multiple agents when**:
- Task spans multiple domains (frontend + backend + infrastructure)
- Requires specialized expertise (security + performance + code quality)
- Complex enough to benefit from specialization
- Each subtask is substantial (not trivial)
- Context window pressure is a concern

❌ **Don't use multiple agents when**:
- Task is simple and focused
- Single domain expertise is sufficient
- Overhead of coordination exceeds benefits
- Agents would need to share too much state

---

## Orchestration Patterns

### Pattern 1: Sequential Pipeline

**Structure**: Task A → Task B → Task C (waterfall)

**Diagram**:
```
User Request
    ↓
[Agent 1: Architect]  → Design
    ↓
[Agent 2: Developer]  → Implementation
    ↓
[Agent 3: Tester]     → Verification
    ↓
Result
```

**Example**:
```
Task: "Build a new authentication system"

1. backend-architect: Design auth architecture
   → Output: API spec, database schema, security patterns

2. backend-developer: Implement auth system
   → Input: Architecture from step 1
   → Output: Working code

3. security-auditor: Review security
   → Input: Code from step 2
   → Output: Security report, fixes needed

4. backend-developer: Apply security fixes
   → Input: Report from step 3
   → Output: Final implementation
```

**When to use**:
- Clear dependencies between tasks
- Output of one task is input to next
- Sequential workflow makes sense

**Pros**:
- ✅ Simple to understand
- ✅ Clear handoffs
- ✅ Easy to track progress

**Cons**:
- ❌ No parallelism
- ❌ Slower overall
- ❌ Blocked if one agent fails

### Pattern 2: Parallel Fan-Out

**Structure**: Task spawns (A, B, C) → Merge results

**Diagram**:
```
User Request
    ↓
[Orchestrator]
    ├→ [Agent A: Frontend] → UI
    ├→ [Agent B: Backend]  → API
    └→ [Agent C: Database] → Schema
         ↓
   [Integration Agent] → Combine all parts
         ↓
     Result
```

**Example**:
```
Task: "Build a complete user dashboard feature"

Main Claude:
1. Analyzes requirements
2. Spawns parallel agents:

   ├─ frontend-developer:     Build dashboard UI
   ├─ backend-developer:      Build dashboard API
   ├─ database-architect:     Design user data schema
   └─ api-documenter:         Write API documentation

3. Waits for all agents to complete
4. Integration agent: Combines all parts
5. Delivers integrated feature
```

**When to use**:
- Independent subtasks
- No dependencies between agents
- Want to maximize speed
- Have sufficient resources

**Pros**:
- ✅ Fast (parallel execution)
- ✅ Efficient use of time
- ✅ Independent failures

**Cons**:
- ❌ Coordination overhead
- ❌ Integration complexity
- ❌ May need conflict resolution

### Pattern 3: Hub-and-Spoke Coordination

**Structure**: Central orchestrator delegates to specialists

**Diagram**:
```
        [Orchestrator]
         /  |  |  \
        /   |  |   \
    [A]   [B] [C]  [D]
     |     |   |    |
     └─────┴───┴────┘
          Results
```

**Example**:
```
Task: "Comprehensive code review of pull request"

task-orchestrator:
├─ Delegates to code-reviewer:     Code quality analysis
├─ Delegates to security-auditor:  Security vulnerabilities
├─ Delegates to performance-analyzer: Performance issues
└─ Delegates to test-reviewer:     Test coverage

Aggregates all reports:
- Overall score
- Prioritized issues
- Recommended actions
```

**When to use**:
- Complex workflows with many specialized tasks
- Need central coordination
- Want to aggregate results
- Tasks may be conditionally executed

**Pros**:
- ✅ Centralized control
- ✅ Easy to add/remove agents
- ✅ Clear coordination point

**Cons**:
- ❌ Orchestrator becomes complex
- ❌ Single point of failure
- ❌ Context window pressure on orchestrator

### Pattern 4: Iterative Refinement

**Structure**: Agent A → Agent B → Agent A → Agent B (back-and-forth)

**Diagram**:
```
[Agent A: Designer] → Draft Design
        ↓
[Agent B: Reviewer] → Feedback
        ↓
[Agent A: Designer] → Refined Design
        ↓
[Agent B: Reviewer] → Approval
```

**Example**:
```
Task: "Create optimal API design"

Round 1:
api-designer: Create initial API spec
    ↓
backend-architect: Review for scalability
    → Feedback: "Add pagination, improve error handling"

Round 2:
api-designer: Refine spec with feedback
    ↓
security-auditor: Review for security
    → Feedback: "Add rate limiting, improve auth"

Round 3:
api-designer: Final spec incorporating all feedback
    ↓
code-reviewer: Final approval
    → Approved ✓
```

**When to use**:
- Quality critical
- Iterative improvement needed
- Multiple perspectives valuable
- Time allows for iteration

**Pros**:
- ✅ High quality output
- ✅ Multiple expert reviews
- ✅ Continuous improvement

**Cons**:
- ❌ Time consuming
- ❌ Context window growth
- ❌ May not converge

### Pattern 5: Conditional Routing

**Structure**: Decision → Agent A OR Agent B OR Agent C

**Diagram**:
```
[Analysis Agent]
    ↓
 Determine type
    ↓
┌───┴───┬────────┐
│       │        │
Bug    Feature  Refactor
│       │        │
v       v        v
[Debugger] [Developer] [Architect]
```

**Example**:
```
Task: "Handle user issue"

issue-analyzer: Analyze user report
    ↓
If bug:        → debugger (find and fix bug)
If feature:    → feature-developer (implement feature)
If question:   → documentation-writer (improve docs)
If performance: → performance-engineer (optimize)
```

**When to use**:
- Different types of tasks
- Route based on analysis
- Want specialized handling
- Clear decision criteria

**Pros**:
- ✅ Efficient routing
- ✅ Specialized handling
- ✅ Avoids unnecessary work

**Cons**:
- ❌ Requires good analysis
- ❌ Misrouting wastes effort
- ❌ Decision logic can be complex

---

## Orchestration Strategies from the Community

### Strategy 1: Early Delegation (Recommended by Anthropic)

**Principle**: Delegate complex tasks to subagents EARLY to preserve main context

**Example**:
```
User: "Build an e-commerce platform"

Main Claude (immediately):
"This is a complex multi-domain task. Let me delegate to specialized agents:

1. backend-architect: Design system architecture
2. database-architect: Design data model
3. frontend-developer: Create UI mockups
4. devops-engineer: Plan infrastructure

I'll coordinate the results and ensure integration."
```

**Benefits**:
- Preserves main Claude's context window
- Specialized expertise from the start
- Parallel work possible
- Clear separation of concerns

### Strategy 2: Progressive Delegation

**Principle**: Start broad, delegate specific subtasks as complexity emerges

**Example**:
```
User: "Improve application performance"

Main Claude:
1. Analyzes codebase
2. Identifies bottlenecks
3. Delegates specific issues:
   ├─ database-optimizer: "Optimize these 5 queries"
   ├─ frontend-developer: "Reduce bundle size of dashboard"
   └─ backend-developer: "Implement caching for API endpoints"
4. Integrates all optimizations
```

**Benefits**:
- Focused delegation
- Only delegate when needed
- Main Claude maintains overview

### Strategy 3: Specialist Consultation

**Principle**: Use agents as consultants for specific questions

**Example**:
```
Main Claude: (implementing auth system)
1. Writes initial implementation
2. Consults security-auditor: "Review this auth flow"
3. Incorporates feedback
4. Consults performance-engineer: "Is this OAuth flow efficient?"
5. Refines implementation
6. Delivers final code
```

**Benefits**:
- Main Claude stays in control
- Expert validation at checkpoints
- Lower coordination overhead

---

## Orchestration Anti-Patterns

### ❌ Anti-Pattern 1: Over-Delegation

**Problem**: Creating agents for trivial tasks

**Example**:
```
User: "Add a console.log statement"

Main Claude:
└─ Delegates to logger-expert agent
   └─ Delegates to javascript-syntax-validator agent
      └─ Delegates to code-formatter agent
         └─ Finally adds console.log
```

**Solution**: Handle simple tasks directly; only delegate complex work

### ❌ Anti-Pattern 2: Circular Dependencies

**Problem**: Agents waiting on each other

**Example**:
```
frontend-developer: "Need API spec from backend-developer"
    ↓
backend-developer: "Need UI mockups from frontend-developer"
    ↓
(Deadlock)
```

**Solution**: Use orchestrator to resolve dependencies or define clear order

### ❌ Anti-Pattern 3: Context Explosion

**Problem**: Too many agents with too much state sharing

**Example**:
```
10 agents all need to know:
- Current architecture
- Database schema
- API contracts
- Business requirements
- User preferences

= 10x context duplication
```

**Solution**: Minimize state sharing; use orchestrator as single source of truth

### ❌ Anti-Pattern 4: Agent Ping-Pong

**Problem**: Agents passing work back and forth indefinitely

**Example**:
```
Round 1: Designer → Reviewer (feedback)
Round 2: Designer → Reviewer (feedback)
Round 3: Designer → Reviewer (feedback)
Round 4: Designer → Reviewer (feedback)
... (never converges)
```

**Solution**: Set iteration limits; establish clear acceptance criteria

---

## Orchestration Best Practices

### ✅ DO:

1. **Delegate early for complex tasks** (Anthropic recommendation)
2. **Use parallel execution when possible** (maximize efficiency)
3. **Minimize state sharing** (reduce context duplication)
4. **Set clear boundaries** (each agent has defined role)
5. **Establish handoff protocols** (what each agent produces/consumes)
6. **Monitor context usage** (watch for explosion)
7. **Use orchestrators for complex flows** (centralized coordination)
8. **Define success criteria upfront** (prevent endless iteration)

### ❌ DON'T:

1. **Over-delegate trivial tasks** (overhead exceeds benefit)
2. **Create circular dependencies** (leads to deadlock)
3. **Share too much context** (duplication wastes tokens)
4. **Let agents iterate indefinitely** (set limits)
5. **Forget integration** (agents must produce compatible outputs)
6. **Ignore failures** (have fallback plans)
7. **Make orchestrator too complex** (it becomes a bottleneck)

---

## Orchestrator Agent Pattern

### Meta-Orchestrator Design

Many repositories include a dedicated orchestrator agent:

**Example** (task-orchestrator pattern):
```yaml
---
name: task-orchestrator
description: "Coordinate multiple subagents for complex workflows. Use PROACTIVELY for multi-step tasks requiring diverse expertise."
tools: [Read, Write]  # Minimal tools (delegates execution)
model: opus  # Needs strong reasoning
---

You are a task orchestrator specializing in breaking down complex problems and coordinating specialized subagents.

## Approach
1. **Analyze**: Understand full scope and requirements
2. **Decompose**: Break into independent subtasks
3. **Delegate**: Assign each subtask to appropriate agent
4. **Monitor**: Track progress of all agents
5. **Integrate**: Combine results into cohesive solution
6. **Validate**: Ensure all requirements met

## Delegation Strategy
- Identify required expertise for each subtask
- Match subtasks to agent capabilities
- Determine dependencies (sequential vs parallel)
- Set clear success criteria for each agent
- Plan integration approach

## Output
- Task breakdown with assignments
- Dependency graph
- Integration plan
- Final validated result
```

**When to create an orchestrator**:
- Frequently coordinate multiple agents
- Complex multi-step workflows
- Want reusable coordination logic
- Managing 4+ agents regularly

---

## Real-World Orchestration Examples

### Example 1: Feature Implementation

```
Task: "Implement user authentication with OAuth2"

Orchestration flow:
1. Main Claude analyzes requirements
2. Parallel delegation:
   ├─ backend-architect: Design auth architecture
   │  → API endpoints, flow diagram, security patterns
   │
   ├─ database-architect: Design user/session schema
   │  → Tables, indexes, relationships
   │
   └─ security-auditor: Review OAuth2 implementation plan
      → Security checklist, compliance requirements

3. Main Claude integrates designs

4. Sequential implementation:
   backend-developer: Implement based on integrated design
   → Working authentication system

5. Verification:
   ├─ security-auditor: Final security review
   └─ code-reviewer: Code quality review

6. Main Claude delivers final, reviewed implementation
```

**Duration**: ~30 minutes
**Agents used**: 5
**Context saved**: ~50k tokens (vs. main Claude doing everything)

### Example 2: Performance Crisis

```
Task: "API response time increased 10x, fix urgently"

Orchestration flow:
1. devops-troubleshooter: Rapid incident analysis
   → Identifies database query issue

2. Parallel investigation:
   ├─ database-optimizer: Analyze slow queries
   │  → Missing index on users table
   │
   └─ backend-developer: Review API endpoint code
      → N+1 query problem found

3. database-optimizer: Add index (immediate fix)
   → Response time improved 80%

4. backend-developer: Refactor to eliminate N+1
   → Response time back to normal

5. performance-engineer: Prevent recurrence
   → Add query monitoring, performance budgets
```

**Duration**: ~15 minutes
**Agents used**: 4
**Result**: Issue resolved, prevention measures added

### Example 3: Large Refactoring

```
Task: "Refactor monolith to microservices"

Orchestration flow:
1. task-orchestrator: Analyze scope
   → Massive task, coordinate multiple agents

2. Sequential analysis:
   backend-architect: Design microservice boundaries
   → Identifies 5 services

3. For each service (parallel):
   service-extractor: Extract service from monolith
   → Individual service codebases

4. Sequential for each:
   ├─ backend-developer: Refine and test service
   ├─ api-designer: Create service API docs
   └─ devops-engineer: Deploy service

5. Integration:
   ├─ backend-architect: Design inter-service communication
   └─ devops-engineer: Set up API gateway

6. Validation:
   ├─ code-reviewer: Review all service code
   ├─ security-auditor: Review service security
   └─ performance-engineer: Load test entire system
```

**Duration**: ~2 hours
**Agents used**: 8
**Services created**: 5
**Context saved**: Massive (vs. single session)

---

## Measuring Orchestration Effectiveness

### Metrics to Track

1. **Task Completion Time**
   - Single agent vs. multi-agent
   - Sequential vs. parallel

2. **Context Token Usage**
   - Main session tokens
   - Total across all agents
   - Savings from delegation

3. **Quality Metrics**
   - Code quality scores
   - Test coverage
   - Security vulnerabilities found

4. **Agent Utilization**
   - How often each agent is used
   - Success rate per agent
   - Rework frequency

### Success Indicators

✅ **Good orchestration**:
- Tasks complete faster
- Higher quality output
- Main context stays clean
- Clear agent responsibilities
- Minimal rework needed

❌ **Poor orchestration**:
- More time than single agent
- Coordination overhead high
- Context duplication
- Unclear responsibilities
- Frequent back-and-forth

---

## Conclusion

Effective agent orchestration:
1. **Delegate early** for complex tasks (preserve context)
2. **Use parallel execution** when possible (maximize speed)
3. **Choose right pattern** (sequential, parallel, hub-spoke, etc.)
4. **Minimize state sharing** (reduce context duplication)
5. **Set clear boundaries** (each agent has defined role)
6. **Monitor and iterate** (improve based on metrics)

**Key Principle**:
> Use specialized agents for specialized tasks. Coordinate thoughtfully. Integrate carefully.

---

**Related Documents**:
- `behavior-descriptions.md` - How to write effective agent descriptions
- `system-prompt-patterns.md` - Structuring agent prompts
- `tool-selection-guide.md` - Choosing the right tools for agents
