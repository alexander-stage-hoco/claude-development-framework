# Claude Development Framework - REST API Project

**Project Type**: REST API / Microservice
**Framework**: FastAPI + SQLAlchemy + PostgreSQL
**Template Version**: 1.0.0
**Last Updated**: 2025-10-03

---

## Project Overview

**What This Is**: A REST API built using the Claude Development Framework with FastAPI.

**Purpose**: [CUSTOMIZE: Describe your API's purpose - e.g., "User management and authentication service for XYZ platform"]

**Core Functionality**:
- [CUSTOMIZE: List main features - e.g., "User registration and authentication"]
- [CUSTOMIZE: Add more features]

---

## Quick Start for Claude

### Before Every Session

**You MUST read these files in order**:

1. **This file** (`.claude/CLAUDE.md`) - Project overview
2. **`development-rules.md`** - The 12 Non-Negotiable Rules (adapted for APIs)
3. **`planning/current-iteration.md`** - What we're working on now
4. **`status/session-state.md`** - Session context and progress

### Session Start Protocol

```markdown
## Claude's Session Start Checklist

- [ ] Read .claude/CLAUDE.md (this file)
- [ ] Read .claude/development-rules.md
- [ ] Read planning/current-iteration.md
- [ ] Read status/session-state.md
- [ ] Understand current context
- [ ] Ask user for session goals if unclear
```

---

## The 12 Non-Negotiable Rules (REST API Adapted)

### 1. **Specifications Are Law**
- Every API endpoint traces to a use case specification
- `specs/use-cases/` contains all UC specs
- No endpoint implementation without UC spec

### 2. **Tests Define Correctness**
- Unit tests for services (`tests/unit/`)
- Integration tests for endpoints (`tests/integration/`)
- BDD tests for user flows (`tests/bdd/`)
- **ALL tests must pass before merging**

### 3. **Incremental Above All**
- One endpoint at a time
- Iterations max 1-3 hours
- Small, tested, working increments

### 4. **Research Informs Implementation**
- Research FastAPI patterns → `research/fastapi-patterns/`
- Database optimization → `research/db-optimization/`
- Authentication strategies → `research/auth-strategies/`

### 5. **Two-Level Planning**
- **Strategic**: Milestones group related endpoints (e.g., "User Management APIs")
- **Tactical**: Iterations implement 1-3 endpoints (1-3 hours each)

### 6. **No Shortcuts**
- No TODO comments
- No disabled tests
- No skipped validation
- Error handling from day 1

### 7. **Technical Decisions Are Binding**
- API design decisions → ADRs
- Database schema changes → ADRs
- Authentication approach → ADR-003 (already documented)
- `specs/adrs/` is the source of truth

### 8. **BDD for User-Facing Features**
- Every user-facing endpoint has a `.feature` file
- Gherkin scenarios test full request/response flow
- Use `@bdd-scenario-writer` agent

### 9. **Code Quality Standards**
- FastAPI route handlers: thin, delegate to services
- Business logic: in `src/services/`, fully tested
- Models: clear separation (SQLAlchemy models vs Pydantic schemas)
- Linting: pylint, black formatting, mypy type hints

### 10. **Session Discipline**
- Start: Update `status/session-state.md`
- During: Track progress, note blockers
- End: Summary in session state, update iteration status

### 11. **Git Workflow**
- Branch per iteration: `iteration-XX-description`
- Commit per UC: `feat(UC-XXX): implement endpoint description`
- PR per iteration with API changes documented

### 12. **API Documentation Mandatory**
- FastAPI auto-generates OpenAPI docs
- All endpoints must have docstrings
- Request/response examples in docstrings
- Schema descriptions in Pydantic models

---

## Project Structure (REST API Specific)

```
.
├── .claude/                    # Framework configuration
├── specs/
│   ├── use-cases/              # API endpoint specs
│   ├── services/               # Business logic specs
│   └── adrs/                   # Technical decisions
├── src/
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration
│   ├── api/                    # Route handlers (thin layer)
│   │   ├── deps.py             # Dependencies (auth, DB)
│   │   ├── users.py            # User endpoints
│   │   └── auth.py             # Auth endpoints
│   ├── models/                 # Data models
│   │   ├── user.py             # SQLAlchemy models
│   │   └── schemas.py          # Pydantic schemas
│   ├── services/               # Business logic (thick layer)
│   │   ├── user_service.py
│   │   └── auth_service.py
│   └── db/
│       ├── database.py         # DB connection
│       └── migrations/         # Alembic migrations
├── tests/
│   ├── unit/                   # Service layer tests
│   ├── integration/            # API endpoint tests
│   └── bdd/                    # BDD scenarios
└── docs/
    ├── api-design.md           # API design principles
    └── database-schema.md      # Schema documentation
```

---

## Development Workflow (REST API)

### Adding a New Endpoint

#### Phase 1: Specification
1. Create UC spec: `specs/use-cases/UC-XXX-endpoint-name.md`
2. Define:
   - HTTP method and path
   - Request schema (Pydantic)
   - Response schema (Pydantic)
   - Error cases (4xx, 5xx)
   - Authentication requirements

#### Phase 2: Database (if needed)
1. Update SQLAlchemy models in `src/models/`
2. Create Alembic migration: `alembic revision --autogenerate -m "description"`
3. Review and apply migration: `alembic upgrade head`

#### Phase 3: Tests First (TDD)
1. **Unit tests** (`tests/unit/`):
   ```python
   def test_create_user_service():
       # Test business logic in service layer
       user_data = UserCreate(email="test@example.com", ...)
       user = user_service.create_user(user_data)
       assert user.email == "test@example.com"
   ```

2. **Integration tests** (`tests/integration/`):
   ```python
   def test_create_user_endpoint(client):
       # Test full HTTP flow
       response = client.post("/api/v1/users", json={...})
       assert response.status_code == 201
       assert response.json()["email"] == "test@example.com"
   ```

3. **BDD tests** (`tests/bdd/features/`):
   ```gherkin
   Scenario: Create a new user
     Given I am an API client
     When I POST to "/api/v1/users" with valid data
     Then I receive a 201 status code
     And the response contains the user ID
   ```

4. **Run tests** (they should fail):
   ```bash
   pytest tests/ -v
   ```

#### Phase 4: Implement

1. **Service layer** (`src/services/`):
   ```python
   class UserService:
       def create_user(self, user_data: UserCreate) -> User:
           # Business logic here
           # Validation, hashing, DB operations
           pass
   ```

2. **API endpoint** (`src/api/`):
   ```python
   @router.post("/", response_model=UserResponse, status_code=201)
   async def create_user(
       user_data: UserCreate,
       db: Session = Depends(get_db)
   ):
       """
       Create a new user.

       - **email**: User email (unique)
       - **username**: Username (unique)
       - **password**: Password (will be hashed)
       """
       service = UserService(db)
       user = service.create_user(user_data)
       return user
   ```

3. **Update OpenAPI docs**:
   - Add examples in Pydantic schemas
   - Add descriptions to fields
   - Document error responses

#### Phase 5: Validate
1. Run tests: `pytest tests/ -v`
2. Check coverage: `pytest --cov=src tests/`
3. Manual API test: Check `/docs` endpoint
4. Lint: `black src/ tests/` and `pylint src/`

---

## REST API Best Practices (This Template)

### 1. Layered Architecture
- **API layer** (`src/api/`): HTTP concerns only (request/response, status codes)
- **Service layer** (`src/services/`): Business logic, fully unit tested
- **Data layer** (`src/models/`, `src/db/`): Database operations

### 2. Request/Response Validation
- Use Pydantic models for ALL requests and responses
- Define in `src/models/schemas.py`
- Automatic validation by FastAPI

### 3. Error Handling
```python
try:
    result = service.do_something()
    return result
except NotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
except ValidationError as e:
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

### 4. Authentication
- JWT tokens (see `src/api/auth.py`)
- Protected endpoints use `Depends(get_current_user)`
- Token validation in middleware

### 5. Database Sessions
- Use dependency injection: `db: Session = Depends(get_db)`
- Always close sessions (handled by dependency)
- Use transactions for multi-step operations

### 6. API Versioning
- Include version in path: `/api/v1/...`
- Breaking changes → new version `/api/v2/...`
- Document in ADRs

---

## Common Commands (REST API Development)

### Development
```bash
# Start dev server
uvicorn src.main:app --reload

# Start with Docker
docker-compose up api

# Run tests
pytest tests/ -v

# Run with coverage
pytest --cov=src --cov-report=html tests/

# Database migrations
alembic revision --autogenerate -m "description"
alembic upgrade head

# API documentation
# Visit http://localhost:8000/docs
```

### Quality Checks
```bash
# Format code
black src/ tests/

# Lint
pylint src/

# Type check
mypy src/

# All quality checks
claude-dev check all
```

### Database
```bash
# Create migration
alembic revision --autogenerate -m "add user table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Reset database (dev only!)
alembic downgrade base && alembic upgrade head
```

---

## Integration with Claude Agents

### Available Agents

1. **@uc-writer** - Generate API endpoint specs
   ```
   @uc-writer create spec for user registration endpoint
   ```

2. **@test-writer** - Generate tests for endpoint
   ```
   @test-writer generate tests for UC-001
   ```

3. **@bdd-scenario-writer** - Create BDD scenarios
   ```
   @bdd-scenario-writer create scenarios for user authentication flow
   ```

4. **@code-quality-checker** - Validate before commit
   ```
   @code-quality-checker check src/api/users.py
   ```

5. **@service-designer** - Design service interfaces
   ```
   @service-designer design UserService for UC-001, UC-002, UC-003
   ```

---

## API-Specific Reminders

### When Adding Endpoints
- [ ] UC specification exists
- [ ] Request schema defined (Pydantic)
- [ ] Response schema defined (Pydantic)
- [ ] Error cases documented
- [ ] Tests written first
- [ ] Service layer implements business logic
- [ ] API layer is thin (just HTTP handling)
- [ ] OpenAPI docs updated
- [ ] Authentication added if needed
- [ ] Database migration if schema changes

### When Modifying Schema
- [ ] Create Alembic migration
- [ ] Update SQLAlchemy models
- [ ] Update Pydantic schemas
- [ ] Update tests
- [ ] Document in ADR if significant change

### Before Commit
- [ ] All tests pass
- [ ] Coverage ≥ 90%
- [ ] Code formatted (black)
- [ ] No linting errors
- [ ] API docs updated
- [ ] Migration applied (if any)

---

## Troubleshooting

### Common Issues

**Database connection errors**:
- Check `DATABASE_URL` in `.env`
- Ensure PostgreSQL is running
- Verify migrations applied: `alembic current`

**Import errors**:
- Check `PYTHONPATH` includes `src/`
- Use absolute imports: `from src.models import User`

**Tests failing**:
- Use test database (see `tests/conftest.py`)
- Reset test DB between tests
- Check fixtures are properly defined

**OpenAPI docs not updating**:
- Restart server after schema changes
- Clear browser cache
- Check Pydantic model definitions

---

## Project Customization

### To Adapt This Template:

1. **Update Project Info**:
   - Edit this file (`.claude/CLAUDE.md`)
   - Update `README.md`
   - Modify `src/config.py` with project name

2. **Replace Example UCs**:
   - Delete example UCs in `specs/use-cases/`
   - Create your own UC specifications
   - Update `src/api/` endpoints accordingly

3. **Adapt Database**:
   - Modify `src/models/` for your schema
   - Create new migrations
   - Update connection in `src/db/database.py` if needed

4. **Configure Deployment**:
   - Update `Dockerfile` and `docker-compose.yml`
   - Set environment variables in `.env`
   - Configure CI/CD in `.github/workflows/`

---

## Next Steps

1. **Read the framework rules**: `.claude/development-rules.md`
2. **Review current iteration**: `planning/current-iteration.md`
3. **Check session state**: `status/session-state.md`
4. **Start coding**: Follow TDD cycle for your first endpoint

---

**Remember**:
- Specifications first
- Tests before code
- Incremental progress
- Quality always

Good luck building your API! 🚀

---

**Last Updated**: 2025-10-03
**Framework Version**: v2.1
**Template Type**: REST API (FastAPI)
