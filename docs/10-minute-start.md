# 10-Minute Start - Claude Development Framework

**Get from zero to your first Claude session in 10 minutes.**

No lengthy reading required. Just follow these 5 steps.

---

## You Need

- Terminal access
- Claude (CLI, web, or API)
- 10 minutes of your time

---

## 5 Steps to Start

### Step 1: Initialize Project (30 seconds)

From the framework template directory:

```bash
./init-project.sh my-project
```

**Output**: Project structure created with all framework files.

---

### Step 2: Enter Your Project (5 seconds)

```bash
cd my-project
```

Your project now has 33+ files ready to guide Claude.

---

### Step 3: Start Claude (10 seconds)

Open Claude and start with this simple prompt:

```
Please analyze this project directory and tell me what this is.
```

**OR** if you know what you're building:

```
I want to build [YOUR PROJECT IDEA]. Please help me set it up.
```

---

### Step 4: Answer Claude's Questions (5 minutes)

Claude will ask about your project:

**Expected Questions**:
- What are you building?
- What problem does it solve?
- Who are the users?
- What are the main features?

**Be specific!** Good answers = better specifications.

**Example**:
```
User: I want to build a task management API

Claude: What problem does it solve?

User: Teams need simple task tracking without complex PM tools.
Just create, assign, and complete tasks.

Claude: What are the main features?

User:
1. Create and update tasks
2. Assign tasks to team members
3. Mark tasks complete
4. List tasks with filters
5. Basic authentication
```

---

### Step 5: Review Specifications (3 minutes)

Claude creates your initial specifications:
- ✅ `specs/00-project-overview.md` - Your project vision
- ✅ Initial use case files
- ✅ Project structure documented

**Claude will NOT write code yet** - this is correct! Specifications come first.

---

## What Just Happened?

In 10 minutes you have:

✅ **Complete project structure** - All directories and framework files
✅ **Framework configured** - Claude knows the disciplined approach
✅ **Initial specifications** - Your vision documented clearly
✅ **Ready for development** - Solid foundation established

---

## What's Different Here?

**Traditional approach**:
```
You: "Build feature X"
AI: [Dumps 500 lines of code]
You: "This isn't what I wanted..."
```

**This framework**:
```
You: "Build feature X"
Claude: "Let me create specification first..."
        [Creates spec]
        "Does this match your needs?"
You: "Yes, plus add Y"
Claude: "Updated spec. Now tests first..."
        [Tests written, failing]
        "Tests ready. Implement?"
You: "Yes"
Claude: [Implementation passes tests]
        "Feature complete ✓"
```

**Result**: You get exactly what you wanted, fully tested, properly documented.

---

## Next Steps

### Option 1: Continue Building (Recommended)

Continue your Claude session:
```
Great! Now let's refine the first use case.
```

### Option 2: Learn the Full Framework

Read the detailed guides:
- **`quick-start-guide.md`** (15 min) - Complete walkthrough
- **`docs/claude-development-framework.md`** (30 min) - Full framework
- **`docs/walkthrough-todo-api.md`** (20 min) - Real example

### Option 3: Resume Later

When you return:
```bash
cd my-project
```

Start Claude with:
```
Continue from session 1. Read planning/session-state.md first.
```

---

## Quick Troubleshooting

### "Claude seems confused"
**Fix**: Say `"Reload framework files"`

### "Not sure what to work on"
**Fix**: Say `"Show me planning/current-iteration.md"`

### "Want to skip specs and code"
**Fix**: Claude will refuse (correctly!). Specs prevent building the wrong thing.

### "Framework feels rigid"
**Fix**: Give it 2-3 sessions - you'll see the value. The "rigidity" ensures quality.

---

## Common First Questions

**Q: Do I need to memorize commands?**
A: No! Ask Claude naturally: "What should we work on next?"

**Q: Can I skip straight to coding?**
A: Claude will refuse. Specs first = build the right thing correctly.

**Q: What if requirements change?**
A: Update specs first, then code. Claude helps you do this properly.

**Q: Do I really need tests first?**
A: Yes - Rule #2. Tests define correctness. Actually faster long-term.

---

## You're Ready!

That's it. In 10 minutes you went from nothing to a properly initialized project with Claude as your disciplined development partner.

**Philosophy**: "Slow is smooth, smooth is fast."

The framework might feel slower initially (specs, tests, discipline), but it's actually **faster** because:
- You build the right thing (specs ensure alignment)
- You build it correctly (tests catch issues immediately)
- You can maintain it (documentation explains decisions)
- You can extend it (clean architecture, good tests)

---

## Want More Details?

**Quick Reference** (10 min):
- `.claude/quick-ref/commands.md` - Common commands
- `.claude/READING-ORDER.md` - What to read when

**Full Documentation** (30-60 min):
- `quick-start-guide.md` - Complete walkthrough
- `docs/claude-development-framework.md` - Deep dive
- `docs/session-types.md` - 10 session patterns
- `docs/examples/README.md` - 10 real examples

**Ask Claude**:
Claude has read all framework documentation. Just ask:
- "How does this framework work?"
- "Show me the 12 development rules"
- "What's the test-first process?"

---

**Ready to build with excellence!** 🚀

---

**Guide Version**: 1.0
**Framework**: Claude Development Framework v2.0
**Reading Time**: 5 minutes
**Execution Time**: 10 minutes
