#!/bin/bash
# Claude Development Framework - Project Initialization Script
# Version 2.0

set -e

PROJECT_NAME="${1:-my-project}"

echo "========================================="
echo "Claude Development Framework Setup"
echo "========================================="
echo ""
echo "Initializing project: $PROJECT_NAME"
echo ""

# Create project directory
if [ -d "$PROJECT_NAME" ]; then
    echo "⚠️  Directory '$PROJECT_NAME' already exists!"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create directory structure
echo "📁 Creating directory structure..."

mkdir -p "$PROJECT_NAME"/{.claude/{guides,templates,subagents},specs/{use-cases,apis,data-models,architecture},services,research/{papers,articles,implementations,learnings,decisions},planning/{milestones,iterations},implementation/{src,tests/{unit,integration,bdd,system}}}

echo "✅ Directory structure created"

# Copy framework files
echo "📄 Copying framework files..."

# Copy core documentation
cp README.md "$PROJECT_NAME/README-FRAMEWORK.md"
cp quick-start-guide.md "$PROJECT_NAME/"
cp .gitignore "$PROJECT_NAME/" 2>/dev/null || true

# Copy docs folder
mkdir -p "$PROJECT_NAME/docs/advanced"
cp docs/claude-development-framework.md "$PROJECT_NAME/docs/"
cp docs/troubleshooting.md "$PROJECT_NAME/docs/"
cp docs/walkthrough-todo-api.md "$PROJECT_NAME/docs/"
cp docs/example-first-session.md "$PROJECT_NAME/docs/"
cp docs/session-types.md "$PROJECT_NAME/docs/"
cp docs/advanced/tool-integration.md "$PROJECT_NAME/docs/advanced/"
cp docs/advanced/large-codebase-context.md "$PROJECT_NAME/docs/advanced/"

