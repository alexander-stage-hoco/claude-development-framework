# Claude Code Best Practices - Official Guidance

**Source**: https://www.anthropic.com/engineering/claude-code-best-practices
**Last Updated**: 2025-10-01
**Purpose**: Synthesize Anthropic's official best practices for Claude Code and agents

---

## Core Philosophy

Claude Code is intentionally **"low-level and unopinionated"**, providing close to raw model access without forcing specific workflows. This design choice maximizes flexibility but requires users to establish their own best practices.

### Key Principle
> "Do the simplest thing that works"

---

## Agent Design Philosophy

### When to Use Subagents

**Use subagents for complex problems, especially early in a task.**

Benefits:
- Preserves context availability in main session
- Allows specialized analysis without polluting main context
- Enables parallel work on different aspects

Example pattern:
```
User: "Build a new authentication system"

Claude: "Let me delegate to specialized subagents:
1. security-auditor - Review security requirements
2. backend-architect - Design authentication flow
3. database-designer - Design user/session schema
4. implementation-engineer - Implement the system"
```

### Subagent Invocation Keywords

The description field determines automatic invocation. **Keywords matter**:

#### "PROACTIVELY"
- **Effect**: Claude actively looks for opportunities to delegate
- **Best for**: Common, frequently-needed tasks
- **Example**: `"Use PROACTIVELY when creating UI components"`

**Anthropic Recommendation**:
> "Include terms like 'use PROACTIVELY' or 'MUST BE USED' in the description fields of custom agents to encourage proactive agent use."

#### "MUST BE USED"
- **Effect**: Enforces strict delegation requirements
- **Best for**: Critical domain expertise, compliance requirements
- **Example**: `"MUST BE USED for all API design decisions"`

#### Implicit Triggers (Without Keywords)
- **Effect**: Claude decides based on task match
- **Best for**: Obvious domain matches
- **Example**: `"Senior backend engineer specializing in Python and FastAPI"`

---

## Extended Thinking Mode

### Computational Budget Allocation

Using the word **"think"** triggers extended thinking mode, giving Claude additional computation time.

### Thinking Levels (Ascending Budget)

```
"think" < "think hard" < "think harder" < "ultrathink"
```

Each level allocates progressively more thinking budget:

| Phrase | Thinking Budget | Best For |
|--------|----------------|----------|
| **"think"** | Standard | Normal complexity tasks |
| **"think hard"** | Increased | Complex reasoning, architecture |
| **"think harder"** | High | Multi-step optimization, intricate logic |
| **"ultrathink"** | Maximum | Extremely complex problems, novel solutions |

### Example Usage

```
# Standard
User: "Optimize this function"

# Extended thinking
User: "Think hard about optimizing this algorithm for both speed and memory"

# Maximum thinking
User: "Ultrathink the best architecture for a distributed cache system with consistency guarantees"
```

---

## Context Management

### CLAUDE.md Files

Create `CLAUDE.md` files to provide **persistent context and guidelines**.

#### Strategic Placement

Place `CLAUDE.md` files at different levels:

```
~/CLAUDE.md                    # Global preferences (all projects)
~/projects/CLAUDE.md           # Multi-project defaults
~/projects/my-app/CLAUDE.md    # Project-specific
~/projects/my-app/src/CLAUDE.md # Module-specific
```

**Claude reads all relevant CLAUDE.md files in the hierarchy.**

#### Effective CLAUDE.md Content

```markdown
# Project: My Application

## Development Rules
1. Always write tests first (TDD)
2. Use TypeScript strict mode
3. Follow functional programming patterns

## Subagent Usage
- Use backend-architect PROACTIVELY for API design
- Use security-auditor for ALL authentication code

## Code Style
- ESLint config: .eslintrc.js
- Prettier for formatting
- Maximum line length: 100 characters

## Testing
- Jest for unit tests
- Cypress for E2E tests
- Minimum coverage: 80%
```

### Context Window Management

**Use `/clear` regularly** to reset context window and maintain focus.

#### When to Clear Context

