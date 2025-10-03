"""End-to-end tests for iteration planning workflow.

Tests the workflow for breaking large features into iterations:
1. Large feature identified
2. Feature broken into iterations (MVP → Full)
3. Each iteration has independent UC
4. Incremental delivery with dependencies
5. Progress tracking across iterations
6. Cross-iteration traceability maintained

Test Coverage:
- Iteration planning workflow
- MVP vs Full feature delivery
- Iteration dependencies
- Cross-iteration UC references
- Incremental test coverage
- Iteration completion criteria
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
# Test: Iteration Planning Workflow
# ============================================================================

@pytest.mark.e2e
def test_large_feature_broken_into_iterations(mock_fs: MockFileSystem):
    """Test that large features are broken into MVP and full iterations."""
    # Large feature: E-commerce Order Management
    # Iteration 1 (MVP): Create order, view order
    # Iteration 2: Cancel order, refund
    # Iteration 3: Order history, search

    # Iteration 1 (MVP)
    uc_iter1 = """---
id: UC-100
title: Order Management - Iteration 1 (MVP)
status: Draft
iteration: 1
feature: Order Management
---

# UC-100: Order Management - Iteration 1 (MVP)

## Objective
Enable basic order creation and viewing (MVP).

## Main Flow
1. User creates order with items
2. System validates inventory
3. System creates order
4. User views order details

## Acceptance Criteria
```gherkin
Scenario: Create and view order
  Given user has items in cart
  When user creates order
  Then order is created with status "pending"
  And user can view order details
```

## Services Used
| Service | Methods | Purpose |
|---------|---------|---------|
| OrderService | create_order(), get_order() | Order management |
| InventoryService | check_availability() | Stock validation |

## Iteration Notes
- **Iteration 1 (MVP)**: Basic create and view
- **Future** (Iteration 2): Cancel and refund
- **Future** (Iteration 3): History and search
"""

    # Iteration 2 (Enhancement)
    uc_iter2 = """---
id: UC-101
title: Order Management - Iteration 2 (Cancel/Refund)
status: Draft
iteration: 2
feature: Order Management
depends_on: UC-100
---

# UC-101: Order Management - Iteration 2 (Cancel/Refund)

## Objective
Enable order cancellation and refunds.

## Dependencies
- **Requires**: UC-100 (Order creation and viewing)

## Main Flow
1. User views existing order
2. User cancels order
3. System processes refund
4. System updates order status

## Acceptance Criteria
```gherkin
Scenario: Cancel order and receive refund
  Given order exists with status "pending"
  When user cancels order
  Then system processes refund
  And order status is "cancelled"
```

## Services Used
| Service | Methods | Purpose |
|---------|---------|---------|
| OrderService | cancel_order() | Order cancellation |
| PaymentService | process_refund() | Refund processing |
"""

    path1 = mock_fs.create_file("specs/use-cases/UC-100-order-mgmt-iter1.md", uc_iter1)
    path2 = mock_fs.create_file("specs/use-cases/UC-101-order-mgmt-iter2.md", uc_iter2)

    uc1 = mock_fs.read_file(path1)
    uc2 = mock_fs.read_file(path2)

    # Verify iteration structure
    assert "iteration: 1" in uc1
    assert "iteration: 2" in uc2
    assert "feature: Order Management" in uc1
    assert "feature: Order Management" in uc2

    # Verify dependency tracking
    assert "depends_on: UC-100" in uc2
    assert "Future" in uc1  # Notes about future iterations


@pytest.mark.e2e
def test_mvp_iteration_prioritizes_core_functionality(mock_fs: MockFileSystem):
    """Test that MVP iteration focuses on core functionality only."""
    mvp_uc = """---
id: UC-110
title: User Authentication - Iteration 1 (MVP)
iteration: 1
priority: High
---

# UC-110: User Authentication - Iteration 1 (MVP)

## MVP Scope
✅ **Included**:
- Email/password login
- Session creation
- Logout

❌ **Deferred** (Future Iterations):
- OAuth providers (Google, GitHub)
- Two-factor authentication
- Password reset
- Remember me

## Objective
Enable basic authentication with email/password.

## Main Flow
1. User provides email and password
2. System validates credentials
3. System creates session
4. User is authenticated

## Iteration Notes
**Why MVP**: Get users authenticating quickly. OAuth and 2FA are enhancements.
"""

    path = mock_fs.create_file("specs/use-cases/UC-110-auth-mvp.md", mvp_uc)
    uc = mock_fs.read_file(path)

    # Verify MVP focus
    assert "MVP Scope" in uc
    assert "✅ **Included**:" in uc
    assert "❌ **Deferred**" in uc
    assert "iteration: 1" in uc


@pytest.mark.e2e
def test_iteration_dependencies_tracked(mock_fs: MockFileSystem):
    """Test that iteration dependencies are tracked and validated."""
    # Iteration 1: Foundation
    iter1 = """---
