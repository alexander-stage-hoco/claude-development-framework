# Tool Selection Guide - Restricting Agent Capabilities

**Purpose**: Analysis of tool restriction strategies and patterns from top Claude Code subagent repositories
**Sources**: wshobson/agents (12.5k stars), VoltAgent/awesome-claude-code-subagents (1.6k stars), Official Anthropic guidance
**Last Updated**: 2025-10-01

---

## What are Agent Tools?

The `tools` field in YAML frontmatter specifies which tools an agent can use:

```yaml
---
name: code-reviewer
description: Expert code reviewer...
tools: [Read, Grep, Glob]  # Read-only tools
---
```

**Why restrict tools?**
1. **Focus**: Prevents agents from wandering outside their domain
2. **Security**: Limits potential damage from errors
3. **Clarity**: Makes agent capabilities obvious
4. **Performance**: Faster decision-making with fewer options

---

## Available Tools in Claude Code

### File Operations
- **Read**: Read file contents
- **Write**: Create or overwrite files
- **Edit**: Modify existing files (search/replace)
- **MultiEdit**: Batch edit multiple files
- **Glob**: Pattern-based file search
- **Grep**: Content-based file search

### Execution & System
- **Bash**: Execute shell commands
- **Docker**: Docker container operations
- **Python**: Python execution (some repos)

### Specialized (Repository-Specific)
- **Database**: Database operations (VoltAgent)
- **Redis**: Redis operations (VoltAgent)
- **PostgreSQL**: PostgreSQL operations (VoltAgent)
- **kubectl**: Kubernetes operations (custom)
- **terraform**: Infrastructure as Code (custom)
- **aws-cli, azure-cli, gcloud**: Cloud platform CLIs (custom)

### Documentation & Collaboration (Custom)
- **Magic**: Unknown (VoltAgent)
- **Context7**: Unknown (VoltAgent)
- **Playwright**: Browser automation (VoltAgent)

---

## Tool Restriction Patterns

### Pattern 1: Read-Only Analysis (Most Restrictive)

**Tools**: `[Read, Grep, Glob]`

**When to use**:
- Code reviewers
- Security auditors
- Architecture reviewers
- Documentation reviewers
- Analysis agents

**Examples from repositories**:
```yaml
# wshobson/agents - code-reviewer
tools: [Read, Grep, Glob, git, eslint, sonarqube, semgrep]

# VoltAgent - code-reviewer
tools: [Read, Grep, Glob, git, eslint, sonarqube, semgrep]

# Custom security-auditor
tools: [Read, Grep, nessus, qualys, openvas, prowler, scout suite]
```

**Rationale**:
- ✅ Safe (no modifications possible)
- ✅ Fast (limited decision space)
- ✅ Focused (analysis only)
- ❌ Can't fix issues found
- ❌ Can't generate reports (unless using Write for that)

### Pattern 2: Development (Moderate Restriction)

**Tools**: `[Read, Write, MultiEdit, Bash]`

**When to use**:
- Backend developers
- Frontend developers
- Feature developers
- Test writers

**Examples**:
```yaml
# wshobson/agents - backend-developer (inferred)
tools: [Read, Write, MultiEdit, Bash]

# VoltAgent - backend-developer
tools: [Read, Write, MultiEdit, Bash, Docker, database, redis, postgresql]

# VoltAgent - frontend-developer
tools: [Read, Write, MultiEdit, Bash, npm, git]
```

**Rationale**:
- ✅ Can read and modify code
- ✅ Can run builds and tests
- ✅ Can create new files
- ❌ May modify wrong files
- ⚠️ Requires careful testing

### Pattern 3: Infrastructure (Specialized Tools)

**Tools**: `[Read, Write, Bash, Docker, kubectl, terraform, cloud-cli]`

**When to use**:
- DevOps engineers
- Cloud architects
- Infrastructure as Code specialists
- Platform engineers

**Examples**:
```yaml
# VoltAgent - cloud-architect
tools: [Read, Write, MultiEdit, Bash, aws-cli, azure-cli, gcloud, terraform, kubectl, draw.io]

# Custom devops-engineer
tools: [Read, Write, Bash, Docker, kubectl, helm, terraform]

# Custom kubernetes-architect
tools: [Read, Write, Bash, kubectl, helm, kustomize]
```

**Rationale**:
- ✅ Full infrastructure access
- ✅ Can deploy and configure
- ⚠️ High-impact operations
- ❌ Potential for production changes

### Pattern 4: Full Stack (Least Restrictive)

**Tools**: `[Read, Write, MultiEdit, Bash, Docker, database, redis, postgresql, magic, context7, playwright]`

**When to use**:
- Fullstack developers
- End-to-end feature owners
- Integration specialists

**Example**:
```yaml
# VoltAgent - fullstack-developer
tools: [Read, Write, MultiEdit, Bash, Docker, database, redis, postgresql, magic, context7, playwright]
```

**Rationale**:
- ✅ Complete development freedom
- ✅ Can handle entire feature
- ❌ May blur responsibilities
- ❌ Longer decision time (more tools)

