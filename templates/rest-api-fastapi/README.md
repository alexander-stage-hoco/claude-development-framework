# REST API Template - FastAPI

**Template Type**: REST API / Microservice
**Framework**: FastAPI + SQLAlchemy + PostgreSQL
**Claude Framework Version**: v2.3

---

## What This Template Provides

A production-ready REST API template following the Claude Development Framework with:

✅ **FastAPI Application** - Modern, fast web framework for APIs
✅ **Database Integration** - SQLAlchemy ORM + PostgreSQL
✅ **Authentication** - JWT-based authentication ready to use
✅ **API Documentation** - Auto-generated Swagger/OpenAPI docs
✅ **Example Use Cases** - 3 complete UCs with tests (User management)
✅ **Testing Suite** - Unit, integration, and BDD tests
✅ **Docker Support** - Containerized deployment
✅ **CI/CD Workflows** - GitHub Actions configured

---

## Quick Start

### 1. Copy Template

```bash
# Using init script
./init-project.sh my-api --template rest-api-fastapi

# Or manual copy
cp -r templates/rest-api-fastapi/ my-api/
cd my-api/
```

### 2. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Database

```bash
# Copy environment template
cp .env.example .env

# Update .env with your database credentials
DATABASE_URL=postgresql://user:password@localhost:5432/myapi
SECRET_KEY=your-secret-key-here
```

### 4. Run Database Migrations

```bash
# Initialize database
alembic upgrade head

# Or use Docker Compose for local development
docker-compose up -d postgres
```

### 5. Start Development Server

```bash
# Run FastAPI server
uvicorn src.main:app --reload

# Or with Docker
docker-compose up api
```

### 6. Explore API

- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## Project Structure

```
rest-api-fastapi/
├── .claude/                          # Framework configuration
│   ├── CLAUDE.md                     # Project overview (REST API adapted)
│   ├── development-rules.md          # Adapted for API development
│   ├── templates/                    # Spec templates
│   └── agents/                       # Framework agents
├── specs/
│   ├── use-cases/
│   │   ├── UC-001-create-user.md    # Create user UC
│   │   ├── UC-002-authenticate.md    # Authentication UC
│   │   └── UC-003-list-users.md      # List users UC
│   ├── services/
│   │   ├── SVC-001-user-service.md
│   │   └── SVC-002-auth-service.md
│   └── adrs/
│       ├── ADR-001-fastapi.md        # Why FastAPI
│       ├── ADR-002-postgresql.md     # Database choice
│       └── ADR-003-jwt-auth.md       # Auth strategy
├── src/
│   ├── main.py                       # FastAPI application entry
│   ├── config.py                     # Configuration management
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                   # Dependencies (DB, auth)
│   │   ├── users.py                  # User endpoints
│   │   └── auth.py                   # Auth endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                   # User model
│   │   └── schemas.py                # Pydantic schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py           # User business logic
│   │   └── auth_service.py           # Auth business logic
│   └── db/
│       ├── __init__.py
│       ├── database.py               # Database connection
│       └── migrations/               # Alembic migrations
├── tests/
│   ├── conftest.py                   # Pytest configuration
│   ├── unit/
│   │   ├── test_user_service.py
│   │   └── test_auth_service.py
│   ├── integration/
│   │   ├── test_user_api.py
│   │   └── test_auth_api.py
│   └── bdd/
│       ├── features/
│       │   ├── UC-001-create-user.feature
│       │   └── UC-002-authenticate.feature
│       └── steps/
│           └── user_steps.py
├── docs/
│   ├── api-design.md                 # API design decisions
│   ├── deployment.md                 # Deployment guide
│   └── database-schema.md            # Schema documentation
├── .github/
│   └── workflows/
│       ├── test.yml                  # CI testing
│       └── deploy.yml                # CD deployment
├── docker-compose.yml                # Local development
├── Dockerfile                        # Production container
├── requirements.txt                  # Dependencies
├── .env.example                      # Environment template
└── README.md                         # This file
```

---

## Example Use Cases

### UC-001: Create User

**Specification**: `specs/use-cases/UC-001-create-user.md`

**Endpoint**: `POST /api/v1/users`

