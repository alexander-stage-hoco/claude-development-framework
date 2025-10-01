---
tier: 3
purpose: Implementation phase instructions
reload_trigger: During implementation
estimated_read_time: 5 minutes
---

# Implementation Analysis Session

**Purpose**: Analyze this reference implementation for potential code reuse in our project
**Session Type**: Implementation Analysis
**Framework**: Claude Development Framework v2.0

---

## Your Role

You are analyzing a reference implementation (source code from another project) to determine:
1. **What this code does** and how it works
2. **Why it's relevant** to our project
3. **What we can reuse** and what we should avoid
4. **How to adapt it** for our use case

**IMPORTANT**: You are NOT implementing anything in this session. You are analyzing existing code.

---

## Analysis Protocol

### Step 1: Code Structure Discovery (10 minutes)

**Read the codebase**:
- [ ] Identify primary programming language and framework
- [ ] Map directory structure (key folders and their purpose)
- [ ] Find entry points (main.py, index.js, etc.)
- [ ] Identify main components/modules
- [ ] Note architectural patterns (MVC, Clean Architecture, etc.)

**Output**: Directory map with component descriptions

---

### Step 2: Architecture Analysis (15 minutes)

**Understand the design**:
- [ ] How are responsibilities separated?
- [ ] What design patterns are used?
- [ ] How is data flow organized?
- [ ] What are the key abstractions?
- [ ] How are dependencies managed?

**Questions to answer**:
- Is this a monolith or modular?
- How testable is the architecture?
- How does it handle errors?
- How is configuration managed?

**Output**: Architecture diagram (text-based) and pattern analysis

---

### Step 3: Code Quality Assessment (15 minutes)

**Evaluate code quality**:
- [ ] **Type Safety**: Type hints/annotations present? Enforced?
- [ ] **Testing**: Test coverage? Test quality? Test types (unit/integration)?
- [ ] **Documentation**: README quality? Code comments? API docs?
- [ ] **Error Handling**: Proper exception handling? Logging?
- [ ] **Code Style**: Consistent? Follows conventions? Linted?
- [ ] **Dependencies**: Up-to-date? Security vulnerabilities?
- [ ] **Performance**: Any obvious performance issues?

**Output**: Quality scorecard with ratings (Excellent/Good/Fair/Poor)

---

### Step 4: Identify Reusable Components (20 minutes)

**Find valuable code**:
- [ ] Which functions/classes solve problems we have?
- [ ] Which patterns could we adopt?
- [ ] Which algorithms are relevant?
- [ ] Which utilities could we reuse?

**For each reusable component, document**:
- **File path**: Where is it?
- **Purpose**: What does it do?
- **Dependencies**: What does it require?
- **Adaptation needed**: What changes are required?
- **Our use case**: Which UC/SVC would use this?

**Output**: List of reusable components with details

---

### Step 5: Identify What to Avoid (10 minutes)

**Find anti-patterns and risks**:
- [ ] What's poorly implemented?
- [ ] What's over-complicated?
- [ ] What has security issues?
- [ ] What doesn't fit our needs?

**Output**: List of things NOT to reuse and why

---

### Step 6: License and Attribution Check (5 minutes)

**Legal compliance**:
- [ ] What license does this project use?
- [ ] Is it compatible with our project license?
- [ ] Does it require attribution?
- [ ] Are there any restrictions?

**If unclear**: Check LICENSE file, package.json, README, or source file headers

**Output**: License summary and compliance requirements

---

### Step 7: Create Summary Document (15 minutes)

**Fill out `summary.md`** with:
1. **Project Overview** (2-3 sentences)
2. **Relevance to Our Project** (which UCs/specs benefit)
3. **Architecture Summary** (key patterns and design)
4. **Code Quality Assessment** (ratings and notes)
5. **Reusable Components** (detailed list with locations)
6. **What to Avoid** (anti-patterns identified)
7. **License Compliance** (requirements)
8. **Next Steps** (action items for reusing code)

Use the template from `.claude/templates/implementation-summary.md`

---

### Step 8: Create Detailed Analysis (Optional, 20 minutes)

If the implementation is complex or particularly valuable, create `analysis.md` with:
- Detailed architecture documentation
- Sequence diagrams for key flows
- In-depth pattern analysis
- Performance considerations
- Security considerations

---

## Expected Outputs

When you complete this analysis session, the folder should contain:

✅ **summary.md** - High-level findings (REQUIRED)
✅ **reusable-code.md** - Specific code we can adapt (REQUIRED)
✅ **analysis.md** - Detailed technical analysis (OPTIONAL)
✅ **CLAUDE.md** - This file (already present)

---

## Example Session Flow

```
User: Analyze this FastAPI authentication example

Claude:
✅ Step 1: Discovered structure
   - FastAPI app with JWT authentication
   - Key modules: auth/, models/, routes/
   - Entry: main.py

✅ Step 2: Architecture analysis
   - Clean Architecture pattern
   - Dependency injection for services
   - Repository pattern for data access

✅ Step 3: Quality assessment
   - Type Safety: Excellent (full type hints, mypy)
   - Testing: Good (80% coverage, pytest)
   - Documentation: Fair (README but sparse comments)

✅ Step 4: Reusable components found:
   - JWTHandler class (auth/jwt_handler.py)
   - PasswordHasher utility (auth/security.py)
   - Auth dependency injection pattern (auth/dependencies.py)

✅ Step 5: Avoid:
   - Hardcoded secrets in config.py (security issue)
   - Over-complicated permission system (too complex for our needs)

✅ Step 6: License check
   - MIT License (compatible)
   - Attribution required in comments

✅ Step 7: Created summary.md

Ready to reuse! See summary.md for details.
```

---

## Integration with Main Project

After analysis, when implementing features in the main project:

1. **Reference this analysis** in your implementation:
   ```python
   """
   Authentication handler.

   Specification: UC-002#authentication
   Reference Implementation: research/implementations/fastapi-auth-example/
   Adapted from: JWTHandler pattern (see summary.md)
   """
   ```

2. **Follow code reuse checklist** (`.claude/templates/code-reuse-checklist.md`)
3. **Add attribution** if license requires
4. **Write tests FIRST** for adapted code
5. **Don't copy blindly** - adapt to our architecture

---

## Self-Check Questions

Before finishing this session:
- ✅ Do I understand what this code does?
- ✅ Have I identified specific reusable components?
- ✅ Have I checked the license?
- ✅ Have I created summary.md?
- ✅ Can someone else understand my findings?

---

## Tips for Effective Analysis

1. **Start broad, go deep**: Understand overall structure before diving into details
2. **Focus on relevance**: Not everything needs deep analysis - focus on what we need
3. **Be critical**: Don't assume code is good just because it's published
4. **Think adaptation**: Always consider how to adapt, not just copy
5. **Document thoroughly**: Future you will thank present you

---

**Remember**: This is analysis, not implementation. Your output helps the main project team reuse code effectively.
---

**Template Version**: 1.0
**Framework**: Claude Development Framework v2.0
**Last Updated**: 2025-10-01
**Compatibility**: Framework v2.0+
