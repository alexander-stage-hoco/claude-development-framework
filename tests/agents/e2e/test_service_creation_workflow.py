"""End-to-end tests for service creation workflow.

Tests the workflow for service-oriented development:
1. UC identifies required services
2. Service specifications created
3. Service interfaces designed
4. Service tests written
5. Service implementation
6. Service registry updated
7. Service reuse across UCs

Test Coverage:
- Service identification from UCs
- Service specification workflow
- Service interface design
- Service dependency management
- Service testing strategy
- Service registry maintenance
- Cross-UC service reuse
"""

import pytest
from pathlib import Path
from typing import Dict, Any

from tests.agents.fixtures import MockFileSystem


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_fs(tmp_path: Path) -> MockFileSystem:
    """Mock file system for testing."""
    return MockFileSystem(tmp_path)


# ============================================================================
# Test: Service Identification and Specification
# ============================================================================

@pytest.mark.e2e
def test_uc_identifies_required_services(mock_fs: MockFileSystem):
    """Test that UC clearly identifies required services."""
    uc_content = """---
id: UC-300
title: User Registration
---

# UC-300: User Registration

## Services Used
| Service | Methods | Purpose |
|---------|---------|---------|
| UserService | create_user() | User creation and validation |
| EmailService | send_welcome_email() | Welcome email delivery |
| AuthService | create_session() | Session management |

## Service Dependencies
- UserService → EmailService (sends welcome email after creation)
- UserService → AuthService (creates session after registration)

## New Services Required
- ❌ UserService (new, needs specification)
- ✅ EmailService (exists, reuse)
- ✅ AuthService (exists, reuse)
"""

    path = mock_fs.create_file("specs/use-cases/UC-300.md", uc_content)
    uc = mock_fs.read_file(path)

    # Verify service identification
    assert "## Services Used" in uc
    assert "UserService" in uc
    assert "EmailService" in uc
    assert "AuthService" in uc
    assert "Service Dependencies" in uc
    assert "New Services Required" in uc


@pytest.mark.e2e
def test_service_specification_created_from_uc(mock_fs: MockFileSystem):
    """Test that service specification is created from UC requirements."""
    # UC identifies service need
    uc = """---
id: UC-301
---
# UC-301: Product Search

## Services Used
| Service | Methods | Purpose |
|---------|---------|---------|
| SearchService | search(), filter() | Product search and filtering |
"""

    # Service specification created
    service_spec = """---
service_id: SVC-010
service_name: SearchService
created_for: UC-301
status: Draft
---

# SearchService Specification

## Purpose
Provide product search and filtering capabilities.

## Interface

### search(query: str, options: SearchOptions) -> SearchResult
Search products by query string.

**Specification**: UC-301#search
**Parameters**:
- query: Search query string
- options: Search configuration (pagination, sort)

**Returns**: SearchResult with matched products

**Exceptions**:
- InvalidQueryError: Query is empty or malformed

### filter(products: List[Product], filters: Dict[str, Any]) -> List[Product]
Filter products by criteria.

**Specification**: UC-301#filter
**Parameters**:
- products: Product list to filter
- filters: Filter criteria (price, category, etc.)

**Returns**: Filtered product list

## Dependencies
| Service | Usage |
|---------|-------|
| ProductService | Fetch product data |
| CacheService | Cache search results |

## Architecture
**ADR-003**: Repository Pattern (uses ProductRepository)
**ADR-001**: Type hints required
**ADR-002**: pytest for testing
"""

    uc_path = mock_fs.create_file("specs/use-cases/UC-301.md", uc)
    spec_path = mock_fs.create_file("specs/services/SVC-010-search-service.md", service_spec)

    uc_content = mock_fs.read_file(uc_path)
    spec_content = mock_fs.read_file(spec_path)

    # Verify specification quality
    assert "service_id: SVC-010" in spec_content
    assert "created_for: UC-301" in spec_content
    assert "## Interface" in spec_content
    assert "## Dependencies" in spec_content
    assert "## Architecture" in spec_content
    assert "Specification" in spec_content and "UC-301" in spec_content


