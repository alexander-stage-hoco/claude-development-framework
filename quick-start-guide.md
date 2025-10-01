# Quick Start Guide - Your First 5 Minutes

**Claude Development Framework v2.0**

---

## What This Is

This is a **template** for setting up new software projects with a disciplined, specification-driven development approach using Claude AI.

The framework ensures:
✅ Specifications come before code
✅ Tests are written before implementation
✅ Work happens in small, manageable iterations
✅ Quality is maintained throughout development

---

## Step 1: Initialize Your Project (30 seconds)

From this template directory, run:

```bash
./init-project.sh my-awesome-project
```

This creates a complete project structure with:
- All framework files configured
- Directory structure created
- Initial placeholder files

**Output**:
```
✅ Project initialized successfully!
📁 Project location: ./my-awesome-project
```

---

## Step 2: Enter Your Project (5 seconds)

```bash
cd my-awesome-project
```

Your project now has:
```
my-awesome-project/
├── .claude/              # Claude configuration
│   ├── CLAUDE.md        # Main instructions
│   ├── start-here.md    # Framework orientation
│   └── ...
├── specs/               # Specifications
├── planning/            # Planning docs
├── implementation/      # Code goes here
└── README.md
```

---

## Step 3: Start Claude (10 seconds)

Open Claude (CLI, web, or API) and start with a **simple prompt**:

```
Please analyze this project directory and tell me what this is and how to use it.
```