**Request**:
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Response**:
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "username": "johndoe",
  "created_at": "2025-10-03T10:30:00Z"
}
```

**Tests**:
- Unit: `tests/unit/test_user_service.py::test_create_user`
- Integration: `tests/integration/test_user_api.py::test_create_user_endpoint`
- BDD: `tests/bdd/features/UC-001-create-user.feature`

---

### UC-002: Authenticate User

**Specification**: `specs/use-cases/UC-002-authenticate.md`

**Endpoint**: `POST /api/v1/auth/login`

**Request**:
```json
{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**Tests**:
- Unit: `tests/unit/test_auth_service.py::test_authenticate`
- Integration: `tests/integration/test_auth_api.py::test_login_endpoint`
- BDD: `tests/bdd/features/UC-002-authenticate.feature`

---

### UC-003: List Users

**Specification**: `specs/use-cases/UC-003-list-users.md`

**Endpoint**: `GET /api/v1/users`

**Query Parameters**:
- `skip`: Offset for pagination (default: 0)
- `limit`: Number of results (default: 10, max: 100)

**Response**:
```json
{
  "items": [
    {
      "id": "uuid",
      "email": "user@example.com",
      "username": "johndoe",
      "created_at": "2025-10-03T10:30:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 10
}
```

**Tests**:
- Unit: `tests/unit/test_user_service.py::test_list_users`
- Integration: `tests/integration/test_user_api.py::test_list_users_endpoint`
- BDD: `tests/bdd/features/UC-003-list-users.feature`

---

## Technology Stack

### Core
- **FastAPI** (0.104+) - Web framework
- **Python** (3.11+) - Programming language
- **Pydantic** (2.0+) - Data validation

### Database
- **SQLAlchemy** (2.0+) - ORM
- **PostgreSQL** (14+) - Database
- **Alembic** - Database migrations

### Authentication
- **python-jose** - JWT handling
- **passlib** - Password hashing
- **bcrypt** - Hashing algorithm

### Testing
- **pytest** - Test framework
- **pytest-asyncio** - Async testing
- **httpx** - HTTP client for testing
- **pytest-bdd** - BDD testing

### DevOps
- **Docker** - Containerization
- **docker-compose** - Local orchestration
- **GitHub Actions** - CI/CD

---

## Development Workflow

### 1. Create New Use Case

```bash
# Create UC specification
claude-dev spec new use-case --id UC-004 --title "Update User"

# Or manually create in specs/use-cases/
```

### 2. Write Tests First (TDD)

```bash
# Create test file
touch tests/unit/test_update_user.py

# Write failing tests
# Then run: pytest tests/unit/test_update_user.py
```

### 3. Implement Feature

```python
# Add endpoint in src/api/users.py
@router.put("/{user_id}")
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    # Implementation here
    pass
```

### 4. Run All Tests

```bash
# Run full test suite
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

### 5. Check Quality

```bash
# Run all quality checks
claude-dev check all

# Or manually
black src/ tests/
pylint src/
mypy src/
```

---

## API Design Patterns

### 1. Request/Response Models

Use Pydantic schemas for validation:

```python
# src/models/schemas.py
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    created_at: datetime

    class Config:
        from_attributes = True
```

### 2. Service Layer

Business logic in services, not endpoints:

```python
# src/services/user_service.py
class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:
        # Business logic here
        pass
```

### 3. Error Handling

Consistent error responses:

```python
# src/api/users.py
@router.post("/")
async def create_user(user_data: UserCreate):
    try:
        user = user_service.create_user(user_data)
        return user
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

---

## Deployment

### Docker Deployment

```bash
# Build image
docker build -t my-api:latest .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e SECRET_KEY=... \
  my-api:latest
```

### Kubernetes (Coming Soon)

See `docs/deployment.md` for Kubernetes manifests.

### Cloud Deployment

- **AWS**: ECS/Fargate or Lambda (with Mangum adapter)
- **GCP**: Cloud Run or GKE
- **Azure**: Container Instances or AKS

---

## Next Steps

1. **Customize for Your Domain**
   - Replace example use cases with your requirements
   - Adapt database models
   - Update API endpoints

2. **Add Your Features**
   - Follow TDD cycle: Test → Implement → Refactor
   - Use `claude-dev` commands for consistency
   - Keep spec-code alignment

3. **Configure Deployment**
   - Update Docker configuration
   - Set up CI/CD secrets
   - Configure production database

4. **Scale Up**
   - Add caching (Redis)
   - Implement rate limiting
   - Set up monitoring (Prometheus/Grafana)

---

## FAQ

**Q: Can I use MySQL instead of PostgreSQL?**
A: Yes! Update `DATABASE_URL` in `.env` and `requirements.txt`. SQLAlchemy supports multiple databases.

**Q: How do I add new endpoints?**
A: Create UC spec → Write tests → Implement in `src/api/` → Run tests → Deploy.

**Q: Where do I put business logic?**
A: In `src/services/`. Keep endpoints thin - they should just handle HTTP concerns.

**Q: How do I handle authentication?**
A: Example JWT auth is in `src/api/auth.py`. Use `get_current_user` dependency in protected endpoints.

**Q: Can I use async database operations?**
A: Yes! This template uses sync SQLAlchemy, but you can switch to `asyncpg` + async SQLAlchemy.

---

## Support

- **Template Issues**: Check `docs/` directory
- **Framework Questions**: See `.claude/CLAUDE.md`
- **FastAPI Docs**: https://fastapi.tiangolo.com/

---

**Version**: 1.0.0
**Last Updated**: 2025-10-03
**Template Type**: REST API (FastAPI)
**Part of**: Claude Development Framework v2.1

Happy API building! 🚀
