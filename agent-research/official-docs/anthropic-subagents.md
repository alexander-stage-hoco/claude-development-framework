# Claude Code Subagents - Official Documentation Synthesis

**Source**: https://docs.claude.com/en/docs/claude-code/sub-agents
**Last Updated**: 2025-10-01
**Purpose**: Synthesize official Anthropic documentation on Claude Code subagents

---

## What Are Subagents?

**Subagents are specialized AI assistants** that can be invoked to handle specific types of tasks. They enable more efficient problem-solving by providing task-specific configurations with:

- Customized system prompts
- Restricted tool access
- Separate context windows
- Domain-specific expertise

### Key Benefits

1. **Isolated Context**: Each subagent operates in its own context window, preventing pollution of the main conversation
2. **Specialized Expertise**: Pre-configured for specific domains or tasks
3. **Improved Focus**: Restricted tool access keeps agents focused on their domain
4. **Preserves Main Context**: Main conversation context remains clean while subagents handle specific tasks

---

## Configuration Structure

Subagents are defined using **YAML frontmatter** followed by a **system prompt**:

```yaml
---
name: your-sub-agent-name
description: When this subagent should be invoked
tools: [optional tool list]
model: sonnet  # Optional model selection
---

System prompt defining role and capabilities
```

### Configuration Fields

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| **name** | Yes | Unique identifier (lowercase, hyphen-separated) | `code-reviewer` |
| **description** | Yes | Natural language explanation of purpose and when to invoke | `"Expert code review specialist. Proactively reviews code for quality."` |
| **tools** | No | Optional list of allowed tools | `[Read, Grep, Glob, Bash]` |
| **model** | No | Model selection: `sonnet`, `opus`, `haiku`, or `inherit` | `opus` |

### Description Field Best Practices

The `description` field is crucial for automatic delegation. Claude Code uses it to determine when to invoke the subagent.

**Effective descriptions include**:
- **Clear trigger conditions**: "when creating REST APIs"
- **Domain expertise**: "Expert React developer"
- **Proactive keywords**: "PROACTIVELY", "MUST BE USED"

**Example descriptions**:

```yaml
# Good - Clear and specific
description: "Expert React developer. Use PROACTIVELY when creating UI components or fixing frontend issues."

# Good - Strong trigger
description: "Design RESTful APIs and database schemas. MUST BE USED for new backend service architecture."

# Bad - Too vague
description: "Helps with development tasks"

# Bad - No clear trigger
description: "General purpose developer"
```

---

## Subagent Locations

Subagents can be stored in three locations:

### 1. Project-Level (Recommended for project-specific agents)
```
.claude/agents/
```
- Specific to the current project
- Version controlled with project
- Shared with team members

### 2. User-Level (Recommended for personal agents)
```
~/.claude/agents/
```
- Available across all projects
- Personal preferences and tools
- Not shared with team

### 3. CLI-Defined (Temporary, for testing)
```bash
claude-code --agent "name:test-agent,description:Testing,tools:Read,Write"
```
- Temporary for current session only
- Useful for experimentation
- Not persisted

---

## Invocation Methods

### 1. Automatic Delegation (Preferred)

Claude Code automatically delegates tasks based on:
- Task description in your prompt
- `description` field in subagent configuration
- Current context

**Example**:
```
User: "Review the authentication code for security issues"

Claude Code automatically delegates to security-auditor subagent
```

### 2. Explicit Invocation

You can explicitly request a specific subagent:

```
User: "Use the code-reviewer subagent to analyze this file"
```

---

## Tool Restrictions

Subagents can have restricted tool access for **security and focus**:

```yaml
# Minimal tools (read-only analysis)
tools: [Read, Grep, Glob]

# Backend development tools
tools: [Read, Write, MultiEdit, Bash, Docker]

# Full access (no restrictions)
tools: []  # or omit the tools field
```

### Common Tool Combinations

| Agent Type | Typical Tools | Rationale |
|------------|---------------|-----------|
| **Code Reviewer** | `[Read, Grep, Glob]` | Read-only analysis, no modifications |
| **Backend Developer** | `[Read, Write, Bash, Docker]` | Full development capability |
| **Security Auditor** | `[Read, Grep]` | Analysis only, no code changes |
| **Documentation Writer** | `[Read, Write]` | Read code, write docs |
| **DevOps Engineer** | `[Read, Bash, Docker]` | Infrastructure management |

---

## Model Selection

Choose the appropriate model based on task complexity:

### **Haiku** (Fastest, Cheapest)
- **Best for**: Quick, focused tasks
- **Examples**: Code formatting, simple refactoring, documentation updates
- **Latency**: Lowest
- **Cost**: Lowest