**OR** (if you know what you're building):

```
I want to build [DESCRIPTION]. Please read .claude/CLAUDE.md and help me set up this project.
```

---

## Step 4: Answer Claude's Questions (3-5 minutes)

Claude will have read the framework files and will ask about your project:

**Expected Questions**:
1. What are you building?
2. What problem does it solve?
3. Who are the users?
4. What are the main capabilities/features?
5. Any technical constraints?

**Be specific!** Good answers lead to better specifications.

**Example**:
```
User: I want to build a task management API

Claude asks: What problem does it solve?

User: Teams need a simple way to track tasks without complex project
management tools. Just create, assign, and complete tasks.

Claude asks: What are the main capabilities?

User:
1. Create and update tasks
2. Assign tasks to users
3. Mark tasks complete
4. List tasks with filters
5. Basic user authentication
```

---

## Step 5: Let Claude Create Specifications (Automatic)

After hearing about your project, Claude will:

✅ Update `specs/00-project-overview.md` with your vision
✅ Identify 3-5 initial use cases
✅ Create skeleton specification files
✅ Document any technical decisions (ADRs)

**Important**: Claude will **NOT** write implementation code yet (this is correct!)

---

## What Just Happened?

You now have:

✅ **Complete project structure** with all necessary folders
✅ **Framework files** that guide Claude's behavior
✅ **Initial specifications** documenting your vision
✅ **Claude trained** on your disciplined development approach
✅ **Clean foundation** for spec-first, test-driven development

---

## Your Next Session

When you're ready to continue:

```bash
cd my-awesome-project  # If not already there
```

Start Claude with:

```
Continue from session 1. Read planning/session-state.md first.
```

Claude will:
1. Load the session state
2. Resume where you left off
3. Continue following the framework

---

## Common First-Timer Questions

### Q: Do I need to memorize specific commands?

**A**: No! Just ask Claude naturally. The framework files teach Claude what to do. You can say things like:
- "What should we work on next?"
- "Show me the current status"
- "Let's start implementing the simplest feature"

### Q: Can I skip straight to coding?

**A**: Claude will refuse (correctly!). The framework requires specifications before implementation. This saves time by building the right thing correctly.

### Q: What if I change my mind about features?

**A**: Update the specifications first, then implementation. Always spec-driven. Claude will help you update specs properly.

### Q: Do I really need to write tests first?

**A**: Yes - it's Rule #2. Tests define correctness. The framework enforces test-first development. It's actually faster long-term because you catch bugs immediately.

### Q: What if Claude doesn't follow the rules?

**A**: Say:
- "Check development rules"
- "Tests first, then implementation"
- "What does the specification say?"

Claude will self-correct.

### Q: Where does my project get created?

**A**: Projects are created as **subdirectories relative to the template location**.

**Example**:
```bash
# If you're in /Users/yourname/templates/claude-framework/
./init-project.sh my-project

# Creates: /Users/yourname/templates/claude-framework/my-project/
```

**Recommendation**: Create projects **outside** the template directory:

```bash
# Option 1: Specify relative path
./init-project.sh ../my-projects/my-project
# Creates: /Users/yourname/templates/my-projects/my-project/

# Option 2: Specify absolute path
./init-project.sh /Users/yourname/projects/my-project
# Creates: /Users/yourname/projects/my-project/

# Option 3: Navigate first, then specify relative path
cd ~/projects
/path/to/claude-framework/init-project.sh my-project
# Creates: ~/projects/my-project/
```

**Why create outside the template?**
- Keeps template clean (can be updated/cloned fresh)
- Separates "framework template" from "your projects"
- Easier to manage multiple projects
- Prevents accidental commits to template repo

**Path Types Supported**:
- **Relative path**: `./my-project` (from current directory)
- **Relative with parent**: `../projects/my-project` (up one level, then down)
- **Absolute path**: `/full/path/to/my-project`

---

## Typical First Few Sessions

### Session 1 (Specifications)
- Define project vision
- Identify use cases
- Create initial specs
- **No code written** ✓

### Session 2 (Refinement)
- Detail one use case
- Define acceptance criteria
- Create BDD scenarios
- Plan first iteration

### Session 3 (First Implementation)
- Write tests (they fail)
- Implement to pass tests
- All tests green
- First feature complete! ✓

### Session 4+ (Incremental Development)
- Pick next iteration
- Test-first cycle
- Build incrementally
- Maintain quality

---

## What Makes This Different

**Traditional Approach**:
```
User: "Build a login system"
AI: [Generates 500 lines of code]
User: "This isn't quite what I wanted..."
```

**This Framework**:
```
User: "Build a login system"
Claude: "Let me create a specification first..."
        [Creates UC-002: User Authentication spec]
        "Does this match your needs?"
User: "Yes, but also add 'remember me'"
Claude: "Updated spec. Now let's write tests first..."
        [Writes tests, they fail]
        "Tests are failing as expected. Implement now?"
User: "Yes"
Claude: [Implements, tests pass]
        "All tests green. Login system complete."
```

**Result**: You get exactly what you wanted, fully tested, properly documented.

---

## Framework Features You'll Love

### 1. Session Continuity
Claude picks up exactly where you left off, even days later.

### 2. Always-Tested Code
Every feature has tests. No "we'll test it later" technical debt.

### 3. Clear Documentation
Specifications show WHY code exists, not just WHAT it does.

### 4. Incremental Progress
Small iterations mean visible progress every session.

### 5. Quality Enforcement
Claude refuses shortcuts that compromise quality.

---

## Troubleshooting

### Claude seems confused
**Say**: "Reload framework files"
**Claude will**: Re-read .claude/CLAUDE.md and development-rules.md

### Not sure what to work on
**Say**: "Show me planning/current-iteration.md"
**Claude will**: Show current iteration status and next steps

### Want to see all use cases
**Say**: "List all use cases in specs/use-cases/"
**Claude will**: Show all defined use cases

### Framework feels too rigid
**Say**: "Explain why we need specs before code"
**Claude will**: Explain the reasoning and benefits

**Note**: The "rigidity" is what ensures quality. Give it 2-3 sessions - you'll see the value.

---

## Getting Help

### Documentation Files

- **Full Framework**: `docs/claude-development-framework.md` (comprehensive)
- **Example Project**: `docs/walkthrough-todo-api.md` (5-session example)
- **Templates**: `.claude/templates/` (23 copy-paste ready templates)
- **Troubleshooting**: `docs/troubleshooting.md` (common issues)
- **Tools**: `docs/advanced/tool-integration.md` (Git hooks, CI/CD)

### Ask Claude

Claude has read all the framework documentation. Just ask:
- "How does this framework work?"
- "Show me an example of test-first development"
- "What are the 10 development rules?"

---

## Success Stories

This framework was used to build:
- **Knowledge Graph Builder**: 6 use cases, 93 test files, 1,176 tests, 100% coverage
- Successfully maintained quality across long development timeline
- Complete spec-to-implementation traceability

Your project can achieve similar results!

---

## Quick Commands Reference

```bash
# Initialize new project
./init-project.sh project-name

# Start first session
"Please analyze this project directory"

# Continue later session
"Continue from session N. Read planning/session-state.md"

# Check status
"What's the current status?"

# See iterations
"Show me planning/current-iteration.md"

# Reload framework
"Reload framework files"
```

---

## Next Steps

1. ✅ You've initialized your project
2. ✅ You've had your first session with Claude
3. ✅ Specifications are created

**Now**:
- Read `docs/claude-development-framework.md` (20 min) - understand the full approach
- Read `docs/walkthrough-todo-api.md` (15 min) - see complete example
- Start your second session - refine specs or begin implementation

---

## Philosophy

> **"Slow is smooth, smooth is fast."**

This framework might feel slower at first (specs before code, tests before implementation), but it's actually faster because:
- You build the right thing (specs ensure alignment)
- You build it correctly (tests catch issues immediately)
- You can maintain it (documentation explains decisions)
- You can extend it (clean architecture, good tests)

**Give it 3 sessions**. You'll see the value.

---

## Welcome!

You're now set up with a professional, disciplined development framework. Claude will be your partner in maintaining quality throughout your project.

**Remember**:
- Claude enforces quality - let it
- Specs come before code - always
- Tests define correctness - never weaken them
- Small iterations - stay disciplined

**Ready to build with excellence!** 🚀

---

**Framework Version**: 2.0
**Questions?** Ask Claude - it knows the framework thoroughly.