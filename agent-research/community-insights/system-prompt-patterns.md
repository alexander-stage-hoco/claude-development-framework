# System Prompt Patterns - Structure & Best Practices

**Purpose**: Analysis of effective system prompt structures from top Claude Code subagent repositories
**Sources**: wshobson/agents (12.5k stars), VoltAgent/awesome-claude-code-subagents (1.6k stars), Official Anthropic guidance
**Last Updated**: 2025-10-01

---

## What is a System Prompt?

The content after the YAML frontmatter that defines the agent's:
- **Role and identity**
- **Expertise and capabilities**
- **Approach and methodology**
- **Output format and style**
- **Behavioral traits**

```yaml
---
name: agent-name
description: When to invoke this agent
tools: [Read, Write]
---

Everything after this line is the system prompt.
```

---

## The "Right Altitude" Principle

From Anthropic's official guidance:

> **Too vague**: "You are a helpful assistant. Do good work."
>
> **Too complex**: "If condition A and condition B, unless flag C is set..."
>
> **Just right**: Clear role + Specific responsibilities + Structured approach

---

## Common Prompt Structures

### Structure 1: Minimal (wshobson/agents - Simple Agents)

**Pattern**: Role + Focus Areas + Approach + Output

**Example** (backend-architect, ~200 words):
```markdown
You are a backend system architect specializing in scalable API design and microservices.

## Focus Areas
- RESTful API design with proper versioning and error handling
- Service boundary definition and inter-service communication
- Database schema design (normalization, indexes, sharding)

## Approach
1. Start with clear service boundaries
2. Design APIs contract-first
3. Consider data consistency requirements

## Output
- API endpoint definitions with example requests/responses
- Service architecture diagram (mermaid or ASCII)
- Database schema with key relationships
```

**When to use**: Simple, focused agents with narrow domains

**Length**: 200-400 words

### Structure 2: Comprehensive (wshobson/agents - Complex Agents)

**Pattern**: Role + Purpose + Capabilities + Behavioral Traits + Knowledge Base + Response Approach + Examples

**Example** (ai-engineer, ~800 words):
```markdown
You are an AI engineer specializing in production-grade LLM applications...

## Purpose
[Why this agent exists, what problems it solves]

## Core Expertise
### LLM Application Development
- OpenAI, Anthropic (Claude), Gemini, and open-source LLMs
- Prompt engineering and optimization

### RAG (Retrieval-Augmented Generation)
- Vector databases (Pinecone, Weaviate, Qdrant, Chroma)
- Embedding models and semantic search

## Development Approach
1. **Requirements** - Define use case, users, success metrics
2. **Architecture** - Choose models, tools, data sources

## Output Style
- Concrete code examples with modern best practices
- Architecture diagrams for complex systems

## Best Practices
- Start simple - basic LLM call before complex RAG
- Evaluate early and often with real data
```

**When to use**: Complex domains requiring detailed guidance

**Length**: 600-1000 words

### Structure 3: Checklist-Driven (VoltAgent)

**Pattern**: Role + Checklist + Workflow + Technology Stack + Best Practices

**Example** (fullstack-developer, ~400 words):
```markdown
You are an end-to-end fullstack developer...

## Core Expertise

### Fullstack Development Checklist
- **Architecture**: System design, tech stack selection
- **Backend**: APIs, microservices, authentication
- **Frontend**: React/Vue/Angular, responsive design
- **Testing**: Unit, integration, E2E tests

### Workflow
1. **Requirements** - Understand user needs
2. **Architecture** - Design full-stack solution
3. **Backend** - Implement APIs
4. **Frontend** - Build UI
5. **Integration** - Connect all layers

### Technology Stack
- **Frontend**: React, Next.js, TypeScript
- **Backend**: Node.js, Python, Express
- **Database**: PostgreSQL, MongoDB, Redis

## Best Practices
- Start with API design and database schema
- Use TypeScript across the stack
- Test at each integration point
```

**When to use**: Practical, implementation-focused agents

**Length**: 400-600 words

---

## Section-by-Section Analysis

### 1. Role Definition

**Purpose**: Establish identity and primary expertise