@pytest.mark.e2e
def test_service_interface_uses_type_hints(mock_fs: MockFileSystem):
    """Test that service interfaces use type hints (ADR-001)."""
    service_interface = """\"\"\"Payment service interface.

Architecture: ADR-001 Type Hints Required
Specification: SVC-020
\"\"\"
from typing import Dict, Any, Optional
from decimal import Decimal


class PaymentService:
    \"\"\"Service for payment processing.

    Architecture: ADR-003 Service Layer
    Specification: UC-310 Payment Processing
    \"\"\"

    def process_payment(
        self,
        amount: Decimal,
        payment_method: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        \"\"\"Process payment.

        Specification: UC-310#process-payment

        Args:
            amount: Payment amount
            payment_method: Payment method (card, paypal, etc.)
            metadata: Optional payment metadata

        Returns:
            Payment result with transaction ID

        Raises:
            PaymentError: Payment processing failed
        \"\"\"
        pass

    def refund_payment(
        self,
        transaction_id: str,
        amount: Optional[Decimal] = None
    ) -> Dict[str, Any]:
        \"\"\"Refund payment.

        Specification: UC-311#refund

        Args:
            transaction_id: Original transaction ID
            amount: Refund amount (None for full refund)

        Returns:
            Refund result with refund ID
        \"\"\"
        pass
"""

    path = mock_fs.create_file("src/services/payment_service.py", service_interface)
    impl = mock_fs.read_file(path)

    # Verify type hints (ADR-001)
    assert "from typing import" in impl
    assert "amount: Decimal" in impl
    assert "-> Dict[str, Any]:" in impl
    assert "Architecture: ADR-001" in impl


@pytest.mark.e2e
def test_service_tests_created_before_implementation(mock_fs: MockFileSystem):
    """Test that service tests are created before implementation (TDD)."""
    # Service specification
    spec = """---
service_id: SVC-030
service_name: NotificationService
---

## Interface
### send_notification(user_id: int, message: str) -> bool
"""

    # Tests created FIRST (RED state)
    tests = """\"\"\"Tests for NotificationService.

Specification: SVC-030
Architecture: ADR-002 pytest Required
\"\"\"
import pytest
from unittest.mock import Mock
from src.services.notification_service import NotificationService


@pytest.fixture
def mock_email_client() -> Mock:
    return Mock()


@pytest.fixture
def notification_service(mock_email_client: Mock) -> NotificationService:
    return NotificationService(email_client=mock_email_client)


def test_send_notification_success(notification_service: NotificationService) -> None:
    \"\"\"Test successful notification send.

    Specification: SVC-030#send-notification
    \"\"\"
    # Arrange
    user_id = 123
    message = "Test notification"

    # Act
    result = notification_service.send_notification(user_id, message)

    # Assert
    assert result is True


def test_send_notification_validates_user_id(notification_service: NotificationService) -> None:
    \"\"\"Test notification validates user ID.

    Specification: SVC-030#validation
    \"\"\"
    # Arrange
    invalid_user_id = -1

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid user ID"):
        notification_service.send_notification(invalid_user_id, "Test")
"""

    # Implementation created AFTER tests (GREEN state)
    impl = """\"\"\"Notification service implementation.

Architecture: ADR-001 Type Hints Required
Specification: SVC-030
\"\"\"
from typing import Optional


class NotificationService:
    \"\"\"Service for sending notifications.

    Specification: SVC-030
    \"\"\"

    def __init__(self, email_client):
        self.email_client = email_client

    def send_notification(self, user_id: int, message: str) -> bool:
        \"\"\"Send notification to user.

        Specification: SVC-030#send-notification

        Args:
            user_id: User ID
            message: Notification message

        Returns:
            True if sent successfully

        Raises:
            ValueError: Invalid user ID
        \"\"\"
        if user_id < 0:
            raise ValueError("Invalid user ID")

        # Send notification
        self.email_client.send(user_id, message)
        return True
"""

    spec_path = mock_fs.create_file("specs/services/SVC-030.md", spec)
    test_path = mock_fs.create_file("tests/unit/services/test_notification_service.py", tests)
    impl_path = mock_fs.create_file("src/services/notification_service.py", impl)

    # Verify TDD workflow (tests before implementation)
    assert mock_fs.file_exists(spec_path)
    assert mock_fs.file_exists(test_path)
    assert mock_fs.file_exists(impl_path)

    test_content = mock_fs.read_file(test_path)
    impl_content = mock_fs.read_file(impl_path)

    # Tests reference specification
    assert "Specification: SVC-030" in test_content
    assert "Specification: SVC-030" in impl_content


