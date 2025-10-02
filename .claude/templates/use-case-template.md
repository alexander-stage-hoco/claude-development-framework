---
tier: 4
purpose: Use case specification template
reload_trigger: When creating new UC
estimated_read_time: 5 minutes
---

# UC-XXX: [Use Case Name]

**Status**: [Draft | In Progress | Complete]
**Priority**: [High | Medium | Low]
**Estimated Effort**: [Small (< 3h) | Medium (3-8h) | Large (8-20h)]
**Dependencies**: [UC-XXX, UC-XXX] or None

---

## Objective

[Clear statement of what user need this satisfies. Why does this use case exist?]

**User Value**: [What value does the user get from this feature?]

---

## Actors

- **Primary Actor**: [Who initiates this use case? e.g., "Authenticated User", "Admin", "Guest"]
- **Secondary Actors**: [Who else is involved? e.g., "Email Service", "Payment Gateway", "Database"]

---

## Preconditions

[What must be true before this use case can begin?]

- [Precondition 1 - e.g., "User is authenticated"]
- [Precondition 2 - e.g., "User has permission to perform this action"]
- [Precondition 3 - e.g., "System has required data available"]

---

## Postconditions

[What will be true after successful completion?]

- [Postcondition 1 - e.g., "Task is created and stored in database"]
- [Postcondition 2 - e.g., "User receives confirmation"]
- [Postcondition 3 - e.g., "Audit log entry created"]

---

## Main Flow (Happy Path)

1. [Actor] [performs action]
2. System [responds/validates/processes]
3. System [stores/updates/returns data]
4. [Actor] receives [confirmation/result]
5. Use case ends successfully

**Example**:
1. User provides task title and description
2. System validates input (title non-empty, description < 5000 chars)
3. System creates task with status "open" and assigns ID
4. System stores task in database
5. System returns task ID and success confirmation

---

## Alternative Flows

### Alternative Flow 1: [Scenario Name]

**Trigger**: [What causes this alternative path?]

**Steps**:
1. [Deviation from main flow starts at step X]
2. [Alternative action taken]
3. [System response]
4. [Return to main flow at step Y, or end]

**Example**:
### Alternative Flow: User Provides Optional Due Date
**Trigger**: User includes due_date field
1. At step 2, system additionally validates due_date (must be future date)
2. System stores task with due_date field populated
3. Returns to step 5 (success confirmation)

---

## Error Scenarios

### Error 1: [Error Case Name]

**Trigger**: [What causes this error?]

**Expected System Behavior**:
- [How should system respond?]
- [What error message to show?]
- [What HTTP status code? (if API)]
- [How to recover?]

**Example**:
### Error: Invalid Input Data
**Trigger**: User provides empty title or description > 5000 chars
**Expected**:
- System returns HTTP 400 Bad Request
- Error message: "Title cannot be empty" or "Description exceeds maximum length (5000 characters)"
- No task is created
- User can correct input and retry

### Error 2: [Another Error Case]
[Same structure as Error 1]

---

## Acceptance Criteria (BDD Format)

Use Given-When-Then format for testable criteria:

```gherkin
Scenario: Successful task creation
  Given user is authenticated
  And user provides valid task title "Fix login bug"
  And user provides description "Login button not responding on mobile"
  When user submits task creation request
  Then system returns 201 Created
  And response includes task ID
  And task is stored in database with status "open"
  And task is assigned to requesting user

Scenario: Task creation with empty title
  Given user is authenticated
  And user provides empty title
  When user submits task creation request
  Then system returns 400 Bad Request
  And error message is "Title cannot be empty"
  And no task is created

Scenario: Task creation with description too long
  Given user is authenticated
  And user provides description longer than 5000 characters
  When user submits task creation request
  Then system returns 400 Bad Request
  And error message indicates description length limit
  And no task is created
```

**Coverage Checklist**:
- [ ] Happy path scenario
- [ ] Each error scenario
- [ ] Each alternative flow
- [ ] Edge cases (boundary conditions, empty data, max sizes)
- [ ] Concurrency scenarios (if applicable)

---

## Data Requirements

### Input Data

| Field | Type | Required | Validation Rules | Example |
|-------|------|----------|------------------|---------|
| `title` | string | Yes | Non-empty, max 200 chars | "Fix login bug" |
| `description` | string | No | Max 5000 chars | "Login button..." |
| `assignee_id` | integer | No | Must be valid user ID | 42 |
| `due_date` | ISO 8601 date | No | Must be future date | "2025-10-15" |

### Output Data

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `task_id` | integer | Unique task identifier | 123 |
| `created_at` | ISO 8601 timestamp | Creation timestamp | "2025-09-30T10:30:00Z" |
| `status` | string | Task status | "open" |
| `owner_id` | integer | User who created task | 7 |

### Data Validation Rules

- Title: Required, 1-200 characters, alphanumeric + punctuation
- Description: Optional, 0-5000 characters
- Assignee ID: Optional, must exist in users table
- Due Date: Optional, must be future date (> current date)

---

## Non-Functional Requirements

### Performance
- **Response Time**: 95th percentile < [X ms]
- **Throughput**: Support [X] requests/second
- **Concurrency**: Handle [X] concurrent users

### Security
- **Authentication**: [Required? Which method?]
- **Authorization**: [Who can perform this action?]
- **Data Encryption**: [Sensitive fields to encrypt?]
- **Audit Logging**: [What to log? PII considerations?]

