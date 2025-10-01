# Example: Service Extraction with Subagent

**Scenario**: User has completed 5 use case specifications and requests service extraction
**Complexity**: Medium
**Duration**: ~30 minutes
**Framework Features**: Service-oriented architecture, subagent automation, UC-Service traceability
**Subagents Used**: service-extractor

---

## Context

**Project**: E-commerce Order Management API
**Session**: 4 (after specifications complete)
**Project State**:
- ✅ 5 use cases specified (UC-001 through UC-005)
- ✅ Project overview complete
- ✅ Technology stack decided (FastAPI, PostgreSQL)
- ❌ No services extracted yet
- ❌ No implementation yet

**Use Cases Defined**:
- UC-001: User Registration
- UC-002: User Login
- UC-003: Create Order
- UC-004: View Order History
- UC-005: Update Order Status

**User Goal**: Extract reusable services from use cases before implementation begins

---

## Session Transcript

### User Request

```
User: "We've completed all 5 use case specifications. Please extract services
from these use cases. Follow the service extraction protocol."
```

---

### Claude's Initial Response

```
Claude: Perfect! I'll use the service-extractor subagent to analyze your use
cases and identify reusable services following service-oriented architecture
principles.

📖 Reading framework files:
- .claude/CLAUDE.md ✅
- .claude/development-rules.md ✅
- .claude/subagents/service-extractor.md ✅

**What I'll do**:
1. Launch service-extractor subagent
2. Analyze all 5 use cases
3. Extract required capabilities
4. Group by domain (Single Responsibility Principle)
5. Define service boundaries (minimize dependencies)
6. Create service specifications
7. Update service registry
8. Update use cases with service references

**Quality Checks**:
- Each service has ≤3 dependencies
- No circular dependencies
- All services follow Single Responsibility Principle
- Complete UC-Service traceability

Launching service-extractor subagent now...
```

---

### Subagent Execution

**Behind the Scenes**: Claude calls the Task tool:

```python
Task(
    subagent_type="general-purpose",
    description="Extract services from use cases",
    prompt="""
You are the service-extractor subagent from .claude/subagents/service-extractor.md.

Context:
- Project: E-commerce Order Management API
- Use cases: specs/use-cases/UC-001 through UC-005
- No services exist yet

Your task:
1. Read all 5 use case specifications
2. Extract required capabilities from each UC
3. Group capabilities by business domain
4. Define service boundaries (Single Responsibility Principle)
5. Create service specifications using template
6. Update .claude/service-registry.md
7. Update each UC with "Services Used" section

Quality requirements:
- Each service ≤3 dependencies
- No circular dependencies
- Stateless preferred (justify if stateful)
- Service names reflect business domain

Work autonomously. Return complete extraction report.
"""
)
```

**Subagent Working** (autonomous execution):

```
[Subagent reads files...]
- specs/use-cases/UC-001-user-registration.md
- specs/use-cases/UC-002-user-login.md
- specs/use-cases/UC-003-create-order.md
- specs/use-cases/UC-004-view-order-history.md
- specs/use-cases/UC-005-update-order-status.md

[Subagent analyzes capabilities...]

UC-001 (User Registration):
- Validate email format
- Hash password securely
- Create user account
- Send confirmation email
- Prevent duplicate registrations

UC-002 (User Login):
- Authenticate credentials
- Create session
- Hash password for comparison
- Log login attempt

UC-003 (Create Order):
- Validate user is authenticated
- Validate product availability
- Calculate order total
- Create order record
- Send order confirmation email

UC-004 (View Order History):
- Validate user is authenticated
- Retrieve user's orders
- Sort by date

UC-005 (Update Order Status):
- Validate user has permission
- Update order status
- Log status change
- Send status update notification

[Subagent groups by domain...]

Authentication & Security:
- Hash password
- Authenticate credentials
- Create session
- Validate authentication

User Management:
- Create user account
- Prevent duplicates

Order Management:
- Create order
- Update order status
- Retrieve orders
- Log changes

Product Management:
- Validate availability
- Calculate pricing

Communication:
- Send confirmation emails
- Send notifications

Validation:
- Email validation
- Input validation

[Subagent defines services...]

Service 1: AuthService
Service 2: UserService
Service 3: OrderService
Service 4: ProductService
Service 5: EmailService
Service 6: ValidationService

[Subagent creates service specifications...]
[Subagent updates service registry...]
[Subagent updates use case files...]
```

