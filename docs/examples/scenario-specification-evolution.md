# Scenario: Specification Evolution Mid-Project

**Scenario**: User changes requirements mid-iteration, framework handles cleanly
**Complexity**: Medium
**Duration**: ~45 minutes
**Problem**: User wants to add task priorities to TODO API (new feature mid-iteration)
**Solution**: Update specs first, then implementation (Rule #1)

---

## Context

**Project**: TODO API
**Session**: 15 (mid-implementation of UC-002: Create Task)
**Current State**:
- ✅ UC-001 (Register) complete
- ⏳ UC-002 (Create Task) 60% complete (tests written, implementation in progress)
- ❌ User now wants task priorities (not in original spec)

---

## Session Transcript

### User Request (Mid-Implementation)

```
User: "Actually, I want to add task priorities (high, medium, low). Can you
add that to the create task feature?"
```

---

### Claude's Response (Enforces Spec-First)

```
Claude: ⚠️ **Specification Change Requested**

This adds scope to the current iteration (UC-002: Create Task).

**Current UC-002 Specification**:
```
Given a user wants to create a task
When they submit title and description
Then task is created with status "pending"
```

**No mention of priorities** ❌

**I cannot add this feature** without updating the specification first (Rule #1:
Specifications Are Law).

**Two Options**:

### Option 1: Finish Current Iteration, Then Add Priority

1. Complete UC-002 as specified (no priorities)
2. Create new UC-006: Add Task Priorities
3. Plan iteration for UC-006
4. Implement with tests

**Timeline**: Current iteration (30 min) + UC-006 specification (15 min) +
UC-006 implementation (2 hours) = ~3 hours total

### Option 2: Update UC-002 Specification Now

1. **STOP** current implementation
2. Update UC-002 spec to include priorities
3. Update existing tests
4. Resume implementation with new spec

**Timeline**: Spec update (15 min) + test updates (30 min) + implementation
(45 min) = ~1.5 hours

**Impact Analysis**:
- ⚠️ Throws away 30 min of current work
- ⚠️ Requires test rewrites
- ✅ Cleaner (one UC instead of two)

**Recommendation**: Option 1 (finish current, add as new UC)

Which approach would you prefer?
```

---

### User Response

```
User: "Option 1. Finish the current task, then we'll add priorities as a new feature."
```

---

### Claude Continues

```
Claude: ✅ Good decision! Continuing with UC-002 as originally specified...

[30 minutes later]

✅ **UC-002: Create Task** - Complete!

- All tests passing (8/8)
- Specification matches implementation
- Git committed

**Now ready for UC-006: Add Task Priorities**

Let me create the specification first...
```

---

### New Specification Created

```markdown
# Use Case UC-006: Add Task Priorities

**Status**: Draft
**Depends On**: UC-002 (Create Task)

## Description

Users can assign priority levels to tasks to indicate urgency.

## Acceptance Criteria

```gherkin
Scenario: Create task with priority
  Given a user is authenticated
  When they create a task with priority "high"
  Then task is created with priority "high"
  And task appears in high-priority list

Scenario: Default priority
  Given a user creates a task without specifying priority
  Then task is created with priority "medium" (default)
```

## Services Used

| Service | Methods Used | Purpose |
|---------|-------------|---------|
| TaskService | `create_task(priority)` | Add priority field |
| TaskService | `get_tasks_by_priority()` | Filter by priority |

## Non-Functional Requirements

- Priority values: "high", "medium", "low"
- Default: "medium"
- Backward compatible (existing tasks default to "medium")

## Data Model Changes

```python
class Task:
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority = TaskPriority.MEDIUM  # NEW
    created_at: datetime
```

---

**Impact Analysis**:
- Database migration required (add priority column)
- TaskService: Add priority parameter
- Tests: 5 new test cases
- Estimated effort: 2 hours
```

---

### Claude Creates Iteration Plan

```
Claude: Specification UC-006 created. Now creating iteration plan...

**Iteration 006: Task Priorities**

**Steps** (TDD Protocol):
1. Create database migration (add priority column with default "medium")
2. Update Task data model (add priority field)
3. Write tests (RED phase):
   - test_create_task_with_priority()
   - test_create_task_default_priority()
   - test_get_tasks_by_priority()
   - test_backward_compatibility()
4. Update TaskService.create_task() (GREEN phase)
5. Implement get_tasks_by_priority() (GREEN phase)
6. Refactor (REFACTOR phase)
7. Run all tests (including UC-002 tests - ensure no regression)
8. Git commit

**Estimated Time**: 2 hours

May I proceed with implementation?
```

---

### User Approves

```
User: "Yes, proceed."
```

---

### Implementation (TDD)

```
Claude: **Step 1: Database Migration**

```sql
-- Migration: Add priority column
ALTER TABLE tasks ADD COLUMN priority VARCHAR(10) DEFAULT 'medium';
ALTER TABLE tasks ADD CONSTRAINT priority_check
    CHECK (priority IN ('high', 'medium', 'low'));
```

✅ Migration created

**Step 2: Update Data Model**

```python
class TaskPriority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class Task:
    priority: TaskPriority = TaskPriority.MEDIUM  # NEW
```

✅ Model updated

**Step 3: Write Tests (RED)**

```python
def test_create_task_with_high_priority():
    task = task_service.create_task(
        title="Urgent bug",
        priority=TaskPriority.HIGH
    )
    assert task.priority == TaskPriority.HIGH

def test_backward_compatibility():
    # Old code that doesn't specify priority
    task = task_service.create_task(title="Task")
    assert task.priority == TaskPriority.MEDIUM  # Default
```

Run: ❌ Tests FAIL (not implemented yet)

**Step 4: Implement** (GREEN)

```python
def create_task(
    self,
    title: str,
    description: Optional[str] = None,
    priority: TaskPriority = TaskPriority.MEDIUM,  # NEW with default
) -> Result[Task, TaskError]:
    task = Task(
        title=title,
        description=description,
        priority=priority,  # NEW
        status=TaskStatus.PENDING,
        created_at=datetime.utcnow()
    )
    return self.repository.save(task)
```

Run: ✅ Tests PASS (13/13, including 5 new tests)

**Step 5: Verify No Regression**

Run all tests from UC-002:
✅ All 8 UC-002 tests still pass (backward compatible)

**Step 6: Git Commit**

```bash
git commit -m "feat: add task priorities (high/medium/low)

Specification: UC-006
Tests: 13 passing / 13 total
Backward compatible: Yes (defaults to 'medium')
Migration: add_priority_column.sql"
```

✅ UC-006 Complete!
```

---

## Outcome

✅ **Requirements Change Handled Cleanly**

**What Framework Prevented**:
- ❌ Adding undocumented features
- ❌ Scope creep during iteration
- ❌ Specification drift

**What Framework Ensured**:
- ✅ Specifications updated FIRST
- ✅ Impact analysis performed
- ✅ Backward compatibility tested
- ✅ No regression (old tests still pass)

**Timeline**:
- Original UC-002: 30 min
- UC-006 specification: 15 min
- UC-006 implementation: 90 min
- **Total**: 2 hours 15 min (vs. 3+ hours if done ad-hoc)

---

## Key Takeaways

**Framework Enforcement**: Refused to code without spec update (Rule #1)
**User Guidance**: Presented options with impact analysis
**Quality Maintained**: Backward compatibility tested, no regression
**Time Saved**: Structured approach faster than ad-hoc changes

---

## Files Created/Modified

**Created**:
- `specs/use-cases/UC-006-task-priorities.md`
- `planning/iteration-006-task-priorities.md`
- `migrations/add_priority_column.sql`

**Modified**:
- `services/task-service/models.py` (added TaskPriority enum)
- `services/task-service/implementation.py` (priority parameter)
- `services/task-service/tests/test_unit.py` (5 new tests)

---

**Session End**: Requirements evolution handled cleanly, quality maintained ✅