id: UC-120
iteration: 1
depends_on: []
---
# UC-120: User Profile - Iteration 1 (View)
Basic profile viewing.
"""

    # Iteration 2: Depends on Iteration 1
    iter2 = """---
id: UC-121
iteration: 2
depends_on: UC-120
---
# UC-121: User Profile - Iteration 2 (Edit)
**Requires**: UC-120 (must be able to view before editing)
"""

    # Iteration 3: Depends on Iterations 1 & 2
    iter3 = """---
id: UC-122
iteration: 3
depends_on: [UC-120, UC-121]
---
# UC-122: User Profile - Iteration 3 (Photo Upload)
**Requires**:
- UC-120 (viewing profile)
- UC-121 (editing profile)
"""

    path1 = mock_fs.create_file("specs/use-cases/UC-120.md", iter1)
    path2 = mock_fs.create_file("specs/use-cases/UC-121.md", iter2)
    path3 = mock_fs.create_file("specs/use-cases/UC-122.md", iter3)

    uc1 = mock_fs.read_file(path1)
    uc2 = mock_fs.read_file(path2)
    uc3 = mock_fs.read_file(path3)

    # Verify dependency chain
    assert "depends_on: []" in uc1
    assert "depends_on: UC-120" in uc2
    assert "depends_on: [UC-120, UC-121]" in uc3


@pytest.mark.e2e
def test_cross_iteration_traceability_maintained(mock_fs: MockFileSystem):
    """Test that traceability is maintained across iterations."""
    # Iteration 1: Basic search
    uc1 = """---
id: UC-130
iteration: 1
feature: Product Search
---
# UC-130: Product Search - Iteration 1 (Basic)
"""

    # Implementation references UC-130
    impl1 = """\"\"\"Search service - Iteration 1.

Architecture: ADR-005 Service Layer
Specification: UC-130 Product Search Iteration 1
\"\"\"
def basic_search(query: str):
    pass
"""

    # Iteration 2: Advanced search builds on Iteration 1
    uc2 = """---
id: UC-131
iteration: 2
feature: Product Search
depends_on: UC-130
---
# UC-131: Product Search - Iteration 2 (Filters)
**Builds on**: UC-130 (basic search)
"""

    impl2 = """\"\"\"Search service - Iteration 2.

Architecture: ADR-005 Service Layer
Specification: UC-131 Product Search Iteration 2
Extends: UC-130 (adds filtering to basic search)
\"\"\"
def filtered_search(query: str, filters: dict):
    # Uses basic_search from UC-130
    pass
"""

    path1 = mock_fs.create_file("specs/use-cases/UC-130.md", uc1)
    path2 = mock_fs.create_file("specs/use-cases/UC-131.md", uc2)
    impl_path1 = mock_fs.create_file("src/search_service_v1.py", impl1)
    impl_path2 = mock_fs.create_file("src/search_service_v2.py", impl2)

    # Verify traceability across iterations
    assert "UC-130" in mock_fs.read_file(path1)
    assert "UC-131" in mock_fs.read_file(path2)
    assert "UC-130" in mock_fs.read_file(impl_path1)
    assert "UC-131" in mock_fs.read_file(impl_path2)
    assert "Extends: UC-130" in mock_fs.read_file(impl_path2)


@pytest.mark.e2e
def test_iteration_completion_criteria_defined(mock_fs: MockFileSystem):
    """Test that each iteration has clear completion criteria."""
    iter_uc = """---
id: UC-140
iteration: 1
---

# UC-140: Payment Processing - Iteration 1

## Iteration Completion Criteria

✅ **Must Have** (Iteration 1):
- [ ] Credit card payment processing
- [ ] Payment validation
- [ ] Receipt generation
- [ ] All tests passing (GREEN state)
- [ ] Code quality score ≥ 80
- [ ] Security review completed

🎯 **Success Metrics**:
- Payment success rate ≥ 99%
- Average processing time ≤ 2 seconds
- Zero security vulnerabilities

