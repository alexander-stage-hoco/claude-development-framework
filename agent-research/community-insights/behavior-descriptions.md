# Behavior Descriptions - Community Patterns & Best Practices

**Purpose**: Analysis of effective behavior description patterns from top Claude Code subagent repositories
**Sources**: wshobson/agents (12.5k stars), VoltAgent/awesome-claude-code-subagents (1.6k stars)
**Last Updated**: 2025-10-01

---

## What is a Behavior Description?

The `description` field in a subagent's YAML frontmatter determines when Claude Code automatically invokes that agent. It's the **single most important field** for automatic delegation.

```yaml
---
name: your-agent
description: This text controls when the agent is automatically invoked
tools: [Read, Write]
---
```

---

## The Magic Keywords

### 1. "PROACTIVELY"

**Effect**: Claude actively looks for opportunities to delegate to this agent

**Pattern from wshobson/agents**:
```yaml
description: "Build React components, implement responsive layouts... Use PROACTIVELY when creating UI components or fixing frontend issues."
```

**When to use**:
- Frequently-needed agents (frontend, backend, code review)
- Core development tasks
- Common workflow agents

**Examples from community**:
- ✅ "Use PROACTIVELY for API documentation or developer portal creation" (api-documenter)
- ✅ "Use PROACTIVELY when creating UI components or fixing frontend issues" (frontend-developer)
- ✅ "Use PROACTIVELY for debugging, incident response, or system troubleshooting" (devops-troubleshooter)

### 2. "MUST BE USED"

**Effect**: Enforces strict delegation requirements

**When to use**:
- Critical domain expertise
- Compliance requirements
- Security-sensitive tasks
- High-stakes decisions

**Examples**:
- ✅ "MUST BE USED for all API design decisions"
- ✅ "MUST BE USED for security audits and compliance validation"
- ✅ "MUST BE USED for production database schema changes"

### 3. "Expert" / "Specializing in" / "Masters"

**Effect**: Establishes credibility and domain expertise

**Pattern Analysis**:
- wshobson/agents: "Expert X specializing in Y. Masters Z."
- VoltAgent: "Expert X engineer specializing in Y... Masters Z with focus on W."

**Examples**:
- "Expert security auditor specializing in DevSecOps, comprehensive cybersecurity..."
- "Expert cloud architect specializing in multi-cloud strategies..."
- "Masters vector search, multimodal AI, agent orchestration..."

---

## Anatomy of Great Behavior Descriptions

### Pattern 1: Triple-Component Structure (wshobson/agents)

```
[Role] + [Expertise] + [Trigger Keywords]
```

**Example**:
```yaml
description: "Expert DevOps troubleshooter specializing in rapid incident response, advanced debugging, and modern observability. Masters log analysis, distributed tracing, Kubernetes debugging, performance optimization, and root cause analysis. Use PROACTIVELY for debugging, incident response, or system troubleshooting."
```

**Breakdown**:
1. **Role**: "Expert DevOps troubleshooter"
2. **Expertise**: "specializing in rapid incident response... Masters log analysis..."
3. **Trigger**: "Use PROACTIVELY for debugging, incident response, or system troubleshooting"

### Pattern 2: Focus-First Structure (VoltAgent)

```
[Role] + [Core Capability] + [Focus Areas]
```

**Example**:
```yaml
description: "Senior backend engineer specializing in scalable API development and microservices architecture. Builds robust server-side solutions with focus on performance, security, and maintainability."
```

**Breakdown**:
1. **Role**: "Senior backend engineer"
2. **Core Capability**: "scalable API development and microservices architecture"
3. **Focus Areas**: "performance, security, and maintainability"

---

## Length Guidelines

### From Repository Analysis

**wshobson/agents** (verbose, explicit triggers):
- Average: 200-300 characters
- Includes explicit "Use PROACTIVELY" or trigger conditions
- Lists specific technologies and domains

**VoltAgent** (concise, focused):
- Average: 150-200 characters
- Omits trigger keywords (relies on domain match)
- Focuses on core expertise

### Recommended Length

- **Minimum**: 100 characters (enough for role + expertise + trigger)
- **Optimal**: 150-250 characters (detailed without overwhelming)
- **Maximum**: 400 characters (avoid overly complex descriptions)

---

## Common Patterns by Agent Type