@pytest.mark.e2e
def test_service_registry_tracks_all_services(mock_fs: MockFileSystem):
    """Test that service registry tracks all services."""
    registry = """# Service Registry

## Active Services

### SVC-010: SearchService
- **Specification**: specs/services/SVC-010-search-service.md
- **Implementation**: src/services/search_service.py
- **Tests**: tests/unit/services/test_search_service.py
- **Used By**: UC-301, UC-302, UC-303
- **Status**: Active
- **Version**: 1.0.0

### SVC-020: PaymentService
- **Specification**: specs/services/SVC-020-payment-service.md
- **Implementation**: src/services/payment_service.py
- **Tests**: tests/unit/services/test_payment_service.py
- **Used By**: UC-310, UC-311
- **Dependencies**: SVC-030 (NotificationService)
- **Status**: Active
- **Version**: 1.2.0

### SVC-030: NotificationService
- **Specification**: specs/services/SVC-030-notification-service.md
- **Implementation**: src/services/notification_service.py
- **Tests**: tests/unit/services/test_notification_service.py
- **Used By**: UC-300, UC-310, UC-320
- **Status**: Active
- **Version**: 2.0.0

## Service Dependencies

```
PaymentService (SVC-020)
  └─> NotificationService (SVC-030)

SearchService (SVC-010)
  └─> ProductService (SVC-015)
      └─> CacheService (SVC-005)
```

## Service Statistics
- Total services: 3
- Average reuse: 2.3 UCs per service
- Test coverage: 95% (all services)
"""

    path = mock_fs.create_file("specs/service-registry.md", registry)
    reg = mock_fs.read_file(path)

    # Verify registry completeness
    assert "# Service Registry" in reg
    assert "SVC-010" in reg
    assert "SVC-020" in reg
    assert "SVC-030" in reg
    assert "Used By" in reg
    assert "Dependencies" in reg
    assert "Service Statistics" in reg


@pytest.mark.e2e
def test_service_reused_across_multiple_ucs(mock_fs: MockFileSystem):
    """Test that services are reused across multiple UCs."""
    # UC 1 uses EmailService
    uc1 = """---
id: UC-320
---
# UC-320: User Registration

## Services Used
| Service | Methods | Purpose |
|---------|---------|---------|
| EmailService | send_welcome_email() | Welcome email |
"""

    # UC 2 also uses EmailService
    uc2 = """---
id: UC-321
---
# UC-321: Password Reset

## Services Used
| Service | Methods | Purpose |
|---------|---------|---------|
| EmailService | send_reset_email() | Password reset email |
"""

    # UC 3 also uses EmailService
    uc3 = """---
id: UC-322
---
# UC-322: Order Confirmation

## Services Used
| Service | Methods | Purpose |
|---------|---------|---------|
| EmailService | send_confirmation_email() | Order confirmation |
"""

    # EmailService serves all three UCs
    email_service = """\"\"\"Email service implementation.

Specification: SVC-040
Used By: UC-320, UC-321, UC-322
\"\"\"


class EmailService:
    \"\"\"Centralized email service for all UC email needs.

    Specification: SVC-040
    \"\"\"

    def send_welcome_email(self, user_id: int) -> bool:
        \"\"\"Send welcome email.

        Specification: UC-320#welcome-email
        \"\"\"
        pass

    def send_reset_email(self, user_id: int, reset_token: str) -> bool:
        \"\"\"Send password reset email.

        Specification: UC-321#reset-email
        \"\"\"
        pass

    def send_confirmation_email(self, order_id: int) -> bool:
        \"\"\"Send order confirmation email.

        Specification: UC-322#confirmation-email
        \"\"\"
        pass
"""

    mock_fs.create_file("specs/use-cases/UC-320.md", uc1)
    mock_fs.create_file("specs/use-cases/UC-321.md", uc2)
    mock_fs.create_file("specs/use-cases/UC-322.md", uc3)
    service_path = mock_fs.create_file("src/services/email_service.py", email_service)

    service = mock_fs.read_file(service_path)

    # Verify service reuse
    assert "Used By: UC-320, UC-321, UC-322" in service
    assert "send_welcome_email" in service
    assert "send_reset_email" in service
    assert "send_confirmation_email" in service