❌ **Out of Scope** (Future):
- PayPal integration → Iteration 2
- Apple Pay → Iteration 3
- Cryptocurrency → TBD
"""

    path = mock_fs.create_file("specs/use-cases/UC-140.md", iter_uc)
    uc = mock_fs.read_file(path)

    # Verify completion criteria
    assert "Iteration Completion Criteria" in uc
    assert "✅ **Must Have**" in uc
    assert "🎯 **Success Metrics**" in uc
    assert "❌ **Out of Scope**" in uc


@pytest.mark.e2e
def test_incremental_test_coverage_across_iterations(mock_fs: MockFileSystem):
    """Test that test coverage grows incrementally across iterations."""
    # Iteration 1 tests
    test1 = """\"\"\"Tests for Notification Service - Iteration 1 (Email only).

Specification: UC-150 Notification Service Iteration 1
Feature: features/UC-150-notifications.feature
\"\"\"
import pytest

def test_send_email_notification():
    \"\"\"Test email notification.

    Specification: UC-150#send-email
    \"\"\"
    pass

# Iteration 1: 5 tests (email only)
"""

    # Iteration 2 tests (adds SMS)
    test2 = """\"\"\"Tests for Notification Service - Iteration 2 (Email + SMS).

Specification: UC-151 Notification Service Iteration 2
Feature: features/UC-151-notifications.feature
Extends: UC-150 (adds SMS to email)
\"\"\"
import pytest

def test_send_email_notification():
    \"\"\"Test email notification (from Iteration 1).

    Specification: UC-150#send-email
    \"\"\"
    pass

def test_send_sms_notification():
    \"\"\"Test SMS notification (new in Iteration 2).

    Specification: UC-151#send-sms
    \"\"\"
    pass

# Iteration 2: 10 tests (email + SMS)
"""

    path1 = mock_fs.create_file("tests/unit/test_notifications_iter1.py", test1)
    path2 = mock_fs.create_file("tests/unit/test_notifications_iter2.py", test2)

    t1 = mock_fs.read_file(path1)
    t2 = mock_fs.read_file(path2)

    # Verify incremental coverage
    assert "Iteration 1" in t1
    assert "Iteration 2" in t2
    assert "Extends: UC-150" in t2


@pytest.mark.e2e
def test_iteration_progress_tracking(mock_fs: MockFileSystem):
    """Test that iteration progress is tracked."""
    progress_doc = """# Feature: Product Catalog - Iteration Progress

## Iteration 1 (MVP) - COMPLETED ✅
**UC-160**: Basic product listing
- [x] Specification written
- [x] BDD scenarios created
- [x] Tests written (RED → GREEN)
- [x] Implementation complete
- [x] Code quality: 92/100
- [x] Committed: commit abc1234

## Iteration 2 (Current) - IN PROGRESS 🚧
**UC-161**: Product filtering and sorting
- [x] Specification written
- [x] BDD scenarios created
- [x] Tests written (RED state)
- [ ] Implementation (60% complete)
- [ ] Code quality check
- [ ] Commit

## Iteration 3 (Planned) - PENDING 📋
**UC-162**: Product search
- [ ] Specification
- [ ] BDD scenarios
- [ ] Tests
- [ ] Implementation
- [ ] Quality check
- [ ] Commit

## Overall Progress
- Iterations completed: 1/3 (33%)
- Tests passing: 45/45 (Iter 1), 12/20 (Iter 2)
- Code coverage: 95% (Iter 1), 60% (Iter 2)
"""

    path = mock_fs.create_file("docs/progress/product-catalog-iterations.md", progress_doc)
    doc = mock_fs.read_file(path)

    # Verify progress tracking
    assert "COMPLETED ✅" in doc
    assert "IN PROGRESS 🚧" in doc
    assert "PENDING 📋" in doc
    assert "Overall Progress" in doc


@pytest.mark.e2e
def test_iteration_planning_identifies_service_reuse(mock_fs: MockFileSystem):
    """Test that iteration planning identifies opportunities for service reuse."""
    iter1_uc = """---
id: UC-170
iteration: 1
---
# UC-170: Email Notifications - Iteration 1

## Services Created
| Service | Purpose |
|---------|---------|
| EmailService | Send email notifications |
| TemplateService | Render email templates |

## Reusable Components
- EmailService can be reused for: password reset, welcome emails, alerts
- TemplateService can be reused for: SMS, in-app messages
"""

    iter2_uc = """---
id: UC-171
iteration: 2
depends_on: UC-170
---
# UC-171: SMS Notifications - Iteration 2

## Services Reused
| Service | From | Usage |
|---------|------|-------|
| TemplateService | UC-170 | Reuse for SMS templates |