### Pattern 5: Specialized Domains

**Tools**: Custom tool sets for specific domains

**Examples**:
```yaml
# ML Engineer
tools: [mlflow, kubeflow, tensorflow, sklearn, optuna]

# Blockchain Developer
tools: [truffle, hardhat, web3, ethers, solidity, foundry]

# CLI Developer
tools: [Read, Write, MultiEdit, Bash, commander, yargs, inquirer, chalk, ora, blessed]

# Data Scientist
tools: [python, jupyter, pandas, sklearn, matplotlib, statsmodels]

# API Designer
tools: [Read, Write, MultiEdit, Bash, openapi-generator, graphql-codegen, postman, swagger-ui, spectral]
```

**Rationale**:
- ✅ Domain-specific capabilities
- ✅ Clear expertise boundaries
- ⚠️ May require custom tool implementation
- ❌ Less portable across projects

---

## Tool Selection Decision Tree

```
What does the agent do?

Analysis/Review Only?
├─ YES → [Read, Grep, Glob, domain-specific-linters]
└─ NO  → Continue

Modifies Code/Files?
├─ YES → Add [Write, Edit, MultiEdit]
└─ NO  → Continue

Runs Commands?
├─ YES → Add [Bash]
└─ NO  → Continue

Infrastructure Operations?
├─ YES → Add [Docker, kubectl, terraform, cloud-cli]
└─ NO  → Continue

Database Operations?
├─ YES → Add [database, redis, postgresql]
└─ NO  → Continue

Specialized Domain?
├─ YES → Add domain-specific tools
└─ NO  → Done

Final Tool Set:
- Start with base: [Read, ...]
- Add capabilities incrementally
- Remove unnecessary tools
- Test with real scenarios
```

---

## Tool Combinations by Agent Type

### Code Quality & Review

| Agent Type | Tools | Rationale |
|------------|-------|-----------|
| **Code Reviewer** | `[Read, Grep, Glob, git, eslint, sonarqube, semgrep]` | Read-only analysis |
| **Security Auditor** | `[Read, Grep, nessus, qualys, openvas, prowler]` | Security scanning |
| **Performance Analyzer** | `[Read, Grep, Bash, profiling-tools]` | Analysis + benchmarking |

### Development

| Agent Type | Tools | Rationale |
|------------|-------|-----------|
| **Backend Developer** | `[Read, Write, MultiEdit, Bash, Docker, database]` | Full backend dev |
| **Frontend Developer** | `[Read, Write, MultiEdit, Bash, npm]` | Frontend + build tools |
| **Fullstack Developer** | `[Read, Write, MultiEdit, Bash, Docker, database, redis, playwright]` | Everything needed |

### Infrastructure

| Agent Type | Tools | Rationale |
|------------|-------|-----------|
| **Cloud Architect** | `[Read, Write, Bash, aws-cli, azure-cli, gcloud, terraform, kubectl]` | Multi-cloud IaC |
| **DevOps Engineer** | `[Read, Write, Bash, Docker, kubectl, helm]` | Container orchestration |
| **Network Engineer** | `[Read, Write, Bash, network-tools]` | Network config |

### Data & AI

| Agent Type | Tools | Rationale |
|------------|-------|-----------|
| **ML Engineer** | `[mlflow, kubeflow, tensorflow, sklearn, optuna]` | ML lifecycle |
| **Data Scientist** | `[python, jupyter, pandas, sklearn, matplotlib, statsmodels]` | Data analysis |
| **AI Engineer** | `[Read, Write, Bash, llm-tools, vector-db-tools]` | LLM applications |

### Specialized

| Agent Type | Tools | Rationale |
|------------|-------|-----------|
| **Blockchain Developer** | `[truffle, hardhat, web3, ethers, solidity, foundry]` | Smart contracts |
| **CLI Developer** | `[Read, Write, Bash, commander, yargs, inquirer, chalk]` | CLI frameworks |
| **API Designer** | `[Read, Write, openapi-generator, graphql-codegen, postman, swagger-ui]` | API design tools |

---

## Tool Selection Best Practices

### ✅ DO:

1. **Start minimal** - Add tools only when needed
2. **Match domain** - Tools should align with agent's expertise
3. **Consider safety** - Read-only for analysis agents
4. **Group logically** - Related tools together (e.g., cloud CLIs)
5. **Test thoroughly** - Verify agent can complete tasks with available tools
6. **Document rationale** - Why each tool is included
7. **Review periodically** - Remove unused tools

### ❌ DON'T:

1. **Give everything** - Reduces focus and increases decision time
2. **Forget dependencies** - If using Docker, may need Bash
3. **Mix conflicting tools** - Avoid overlapping functionality
4. **Ignore security** - Don't give write access to read-only agents
5. **Add "just in case"** - Every tool should have a clear purpose
6. **Duplicate functionality** - One tool per capability

---

## Security Implications by Tool Set