@pytest.mark.e2e
def test_service_versioning_tracked(mock_fs: MockFileSystem):
    """Test that service versions are tracked."""
    service_changelog = """# EmailService Changelog

## Version 2.0.0 (2025-10-03)
**Breaking Changes**:
- Changed send_email() signature: added `priority` parameter
- Removed deprecated send_html_email() (use send_email with html=True)

**Migration Guide**:
```python
# Before (v1.x)
service.send_email(to, subject, body)

# After (v2.0)
service.send_email(to, subject, body, priority="normal")
```

**UCs Updated**: UC-320, UC-321, UC-322

## Version 1.5.0 (2025-09-15)
**Features**:
- Added send_bulk_email() for batch sending
- Added email templates support

**UCs Using**: UC-330 (bulk notifications)

## Version 1.0.0 (2025-08-01)
**Initial Release**:
- send_email()
- send_html_email()

**UCs Using**: UC-300 (registration)
"""

    path = mock_fs.create_file("specs/services/email-service-changelog.md", service_changelog)
    changelog = mock_fs.read_file(path)

    # Verify versioning
    assert "Version 2.0.0" in changelog
    assert "Version 1.5.0" in changelog
    assert "Version 1.0.0" in changelog
    assert "Breaking Changes" in changelog
    assert "Migration Guide" in changelog
    assert "UCs Updated" in changelog


@pytest.mark.e2e
def test_service_dependencies_managed(mock_fs: MockFileSystem):
    """Test that service dependencies are properly managed."""
    # High-level service depends on lower-level services
    order_service = """\"\"\"Order service implementation.

Architecture: ADR-003 Service Layer
Specification: SVC-050
Dependencies: SVC-020 (PaymentService), SVC-030 (NotificationService), SVC-015 (ProductService)
\"\"\"
from typing import Dict, Any
from src.services.payment_service import PaymentService
from src.services.notification_service import NotificationService
from src.services.product_service import ProductService


class OrderService:
    \"\"\"Service for order management.

    Specification: SVC-050
    \"\"\"

    def __init__(
        self,
        payment_service: PaymentService,
        notification_service: NotificationService,
        product_service: ProductService
    ):
        \"\"\"Initialize order service.

        Dependencies:
        - SVC-020 (PaymentService): Process payments
        - SVC-030 (NotificationService): Send confirmations
        - SVC-015 (ProductService): Validate products
        \"\"\"
        self.payment_service = payment_service
        self.notification_service = notification_service
        self.product_service = product_service

    def create_order(self, user_id: int, items: list) -> Dict[str, Any]:
        \"\"\"Create order.

        Specification: UC-340#create-order

        Workflow:
        1. Validate products (ProductService)
        2. Process payment (PaymentService)
        3. Send confirmation (NotificationService)
        \"\"\"
        # Use injected dependencies
        self.product_service.validate(items)
        payment_result = self.payment_service.process_payment(...)
        self.notification_service.send_notification(user_id, "Order confirmed")
        return {"order_id": 123}
"""

    path = mock_fs.create_file("src/services/order_service.py", order_service)
    service = mock_fs.read_file(path)

    # Verify dependency management
    assert "Dependencies: SVC-020" in service
    assert "from src.services.payment_service import PaymentService" in service
    assert "payment_service: PaymentService" in service


