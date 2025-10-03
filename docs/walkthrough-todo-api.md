# Complete Walkthrough: Building a TODO API

**Purpose**: End-to-end example demonstrating the Claude Development Framework in practice

**Project**: Simple TODO REST API
**Timeline**: 5 sessions over 2 weeks
**Outcome**: Fully tested, spec-driven implementation

**Last Updated**: 2025-09-30

---

## Project Overview

**Goal**: Build a REST API for TODO list management

**Scope**:
- Create TODO items
- List all TODOs
- Update TODO items
- Delete TODO items

**Why This Example**:
- Simple enough to understand quickly
- Complex enough to show framework principles
- Demonstrates complete workflow from spec to deployment

---

## Session 1: Project Initialization (45 minutes)

### User Input
```
"I want to build a REST API for managing TODO items.
 Users should be able to create, list, update, and delete TODOs.
 Each TODO has a title, optional description, and completion status.

 Please read .claude/CLAUDE.md first."
```

### Claude Response

```
I've read .claude/development-rules.md and understand the disciplined approach.
Let me start with research and specifications—NO CODE YET.

## Phase 1: Project Structure

I'll create:
1. specs/00-project-overview.md
2. specs/use-cases/UC-001-create-todo.md
3. specs/use-cases/UC-002-list-todos.md
4. specs/use-cases/UC-003-update-todo.md
5. specs/use-cases/UC-004-delete-todo.md
6. specs/architecture/technology-stack.md

## Phase 2: Technology Stack Recommendation

Based on requirements:
- **FastAPI**: Modern, async, auto-generates OpenAPI docs
- **SQLite**: Embedded database, perfect for MVP
- **Pydantic**: Data validation aligns with spec-first approach
- **pytest**: Standard Python testing framework

I'll create ADR-001 to document this decision.

May I proceed with creating these specification files?
```

### Files Created

#### `specs/00-project-overview.md`
```markdown
# TODO API - Project Overview

## Vision
A simple, well-tested REST API for TODO list management that demonstrates
disciplined, incremental development practices.

## Scope

**In Scope**:
- CRUD operations for TODO items
- REST API with JSON
- Local SQLite database
- Comprehensive test coverage

**Out of Scope** (Future):
- User authentication
- Multiple TODO lists
- Real-time updates
- Mobile applications

## Success Criteria
- All 4 use cases implemented and tested
- 100% test coverage on core logic
- API documentation auto-generated (OpenAPI/Swagger)
- Deployment-ready artifact

## Timeline
- **Week 1**: UC-001, UC-002 (Create, List)
- **Week 2**: UC-003, UC-004 (Update, Delete)
- **Total**: ~10 hours over 2 weeks
```

#### `specs/use-cases/UC-001-create-todo.md`
```markdown
# UC-001: Create TODO Item

**Priority**: Critical
**Complexity**: Low (2-3 iterations)
**Status**: Not Started

## Overview
Allow users to create a new TODO item via REST API.

## Main Flow
1. User sends POST request to /todos with JSON body
2. System validates input (title required, max 200 chars)
3. System generates unique ID
4. System stores TODO in database
5. System returns 201 Created with TODO object

## Alternative Flows
**AF-1: Missing Title**
- System returns 400 Bad Request
- Error message: "title is required"

**AF-2: Title Too Long**
- System returns 400 Bad Request
- Error message: "title maximum 200 characters"

## Acceptance Criteria

### AC-1: Successful Creation
```gherkin
Given user provides valid TODO data
When user POST to /todos with title "Buy groceries"
Then system returns 201 status
And system returns created TODO with ID
And TODO is stored in database
And completed defaults to false
```

### AC-2: Validation - Missing Title
```gherkin
Given user provides TODO without title
When user POST to /todos
Then system returns 400 Bad Request
And error message is "title is required"
```

### AC-3: Validation - Title Too Long
```gherkin
Given user provides title with 201 characters
When user POST to /todos
Then system returns 400 Bad Request
And error message is "title maximum 200 characters"
```

## Data Model
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-09-30T10:30:00Z"
}
```