### Development Agents
```yaml
# Backend
description: "Senior backend engineer specializing in scalable API development and microservices architecture. Use PROACTIVELY when creating new backend services or APIs."

# Frontend
description: "Build React components, implement responsive layouts, and handle client-side state management. Use PROACTIVELY when creating UI components or fixing frontend issues."

# Fullstack
description: "End-to-end feature owner with expertise across the entire stack. Delivers complete solutions from database to UI with focus on seamless integration."
```

### Specialist Agents
```yaml
# Security
description: "Expert security auditor specializing in DevSecOps, comprehensive cybersecurity, and compliance frameworks. Use PROACTIVELY for security audits, DevSecOps, or compliance implementation."

# Performance
description: "Performance optimization expert. Masters profiling, benchmarking, and system optimization. Use when optimizing code, queries, or infrastructure performance."

# AI/ML
description: "Build production-ready LLM applications, advanced RAG systems, and intelligent agents. Use PROACTIVELY for LLM features, chatbots, AI agents, or AI-powered applications."
```

### Infrastructure Agents
```yaml
# Cloud
description: "Expert cloud architect specializing in multi-cloud strategies, scalable architectures, and cost-effective solutions. Masters AWS, Azure, and GCP with focus on security, performance, and compliance."

# DevOps
description: "Expert DevOps troubleshooter specializing in rapid incident response, advanced debugging, and modern observability. Use PROACTIVELY for debugging, incident response, or system troubleshooting."

# Database
description: "Database architect specializing in schema design, query optimization, and data modeling. Use PROACTIVELY for database design decisions."
```

---

## Anti-Patterns to Avoid

### ❌ Too Vague
```yaml
description: "Helps with development tasks"
# Problem: No clear trigger, no domain expertise
```

### ❌ Too Generic
```yaml
description: "General purpose developer"
# Problem: Won't be invoked automatically, overlaps with main Claude
```

### ❌ Too Complex
```yaml
description: "If the user needs frontend work and it involves React or Vue, but not Angular unless it's TypeScript, and also handles state management except for Redux which should use the redux-specialist, then use this agent, but only on Tuesdays."
# Problem: Overly specific logic confuses invocation
```

### ❌ No Trigger Keywords
```yaml
description: "I write code in Python and JavaScript"
# Problem: No indication of when to invoke
```

### ❌ Lists Only Technologies
```yaml
description: "React, Next.js, TypeScript, Tailwind, Jest, Cypress"
# Problem: Missing role, capabilities, and triggers
```

---

## Testing Your Description

### Manual Testing Checklist

1. **Is the role clear?**
   - Can someone instantly understand what this agent does?

2. **Is the expertise specific?**
   - Does it list concrete skills and domains?

3. **Are trigger conditions obvious?**
   - Does it include "PROACTIVELY" or "when X" clauses?

4. **Is it concise?**
   - Can it be read and understood in 5 seconds?

5. **Does it avoid overlap?**
   - Is it distinct from other agents in your set?

### A/B Testing Framework

Create two variations and observe invocation frequency:

**Variation A** (Implicit):
```yaml
description: "Senior backend engineer specializing in scalable API development and microservices architecture."
```

**Variation B** (Explicit):
```yaml
description: "Senior backend engineer specializing in scalable API development and microservices architecture. Use PROACTIVELY when creating new backend services or APIs."
```

**Result**: Variation B typically sees 2-3x more automatic invocations

---

## Decision Tree for Trigger Keywords

```
Should I use "PROACTIVELY"?
├─ Is this agent frequently needed? → YES: Use PROACTIVELY
├─ Is this a core development task? → YES: Use PROACTIVELY
└─ Is this a specialized/rare task? → NO: Use specific trigger ("when X")

Should I use "MUST BE USED"?
├─ Is this security-critical? → YES: Use MUST BE USED
├─ Is this compliance-related? → YES: Use MUST BE USED
├─ Is incorrect execution dangerous? → YES: Use MUST BE USED
└─ Otherwise → NO: Use PROACTIVELY or implicit trigger

Should I list specific triggers?
├─ Is the domain narrow (e.g., GraphQL)? → YES: "when designing GraphQL schemas"
├─ Is the task infrequent? → YES: "for blockchain smart contracts"
└─ Is it frequently needed? → NO: Just use PROACTIVELY
```

---

## Real-World Examples Analysis

### Example 1: backend-architect (wshobson/agents)

```yaml
description: "Design RESTful APIs, microservice boundaries, and database schemas. Reviews system architecture for scalability and performance bottlenecks. Use PROACTIVELY when creating new backend services or APIs."
```