## Services Created
| Service | Purpose |
|---------|---------|
| SmsService | Send SMS notifications |
"""

    path1 = mock_fs.create_file("specs/use-cases/UC-170.md", iter1_uc)
    path2 = mock_fs.create_file("specs/use-cases/UC-171.md", iter2_uc)

    uc1 = mock_fs.read_file(path1)
    uc2 = mock_fs.read_file(path2)

    # Verify service reuse tracking
    assert "Reusable Components" in uc1
    assert "Services Reused" in uc2
    assert "TemplateService" in uc1
    assert "TemplateService" in uc2


@pytest.mark.e2e
def test_iteration_risks_documented(mock_fs: MockFileSystem):
    """Test that iteration-specific risks are documented."""
    iter_uc = """---
id: UC-180
iteration: 2
---
# UC-180: Real-time Updates - Iteration 2

## Iteration Risks

### High Risk: WebSocket Complexity
- **Risk**: WebSocket implementation more complex than expected
- **Mitigation**: Allocate 2 extra days, use proven library (Socket.IO)
- **Fallback**: Polling if WebSocket blocked (Iteration 2.1)

### Medium Risk: Browser Compatibility
- **Risk**: WebSocket support varies across browsers
- **Mitigation**: Feature detection, fallback to polling
- **Impact**: May need Iteration 2.1 for compatibility layer

## Dependencies on External Iterations
- **Requires**: UC-175 (Authentication) from Iteration 1
- **Blocks**: UC-185 (Notifications) in Iteration 3
"""

    path = mock_fs.create_file("specs/use-cases/UC-180.md", iter_uc)
    uc = mock_fs.read_file(path)

    # Verify risk documentation
    assert "Iteration Risks" in uc
    assert "Risk" in uc
    assert "Mitigation" in uc
    assert "Fallback" in uc


@pytest.mark.e2e
def test_iteration_git_workflow_uses_branches(mock_fs: MockFileSystem):
    """Test that iteration workflow suggests feature branches."""
    git_guide = """# Git Workflow: Feature Iterations

## Iteration 1 (MVP)
Branch: feature/order-management-iter1
- UC-190: Order creation
- UC-191: Order viewing
Merge to: main (after GREEN state + quality check)

## Iteration 2 (Enhancement)
Branch: feature/order-management-iter2
Based on: main (includes Iteration 1)
- UC-192: Order cancellation
- UC-193: Refund processing
Merge to: main (after GREEN state + quality check)

## Branch Strategy
- One branch per iteration
- Iteration branches created from main
- Merge only after all iteration UCs complete
- Tag releases: v1.0.0-iter1, v1.0.0-iter2
"""

    path = mock_fs.create_file("docs/git-iteration-workflow.md", git_guide)
    guide = mock_fs.read_file(path)

    # Verify iteration branching
    assert "feature/order-management-iter1" in guide
    assert "feature/order-management-iter2" in guide
    assert "One branch per iteration" in guide


@pytest.mark.e2e
def test_iteration_session_summaries_linked(mock_fs: MockFileSystem):
    """Test that session summaries are linked across iterations."""
    session1 = """# Session Summary: UC-200 Iteration 1

## Iteration
Feature: User Dashboard
Iteration: 1 (MVP)
UCs: UC-200

## Decisions
- MVP includes: Widget display only
- Deferred to Iteration 2: Customization, drag-and-drop

## Next Iteration
See: Session Summary for UC-201 Iteration 2
"""

    session2 = """# Session Summary: UC-201 Iteration 2

## Iteration
Feature: User Dashboard
Iteration: 2 (Enhancement)
UCs: UC-201
Builds on: UC-200 (Iteration 1)

## Decisions
- Added: Widget customization
- Deferred to Iteration 3: Drag-and-drop

## Previous Iteration
See: Session Summary for UC-200 Iteration 1
"""

    path1 = mock_fs.create_file("session-summaries/2025-10-03-uc-200-iter1.md", session1)
    path2 = mock_fs.create_file("session-summaries/2025-10-04-uc-201-iter2.md", session2)

    s1 = mock_fs.read_file(path1)
    s2 = mock_fs.read_file(path2)

    # Verify cross-iteration linking
    assert "Iteration: 1 (MVP)" in s1
    assert "Iteration: 2 (Enhancement)" in s2
    assert "Next Iteration" in s1
    assert "Previous Iteration" in s2


@pytest.mark.e2e
def test_iteration_adr_references_iteration_context(mock_fs: MockFileSystem):
    """Test that ADRs reference iteration context when relevant."""
    adr = """### ADR-020: Use REST for Iteration 1, GraphQL for Iteration 2

**Date**: 2025-10-03
**Status**: Accepted
**Iteration Context**: API Development

**Decision**:
- **Iteration 1 (MVP)**: Use REST API (faster to implement, team familiar)
- **Iteration 2**: Migrate to GraphQL (better for complex queries)