---

### Subagent Report to Claude

```markdown
# Service Extraction Report

**Date**: 2024-09-30
**Use Cases Analyzed**: 5 files
**Services Identified**: 6 services
**Files Created**: 6 service specifications
**Files Updated**: 5 use cases + service registry

---

## Services Extracted

### SVC-001: AuthService
**Responsibility**: Manage authentication and password security
**State Management**: Stateless
**Used By**: UC-001, UC-002, UC-003, UC-004, UC-005
**Dependencies**: SVC-006 (ValidationService)

**Methods**:
```python
def hash_password(password: str) -> str
def verify_password(password: str, hash: str) -> bool
def authenticate(email: str, password: str) -> Result[Session, AuthError]
def create_session(user_id: int) -> Result[Session, SessionError]
```

**File Created**: `services/auth-service/service-spec.md`

---

### SVC-002: UserService
**Responsibility**: Manage user accounts and profiles
**State Management**: Stateless (uses database for persistence)
**Used By**: UC-001, UC-002
**Dependencies**: SVC-001 (AuthService), SVC-006 (ValidationService)

**Methods**:
```python
def create_user(email: str, password_hash: str) -> Result[User, UserError]
def get_user_by_email(email: str) -> Result[User, NotFoundError]
def get_user_by_id(user_id: int) -> Result[User, NotFoundError]
def email_exists(email: str) -> bool
```

**File Created**: `services/user-service/service-spec.md`

---

### SVC-003: OrderService
**Responsibility**: Manage order lifecycle (create, update, retrieve)
**State Management**: Stateless (uses database for persistence)
**Used By**: UC-003, UC-004, UC-005
**Dependencies**: SVC-006 (ValidationService)

**Methods**:
```python
def create_order(user_id: int, items: List[OrderItem]) -> Result[Order, OrderError]
def get_order(order_id: int) -> Result[Order, NotFoundError]
def get_user_orders(user_id: int, limit: int, offset: int) -> List[Order]
def update_order_status(order_id: int, status: OrderStatus) -> Result[Order, OrderError]
def log_status_change(order_id: int, old_status: str, new_status: str) -> None
```

**File Created**: `services/order-service/service-spec.md`

---

### SVC-004: ProductService
**Responsibility**: Manage product catalog and availability
**State Management**: Stateless (uses database + cache)
**Used By**: UC-003
**Dependencies**: None

**Methods**:
```python
def get_product(product_id: int) -> Result[Product, NotFoundError]
def check_availability(product_id: int, quantity: int) -> bool
def calculate_total(items: List[OrderItem]) -> Decimal
def reserve_stock(product_id: int, quantity: int) -> Result[None, StockError]
```

**File Created**: `services/product-service/service-spec.md`

---

### SVC-005: EmailService
**Responsibility**: Send transactional emails to users
**State Management**: Stateless
**Used By**: UC-001, UC-003, UC-005
**Dependencies**: None

**Methods**:
```python
def send_email(to: str, subject: str, body: str) -> Result[EmailSent, EmailError]
def send_template(to: str, template: str, context: dict) -> Result[EmailSent, EmailError]
def send_confirmation(user: User) -> Result[EmailSent, EmailError]
def send_order_confirmation(order: Order) -> Result[EmailSent, EmailError]
def send_status_update(order: Order) -> Result[EmailSent, EmailError]
```

**File Created**: `services/email-service/service-spec.md`

---

### SVC-006: ValidationService
**Responsibility**: Validate user inputs against business rules
**State Management**: Stateless
**Used By**: SVC-001, SVC-002, SVC-003
**Dependencies**: None

**Methods**:
```python
def validate_email(email: str) -> Result[None, ValidationError]
def validate_password(password: str) -> Result[None, ValidationError]
def validate_order_items(items: List[OrderItem]) -> Result[None, ValidationError]
```

**File Created**: `services/validation-service/service-spec.md`

---

## Dependency Analysis

### Layered Architecture

```
Layer 1 (No dependencies):
├── SVC-004: ProductService
├── SVC-005: EmailService
└── SVC-006: ValidationService

Layer 2 (Depends on Layer 1):
├── SVC-001: AuthService → SVC-006
└── SVC-003: OrderService → SVC-006