**Analysis**:
- ✅ Clear role: "Design RESTful APIs..."
- ✅ Specific capabilities: "microservice boundaries, database schemas"
- ✅ Explicit trigger: "Use PROACTIVELY when creating new backend services or APIs"
- ✅ Length: 202 characters (optimal)
- ✅ Model selection: `opus` (complex reasoning tasks)

**Invocation triggers**:
- "Create a new microservice for user authentication"
- "Design the database schema for our e-commerce platform"
- "Review our API architecture for scalability"

### Example 2: security-auditor (VoltAgent)

```yaml
description: "Expert security auditor specializing in comprehensive security assessments, compliance validation, and risk management. Masters security frameworks, audit methodologies, and compliance standards with focus on identifying vulnerabilities and ensuring regulatory adherence."
```

**Analysis**:
- ✅ Strong role: "Expert security auditor"
- ✅ Comprehensive expertise: "security assessments, compliance validation, risk management"
- ✅ Domain authority: "Masters security frameworks, audit methodologies"
- ❌ No explicit trigger keywords (relies on domain matching)
- ✅ Length: 283 characters (detailed)

**Invocation triggers**:
- "Audit our authentication system for security vulnerabilities"
- "Review compliance with SOC 2 requirements"
- "Perform security assessment of our API"

### Example 3: ai-engineer (wshobson/agents)

```yaml
description: "Build production-ready LLM applications, advanced RAG systems, and intelligent agents. Implements vector search, multimodal AI, agent orchestration, and enterprise AI integrations. Use PROACTIVELY for LLM features, chatbots, AI agents, or AI-powered applications."
```

**Analysis**:
- ✅ Action-oriented role: "Build production-ready LLM applications"
- ✅ Specific technologies: "RAG systems, vector search, multimodal AI"
- ✅ Multiple explicit triggers: "LLM features, chatbots, AI agents, AI-powered applications"
- ✅ Strong keyword: "Use PROACTIVELY"
- ✅ Length: 265 characters
- ✅ Model: `opus` (complex AI reasoning)

**Invocation triggers**:
- "Add a chatbot to our customer support page"
- "Implement RAG for our documentation search"
- "Build an AI agent that processes customer emails"

---

## Best Practices Summary

### ✅ DO:

1. **Start with a strong role** ("Expert X", "Senior Y", "Build Z")
2. **Include specific expertise** (technologies, domains, methodologies)
3. **Add explicit triggers** ("Use PROACTIVELY when...", "MUST BE USED for...")
4. **Keep it scannable** (150-250 characters optimal)
5. **Test both with and without keywords** (A/B test)
6. **Make it unique** (distinct from other agents)
7. **Use action verbs** ("Build", "Design", "Audit", "Optimize")

### ❌ DON'T:

1. **Be vague** ("Helps with things")
2. **List only technologies** (missing context of use)
3. **Overcomplicate** (nested conditions, excessive detail)
4. **Duplicate existing agents** (overlap causes confusion)
5. **Forget trigger keywords** (reduces automatic invocation)
6. **Write novels** (>400 characters is too long)
7. **Ignore your model selection** (description should match model complexity)

---

## Template Library

### General Development
```yaml
description: "[Senior/Expert] [Role] specializing in [Domain]. [Key capabilities]. Use PROACTIVELY when [trigger conditions]."
```

### Security/Compliance
```yaml
description: "Expert [Role] specializing in [Domain]. Masters [expertise areas]. MUST BE USED for [critical tasks]."
```

### Specialized Technical
```yaml
description: "[Action verb] [deliverables] with focus on [outcomes]. Masters [technologies]. Use when [specific trigger]."
```

### Meta/Orchestration
```yaml
description: "[Orchestration role] coordinating [what]. Delegates to specialized agents for [tasks]. Use PROACTIVELY for [complex workflows]."
```

---

## Conclusion

Effective behavior descriptions are:
1. **Clear**: Role and expertise immediately obvious
2. **Specific**: Concrete technologies and domains
3. **Triggered**: Explicit keywords for automatic invocation
4. **Concise**: 150-250 characters sweet spot
5. **Unique**: Distinct from other agents

The description field is the primary mechanism for automatic agent delegation - invest time in crafting it well.

---

**Next Steps**:
- Review your agent descriptions against these patterns
- A/B test with/without "PROACTIVELY" keyword
- Monitor which agents are invoked automatically
- Iterate based on usage patterns