@pytest.mark.e2e
def test_service_tests_use_mocks_for_dependencies(mock_fs: MockFileSystem):
    """Test that service tests mock dependencies."""
    service_tests = """\"\"\"Tests for OrderService.

Specification: SVC-050
\"\"\"
import pytest
from unittest.mock import Mock
from src.services.order_service import OrderService


@pytest.fixture
def mock_payment_service() -> Mock:
    \"\"\"Mock PaymentService dependency.\"\"\"
    service = Mock()
    service.process_payment.return_value = {"transaction_id": "txn_123"}
    return service


@pytest.fixture
def mock_notification_service() -> Mock:
    \"\"\"Mock NotificationService dependency.\"\"\"
    service = Mock()
    service.send_notification.return_value = True
    return service


@pytest.fixture
def mock_product_service() -> Mock:
    \"\"\"Mock ProductService dependency.\"\"\"
    service = Mock()
    service.validate.return_value = True
    return service


@pytest.fixture
def order_service(
    mock_payment_service: Mock,
    mock_notification_service: Mock,
    mock_product_service: Mock
) -> OrderService:
    \"\"\"OrderService with mocked dependencies.\"\"\"
    return OrderService(
        payment_service=mock_payment_service,
        notification_service=mock_notification_service,
        product_service=mock_product_service
    )


def test_create_order_calls_all_dependencies(order_service: OrderService) -> None:
    \"\"\"Test that create_order uses all injected services.

    Specification: SVC-050#create-order
    \"\"\"
    # Arrange
    user_id = 123
    items = [{"product_id": 1, "quantity": 2}]

    # Act
    result = order_service.create_order(user_id, items)

    # Assert
    order_service.product_service.validate.assert_called_once()
    order_service.payment_service.process_payment.assert_called_once()
    order_service.notification_service.send_notification.assert_called_once()
"""

    path = mock_fs.create_file("tests/unit/services/test_order_service.py", service_tests)
    tests = mock_fs.read_file(path)

    # Verify dependency mocking
    assert "@pytest.fixture" in tests
    assert "mock_payment_service" in tests
    assert "mock_notification_service" in tests
    assert "mock_product_service" in tests
    assert "Mock()" in tests


@pytest.mark.e2e
def test_service_interface_documented_in_spec(mock_fs: MockFileSystem):
    """Test that service interface is documented in specification."""
    service_spec = """---
service_id: SVC-060
service_name: CacheService
---

# CacheService Specification

## Interface Documentation

### set(key: str, value: Any, ttl: Optional[int] = None) -> bool
Store value in cache.

**Parameters**:
- `key`: Cache key (must be non-empty string)
- `value`: Value to cache (serializable)
- `ttl`: Time-to-live in seconds (None = no expiration)

**Returns**: True if stored successfully

**Exceptions**:
- `ValueError`: Invalid key or value
- `CacheError`: Cache storage failed

**Example**:
```python
cache.set("user:123", {"name": "John"}, ttl=3600)
```

### get(key: str) -> Optional[Any]
Retrieve value from cache.

**Parameters**:
- `key`: Cache key

**Returns**: Cached value or None if not found/expired

**Example**:
```python
user = cache.get("user:123")
if user is None:
    user = db.fetch_user(123)
    cache.set("user:123", user)
```

### delete(key: str) -> bool
Remove key from cache.

**Parameters**:
- `key`: Cache key

**Returns**: True if key was deleted

### clear() -> None
Clear entire cache.

**Warning**: Use with caution in production.

## Implementation Notes
- Use Redis for distributed caching
- Serialize with JSON for compatibility
- Handle connection failures gracefully
"""

    path = mock_fs.create_file("specs/services/SVC-060-cache-service.md", service_spec)
    spec = mock_fs.read_file(path)

    # Verify interface documentation
    assert "## Interface Documentation" in spec
    assert "**Parameters**:" in spec
    assert "**Returns**:" in spec
    assert "**Exceptions**:" in spec
    assert "**Example**:" in spec