**Patterns**:
```markdown
# Pattern A: Simple role statement
"You are a [ROLE] specializing in [DOMAIN]."

# Pattern B: Role with expertise
"You are a [SENIORITY] [ROLE] with expertise in [DOMAIN1], [DOMAIN2], and [DOMAIN3]."

# Pattern C: Role with focus
"You are a [ROLE] specializing in [DOMAIN]. Your focus spans [AREA1], [AREA2], and [AREA3] with emphasis on [PRIMARY_GOAL]."
```

**Examples from repositories**:
```markdown
# wshobson/agents (simple)
"You are a backend system architect specializing in scalable API design and microservices."

# VoltAgent (detailed)
"You are a senior code reviewer with expertise in identifying code quality issues, security vulnerabilities, and optimization opportunities across multiple programming languages. Your focus spans correctness, performance, maintainability, and security with emphasis on constructive feedback, best practices enforcement, and continuous improvement."
```

**Best practice**: Use Pattern C for complex agents, Pattern A for simple agents

### 2. Core Expertise / Capabilities

**Purpose**: Define specific skills and knowledge areas

**Patterns**:
```markdown
# Pattern A: Bulleted list
## Core Expertise
- Skill 1
- Skill 2
- Skill 3

# Pattern B: Categorized sections
## Core Expertise
### Category 1
- Skill A
- Skill B

### Category 2
- Skill C
- Skill D

# Pattern C: Checklist format
## Development Checklist
- **Area 1**: Specific skills
- **Area 2**: Specific skills
```

**When to use each**:
- **Pattern A**: Simple agents with <10 skills
- **Pattern B**: Complex agents with distinct domains (most common)
- **Pattern C**: Practical, implementation-focused agents (VoltAgent style)

### 3. Workflow / Approach

**Purpose**: Define step-by-step methodology

**Patterns**:
```markdown
# Pattern A: Numbered steps (wshobson)
## Approach
1. Step 1
2. Step 2
3. Step 3

# Pattern B: Workflow with descriptions (VoltAgent)
## Workflow
1. **Step Name** - Description of what happens
2. **Step Name** - Description of what happens

# Pattern C: Phase-based
## Development Phases
### Phase 1: Discovery
- Activity A
- Activity B

### Phase 2: Implementation
- Activity C
- Activity D
```

**Best practice**: Use Pattern B (workflow with descriptions) for clarity

### 4. Technology Stack

**Purpose**: List specific tools, frameworks, and technologies

**Pattern**:
```markdown
## Technology Stack
- **Category 1**: Tool A, Tool B, Tool C
- **Category 2**: Tool D, Tool E
- **Category 3**: Tool F, Tool G
```

**Examples**:
```markdown
# Frontend Developer
### Technology Stack
- **Frontend**: React, Next.js, TypeScript, Tailwind CSS
- **State Management**: Zustand, Jotai, React Context
- **Testing**: Jest, Vitest, Playwright, Cypress
- **Tools**: Vite, Turbopack, ESLint, Prettier

# Cloud Architect
### Technology Stack
- **Cloud Platforms**: AWS, Azure, GCP
- **IaC Tools**: Terraform, CloudFormation, Pulumi
- **Container Orchestration**: Kubernetes, ECS, AKS, GKE
```

**Best practice**: Categorize technologies by function or layer

### 5. Output Format / Style

**Purpose**: Define expected output structure

**Patterns**:
```markdown
# Pattern A: Bulleted expectations
## Output
- Format 1
- Format 2
- Format 3

# Pattern B: Structured format
## Output Format
- **Component 1**: Description
- **Component 2**: Description
- **Component 3**: Description

# Pattern C: For-each-issue format (code reviewers)
## Output Format
For each issue found:
- **Severity**: Critical / High / Medium / Low
- **Category**: Security / Performance / Bug
- **Location**: File path and line number
- **Issue**: Clear description
```

**Best practice**: Use Pattern C for analysis agents, Pattern B for builders

### 6. Best Practices / Guidelines

**Purpose**: Encode domain wisdom and principles

**Pattern**:
```markdown
## Best Practices
- Practice 1: Explanation
- Practice 2: Explanation
- Practice 3: Explanation
```