- After completing a major task
- When switching to different area of codebase
- At 70-80% context usage
- When responses become less focused

#### Context Preservation Strategy

Before clearing:
1. Summarize current state
2. Update relevant documentation
3. Commit work with clear message
4. Use subagents to offload specialized analysis

---

## Tool Permissions

### Start Conservative

**Anthropic Recommendation**: Start conservatively with tool permissions, then expand as needed.

### Permission Configuration

#### Via `/permissions` Command
```
/permissions
```
Shows current allowed tools and lets you customize.

#### Via CLI Flag (Session-Specific)
```bash
claude-code --allowedTools "Read,Write,Bash"
```

### Recommended Tool Sets by Use Case

| Use Case | Recommended Tools | Rationale |
|----------|------------------|-----------|
| **Code Review** | `Read, Grep, Glob` | Read-only, no modifications |
| **Development** | `Read, Write, MultiEdit, Bash` | Full dev workflow |
| **Documentation** | `Read, Write` | Read code, write docs |
| **DevOps** | `Read, Bash, Docker` | Infrastructure tasks |
| **Research** | `Read, WebFetch, WebSearch` | Information gathering |

---

## Workflow Patterns

### 1. Test-Driven Development (TDD)

**Best Practice**: Prefer workflows with explicit targets (tests).

```
1. Write failing test
2. Implement minimal code to pass
3. Refactor
4. Verify all tests pass
```

**Why it works**: Tests provide concrete success criteria.

### 2. Visual Design Iteration

**Best Practice**: Use visual targets (mockups, screenshots) for UI work.

```
1. Provide design mockup
2. Implement UI
3. Generate screenshot
4. Compare to mockup
5. Iterate until match
```

**Why it works**: Visual feedback is unambiguous.

### 3. Explore → Plan → Code → Commit

**Best Practice**: Break work into phases with explicit milestones.

```
Phase 1: Explore (gather context, read code)
Phase 2: Plan (design approach, identify changes)
Phase 3: Code (implement with tests)
Phase 4: Commit (save progress, document)
```

**Why it works**: Checkpoints prevent context drift.

### 4. Iterative Refinement

**Best Practice**: Multiple iterations refine output quality.

```
Iteration 1: "Generate initial implementation"
Iteration 2: "Improve error handling"
Iteration 3: "Add comprehensive tests"
Iteration 4: "Optimize performance"
```

**Why it works**: Incremental improvements are easier than perfect first try.

---

## Multi-Agent Orchestration

### Sequential Pipeline

**Pattern**: Task A → outputs to → Task B → outputs to → Task C

```
1. architect-agent: Design system architecture
2. implementation-agent: Implement core logic
3. test-agent: Write comprehensive tests
4. review-agent: Code review and suggestions
```

**When to use**: Clear dependencies between tasks

### Parallel Fan-Out

**Pattern**: Task A → spawns → (Task B1, Task B2, Task B3) → merge results

```
1. main-agent: Analyzes requirements
2. Spawn parallel agents:
   - frontend-agent: Build UI
   - backend-agent: Build API
   - database-agent: Design schema
3. integration-agent: Combine all parts
```

**When to use**: Independent subtasks that can run concurrently

### Hub-and-Spoke Coordination

**Pattern**: Central orchestrator delegates to specialized agents

```
task-orchestrator (hub)
├── delegates to → security-auditor
├── delegates to → performance-analyzer
├── delegates to → code-reviewer
└── aggregates results and reports
```

**When to use**: Complex workflows with many specialized tasks

---

## Reliability Improvements

### 1. Be Specific

❌ **Vague**: "Make it better"
✅ **Specific**: "Reduce API response time from 500ms to <100ms by adding caching"

### 2. Provide Quantitative Targets

❌ **Qualitative**: "Improve test coverage"
✅ **Quantitative**: "Increase test coverage from 65% to 90%"

### 3. Give Visual/Concrete Examples

❌ **Abstract**: "Make the UI modern"
✅ **Concrete**: "Match the design in design-mockup.png"

### 4. Use Verification Steps