Layer 3 (Depends on Layers 1-2):
└── SVC-002: UserService → SVC-001, SVC-006
```

### Dependency Count

| Service | Dependencies | Count | Status |
|---------|--------------|-------|--------|
| SVC-001: AuthService | SVC-006 | 1 | ✅ OK |
| SVC-002: UserService | SVC-001, SVC-006 | 2 | ✅ OK |
| SVC-003: OrderService | SVC-006 | 1 | ✅ OK |
| SVC-004: ProductService | None | 0 | ✅ OK |
| SVC-005: EmailService | None | 0 | ✅ OK |
| SVC-006: ValidationService | None | 0 | ✅ OK |

**Result**: ✅ All services have ≤3 dependencies

### Circular Dependencies

**Cycle Detection**: Ran depth-first search on dependency graph

**Result**: ✅ No circular dependencies detected

---

## Service-to-UC Traceability

### By Service

**SVC-001: AuthService**
- UC-001: User Registration (`hash_password`, `create_session`)
- UC-002: User Login (`authenticate`, `create_session`)
- UC-003: Create Order (`create_session` for auth check)
- UC-004: View Order History (session validation)
- UC-005: Update Order Status (session validation)

**SVC-002: UserService**
- UC-001: User Registration (`create_user`, `email_exists`)
- UC-002: User Login (`get_user_by_email`)

**SVC-003: OrderService**
- UC-003: Create Order (`create_order`)
- UC-004: View Order History (`get_user_orders`)
- UC-005: Update Order Status (`update_order_status`, `log_status_change`)

**SVC-004: ProductService**
- UC-003: Create Order (`get_product`, `check_availability`, `calculate_total`)

**SVC-005: EmailService**
- UC-001: User Registration (`send_confirmation`)
- UC-003: Create Order (`send_order_confirmation`)
- UC-005: Update Order Status (`send_status_update`)

**SVC-006: ValidationService**
- Used internally by SVC-001, SVC-002, SVC-003

### By Use Case

| Use Case | Services Referenced | Count |
|----------|---------------------|-------|
| UC-001: User Registration | SVC-001, SVC-002, SVC-005, SVC-006 | 4 |
| UC-002: User Login | SVC-001, SVC-002 | 2 |
| UC-003: Create Order | SVC-001, SVC-003, SVC-004, SVC-005 | 4 |
| UC-004: View Order History | SVC-001, SVC-003 | 2 |
| UC-005: Update Order Status | SVC-001, SVC-003, SVC-005 | 3 |

**Result**: ✅ All use cases reference services

---

## Files Created

**Service Specifications**:
- `services/auth-service/service-spec.md` (285 lines)
- `services/user-service/service-spec.md` (220 lines)
- `services/order-service/service-spec.md` (310 lines)
- `services/product-service/service-spec.md` (240 lines)
- `services/email-service/service-spec.md` (195 lines)
- `services/validation-service/service-spec.md` (180 lines)

**Registry Update**:
- `.claude/service-registry.md` (updated with 6 services)

**Use Case Updates**:
- Added "Services Used" sections to all 5 UCs
- Added service flow diagrams to all 5 UCs

---

## Quality Metrics

- **Average Dependencies per Service**: 0.67
- **Max Dependencies**: 2 (UserService)
- **Services with 0 Dependencies**: 3 (50%)
- **Circular Dependencies**: 0 ✅
- **UC Coverage**: 100% (all UCs reference services) ✅
- **Service Reuse**: 3.0 UCs per service (average)

**Overall Quality**: ✅ Excellent

---

## Next Steps

1. ✅ Service extraction complete
2. **Recommended**: Run service-library-finder for external libraries
3. **Recommended**: Run service-designer for detailed interface design
4. **Required**: Run service-dependency-analyzer to validate architecture
5. **Then**: Begin TDD implementation (Layer 1 services first)

**Ready for Next Phase**: ✅ Yes

---

**Extraction Complete**: 2024-09-30 10:45 AM
**Total Time**: 8 minutes
```

---

### Claude Presents Results to User