# Copy guides
cp -r .claude/guides/* "$PROJECT_NAME/.claude/guides/"

# Copy templates
cp -r .claude/templates/* "$PROJECT_NAME/.claude/templates/"

# Copy quick-ref
mkdir -p "$PROJECT_NAME/.claude/quick-ref"
cp .claude/quick-ref/* "$PROJECT_NAME/.claude/quick-ref/"

echo "✅ Framework files copied"

# Create initial project files
echo "📝 Creating initial project files..."

# Create .claude/CLAUDE.md from template
cat > "$PROJECT_NAME/.claude/CLAUDE.md" << 'EOF'
# MANDATORY: Read This First in Every Session

**Project**: [PROJECT_NAME]
**Last Updated**: [DATE]

---

## Session Protocol

### At Session Start (ALWAYS)
1. Read this file (CLAUDE.md)
2. Read `.claude/development-rules.md`
3. Read `planning/current-iteration.md`
4. Read `planning/session-state.md` (if exists)
5. Report context usage and current focus

### Before ANY Implementation
1. **STOP** - Do tests exist?
2. **STOP** - Are tests written and failing?
3. **STOP** - Do you have user approval to implement?
4. **Only THEN** write implementation code

### When Tests Fail
- ❌ NEVER simplify tests to make them pass
- ❌ NEVER mock away the problem
- ✅ ALWAYS fix the system/product issue
- ✅ If tests reveal spec issues, update specs first

### At Session End
1. Update `planning/current-iteration.md` with progress
2. Update `planning/session-state.md` for next session
3. Commit work with descriptive message
4. Summarize what was accomplished

---

## The 12 Non-Negotiable Rules

(See `.claude/development-rules.md` for full details)

1. **Specifications Are Law** - Every line traces to a spec, use cases must reference services
2. **Tests Define Correctness** - Written before implementation, never weakened
3. **Incremental Above All** - Max 3 hours per iteration
4. **Research Informs Implementation** - Read before building
5. **Two-Level Planning** - Strategic (UC) + Tactical (iteration)
6. **No Shortcuts** - No TODOs, no skipped error handling
7. **Technical Decisions Are Binding** - ADRs must be followed
8. **BDD for User-Facing Features** - Gherkin files match UC acceptance criteria
9. **Code Quality Standards** - Type hints, docstrings, SRP
10. **Session Discipline** - Start with rules, end with status update
11. **Git Workflow Discipline** - Branch per iteration/UC, commit when tests pass
12. **Mandatory Refactoring** - RED-GREEN-REFACTOR (never skip!)

---

## Anti-Patterns to Reject

If the user asks you to:
- ❌ "Let's skip the spec for now" → REFUSE, say "Spec must exist first"
- ❌ "This test is too strict" → REFUSE, say "Let's analyze root cause"
- ❌ "Let's mock this to make it pass" → REFUSE unless spec requires mock
- ❌ "We can fix the tests later" → REFUSE, say "Tests define correctness"
- ❌ "Let's build multiple features at once" → REFUSE, say "One iteration at a time"

**Your job**: Enforce quality, not just generate code.

---

**Remember**: You are a **disciplined development partner**, not just a code generator.
EOF

# Copy additional framework files to .claude/
cp .claude/templates/development-rules.md "$PROJECT_NAME/.claude/"
cp .claude/templates/start-here.md "$PROJECT_NAME/.claude/"
cp .claude/templates/session-checklist.md "$PROJECT_NAME/.claude/"
cp .claude/templates/context-priority.md "$PROJECT_NAME/.claude/"
cp .claude/templates/technical-decisions.md "$PROJECT_NAME/.claude/"
cp .claude/templates/service-registry.md "$PROJECT_NAME/.claude/"

# Copy research organization guide to research folder
cp .claude/guides/research-organization.md "$PROJECT_NAME/research/README.md"

# Copy services README template
cp .claude/templates/services-README-template.md "$PROJECT_NAME/services/README.md"

# Create README
cat > "$PROJECT_NAME/README.md" << EOF
# $PROJECT_NAME

**Development Framework**: Claude Development Framework v2.0
**Created**: $(date +%Y-%m-%d)

## Project Overview

[Describe your project here]

## Getting Started

### First Session with Claude

Start your first session with any natural prompt:

\`\`\`
Please analyze this project directory and tell me what this is
\`\`\`

OR

\`\`\`
I want to build [X]. Please help me set up this project.
\`\`\`

Claude will automatically read the framework files and guide you through creating specifications.

### For Claude: First Session Protocol

When starting a new session:
1. Read \`.claude/start-here.md\` first (framework orientation)
2. Follow the protocol in \`.claude/CLAUDE.md\`
3. Check \`planning/current-iteration.md\` for current work
4. Review \`planning/session-state.md\` for context (if exists)

The framework is self-teaching - Claude learns everything from these files.

### Development Approach

This project follows a disciplined, spec-driven, incremental development approach:

1. **Specifications First** - Every feature starts with a specification
2. **Test-Driven Development** - Tests written before implementation
3. **Incremental Progress** - Work in 1-3 hour iterations
4. **Research-Informed** - Learn before building
5. **Quality-Focused** - Never compromise tests or standards

See \`claude-development-framework.md\` for complete framework documentation.

## Project Structure

\`\`\`
$PROJECT_NAME/
├── .claude/                    # Claude configuration and guides
│   ├── CLAUDE.md              # Main instructions for Claude
│   ├── development-rules.md   # The 12 non-negotiable rules
│   ├── service-registry.md    # Service catalog and traceability
│   ├── subagents/             # Subagent configurations (for future use)
│   └── guides/                # Reference guides
├── specs/                     # Specifications
│   ├── use-cases/             # Business requirements (must reference services!)
│   └── architecture/          # System design
├── services/                  # Service layer (NEW in v2.0)
│   ├── README.md              # Service architecture guide
│   └── [service-name]/        # Individual services
│       ├── service-spec.md
│       ├── tests/
│       └── benchmarks/
├── research/                  # Research and learnings
├── planning/                  # Planning artifacts
│   ├── current-iteration.md   # Active work
│   └── session-state.md       # Session continuity
└── implementation/            # Source code and tests
    ├── src/
    └── tests/
\`\`\`

## Next Steps

1. Update this README with project-specific information
2. Create \`specs/00-project-overview.md\` with vision and scope
3. Start first session with Claude
4. Let Claude help you create initial specifications

## Framework Resources

- **Main Guide**: \`docs/claude-development-framework.md\`
- **Service Architecture**: \`docs/service-architecture.md\` (NEW in v2.0)
- **Example Project**: \`docs/walkthrough-todo-api.md\`
- **Session Types**: \`docs/session-types.md\` (10 session types)
- **Troubleshooting**: \`docs/troubleshooting.md\`
- **Tool Integration**: \`docs/advanced/tool-integration.md\`
- **Large Codebase**: \`docs/advanced/large-codebase-context.md\`

---

**Remember**: Slow is smooth, smooth is fast. Build with discipline! 🚀
EOF

echo "✅ Initial files created"

# Create placeholder files
echo "📋 Creating placeholder files..."

cat > "$PROJECT_NAME/planning/current-iteration.md" << EOF
# Current Iteration

**Status**: Not Started
**Last Updated**: $(date +%Y-%m-%d)

---

## Active Work

None yet - start your first session with Claude!

---

## Next Steps

1. Create project overview specification
2. Define initial use cases
3. Plan first iteration
EOF

cat > "$PROJECT_NAME/specs/00-project-overview.md" << EOF
# Project Overview

**Project**: [PROJECT_NAME]
**Created**: $(date +%Y-%m-%d)
**Status**: Initial Planning

---

## Vision

[What are you building and why?]

## Business Problem

[What problem does this solve?]

## Scope

### In Scope
- [Feature/capability 1]
- [Feature/capability 2]

### Out of Scope
- [What you're NOT building]

## Success Criteria

[How will you know if this succeeds?]

---

**Next**: Define use cases in \`specs/use-cases/\`
EOF

echo "✅ Placeholder files created"

# Final message
echo ""
echo "========================================="
echo "✅ Project initialized successfully!"
echo "========================================="
echo ""
echo "📁 Project location: ./$PROJECT_NAME"
echo ""
echo "🚀 Next steps:"
echo "   1. cd $PROJECT_NAME"
echo ""
echo "   2. Start Claude with a simple prompt:"
echo "      'Please analyze this project directory and tell me what this is'"
echo ""
echo "      Claude will automatically:"
echo "      - Read the framework files"
echo "      - Understand the disciplined approach"
echo "      - Ask about your project"
echo "      - Create specifications"
echo ""
echo "📖 Resources:"
echo "   - Quick Start: quick-start-guide.md"
echo "   - Full Framework: docs/claude-development-framework.md"
echo "   - Example Session: docs/example-first-session.md"
echo "   - Troubleshooting: docs/troubleshooting.md"
echo ""
echo "✨ The framework is self-teaching - just start Claude naturally! 🎯"