```
1. Implement feature
2. Run tests (verify all pass)
3. Generate screenshot (verify matches mockup)
4. Check performance (verify <100ms)
5. Security scan (verify no vulnerabilities)
```

### 5. Leverage Subagents for Verification

```
After implementing authentication:
1. Use security-auditor to verify security
2. Use test-runner to verify test coverage
3. Use performance-analyzer to verify speed
```

---

## Safe "YOLO" Mode

### When to Use Full Autonomy

In **controlled environments**, you can enable more autonomous behavior:

#### Conditions for YOLO Mode
- ✅ Working on dedicated branch (not main)
- ✅ Comprehensive test suite exists
- ✅ Easy to revert changes (git)
- ✅ Non-production environment
- ✅ Clear rollback plan

#### YOLO Mode Workflow
```
1. "Implement feature X with full autonomy"
2. Claude creates branch, writes code, tests, commits
3. You review PR, provide feedback
4. Claude addresses feedback
5. You approve and merge (or reject and rollback)
```

### When NOT to Use YOLO Mode

❌ Production systems without tests
❌ Main branch (protected)
❌ Irreversible operations (database migrations)
❌ Security-critical code
❌ External API calls with side effects

---

## Claude Sonnet 4.5 Specific Improvements

### Enhanced State Tracking

Sonnet 4.5 excels at **long-horizon reasoning tasks** with exceptional state tracking.

**Capability**: Maintains orientation across extended sessions by:
- Tracking progress across multiple steps
- Remembering context from earlier in conversation
- Focusing on incremental progress rather than attempting everything at once

**Best Practice**: Break large tasks into checkpoints and let Sonnet 4.5 track progress.

### Native Subagent Orchestration

Sonnet 4.5 demonstrates **improved native subagent orchestration** capabilities.

**Capability**: Recognizes when tasks would benefit from delegating work to specialized subagents and does so proactively without requiring explicit instruction.

**Best Practice**: Let Sonnet 4.5 decide when to use subagents; it often makes better delegation decisions than explicit instructions.

---

## Anti-Patterns to Avoid

### 1. Over-Prompting

❌ **Problem**: Excessive detail constrains creativity
```
"Use exactly this algorithm: [500 lines of pseudocode]"
```

✅ **Solution**: State requirements, let Claude choose approach
```
"Sort these items by priority. Must be O(n log n) or better."
```

### 2. Micromanagement

❌ **Problem**: Step-by-step instructions remove autonomy
```
"First read file A, then parse line 5, then extract field 3, then..."
```

✅ **Solution**: State goal, trust Claude to figure out steps
```
"Extract user IDs from the access logs"
```

### 3. Context Bloat

❌ **Problem**: Loading too much context upfront
```
[Loads entire codebase before asking simple question]
```

✅ **Solution**: Just-in-time context loading
```
"Tell me about user authentication"
→ Claude reads only relevant auth files
```

### 4. Unclear Success Criteria

❌ **Problem**: No way to verify correctness
```
"Make the code better"
```

✅ **Solution**: Explicit verification
```
"Refactor to reduce cyclomatic complexity below 10, verified by SonarQube"
```

---

## Summary: Golden Rules

1. **Start simple**, add complexity only when needed
2. **Use subagents** for complex, specialized tasks
3. **Include "PROACTIVELY"** in descriptions for automatic delegation
4. **Manage context** with CLAUDE.md files and regular `/clear`
5. **Set permissions** conservatively, expand as needed
6. **Be specific** with requirements and success criteria
7. **Use thinking modes** ("think hard") for complex problems
8. **Iterate** rather than expecting perfection first try
9. **Trust Sonnet 4.5** to orchestrate subagents naturally
10. **Verify** with tests, benchmarks, and checks

---

## References

- **Anthropic Blog Post**: https://www.anthropic.com/engineering/claude-code-best-practices
- **Claude Code Documentation**: https://docs.claude.com/en/docs/claude-code
- **Effective Context Engineering**: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

---

**Document Version**: 1.0
**Last Updated**: 2025-10-01
**Based On**: Official Anthropic engineering blog post on Claude Code best practices