### Reliability
- **Uptime**: [Target uptime %]
- **Error Handling**: [How to handle failures gracefully?]
- **Recovery**: [Rollback/retry strategy?]
- **Data Consistency**: [ACID requirements? Idempotency?]

### Scalability
- **Expected Load**: [Current and future scale]
- **Database Impact**: [Indexing requirements?]
- **Caching**: [What to cache?]

---

## Technical Considerations

### Database Schema
[What tables/collections are involved?]

**Example**:
```sql
Table: tasks
- id (PRIMARY KEY, AUTO_INCREMENT)
- title (VARCHAR(200), NOT NULL)
- description (TEXT)
- status (ENUM('open', 'in_progress', 'done'), DEFAULT 'open')
- owner_id (INT, FOREIGN KEY users.id)
- assignee_id (INT, FOREIGN KEY users.id, NULLABLE)
- due_date (DATE, NULLABLE)
- created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- updated_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP ON UPDATE)
```

### API Specification
[If applicable, specify REST endpoints, request/response format]

**Example**:
```
POST /api/v1/tasks
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "title": "Fix login bug",
  "description": "Login button not responding on mobile",
  "assignee_id": 42,
  "due_date": "2025-10-15"
}

Success Response (201 Created):
{
  "task_id": 123,
  "title": "Fix login bug",
  "status": "open",
  "owner_id": 7,
  "created_at": "2025-09-30T10:30:00Z"
}

Error Response (400 Bad Request):
{
  "error": "validation_error",
  "message": "Title cannot be empty",
  "field": "title"
}
```

---

## Services Used

**Requirement**: This use case MUST reference the services it uses. Service-free use cases should be challenged.

| Service | Methods Used | Purpose |
|---------|-------------|---------|
| [ServiceName] | `method_name()`, `other_method()` | [Why this service is needed] |
| [AnotherService] | `method_x()` | [Purpose in this UC] |

**Service Traceability**:
- All services referenced above must be defined in `services/[service-name]/service-spec.md`
- If no services are needed, explain why (e.g., "Pure UI change, no business logic")

**Example**:
```
| Service | Methods Used | Purpose |
|---------|-------------|---------|
| AuthService | authenticate(), create_session() | User authentication |
| UserService | get_user(), update_last_login() | Retrieve and update user data |
| EmailService | send_email() | Send login notification |
```

---

## Service Flow

Visual representation of service interactions in this use case:

```
1. User submits credentials
   ↓
2. AuthService.authenticate(email, password)
   ├─ Success → Continue to step 3
   └─ Failure → Return error (step 6)
   ↓
3. UserService.get_user(user_id)
   ├─ User found → Continue
   └─ User not found → Return error (step 6)
   ↓
4. AuthService.create_session(user_id)
   ↓
5. EmailService.send_email(user, "login_notification")
   ↓
6. Return result (success with session_token OR error)
```

**Notes**:
- Show the happy path flow
- Indicate error paths where services may fail
- Number steps for traceability

---

## Implementation Plan

### Iteration Breakdown

**Iteration 1** (1-2 hours): Core functionality
- [ ] Database schema
- [ ] Basic endpoint (happy path only)
- [ ] Unit tests for happy path

**Iteration 2** (1-2 hours): Validation & error handling
- [ ] Input validation
- [ ] Error responses
- [ ] Tests for all error scenarios

**Iteration 3** (1-2 hours): Polish & edge cases
- [ ] Alternative flows
- [ ] Edge case handling
- [ ] Integration tests
- [ ] Documentation

### Testing Strategy
- **Unit Tests**: [What to unit test?]
- **Integration Tests**: [End-to-end scenarios]
- **BDD Tests**: [Gherkin scenarios automated]
- **Performance Tests**: [Load testing if needed]

---

## Open Questions

[List any unresolved questions that need user/stakeholder input]

- [ ] **Question 1**: [Specific question requiring clarification]
  - **Impact**: [Why does this matter? What's blocked?]
  - **Options**: [Potential answers or approaches]

- [ ] **Question 2**: [Another question]
  - **Impact**: [Impact description]
  - **Options**: [Options to consider]

---

## ADR References

[Link to relevant Architecture Decision Records that inform this use case]

- **ADR-XXX** ([Decision Name]): [How this ADR affects this use case]
- **ADR-YYY** ([Decision Name]): [Relevant technical choice]

---

## Related Use Cases

[Link to other use cases that interact with this one]

- **UC-XXX** ([Use Case Name]): [Relationship - "depends on", "extends", "precedes"]
- **UC-YYY** ([Use Case Name]): [Relationship]

---

## Change History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2025-09-30 | 1.0 | [Name] | Initial draft |
| 2025-10-01 | 1.1 | [Name] | Added error scenario for... |

---

## Notes

[Any additional context, design rationale, or implementation notes]

**Design Rationale**:
- [Why certain choices were made]
- [Alternatives considered and rejected]

**Future Enhancements**:
- [Features explicitly deferred to future versions]
- [Ideas for improvement]

**References**:
- [Links to related documentation, RFCs, external resources]
---

**Template Version**: 1.0
**Framework**: Claude Development Framework v2.1
**Last Updated**: 2025-10-01
**Compatibility**: Framework v2.1+