```
Claude: ✅ Service extraction complete!

**6 services extracted** from 5 use cases:

1. **AuthService** (SVC-001) - Authentication and security
   - Used by: All 5 use cases
   - Dependencies: ValidationService (1)
   - Layer: 2

2. **UserService** (SVC-002) - User account management
   - Used by: UC-001, UC-002
   - Dependencies: AuthService, ValidationService (2)
   - Layer: 3

3. **OrderService** (SVC-003) - Order lifecycle management
   - Used by: UC-003, UC-004, UC-005
   - Dependencies: ValidationService (1)
   - Layer: 2

4. **ProductService** (SVC-004) - Product catalog and inventory
   - Used by: UC-003
   - Dependencies: None (0)
   - Layer: 1

5. **EmailService** (SVC-005) - Transactional email delivery
   - Used by: UC-001, UC-003, UC-005
   - Dependencies: None (0)
   - Layer: 1

6. **ValidationService** (SVC-006) - Input validation
   - Used by: SVC-001, SVC-002, SVC-003 (internal)
   - Dependencies: None (0)
   - Layer: 1

**Architecture Quality**: ✅ Excellent

- Clean 3-layer architecture
- No circular dependencies
- All services ≤2 dependencies (target: ≤3)
- 100% UC-Service traceability
- High service reuse (avg 3 UCs per service)

**Files Created**:
- 6 service specification files (~1,430 lines total)
- Service registry updated
- All 5 use cases updated with service references

**Next Steps**:

1. **Library Evaluation** (Optional but recommended)
   - Use service-library-finder for AuthService (authentication libraries)
   - Use service-library-finder for EmailService (email delivery)
   - ~15-20 minutes

2. **Interface Design** (Recommended)
   - Use service-designer for detailed Protocol interfaces
   - Add type hints, data models, error types
   - ~20-30 minutes

3. **Dependency Validation** (Required before implementation)
   - Use service-dependency-analyzer to validate architecture
   - Verify no issues before TDD begins
   - ~5 minutes

Would you like me to proceed with library evaluation for AuthService and
EmailService? Or skip to interface design?
```

---

### User Follow-Up

```
User: "Yes, let's do library evaluation next. Focus on AuthService."
```

---

### Claude Response

```
Claude: Perfect! I'll launch the service-library-finder subagent to evaluate
authentication libraries for AuthService.

**Search Criteria**:
- Must-have: Password hashing, JWT tokens, session management
- Platform: Python (FastAPI compatible)
- Quality: Active maintenance, good documentation, type hints
- Target: PyPI packages

Launching service-library-finder subagent...

[Session continues with library evaluation - see subagent-library-evaluation.md example]
```

---

## Key Takeaways

### Framework Enforcement

1. **Spec-First Approach**: No code written yet, only specifications
2. **Service-Oriented Architecture**: Enforced through subagent extraction
3. **Quality Gates**: Dependency limits, cycle detection, SRP validation
4. **Traceability**: Bidirectional UC-Service references created

### Subagent Value

- **Automation**: 8 minutes vs. 2+ hours manual analysis
- **Consistency**: Follows template structure perfectly
- **Quality**: Validates architecture rules automatically
- **Comprehensive**: Analyzes all UCs, creates all specs, updates all files

### Quality Maintained

- Single Responsibility Principle enforced
- Minimal dependencies (max 2, target ≤3)
- No circular dependencies
- Complete traceability
- Layered architecture

### Time Saved

- **Manual service extraction**: 2-3 hours
- **With subagent**: 8 minutes
- **Time saved**: ~2.5 hours
- **Quality improvement**: Higher (no human errors)

---

## Files Created/Modified

**Created**:
- `services/auth-service/service-spec.md`
- `services/user-service/service-spec.md`
- `services/order-service/service-spec.md`
- `services/product-service/service-spec.md`
- `services/email-service/service-spec.md`
- `services/validation-service/service-spec.md`

**Modified**:
- `.claude/service-registry.md` (added 6 services)
- `specs/use-cases/UC-001-user-registration.md` (added Services Used)
- `specs/use-cases/UC-002-user-login.md` (added Services Used)
- `specs/use-cases/UC-003-create-order.md` (added Services Used)
- `specs/use-cases/UC-004-view-order-history.md` (added Services Used)
- `specs/use-cases/UC-005-update-order-status.md` (added Services Used)

---

## Next Steps

**Immediate**:
- Library evaluation (service-library-finder)
- Interface design (service-designer)
- Dependency validation (service-dependency-analyzer)

**Then**:
- TDD implementation (Layer 1 services first)
- Integration tests
- API endpoint implementation

**Session End**: Framework principles maintained, quality assured, ready for next phase ✅