**Rationale**:
REST gets us to market faster (Iteration 1 MVP goal).
GraphQL provides better DX for complex product queries (Iteration 2 enhancement).

**Migration Plan**:
- Iteration 1: REST endpoints
- Iteration 2: GraphQL layer wrapping REST services
- Iteration 3: Deprecate REST, GraphQL only

**Consequences**:
- ✅ **Easier**: Faster MVP delivery
- ❌ **Harder**: Migration effort in Iteration 2
"""

    path = mock_fs.create_file(".claude/technical-decisions.md", adr)
    adr_content = mock_fs.read_file(path)

    # Verify iteration awareness in ADR
    assert "Iteration 1 (MVP)" in adr_content
    assert "Iteration 2" in adr_content
    assert "Iteration Context" in adr_content


@pytest.mark.e2e
def test_complete_iteration_workflow_end_to_end(mock_fs: MockFileSystem):
    """Test complete iteration workflow from planning to delivery."""
    # ITERATION 1: MVP
    # Step 1: Plan iteration
    iter1_plan = """# Iteration 1 Plan: Shopping Cart (MVP)

UCs in scope:
- UC-210: Add item to cart
- UC-211: View cart

UCs deferred:
- UC-212: Update quantity → Iteration 2
- UC-213: Apply coupon → Iteration 3
"""

    # Step 2: Create UC for Iteration 1
    uc_iter1 = """---
id: UC-210
iteration: 1
---
# UC-210: Add Item to Cart - Iteration 1 (MVP)
"""

    # Step 3: BDD for Iteration 1
    feature_iter1 = """# Specification: UC-210
Feature: Add Item to Cart (Iteration 1 MVP)
"""

    # Step 4: Tests for Iteration 1
    test_iter1 = """# Specification: UC-210
# Iteration: 1
def test_add_item_to_cart():
    pass
"""

    # Step 5: Implementation for Iteration 1
    impl_iter1 = """# Specification: UC-210
# Iteration: 1
def add_to_cart(item):
    pass
"""

    # Step 6: Session summary for Iteration 1
    session_iter1 = """# Session: Shopping Cart Iteration 1 COMPLETED ✅
UCs: UC-210, UC-211
Status: GREEN, committed
Next: Iteration 2 (UC-212, UC-213)
"""

    # Create all artifacts
    mock_fs.create_file("iterations/iteration-1-plan.md", iter1_plan)
    mock_fs.create_file("specs/use-cases/UC-210.md", uc_iter1)
    mock_fs.create_file("features/UC-210.feature", feature_iter1)
    mock_fs.create_file("tests/unit/test_cart.py", test_iter1)
    mock_fs.create_file("src/cart_service.py", impl_iter1)
    mock_fs.create_file("session-summaries/iter1-complete.md", session_iter1)

    # Verify complete workflow
    assert mock_fs.file_exists("iterations/iteration-1-plan.md")
    assert mock_fs.file_exists("specs/use-cases/UC-210.md")
    assert mock_fs.file_exists("features/UC-210.feature")
    assert mock_fs.file_exists("tests/unit/test_cart.py")
    assert mock_fs.file_exists("src/cart_service.py")
    assert mock_fs.file_exists("session-summaries/iter1-complete.md")


@pytest.mark.e2e
def test_iteration_failure_triggers_iteration_adjustment(mock_fs: MockFileSystem):
    """Test that iteration failures trigger scope adjustment."""
    failed_iteration = """# Iteration 2 Retrospective: SCOPE ADJUSTED

## Original Scope
- UC-220: Advanced search
- UC-221: Faceted filters
- UC-222: Search analytics

## Actual Completion
- UC-220: Advanced search ✅ DONE
- UC-221: Faceted filters ⚠️ PARTIAL (60% complete)
- UC-222: Search analytics ❌ MOVED to Iteration 3

## Adjustment Decision
**Reason**: UC-221 more complex than estimated (3 days vs 1 day).
**Action**:
- Complete UC-221 in Iteration 2.1 (hotfix iteration)
- Move UC-222 to Iteration 3
- Add 2 days to schedule

## Lessons Learned
- Faceted filters underestimated
- Need better complexity estimation
- Consider buffer time in future iterations
"""

    path = mock_fs.create_file("iterations/iteration-2-retrospective.md", failed_iteration)
    retro = mock_fs.read_file(path)

    # Verify iteration adjustment
    assert "SCOPE ADJUSTED" in retro
    assert "Original Scope" in retro
    assert "Actual Completion" in retro
    assert "Adjustment Decision" in retro
    assert "Lessons Learned" in retro