## API Contract

**Endpoint**: `POST /todos`

**Request Body**:
```json
{
  "title": "string (required, max 200 chars)",
  "description": "string (optional)"
}
```

**Success Response** (201 Created):
```json
{
  "id": "integer",
  "title": "string",
  "description": "string or null",
  "completed": false,
  "created_at": "ISO 8601 timestamp"
}
```

**Error Response** (400 Bad Request):
```json
{
  "detail": "error message"
}
```

## Implementation Plan
- **Iteration 001**: Core TODO creation (happy path)
- **Iteration 002**: Input validation
- **Iteration 003**: Error response formatting
```

#### `.claude/technical-decisions.md`
```markdown
# Technical Decision Records

## ADR-001: Technology Stack for TODO API

**Date**: 2025-09-30
**Status**: Accepted

**Context**:
Building a simple TODO API to learn/demonstrate the Claude Development Framework.
Need modern, well-documented technologies suitable for teaching disciplined development.

**Decision**:
- **FastAPI** for web framework
- **SQLite** for database
- **Pydantic** for data validation
- **pytest** for testing

**Consequences**:

Positive:
- FastAPI provides automatic OpenAPI documentation
- FastAPI has excellent async support (future-proof)
- SQLite requires zero external dependencies
- Pydantic validation integrates perfectly with spec-first approach
- pytest is industry standard with rich plugin ecosystem

Negative:
- SQLite not suitable for high-concurrency production
- May need migration to PostgreSQL for production deployment
- FastAPI relatively new (less mature than Flask/Django)

**Alternatives Considered**:
1. **Flask + SQLAlchemy**: More traditional, but less modern features
2. **Django + DRF**: Too heavy for simple API, overkill
3. **PostgreSQL**: Overkill for learning project, adds setup complexity

**References**:
- https://fastapi.tiangolo.com/
- https://docs.pydantic.dev/
- research/learnings/rest-api-frameworks-comparison.md
```

### Session 1 Outcome
✅ Project structure created
✅ Specifications written (NO CODE YET)
✅ Technical decisions documented
✅ Ready for implementation planning

---

## Session 2: Research & Planning (30 minutes)

### User Input
```
"Specs look good. Let's implement UC-001."
```

### Claude Response

```
Before implementing, I need to research and document best practices.

I'll create:
1. research/learnings/rest-api-design-summary.md
2. research/learnings/fastapi-testing-patterns.md
3. research/learnings/todo-data-modeling.md

Then break UC-001 into 3 iterations:

**Iteration 001** (2h): Core TODO creation
- Pydantic model for TODO
- SQLite schema and connection
- POST /todos endpoint (happy path only)
- Tests: 4 unit, 2 integration

**Iteration 002** (1.5h): Input validation
- Title required validation
- Title length validation
- Tests: 3 validation tests

**Iteration 003** (1h): Error responses
- Proper 400 error formatting
- Error message clarity
- Tests: 2 error handling tests

Let me create planning/iterations/iteration-001-core-todo-creation.md
```

#### `planning/iterations/iteration-001-core-todo-creation.md`
```markdown
# Iteration 001: Core TODO Creation

**Use Case**: UC-001 (Create TODO)
**Estimated**: 2 hours
**Status**: Ready to start

## Goal
Implement POST /todos endpoint that accepts title and description,
creates TODO in database, returns 201 with created TODO object.
100% test coverage on happy path.

## Scope

**In This Iteration**:
- [ ] Pydantic model for TODO
- [ ] SQLite schema and connection
- [ ] POST /todos endpoint (happy path only)
- [ ] Tests for successful creation

**Explicitly NOT In This Iteration**:
- Input validation (iteration 002)
- Error handling beyond basic (iteration 003)
- GET/UPDATE/DELETE endpoints (later UCs)