### **Sonnet** (Balanced, Default)
- **Best for**: Standard development tasks
- **Examples**: Feature implementation, bug fixes, code reviews
- **Latency**: Medium
- **Cost**: Medium

### **Opus** (Most Capable, Expensive)
- **Best for**: Complex reasoning and architecture
- **Examples**: System design, complex refactoring, security analysis
- **Latency**: Highest
- **Cost**: Highest

### **Inherit** (From Main Session)
- Uses the same model as main Claude Code session
- Default if not specified

---

## System Prompt Guidelines

### Structure

Effective system prompts have clear sections:

```markdown
You are a [ROLE] specializing in [DOMAIN].

## Your Responsibilities
1. [Primary responsibility]
2. [Secondary responsibility]
3. [Tertiary responsibility]

## Approach
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Guidelines
- [Guideline 1]
- [Guideline 2]

## Output Format
[Expected output structure]
```

### Length Recommendations

- **Minimum**: 200 words (enough context)
- **Optimal**: 300-600 words (detailed but focused)
- **Maximum**: 1000 words (avoid overly complex prompts)

### Content Balance

**Find the "right altitude"** - not too vague, not too complex:

❌ **Too Vague**: "You help with development"
❌ **Too Complex**: "If X then Y, unless Z, but when A, check B..."
✅ **Just Right**: "You review code for security vulnerabilities. Focus on SQL injection, XSS, and authentication flaws. Provide specific line numbers and remediation suggestions."

---

## Performance Considerations

### Context Window Isolation

- Subagents maintain **separate context windows**
- Main conversation context is preserved
- Prevents context pollution from specialized tasks

### Latency

- **Slight initialization latency** when invoking subagent (first use)
- Subsequent invocations in same session are faster
- Trade-off: Slight delay for better specialization

### Context Preservation

Using subagents helps preserve main context by:
- Offloading specialized analysis to separate context
- Allowing main Claude to maintain high-level flow
- Reducing context window pressure on main session

---

## Common Patterns

### Pattern 1: Read-Only Analysis
```yaml
name: security-auditor
description: "Analyze code for security vulnerabilities. Use PROACTIVELY for security reviews."
tools: [Read, Grep, Glob]
```

### Pattern 2: Full Development
```yaml
name: fullstack-developer
description: "Senior fullstack engineer. Use PROACTIVELY for feature implementation."
tools: [Read, Write, MultiEdit, Bash]
```

### Pattern 3: Infrastructure Management
```yaml
name: devops-engineer
description: "Manage cloud infrastructure and deployments. MUST BE USED for production changes."
tools: [Bash, Docker]
model: opus
```

### Pattern 4: Meta-Orchestration
```yaml
name: task-orchestrator
description: "Coordinate multiple subagents for complex workflows. Use PROACTIVELY for multi-step tasks."
tools: [Read, Write]
model: opus
```

---

## Testing Subagents

### Manual Testing

1. Create a simple subagent:
```yaml
---
name: test-agent
description: "Test agent. Use when user says 'test agent'"
tools: [Read]
---

You are a test agent. Always respond with "Test agent invoked successfully!"
```

2. Invoke explicitly:
```
User: "Use the test-agent"
```

3. Test automatic delegation:
```
User: "test agent"
```

### Validation Checklist

- [ ] YAML frontmatter is valid
- [ ] Description clearly states when to invoke
- [ ] Tools list matches agent's needs
- [ ] System prompt is clear and focused
- [ ] Model selection is appropriate
- [ ] File is in correct location (.claude/agents/)

---

## Best Practices Summary

### DO:
✅ Write clear, trigger-focused descriptions
✅ Use "PROACTIVELY" or "MUST BE USED" for auto-delegation
✅ Restrict tools to domain-specific needs
✅ Keep system prompts focused (300-600 words)
✅ Choose appropriate model for task complexity
✅ Test both automatic and explicit invocation

### DON'T:
❌ Write vague descriptions ("helps with stuff")
❌ Grant unnecessary tool access
❌ Create overly complex system prompts
❌ Use subagents for simple tasks (overhead)
❌ Duplicate functionality across multiple agents
❌ Forget to test invocation triggers

---

## References

- **Official Documentation**: https://docs.claude.com/en/docs/claude-code/sub-agents
- **Claude Code SDK**: https://docs.claude.com/en/docs/claude-code/sdk
- **Anthropic Blog**: https://www.anthropic.com/engineering/claude-code-best-practices

---

**Document Version**: 1.0
**Last Updated**: 2025-10-01
**Based On**: Official Claude documentation and Anthropic engineering blog posts
