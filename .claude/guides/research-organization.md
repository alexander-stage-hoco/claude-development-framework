# Research Folder Structure

**Version**: 2.0
**Last Updated**: 2025-09-30
**Purpose**: Organization system for research artifacts, learnings, and reference materials

---

## Overview

The `research/` folder stores all research artifacts that inform implementation decisions. This includes:
- Academic papers and whitepapers
- Blog posts and articles
- Reference implementations (source code)
- Synthesized learnings
- Research-based decisions (ADRs)

**Key Principle**: Research informs implementation (Rule #4). Document what you learn before building.

---

## Folder Structure

```
research/
├── README.md                    # This file
├── papers/                      # Academic papers and whitepapers
│   ├── authentication/
│   │   ├── oauth2-rfc6749.pdf
│   │   ├── jwt-spec-rfc7519.pdf
│   │   └── paper-summary.md
│   ├── algorithms/
│   │   ├── merkle-tree-paper.pdf
│   │   └── summary-merkle-trees.md
│   └── [topic]/
│       ├── [paper-name].pdf
│       └── summary-[topic].md
│
├── articles/                    # Blog posts, tutorials, guides
│   ├── fastapi-best-practices/
│   │   ├── article-link.md     # Link + key takeaways
│   │   └── code-examples/
│   ├── postgresql-performance/
│   │   ├── article-links.md
│   │   └── summary.md
│   └── [topic]/
│       ├── article-links.md
│       └── summary.md
│
├── implementations/             # Reference source code and examples
│   ├── auth-service-example/
│   │   ├── README.md           # What this example demonstrates
│   │   ├── src/                # Actual code
│   │   └── analysis.md         # What we learned from it
│   ├── payment-gateway-integration/
│   │   ├── stripe-example/
│   │   ├── paypal-example/
│   │   └── comparison.md
│   └── [component]/
│       ├── README.md
│       ├── [source-code]/
│       └── analysis.md
│
├── learnings/                   # Synthesized insights and summaries
│   ├── authentication-approaches.md
│   ├── database-patterns.md
│   ├── api-design-principles.md
│   └── [topic]-learnings.md
│
└── decisions/                   # Research-driven Architecture Decision Records
    ├── ADR-001-python-framework.md
    ├── ADR-002-database-choice.md
    └── ADR-XXX-[decision].md
```

---

## Usage Guidelines

### 1. Papers (Academic Research)

**Purpose**: Store formal research papers, RFCs, specifications, whitepapers

**Structure**:
```
papers/[topic]/
├── [paper-filename].pdf
├── paper-summary.md
└── key-insights.md
```

**Template**: See `.claude/templates/research/paper-summary.md`

---

### 2. Articles (Blog Posts, Tutorials)

**Purpose**: Store links, excerpts, and summaries of blog posts, tutorials

**Structure**:
```
articles/[topic]/
├── article-links.md
├── summary.md
└── code-examples/
```

**Template**: See `.claude/templates/research/article-links.md`

---

### 3. Implementations (Reference Source Code)

**Purpose**: Store reference implementations to learn from

**Recommended Workflow**: Use dedicated Claude session for analysis (see 3a below)

**Structure**:
```
implementations/[project-name]/
├── CLAUDE.md          # Analysis instructions (from template)
├── summary.md         # Analysis output
├── [source-code]/     # Cloned/copied code
└── LICENSE
```

**Templates**:
- `.claude/templates/implementation-CLAUDE.md` - Instructions for Claude
- `.claude/templates/implementation-summary.md` - Summary template
- `.claude/templates/research/implementation-readme.md` - Manual README template

---

### 3a. Implementation Analysis Workflow (Using Dedicated Claude Sessions)

**Purpose**: Systematically analyze reference implementations using dedicated Claude sessions

**When you find valuable reference code**, follow this workflow to analyze it with Claude's help:

#### Step 1: Set Up Implementation Folder

```bash
cd research/implementations/
mkdir [project-name]    # e.g., fastapi-auth-example
cd [project-name]

# Clone or copy the reference code
git clone [repository-url] .
# OR copy files manually
```

#### Step 2: Add Analysis Templates

```bash
# Copy Claude analysis instructions
cp ../../.claude/templates/implementation-CLAUDE.md CLAUDE.md

# Copy summary template
cp ../../.claude/templates/implementation-summary.md summary.md
```

#### Step 3: Start Dedicated Claude Session

**Start a NEW Claude session focused on THIS folder**:

```
Please analyze this reference implementation.
Read CLAUDE.md for instructions.
```

Claude will:
- Read `CLAUDE.md` (analysis protocol)
- Follow 8-step analysis process
- Create `summary.md` with findings
- Optionally create detailed `analysis.md`

**Duration**: Typically 30-60 minutes for thorough analysis

#### Step 4: Review Analysis Output

After Claude completes analysis, you'll have:
- ✅ `summary.md` - High-level findings and reusable components
- ✅ `reusable-code.md` - Specific code snippets to adapt (optional)
- ✅ `analysis.md` - Detailed technical analysis (optional)

#### Step 5: During Main Project Development

When implementing features in your main project, reference this analysis:

```python
"""
Authentication handler for user login.

Specification: UC-002#user-authentication
Reference: research/implementations/fastapi-auth-example/summary.md
Adapted from: JWTHandler pattern (see Component 1 in summary)
"""
```

**Check summary.md for**:
- Relevant components for your use case
- Adaptation requirements
- License compliance
- Quality assessment

#### Step 6: Code Reuse (If Applicable)

Before reusing any code:
1. Read `.claude/templates/code-reuse-checklist.md`
2. Verify license compatibility
3. Extract and adapt code (don't copy blindly)
4. **Write tests FIRST** for adapted code
5. Add attribution if required

---

**Example Complete Workflow**:

```bash
# Found interesting FastAPI auth implementation on GitHub
cd research/implementations/
mkdir fastapi-auth-jwt
cd fastapi-auth-jwt/

# Clone it
git clone https://github.com/example/fastapi-auth .

# Set up analysis
cp ../../.claude/templates/implementation-CLAUDE.md CLAUDE.md
cp ../../.claude/templates/implementation-summary.md summary.md

# Start Claude (new session)
# Say: "Analyze this implementation. Read CLAUDE.md."

# Claude analyzes code and creates summary.md

# Later, during development of UC-002 (User Authentication):
# Reference: research/implementations/fastapi-auth-jwt/summary.md
# Extract JWTHandler component
# Adapt for our architecture
# Test thoroughly
# Integrate into implementation/src/auth/
```

---

**Folder Structure After Analysis**:
```
research/implementations/fastapi-auth-jwt/
├── CLAUDE.md                  # Analysis instructions (from template)
├── summary.md                 # Analysis results ✅
├── reusable-code.md          # Code snippets (optional)
├── analysis.md               # Detailed analysis (optional)
├── src/                       # Original reference code
│   ├── main.py
│   ├── auth/
│   └── tests/
├── LICENSE                    # Original license
└── README.md                  # Original README
```

---

**Why Dedicated Sessions?**

1. **Focus**: Claude focuses solely on analyzing this implementation
2. **Context**: CLAUDE.md provides clear analysis protocol
3. **Thoroughness**: Systematic 8-step analysis process
4. **Reusability**: Summary persists for future reference
5. **Separation**: Keeps analysis separate from main project development

---

**Integration with Main Project**:

The analysis output (summary.md) becomes a **reference document** for your main project:
- Link from specifications: "See research/implementations/[project]/ for pattern"
- Reference during implementation: Check for reusable components
- Inform ADRs: Use findings to make architectural decisions

---

### 4. Learnings (Synthesized Insights)

**Purpose**: Synthesized understanding of a topic after reading multiple sources

**Structure**: Single markdown file per topic
```
learnings/[topic]-learnings.md
```

**Template**: Create custom based on topic (typical sections: Overview, Key Principles, Approaches Considered, Recommended Approach, Implementation Guidance, Pitfalls, References)

---

### 5. Decisions (Architecture Decision Records)

**Purpose**: Document technical decisions based on research

**Structure**: `ADR-XXX-[decision-name].md`

**Location**: `research/decisions/` OR `.claude/technical-decisions.md` (project-wide view)

**Template**: Standard ADR format (Status, Context, Decision, Options Considered, Consequences, References)

---

## Workflow: Research → Decision → Implementation

**Step 1: Identify Knowledge Gap** → Create research plan
**Step 2: Conduct Research** → Gather papers, articles, implementations
**Step 3: Synthesize Learnings** → Create `learnings/[topic].md`
**Step 4: Make Decision** → Create `decisions/ADR-XXX.md`
**Step 5: Update Technical Decisions** → Add to `.claude/technical-decisions.md`
**Step 6: Implement** → Reference research in code docstrings

---

## Research Checklist

Before implementing complex features:
- [ ] Research conducted (papers, articles, implementations)
- [ ] Learnings documented (`learnings/[topic].md`)
- [ ] Decision made (ADR created if needed)
- [ ] Ready to implement (understand problem, know approach)

---

## Tips for Effective Research

1. **Start Broad, Go Deep** - Overview articles → Papers → Implementations
2. **Compare Multiple Sources** - Cross-reference, identify consensus vs. debate
3. **Focus on Applicability** - Always ask "How does this apply to our project?"
4. **Track Learnings Over Time** - Revisit and update as project evolves
5. **Reference Research in Code** - Add ADR references in docstrings

---

## Integration with Claude Development Framework

**Claude's Role**:
- Conducts research when knowledge gap identified (Rule #4)
- Documents findings in appropriate folders
- Creates ADRs for technical decisions
- References research in implementation code

**Context Priority**: Research is TIER 2 (read after CLAUDE.md, development-rules.md, before implementation)

---

**Remember**: Research is Rule #4 - not optional for novel features. Document, decide, then implement.