### Low Risk (Read-Only)
```yaml
tools: [Read, Grep, Glob]
```
- ✅ Cannot modify files
- ✅ Cannot execute code
- ✅ Cannot affect system
- ⚠️ Can read sensitive data

### Medium Risk (Read-Write)
```yaml
tools: [Read, Write, Edit, MultiEdit]
```
- ⚠️ Can modify code
- ⚠️ Can create files
- ⚠️ Can overwrite files
- ❌ Cannot execute (safer)

### High Risk (Execution)
```yaml
tools: [Read, Write, Bash, Docker]
```
- ❌ Can execute arbitrary commands
- ❌ Can modify system
- ❌ Can install packages
- ❌ Potential for destructive operations

### Critical Risk (Infrastructure)
```yaml
tools: [Bash, terraform, kubectl, aws-cli]
```
- ❌ Can modify production infrastructure
- ❌ Can delete resources
- ❌ Can incur costs
- ❌ Requires strict controls

---

## Performance Considerations

### Tool Count Impact

| Tool Count | Decision Time | When to Use |
|------------|---------------|-------------|
| **1-5 tools** | Fast (<1s) | Specialized agents |
| **6-10 tools** | Medium (1-2s) | Standard agents |
| **11-15 tools** | Slow (2-3s) | Complex agents |
| **16+ tools** | Very slow (3-5s) | Avoid if possible |

**Recommendation**: Keep tool count <10 for optimal performance

### Custom Tools

**Benefits**:
- More specific to domain
- Clearer intent
- Better control

**Drawbacks**:
- Requires implementation
- Maintenance burden
- Less portable

**When to create custom tools**:
- Domain-specific operations (e.g., blockchain, ML)
- Frequent operations (worth the effort)
- Security requirements (need granular control)

---

## Common Tool Patterns

### Minimal Base (All Agents)
```yaml
tools: [Read]
```
Every agent needs at least Read to examine code.

### Read-Only Analysis
```yaml
tools: [Read, Grep, Glob]
```
Standard for code review, security audit, documentation review.

### Basic Development
```yaml
tools: [Read, Write, Bash]
```
Minimum for agents that modify code.

### Standard Development
```yaml
tools: [Read, Write, MultiEdit, Bash]
```
Most common for development agents.

### Full Development
```yaml
tools: [Read, Write, MultiEdit, Bash, Docker, database]
```
For fullstack or complex development agents.

### Infrastructure
```yaml
tools: [Read, Write, Bash, Docker, kubectl, terraform]
```
For DevOps and cloud agents.

---

## Migration Strategy: Expanding Tool Sets

### Phase 1: Start Restrictive
```yaml
# Initial version - minimal tools
tools: [Read, Grep, Glob]
```

### Phase 2: Add as Needed
```yaml
# Agent kept failing, needed Write to create reports
tools: [Read, Grep, Glob, Write]
```

### Phase 3: Add Execution
```yaml
# Agent needed to run tests to verify findings
tools: [Read, Grep, Glob, Write, Bash]
```

### Phase 4: Stabilize
```yaml
# Final tool set after real usage
tools: [Read, Grep, Glob, Write, Bash, git]
```

**Process**:
1. Start with minimal tools
2. Monitor agent failures (tool-related errors)
3. Add tools incrementally
4. Remove unused tools after stabilization
5. Document final rationale

---

## Tool Documentation Template

When defining tools for a new agent, document:

```yaml
---
name: my-agent
description: What this agent does
tools: [Tool1, Tool2, Tool3]
---

# Tool Rationale

- **Tool1**: [Why this tool is needed, what it enables]
- **Tool2**: [Why this tool is needed, what it enables]
- **Tool3**: [Why this tool is needed, what it enables]

# Tools Explicitly Excluded

- **ToolX**: [Why we don't include this, what constraint it enforces]
- **ToolY**: [Why we don't include this, what constraint it enforces]
```

**Example**:
```yaml
---
name: security-auditor
tools: [Read, Grep, nessus, qualys, openvas]
---

# Tool Rationale

- **Read**: Required to examine source code and configuration files
- **Grep**: Essential for searching code for security patterns
- **nessus, qualys, openvas**: Industry-standard vulnerability scanners

# Tools Explicitly Excluded

- **Write**: Security auditor should not modify code (separation of concerns)
- **Bash**: Prevents running arbitrary commands (security constraint)
- **Docker**: Audit should not affect infrastructure
```

---

## Conclusion

Effective tool selection:
1. **Start minimal** - Only essential tools
2. **Match domain** - Tools align with agent expertise
3. **Consider security** - Restrict based on risk
4. **Optimize performance** - <10 tools ideal
5. **Document rationale** - Why each tool is included

Tool restrictions are a key mechanism for:
- Focusing agent behavior
- Improving decision speed
- Enhancing security
- Clarifying capabilities

---

**Related Documents**:
- `behavior-descriptions.md` - How to write effective descriptions
- `system-prompt-patterns.md` - Structuring agent prompts
- `orchestration-strategies.md` - Multi-agent coordination patterns