**Examples**:
```markdown
# Backend Developer
## Best Practices
- Design APIs contract-first with OpenAPI/GraphQL schemas
- Implement comprehensive error handling and logging
- Use database transactions for data consistency
- Apply caching at multiple layers (Redis, CDN)

# Security Auditor
## Best Practices
- Follow recognized frameworks (NIST, CIS, OWASP)
- Document all findings with evidence
- Prioritize risks by impact and likelihood
- Provide specific remediation steps
```

**Best practice**: Include 5-10 practices; more is overwhelming, fewer is insufficient

---

## Prompt Length Guidelines

### By Agent Complexity

| Agent Type | Word Count | Example |
|------------|-----------|---------|
| **Simple** | 200-400 words | backend-architect (wshobson) |
| **Standard** | 400-600 words | fullstack-developer (VoltAgent) |
| **Complex** | 600-1000 words | ai-engineer (wshobson) |
| **Very Complex** | 1000-1500 words | security-auditor (comprehensive) |

### Official Anthropic Guidance

- **Minimum**: 200 words (enough context)
- **Optimal**: 300-600 words (detailed but focused)
- **Maximum**: 1000 words (avoid overly complex prompts)

### Token Considerations

- **Haiku agents**: Keep prompts <500 words (fast invocation)
- **Sonnet agents**: 400-800 words optimal
- **Opus agents**: 600-1200 words (can handle complexity)

---

## Tone and Voice Analysis

### wshobson/agents Voice

**Characteristics**:
- Direct and professional
- Action-oriented ("Design", "Build", "Implement")
- Focuses on practical output
- Lists specific technologies

**Example**:
> "Always provide concrete examples and focus on practical implementation over theory."

### VoltAgent Voice

**Characteristics**:
- Systematic and methodical
- Checklist-driven
- Emphasizes process and workflow
- Broader technology coverage

**Example**:
> "Your focus spans correctness, performance, maintainability, and security with emphasis on constructive feedback, best practices enforcement, and continuous improvement."

### Recommended Voice

**Balance both approaches**:
- Be **direct** like wshobson
- Be **systematic** like VoltAgent
- Be **specific** about technologies
- Be **clear** about expected outputs

---

## Common Sections Across Repositories

### Must-Have Sections (>90% of agents include)

1. ✅ **Role definition** (100%)
2. ✅ **Core expertise / capabilities** (95%)
3. ✅ **Workflow / approach** (90%)
4. ✅ **Best practices** (85%)

### Should-Have Sections (50-90%)

5. **Technology stack** (75% - especially for development agents)
6. **Output format** (70% - especially for analysis agents)
7. **Examples** (50% - varies by agent type)

### Nice-to-Have Sections (<50%)

8. **Behavioral traits** (30% - mostly in VoltAgent)
9. **Anti-patterns** (25% - in code review / architecture agents)
10. **Integration guidelines** (20% - in orchestration agents)

---

## Section Order Recommendations

### Option 1: Top-Down (Concept → Practice)
```
1. Role definition
2. Purpose / Core expertise
3. Technology stack
4. Workflow / Approach
5. Output format
6. Best practices
```

**When to use**: Educational agents, architecture agents

### Option 2: Bottom-Up (Practice → Concept)
```
1. Role definition
2. Checklist (what to do)
3. Workflow (how to do it)
4. Technology stack (with what)
5. Best practices (principles)
```

**When to use**: Implementation agents, practical agents (VoltAgent style)

### Option 3: Hybrid (Most Common)
```
1. Role definition
2. Core expertise (categorized)
3. Workflow
4. Technology stack
5. Output format
6. Best practices
```

**When to use**: General-purpose agents, most agents

---

## Prompt Templates by Agent Type

### Development Agent Template
```markdown
You are a [SENIORITY] [ROLE] specializing in [DOMAIN].

## Core Expertise
### [Category 1]
- [Skills]

### [Category 2]
- [Skills]

## Workflow
1. **[Phase 1]** - [Description]
2. **[Phase 2]** - [Description]
3. **[Phase 3]** - [Description]

## Technology Stack
- **[Layer 1]**: [Tools]
- **[Layer 2]**: [Tools]

## Best Practices
- [Practice 1]
- [Practice 2]
- [Practice 3]

Focus on [PRIMARY_GOAL].
```

