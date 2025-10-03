---
id: UC-001
title: Create User
status: implemented
priority: high
created: 2025-10-03
updated: 2025-10-03
version: 1.0.0
---

# UC-001: Create User

## Overview

**Purpose**: Allow new users to register by creating a user account in the system.

**Actor**: API Client (Web/Mobile App, External Service)

**Preconditions**:
- System is operational
- Database is accessible
- Email and username are not already registered

**Postconditions**:
- User account created in database
- User ID returned to client
- User can authenticate with provided credentials

---

## API Specification

### Endpoint

**Method**: `POST`
**Path**: `/api/v1/users`
**Authentication**: None (public endpoint)

### Request

**Headers**:
```
Content-Type: application/json
```

**Body** (JSON):
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Schema** (Pydantic):
```python
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    password: str = Field(..., min_length=8)
```

### Response

#### Success (201 Created)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "johndoe",
  "created_at": "2025-10-03T10:30:00Z"
}
```

**Schema** (Pydantic):
```python
class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    created_at: datetime

    class Config:
        from_attributes = True
```

#### Error Responses

**400 Bad Request** - Invalid input
```json
{
  "detail": "Email already registered"
}
```

**400 Bad Request** - Validation error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

**500 Internal Server Error** - System error
```json
{
  "detail": "Internal server error"
}
```

---

## Business Rules

### BR-001: Email Uniqueness
- Email must be unique across all users
- Case-insensitive comparison
- Return 400 error if email already exists

### BR-002: Username Uniqueness
- Username must be unique across all users
- Case-sensitive comparison
- Return 400 error if username already exists

### BR-003: Password Security
- Minimum 8 characters
- Must be hashed before storage (bcrypt)
- Never return password in response

### BR-004: Email Validation
- Must be valid email format
- Use email-validator library

### BR-005: Username Format
- 3-50 characters
- Alphanumeric, hyphens, underscores only
- Cannot start/end with hyphen or underscore

---

## Acceptance Criteria

### AC-001: Valid User Creation
**Given** I am an API client
**When** I POST to `/api/v1/users` with valid email, username, and password
**Then** I receive a 201 status code
**And** the response contains the user ID
**And** the response contains the email and username
**And** the password is NOT in the response
**And** the user is stored in the database

### AC-002: Duplicate Email Rejected
**Given** a user exists with email "test@example.com"
**When** I POST to `/api/v1/users` with email "test@example.com"
**Then** I receive a 400 status code
**And** the error message indicates "Email already registered"

### AC-003: Duplicate Username Rejected
**Given** a user exists with username "johndoe"
**When** I POST to `/api/v1/users` with username "johndoe"
**Then** I receive a 400 status code
**And** the error message indicates "Username already exists"

### AC-004: Invalid Email Format Rejected
**Given** I am an API client
**When** I POST to `/api/v1/users` with email "invalid-email"
**Then** I receive a 400 status code
**And** the error indicates invalid email format

### AC-005: Weak Password Rejected
**Given** I am an API client
**When** I POST to `/api/v1/users` with password "123"
**Then** I receive a 400 status code
**And** the error indicates password minimum length requirement

### AC-006: Password Hashed
**Given** I create a user with password "SecurePass123!"
**When** the user is stored in the database
**Then** the password is hashed (bcrypt)
**And** the plain password is NOT stored

---

## Implementation Notes

### Database Schema

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

### Service Layer Logic

1. Validate input (Pydantic handles this)
2. Check if email exists (case-insensitive)
3. Check if username exists (case-sensitive)
4. Hash password (bcrypt with salt)
5. Create user record in database
6. Return user (without password)

### Error Handling

```python
try:
    user = user_service.create_user(user_data)
    return user
except EmailAlreadyExistsError:
    raise HTTPException(status_code=400, detail="Email already registered")
except UsernameExistsError:
    raise HTTPException(status_code=400, detail="Username already exists")
except Exception as e:
    logger.error(f"Error creating user: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

---

## Test Plan

### Unit Tests (`tests/unit/test_user_service.py`)

1. `test_create_user_success()` - Valid user creation
2. `test_create_user_duplicate_email()` - Email uniqueness
3. `test_create_user_duplicate_username()` - Username uniqueness
4. `test_password_hashed()` - Password hashing
5. `test_email_case_insensitive()` - Email comparison

### Integration Tests (`tests/integration/test_user_api.py`)

1. `test_create_user_endpoint_success()` - Full API flow
2. `test_create_user_invalid_email()` - Validation error
3. `test_create_user_weak_password()` - Password validation
4. `test_create_user_duplicate_email()` - Duplicate handling
5. `test_create_user_duplicate_username()` - Duplicate handling

### BDD Tests (`tests/bdd/features/UC-001-create-user.feature`)

```gherkin
Feature: User Registration
  As an API client
  I want to create a new user account
  So that users can access the system

  Scenario: Successfully create a new user
    Given I am an API client
    When I POST to "/api/v1/users" with:
      | email              | username | password       |
      | test@example.com   | testuser | SecurePass123! |
    Then I receive a 201 status code
    And the response contains the user ID
    And the response contains email "test@example.com"
    And the response contains username "testuser"
    And the response does not contain the password

  Scenario: Reject duplicate email
    Given a user exists with email "existing@example.com"
    When I POST to "/api/v1/users" with email "existing@example.com"
    Then I receive a 400 status code
    And the error message is "Email already registered"

  Scenario: Reject duplicate username
    Given a user exists with username "existinguser"
    When I POST to "/api/v1/users" with username "existinguser"
    Then I receive a 400 status code
    And the error message is "Username already exists"
```

---

## Dependencies

### Services
- `UserService` - User business logic (to be created)
- Database session - SQLAlchemy session

### External Libraries
- `passlib` - Password hashing
- `email-validator` - Email validation
- `sqlalchemy` - Database ORM

### Related Use Cases
- UC-002: Authenticate User (uses created user credentials)
- UC-003: List Users (displays created users)

---

## Non-Functional Requirements

### Performance
- Response time < 200ms (excluding network latency)
- Support 100 concurrent user registrations

### Security
- Password hashed with bcrypt (cost factor: 12)
- No password in logs or responses
- HTTPS required in production

### Reliability
- Database transaction for atomic user creation
- Rollback on any error
- Idempotent (retry-safe with same data)

---

## Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-10-03 | Initial specification | Template |

---

## References

- ADR-002: Database Selection (PostgreSQL)
- ADR-003: Authentication Strategy (JWT)
- SVC-001: User Service Specification

---

**Status**: Implemented (Example)
**Last Reviewed**: 2025-10-03
**Next Review**: 2025-11-03