## Test-First Approach

### Tests to Write FIRST

**1. tests/unit/models/test_todo_model.py**
```python
def test_todo_model_creation():
    """Spec: UC-001#data-model"""
    todo = Todo(title="Buy milk", description="Organic")
    assert todo.title == "Buy milk"
    assert todo.completed is False

def test_todo_model_defaults():
    """Spec: UC-001#data-model"""
    todo = Todo(title="Test")
    assert todo.description is None
    assert todo.completed is False
```

**2. tests/integration/api/test_create_todo.py**
```python
def test_create_todo_returns_201():
    """Spec: UC-001#ac-1-successful-creation"""
    response = client.post("/todos", json={"title": "Buy milk"})
    assert response.status_code == 201

def test_create_todo_returns_todo_with_id():
    """Spec: UC-001#ac-1-successful-creation"""
    response = client.post("/todos", json={"title": "Buy milk"})
    data = response.json()
    assert "id" in data
    assert data["title"] == "Buy milk"
```

**Expected Results**: All tests fail (modules don't exist yet)

## Implementation Plan

### Files to CREATE:
1. `src/models/todo.py` - Pydantic model
2. `src/db/database.py` - SQLite connection
3. `src/db/schema.sql` - Database schema
4. `src/api/routes/todos.py` - FastAPI router
5. `src/main.py` - FastAPI app

### Implementation Steps:
1. Create TODO Pydantic model (15 min)
2. Create database schema and connection (20 min)
3. Create POST /todos endpoint (30 min)
4. Run tests, debug until green (30 min)
5. Code review and cleanup (15 min)

## Definition of Done
- [ ] All 6 tests passing
- [ ] Test coverage 100% on new code
- [ ] Can POST /todos and receive 201
- [ ] TODO stored in SQLite database
- [ ] Type hints on all functions
- [ ] Docstrings reference UC-001 spec
- [ ] No pylint warnings
- [ ] Iteration status updated in planning/current-iteration.md
```

### Session 2 Outcome
✅ Research documented
✅ Iteration 001 planned
✅ Test list created
✅ Ready for test-first implementation

---

## Session 3: Test-First Implementation (2 hours)

### User Input
```
"Plan looks good. Let's implement iteration 001."
```

### Claude Response
```
Starting iteration 001. Writing tests FIRST.
```

### Step 1: Write Unit Tests

`tests/unit/models/test_todo_model.py`:
```python
"""
Unit tests for TODO data model.
Specification: specs/use-cases/UC-001-create-todo.md#data-model
"""
import pytest
from datetime import datetime
from src.models.todo import Todo

def test_todo_model_creation():
    """Test TODO can be created with required fields.

    Spec: UC-001#data-model
    """
    todo = Todo(
        title="Buy milk",
        description="Organic milk from store"
    )
    assert todo.title == "Buy milk"
    assert todo.description == "Organic milk from store"
    assert todo.completed is False
    assert isinstance(todo.created_at, datetime)

def test_todo_model_defaults():
    """Test TODO has correct default values.

    Spec: UC-001#data-model
    """
    todo = Todo(title="Test task")
    assert todo.id is None  # Not assigned yet
    assert todo.description is None
    assert todo.completed is False
    assert todo.created_at is not None
```

**Run tests**:
```bash
$ pytest tests/unit/models/test_todo_model.py
ERROR: ModuleNotFoundError: No module named 'src.models.todo'
FAILED (2 failed)
```

✅ **Expected failure! Tests work, module doesn't exist.**

**Claude requests approval**:
```
Tests are written and failing correctly (2/2 fail with "module not found").
This is expected TDD behavior.

May I proceed with implementing src/models/todo.py to make tests pass?
```

### Step 2: Implement TODO Model

`src/models/todo.py`:
```python
"""
TODO data model using Pydantic for validation.

Specification: specs/use-cases/UC-001-create-todo.md#data-model
ADR Reference: ADR-001 (Technology Stack - Pydantic)
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Todo(BaseModel):
    """Represents a TODO item.

    Attributes:
        id: Unique identifier (assigned by database)
        title: TODO title (required, validated in iteration 002)
        description: Optional description
        completed: Completion status (defaults to False)
        created_at: Timestamp of creation

    Specification: UC-001#data-model
    """
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: Optional[datetime] = None

    def __init__(self, **data):
        """Initialize TODO with auto-assigned created_at."""
        if 'created_at' not in data:
            data['created_at'] = datetime.utcnow()
        super().__init__(**data)

    class Config:
        """Pydantic configuration."""
        orm_mode = True  # Allow creation from DB rows
```

**Run tests**:
```bash
$ pytest tests/unit/models/test_todo_model.py
PASSED (2/2) ✅ All green!
```

### Step 3: Write Integration Tests

`tests/integration/api/test_create_todo.py`:
```python
"""
Integration tests for TODO creation API.
Specification: specs/use-cases/UC-001-create-todo.md
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_todo_returns_201():
    """Test POST /todos returns 201 Created status.

    Spec: UC-001#ac-1-successful-creation
    """
    response = client.post("/todos", json={
        "title": "Buy milk",
        "description": "Organic milk"
    })
    assert response.status_code == 201

def test_create_todo_returns_todo_with_id():
    """Test POST /todos returns created TODO with assigned ID.

    Spec: UC-001#ac-1-successful-creation
    """
    response = client.post("/todos", json={"title": "Buy milk"})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["id"] is not None
    assert data["title"] == "Buy milk"
    assert data["completed"] is False
```

**Run tests**:
```bash
$ pytest tests/integration/api/test_create_todo.py
ERROR: ModuleNotFoundError: No module named 'src.main'
FAILED (2 failed)
```

✅ **Expected! Now implement the API.**

### Step 4: Implement API (abbreviated)

Files created:
- `src/db/database.py` - SQLite connection
- `src/db/schema.sql` - Database schema
- `src/api/routes/todos.py` - POST /todos endpoint
- `src/main.py` - FastAPI application

**Final test run**:
```bash
$ pytest tests/
PASSED (4/4 tests) ✅ ALL GREEN!

$ pytest --cov=src tests/
Coverage: 100% ✅
```

### Step 5: Update Status

`planning/current-iteration.md`:
```markdown
# Current Iteration Status

**Active**: Iteration 002 (Input Validation)
**Last Completed**: Iteration 001 (Core TODO Creation) ✅

## Iteration 001 - Complete
**Completed**: 2025-09-30 16:45
**Time**: 2.0 hours (exactly as estimated!)
**Tests**: 4 unit, 2 integration (6 total) - all passing
**Coverage**: 100%

**Deliverables**:
- POST /todos endpoint (happy path)
- TODO Pydantic model
- SQLite database integration
- Full test coverage

**Next**: Iteration 002 (Input validation) - 1.5 hours estimated
```

### Session 3 Outcome
✅ Iteration 001 complete
✅ All tests passing (100% coverage)
✅ POST /todos working
✅ Ready for iteration 002

---

## Sessions 4-5: Continue Pattern

### The Pattern
1. **Plan** next iteration
2. **Write tests** first (they fail)
3. **Implement** to make tests pass
4. **All tests green**
5. **Update status**
6. **Move to next** iteration

### Iteration 002: Input Validation (Session 4)
- Add title required validation
- Add title length validation (max 200)
- Add proper error responses
- **Result**: 3 more tests, all passing

### Iteration 003: Error Formatting (Session 4 continued)
- Standardize error response format
- Add error details
- **Result**: 2 more tests, all passing

### UC-002: List TODOs (Session 5)
- GET /todos endpoint
- Returns list of all TODOs
- Empty list if no TODOs
- **Result**: 4 tests, all passing

### UC-003: Update TODO (Session 5)
- PUT /todos/{id} endpoint
- Update title, description, completed
- Return 404 if not found
- **Result**: 5 tests, all passing

### UC-004: Delete TODO (Session 5)
- DELETE /todos/{id} endpoint
- Return 204 No Content
- Return 404 if not found
- **Result**: 3 tests, all passing

---

## Final Result (After 5 Sessions)

### Statistics
- **Total Time**: ~10 hours over 2 weeks
- **Use Cases**: 4 (all complete)
- **Iterations**: 8 (all complete)
- **Tests**: 23 total, all passing
- **Coverage**: 100% on core logic
- **Specifications**: 100% implemented

### Project Artifacts

```
todo-api/
├── .claude/
│   ├── CLAUDE.md
│   ├── development-rules.md
│   └── technical-decisions.md (1 ADR)
├── specs/
│   ├── 00-project-overview.md
│   └── use-cases/
│       ├── UC-001-create-todo.md ✅
│       ├── UC-002-list-todos.md ✅
│       ├── UC-003-update-todo.md ✅
│       └── UC-004-delete-todo.md ✅
├── research/
│   └── learnings/
│       ├── rest-api-design-summary.md
│       ├── fastapi-testing-patterns.md
│       └── todo-data-modeling.md
├── planning/
│   ├── current-iteration.md
│   └── iterations/
│       ├── iteration-001-core-todo-creation.md ✅
│       ├── iteration-002-input-validation.md ✅
│       └── [6 more iterations] ✅
├── src/
│   ├── models/todo.py
│   ├── db/database.py
│   ├── api/routes/todos.py
│   └── main.py
└── tests/
    ├── unit/ (10 tests)
    ├── integration/ (13 tests)
    └── bdd/ (4 feature files with scenarios)
```

### What We Demonstrated

1. **Specification-First**: Wrote specs before any code
2. **Test-Driven**: Every test written before implementation
3. **Incremental**: 8 iterations of 1-2 hours each
4. **Research-Informed**: Documented best practices first
5. **Traceable**: Every line of code traces to a spec
6. **Quality**: 100% test coverage from start
7. **Documented Decisions**: ADR for technology choices
8. **No Shortcuts**: Never weakened tests, never skipped specs

---

## Key Learnings

### What Worked Well
✅ Test-first approach caught issues early
✅ 2-hour iterations kept momentum
✅ Specifications eliminated ambiguity
✅ Pydantic + FastAPI made validation easy
✅ Documentation stayed synchronized

### What Was Challenging
⚠️ Initial setup felt slow (worth it later)
⚠️ Discipline required to not "just code"
⚠️ Writing good acceptance criteria takes practice

### Velocity Over Time
- **Week 1**: 3 iterations (5 hours) - Learning curve
- **Week 2**: 5 iterations (5 hours) - Faster with practice

**Insight**: Disciplined development is FASTER long-term, not slower.

---

## How to Use This Walkthrough

### For Learning
1. Read through once to understand the flow
2. Try building your own TODO API following the pattern
3. Compare your approach to this example

### For Your Projects
1. Use this as a template for project structure
2. Copy the spec templates (UC-001 format)
3. Follow the same iteration pattern
4. Adapt to your domain

### For Teaching Others
1. Show this as proof the framework works
2. Use it to explain test-first development
3. Demonstrate spec-code traceability

---

## Next Steps

Want to extend this example?

**Possible UC-005**: User Authentication
- Add user model
- Require login for TODO operations
- Associate TODOs with users

**Possible UC-006**: TODO Lists
- Group TODOs into lists
- CRUD operations on lists

**Possible UC-007**: Due Dates
- Add due_date field
- List overdue TODOs
- Sort by due date

**Each would follow the same pattern**: Spec → Research → Plan → Test → Implement → Verify

---

**Document Version**: 1.0
**Part of**: Claude Development Framework
**See also**: `.claude/templates/use-case-template.md` for spec templates