### Analysis Agent Template
```markdown
You are a [SENIORITY] [ROLE] with expertise in [DOMAIN].

## Focus Areas
- [Area 1]
- [Area 2]
- [Area 3]

## Analysis Approach
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Output Format
For each [ITEM]:
- **[Field 1]**: [Format]
- **[Field 2]**: [Format]
- **[Field 3]**: [Format]

## Best Practices
- [Practice 1]
- [Practice 2]

[Closing statement about approach]
```

### Infrastructure Agent Template
```markdown
You are an expert [ROLE] with deep knowledge of [PLATFORMS].

## Core Expertise
### [Category 1]
- [Skills]

### [Category 2]
- [Skills]

## Workflow
1. **[Phase]** - [Description]
2. **[Phase]** - [Description]

## Technology Stack
- **[Platform/Tool Category]**: [Specific tools]

## Best Practices
- [Practice 1]
- [Practice 2]

Focus on building [OUTCOME].
```

---

## Anti-Patterns to Avoid

### ❌ Too Vague
```markdown
You are a helpful developer who writes good code.
```
**Problem**: No specific guidance or expertise definition

### ❌ Too Complex
```markdown
You are a developer. When the user asks for X, check if Y is true, and if so, do Z unless A is set, in which case do B, but only if C is not conflicting with D...
```
**Problem**: Overly nested logic that should be in code, not prompt

### ❌ Technology Dump
```markdown
## Technologies
React, Vue, Angular, Svelte, Solid, Qwik, Next.js, Nuxt, SvelteKit, Remix, Astro, TypeScript, JavaScript, HTML, CSS, Sass, Less, Tailwind, Bootstrap, Material-UI...
```
**Problem**: Too many technologies dilutes expertise

### ❌ Missing Structure
```markdown
You are a backend developer. You know Node.js, Python, databases, APIs, Docker, Kubernetes, and cloud platforms. You write good code and follow best practices.
```
**Problem**: No sections, no methodology, no output format

### ❌ Inconsistent Sections
```markdown
## Core Expertise
[Content]

## Approach
[Content]

## Some Random Section
[Content]

## Technologies
[Content]

## Another Thing
[Content]
```
**Problem**: No clear structure or logical flow

---

## Best Practices Summary

### ✅ DO:

1. **Start with clear role** (who is this agent?)
2. **Use consistent section structure** (pick a template and stick to it)
3. **Categorize expertise** (group related skills)
4. **Define workflow** (give step-by-step approach)
5. **List specific technologies** (be concrete)
6. **Specify output format** (what does the agent produce?)
7. **Include 5-10 best practices** (encode domain wisdom)
8. **End with a focus statement** (reinforce primary goal)
9. **Keep it scannable** (use headings, bullets, bold)
10. **Aim for 300-600 words** (detailed but focused)

### ❌ DON'T:

1. **Be vague** (avoid generic statements)
2. **Overload with technologies** (<20 technologies max)
3. **Write novels** (>1200 words is too long)
4. **Skip structure** (always use sections)
5. **Use inconsistent formatting** (be consistent)
6. **Forget output format** (agents need to know what to produce)
7. **Include nested logic** (keep it simple)
8. **Duplicate content** (each section should be unique)

---

## Conclusion

Effective system prompts:
1. **Define clear roles** with specific expertise
2. **Use consistent structure** (templates help)
3. **Provide methodologies** (workflows, approaches)
4. **List technologies** (specific, categorized)
5. **Specify outputs** (formats, structures)
6. **Encode best practices** (domain wisdom)
7. **Stay focused** (300-600 words optimal)

The system prompt is where you encode the agent's expertise - invest time in structuring it well.

---

**Related Documents**:
- `behavior-descriptions.md` - How to write effective descriptions
- `tool-selection-guide.md` - Choosing the right tools for your agent
- `orchestration-strategies.md` - Multi-agent coordination patterns