@pytest.mark.e2e
def test_service_creation_workflow_complete(mock_fs: MockFileSystem):
    """Test complete service creation workflow end-to-end."""
    # Step 1: UC identifies service need
    uc = """---
id: UC-350
---
## Services Used
| Service | Methods | Purpose |
|---------|---------|---------|
| AnalyticsService | track_event() | Event tracking |

## New Services Required
- ❌ AnalyticsService (new)
"""

    # Step 2: Service specification created
    spec = """---
service_id: SVC-070
service_name: AnalyticsService
created_for: UC-350
---
## Interface
### track_event(event_name: str, properties: dict) -> bool
"""

    # Step 3: Service tests created (RED)
    tests = """\"\"\"Tests for AnalyticsService.

Specification: SVC-070
\"\"\"
def test_track_event():
    assert False  # RED state
"""

    # Step 4: Service implementation (GREEN)
    impl = """\"\"\"AnalyticsService implementation.

Specification: SVC-070
\"\"\"
def track_event(event_name: str, properties: dict) -> bool:
    return True  # GREEN state
"""

    # Step 5: Service registry updated
    registry = """# Service Registry

### SVC-070: AnalyticsService
- **Specification**: specs/services/SVC-070.md
- **Implementation**: src/services/analytics_service.py
- **Tests**: tests/unit/services/test_analytics_service.py
- **Used By**: UC-350
- **Status**: Active
"""

    # Create all artifacts
    mock_fs.create_file("specs/use-cases/UC-350.md", uc)
    mock_fs.create_file("specs/services/SVC-070.md", spec)
    mock_fs.create_file("tests/unit/services/test_analytics_service.py", tests)
    mock_fs.create_file("src/services/analytics_service.py", impl)
    mock_fs.create_file("specs/service-registry.md", registry)

    # Verify complete workflow
    assert mock_fs.file_exists("specs/use-cases/UC-350.md")
    assert mock_fs.file_exists("specs/services/SVC-070.md")
    assert mock_fs.file_exists("tests/unit/services/test_analytics_service.py")
    assert mock_fs.file_exists("src/services/analytics_service.py")
    assert mock_fs.file_exists("specs/service-registry.md")

    # Verify traceability
    assert "UC-350" in mock_fs.read_file("specs/use-cases/UC-350.md")
    assert "SVC-070" in mock_fs.read_file("specs/services/SVC-070.md")
    assert "SVC-070" in mock_fs.read_file("tests/unit/services/test_analytics_service.py")
    assert "SVC-070" in mock_fs.read_file("src/services/analytics_service.py")
    assert "SVC-070" in mock_fs.read_file("specs/service-registry.md")


@pytest.mark.e2e
def test_service_error_handling_specified(mock_fs: MockFileSystem):
    """Test that service error handling is specified."""
    service_spec = """---
service_id: SVC-080
---

## Error Handling

### Exception Hierarchy
```
ServiceError (base)
  ├─> ValidationError (invalid input)
  ├─> NotFoundError (resource not found)
  ├─> ConflictError (duplicate/conflict)
  └─> ExternalServiceError (external API failure)
```

### Error Scenarios

#### Error: Invalid Input
**Trigger**: User provides invalid data
**Exception**: ValidationError
**HTTP Status**: 400 Bad Request
**Example**:
```python
raise ValidationError("Email format invalid")
```

#### Error: Resource Not Found
**Trigger**: Requested resource doesn't exist
**Exception**: NotFoundError
**HTTP Status**: 404 Not Found
**Example**:
```python
raise NotFoundError(f"User {user_id} not found")
```

### Retry Strategy
- **Network Errors**: Retry 3 times with exponential backoff
- **Rate Limits**: Retry after rate limit reset
- **Server Errors (5xx)**: Retry 2 times
- **Client Errors (4xx)**: Do NOT retry
"""

    path = mock_fs.create_file("specs/services/SVC-080.md", service_spec)
    spec = mock_fs.read_file(path)

    # Verify error handling specification
    assert "## Error Handling" in spec
    assert "Exception Hierarchy" in spec
    assert "Error Scenarios" in spec
    assert "Retry Strategy" in spec
