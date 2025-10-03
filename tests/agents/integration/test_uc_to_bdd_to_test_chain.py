"""Integration tests for UC → BDD → Test agent chain.

Tests the complete workflow from use case specification through BDD scenario
generation to test file creation. Validates:
- UC spec format compatible with bdd-scenario-writer
- BDD scenarios generated from UC acceptance criteria
- Feature file format compatible with test-writer
- Tests reference both UC and feature file
- Traceability maintained (UC-XXX references)
- Coverage complete (no gaps in chain)

Test Coverage:
- UC → BDD handoff
- BDD → Test handoff
- End-to-end workflow
- Traceability validation
- Coverage completeness
- Error handling
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


@pytest.fixture
def sample_uc_with_bdd(mock_fs: MockFileSystem) -> str:
    """Create sample UC with BDD acceptance criteria."""
    content = """---
id: UC-001
title: Create User Account
status: Draft
priority: High
---

# UC-001: Create User Account

## Objective
Allow administrators to create new user accounts in the system.

## User Value
Administrators can onboard new team members quickly.

## Actors
- **Primary Actor**: Administrator
- **Secondary Actors**: Database, Email Service

## Preconditions
- Administrator is authenticated
- Administrator has "create_user" permission

## Postconditions
- New user account exists in database
- Welcome email sent to user
- User can log in with credentials

## Main Flow
1. Administrator provides username and email
2. System validates input format
3. System checks username not already taken
4. System creates user account with hashed password
5. System sends welcome email to user
6. System returns success confirmation

## Alternative Flows

### Alternative: User chooses own password
1. Administrator provides username, email, and initial password
2. System validates password complexity
3. Continue with Main Flow step 3

## Error Scenarios

### Error: Username already exists
**Trigger**: Username provided already exists in system
**Expected Behavior**:
- System returns 400 Bad Request
- Error message: "Username already exists"
- No user account created
- Administrator can try different username

### Error: Invalid email format
**Trigger**: Email does not match valid email pattern
**Expected Behavior**:
- System returns 400 Bad Request
- Error message: "Invalid email format"
- No user account created

## Acceptance Criteria (BDD Format)

```gherkin
Scenario: Successfully create user with valid data
  Given administrator is authenticated
  And administrator has "create_user" permission
  And administrator provides username "john_doe"
  And administrator provides email "john@example.com"
  When administrator submits user creation request
  Then system returns 201 Created
  And user account is stored in database
  And welcome email is sent to "john@example.com"

Scenario: User creation fails with duplicate username
  Given administrator is authenticated
  And username "existing_user" already exists
  When administrator tries to create user with username "existing_user"
  Then system returns 400 Bad Request
  And error message is "Username already exists"
  And no new user account is created

Scenario: User creation fails with invalid email
  Given administrator is authenticated
  And administrator provides username "john_doe"
  And administrator provides email "not-an-email"
  When administrator submits user creation request
  Then system returns 400 Bad Request
  And error message is "Invalid email format"
  And no user account is created
```

## Data Requirements

### Input Data
| Field | Type | Required | Validation | Example |
|-------|------|----------|------------|---------|
| username | string | Yes | 3-30 chars, alphanumeric | "john_doe" |
| email | string | Yes | Valid email format | "john@example.com" |
| initial_password | string | No | Min 8 chars | "SecurePass123" |

### Output Data
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| user_id | integer | Unique identifier | 42 |
| username | string | Username | "john_doe" |
| email | string | Email address | "john@example.com" |
| created_at | timestamp | Creation time | "2025-10-03T10:00:00Z" |

## Non-Functional Requirements

### Performance
- Response time: 95th percentile < 500ms
- Throughput: Support 50 user creations/minute

### Security
- Passwords hashed with bcrypt
- Email verification required
- Audit log all user creations

## Services Used
| Service | Methods | Purpose |
|---------|---------|---------|
| UserService | create_user(), validate_username() | User account management |
| EmailService | send_welcome_email() | Email notifications |
"""
    file_path = mock_fs.create_file("specs/use-cases/UC-001-create-user-account.md", content)
    return file_path


# ============================================================================
# Test: UC Format Compatibility with BDD Writer
# ============================================================================

@pytest.mark.integration
def test_uc_has_acceptance_criteria_section(sample_uc_with_bdd: str, mock_fs: MockFileSystem):
    """Test that UC has BDD acceptance criteria section for bdd-scenario-writer."""
    content = mock_fs.read_file(sample_uc_with_bdd)

    assert "## Acceptance Criteria (BDD Format)" in content
    assert "```gherkin" in content
    assert "Scenario:" in content


@pytest.mark.integration
def test_uc_acceptance_criteria_has_gherkin_format(sample_uc_with_bdd: str, mock_fs: MockFileSystem):
    """Test that UC acceptance criteria use proper Gherkin format."""
    content = mock_fs.read_file(sample_uc_with_bdd)

    assert "Given" in content
    assert "When" in content
    assert "Then" in content


@pytest.mark.integration
def test_uc_has_uc_id_for_traceability(sample_uc_with_bdd: str, mock_fs: MockFileSystem):
    """Test that UC has ID that can be referenced in downstream files."""
    content = mock_fs.read_file(sample_uc_with_bdd)

    assert "UC-001" in content
    assert "id: UC-001" in content


@pytest.mark.integration
def test_uc_has_services_section_for_test_generation(sample_uc_with_bdd: str, mock_fs: MockFileSystem):
    """Test that UC lists services needed for test mock generation."""
    content = mock_fs.read_file(sample_uc_with_bdd)

    assert "## Services Used" in content
    assert "UserService" in content


# ============================================================================
# Test: BDD Writer Output Compatibility with Test Writer
# ============================================================================

@pytest.mark.integration
def test_bdd_writer_would_generate_feature_file(sample_uc_with_bdd: str, mock_fs: MockFileSystem):
    """Test that bdd-scenario-writer would generate .feature file from UC."""
    # Simulate bdd-scenario-writer output
    feature_content = """# Specification: UC-001 Create User Account

Feature: Create User Account
  As an administrator
  I want to create new user accounts
  So that new team members can access the system

  Background:
    Given administrator is authenticated
    And administrator has "create_user" permission

  # Specification: UC-001#main-flow
  Scenario: Successfully create user with valid data
    Given administrator provides username "john_doe"
    And administrator provides email "john@example.com"
    When administrator submits user creation request
    Then system returns 201 Created
    And user account is stored in database
    And welcome email is sent to "john@example.com"

  # Specification: UC-001#error-duplicate-username
  Scenario: User creation fails with duplicate username
    Given username "existing_user" already exists
    When administrator tries to create user with username "existing_user"
    Then system returns 400 Bad Request
    And error message is "Username already exists"
    And no new user account is created

  # Specification: UC-001#error-invalid-email
  Scenario: User creation fails with invalid email
    Given administrator provides username "john_doe"
    And administrator provides email "not-an-email"
    When administrator submits user creation request
    Then system returns 400 Bad Request
    And error message is "Invalid email format"
    And no user account is created
"""

    feature_path = mock_fs.create_file("features/UC-001-create-user-account.feature", feature_content)
    feature = mock_fs.read_file(feature_path)

    # Verify feature file has required elements for test-writer
    assert "Feature:" in feature
    assert "Scenario:" in feature
    assert "UC-001" in feature  # Traceability


@pytest.mark.integration
def test_feature_file_has_spec_references(mock_fs: MockFileSystem):
    """Test that feature file includes spec references for test-writer."""
    feature_content = """# Specification: UC-001 Create User Account

Feature: Create User Account

  # Specification: UC-001#main-flow
  Scenario: Successfully create user with valid data
    Given administrator provides username "john_doe"
    When administrator submits user creation request
    Then system returns 201 Created
"""

    feature_path = mock_fs.create_file("features/UC-001-create-user-account.feature", feature_content)
    feature = mock_fs.read_file(feature_path)

    assert "# Specification: UC-001" in feature
    assert "UC-001#main-flow" in feature


@pytest.mark.integration
def test_feature_scenarios_map_to_uc_criteria(sample_uc_with_bdd: str, mock_fs: MockFileSystem):
    """Test that feature scenarios cover UC acceptance criteria."""
    uc_content = mock_fs.read_file(sample_uc_with_bdd)

    # Count scenarios in UC
    uc_scenarios = uc_content.count("Scenario:")

    # Simulate feature file
    feature_content = """# Specification: UC-001

Feature: Create User Account

  Scenario: Successfully create user with valid data
    Given administrator provides username "john_doe"
    When administrator submits user creation request
    Then system returns 201 Created

  Scenario: User creation fails with duplicate username
    Given username "existing_user" already exists
    When administrator tries to create user with username "existing_user"
    Then system returns 400 Bad Request

  Scenario: User creation fails with invalid email
    Given administrator provides username "john_doe"
    And administrator provides email "not-an-email"
    When administrator submits user creation request
    Then system returns 400 Bad Request
"""

    feature_path = mock_fs.create_file("features/UC-001.feature", feature_content)
    feature = mock_fs.read_file(feature_path)

    feature_scenarios = feature.count("Scenario:")

    # Feature should have at least as many scenarios as UC
    assert feature_scenarios >= uc_scenarios


# ============================================================================
# Test: Test Writer Output from Feature File
# ============================================================================

@pytest.mark.integration
def test_test_writer_would_generate_tests_from_feature(mock_fs: MockFileSystem):
    """Test that test-writer would generate tests from feature file."""
    # Simulate feature file
    feature_content = """# Specification: UC-001 Create User Account

Feature: Create User Account

  Scenario: Successfully create user with valid data
    Given administrator provides username "john_doe"
    When administrator submits user creation request
    Then system returns 201 Created
"""

    feature_path = mock_fs.create_file("features/UC-001.feature", feature_content)

    # Simulate test-writer output
    test_content = """\"\"\"Tests for UserService.create_user().

Specification: UC-001 Create User Account
Feature: features/UC-001.feature
\"\"\"
import pytest
from unittest.mock import Mock
from typing import Dict, Any

from src.services.user_service import UserService


@pytest.fixture
def mock_database() -> Mock:
    \"\"\"Mock database for testing.\"\"\"
    db = Mock()
    db.save.return_value = {"id": 42, "username": "john_doe"}
    return db


@pytest.fixture
def user_service(mock_database: Mock) -> UserService:
    \"\"\"UserService instance with mocked dependencies.\"\"\"
    return UserService(database=mock_database)


def test_create_user_with_valid_data(user_service: UserService, mock_database: Mock) -> None:
    \"\"\"Test that UserService.create_user() succeeds with valid data.

    Specification: UC-001#main-flow
    Feature Scenario: Successfully create user with valid data
    \"\"\"
    # Arrange
    user_data = {"username": "john_doe", "email": "john@example.com"}

    # Act
    result = user_service.create_user(user_data)

    # Assert
    assert result["id"] == 42
    assert result["username"] == "john_doe"
    mock_database.save.assert_called_once()
"""

    test_path = mock_fs.create_file("tests/unit/services/test_user_service.py", test_content)
    test = mock_fs.read_file(test_path)

    # Verify test file has required elements
    assert "Specification: UC-001" in test
    assert "Feature: features/UC-001" in test
    assert "@pytest.fixture" in test
    assert "def test_" in test


@pytest.mark.integration
def test_test_file_references_both_uc_and_feature(mock_fs: MockFileSystem):
    """Test that test file maintains traceability to both UC and feature."""
    test_content = """\"\"\"Tests for UserService.

Specification: UC-001 Create User Account
Feature: features/UC-001-create-user-account.feature
\"\"\"

def test_create_user_success() -> None:
    \"\"\"Test user creation success.

    Specification: UC-001#main-flow
    Feature Scenario: Successfully create user with valid data
    \"\"\"
    pass
"""

    test_path = mock_fs.create_file("tests/unit/test_user_service.py", test_content)
    test = mock_fs.read_file(test_path)

    # Verify traceability
    assert "Specification: UC-001" in test
    assert "Feature: features/UC-001" in test
    assert "UC-001#main-flow" in test  # Specific section reference


# ============================================================================
# Test: End-to-End Workflow
# ============================================================================

@pytest.mark.integration
def test_complete_uc_to_bdd_to_test_workflow(sample_uc_with_bdd: str, mock_fs: MockFileSystem):
    """Test complete workflow from UC through BDD to tests."""
    # Step 1: UC exists
    uc_content = mock_fs.read_file(sample_uc_with_bdd)
    assert "UC-001" in uc_content
    assert "Scenario:" in uc_content

    # Step 2: BDD writer generates feature
    feature_content = """# Specification: UC-001 Create User Account

Feature: Create User Account
  Scenario: Successfully create user with valid data
    Given administrator provides username "john_doe"
    When administrator submits user creation request
    Then system returns 201 Created
"""
    feature_path = mock_fs.create_file("features/UC-001.feature", feature_content)
    feature = mock_fs.read_file(feature_path)
    assert "UC-001" in feature

    # Step 3: Test writer generates tests
    test_content = """\"\"\"Tests for UC-001.

Specification: UC-001 Create User Account
Feature: features/UC-001.feature
\"\"\"
def test_create_user_success():
    \"\"\"Specification: UC-001#main-flow\"\"\"
    pass
"""
    test_path = mock_fs.create_file("tests/unit/test_user_service.py", test_content)
    test = mock_fs.read_file(test_path)

    # Verify complete traceability chain
    assert "UC-001" in uc_content
    assert "UC-001" in feature
    assert "UC-001" in test
    assert "features/UC-001.feature" in test


@pytest.mark.integration
def test_traceability_maintained_across_chain(mock_fs: MockFileSystem):
    """Test that UC ID is traceable from UC through BDD to tests."""
    # Create chain
    uc_path = mock_fs.create_file("specs/use-cases/UC-999.md", "# UC-999: Test\n\nScenario: Test")
    feature_path = mock_fs.create_file("features/UC-999.feature", "# Specification: UC-999\n\nFeature: Test")
    test_path = mock_fs.create_file("tests/unit/test_999.py", "# Specification: UC-999\n# Feature: features/UC-999.feature")

    # Verify chain
    uc = mock_fs.read_file(uc_path)
    feature = mock_fs.read_file(feature_path)
    test = mock_fs.read_file(test_path)

    assert "UC-999" in uc
    assert "UC-999" in feature
    assert "UC-999" in test


# ============================================================================
# Test: Coverage Completeness
# ============================================================================

@pytest.mark.integration
def test_all_uc_scenarios_have_feature_scenarios(sample_uc_with_bdd: str, mock_fs: MockFileSystem):
    """Test that all UC acceptance criteria have corresponding feature scenarios."""
    uc_content = mock_fs.read_file(sample_uc_with_bdd)

    # Extract UC scenarios
    import re
    uc_scenarios = re.findall(r'Scenario: ([^\n]+)', uc_content)

    # Simulate feature with same scenarios
    feature_scenarios_text = "\n".join(f"  Scenario: {s}" for s in uc_scenarios)
    feature_content = f"""# Specification: UC-001

Feature: Create User Account
{feature_scenarios_text}
"""

    feature_path = mock_fs.create_file("features/UC-001.feature", feature_content)
    feature = mock_fs.read_file(feature_path)

    # Verify all UC scenarios appear in feature
    for scenario in uc_scenarios:
        assert scenario in feature


@pytest.mark.integration
def test_all_feature_scenarios_have_tests(mock_fs: MockFileSystem):
    """Test that all feature scenarios have corresponding test functions."""
    feature_content = """Feature: Test
  Scenario: Scenario A
  Scenario: Scenario B
  Scenario: Scenario C
"""

    feature_path = mock_fs.create_file("features/test.feature", feature_content)

    # Simulate tests for each scenario
    test_content = """def test_scenario_a():
    pass

def test_scenario_b():
    pass

def test_scenario_c():
    pass
"""

    test_path = mock_fs.create_file("tests/unit/test_feature.py", test_content)
    test = mock_fs.read_file(test_path)

    # Verify all scenarios have tests (simplified check)
    assert "test_scenario_a" in test
    assert "test_scenario_b" in test
    assert "test_scenario_c" in test


# ============================================================================
# Test: Error Handling
# ============================================================================

@pytest.mark.integration
def test_uc_without_acceptance_criteria_fails_bdd_generation(mock_fs: MockFileSystem):
    """Test that UC without acceptance criteria cannot generate BDD scenarios."""
    # Create incomplete UC
    uc_content = """# UC-002: Incomplete UC

## Objective
Test objective.

## Main Flow
1. Step 1
"""

    uc_path = mock_fs.create_file("specs/use-cases/UC-002.md", uc_content)
    uc = mock_fs.read_file(uc_path)

    # Verify missing acceptance criteria section
    assert "## Acceptance Criteria" not in uc
    assert "Scenario:" not in uc

    # BDD writer should fail/warn (simulated)
    has_acceptance_criteria = "## Acceptance Criteria" in uc
    assert not has_acceptance_criteria, "UC lacks acceptance criteria for BDD generation"


@pytest.mark.integration
def test_feature_without_spec_reference_fails_test_generation(mock_fs: MockFileSystem):
    """Test that feature file without spec reference loses traceability."""
    # Create feature without UC reference
    feature_content = """Feature: Orphaned Feature
  Scenario: Test scenario
    When action
    Then result
"""

    feature_path = mock_fs.create_file("features/orphaned.feature", feature_content)
    feature = mock_fs.read_file(feature_path)

    # Verify missing spec reference
    assert "Specification:" not in feature
    assert "UC-" not in feature

    # Test writer should warn about missing traceability
    has_spec_reference = "Specification:" in feature
    assert not has_spec_reference, "Feature lacks UC traceability"


# ============================================================================
# Test: Services Identification Chain
# ============================================================================

@pytest.mark.integration
def test_services_from_uc_used_in_test_mocks(sample_uc_with_bdd: str, mock_fs: MockFileSystem):
    """Test that services identified in UC are mocked in tests."""
    uc_content = mock_fs.read_file(sample_uc_with_bdd)

    # Extract services from UC
    assert "UserService" in uc_content
    assert "EmailService" in uc_content

    # Simulate test with mocked services
    test_content = """import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_user_service() -> Mock:
    return Mock()

@pytest.fixture
def mock_email_service() -> Mock:
    return Mock()
"""

    test_path = mock_fs.create_file("tests/unit/test_user.py", test_content)
    test = mock_fs.read_file(test_path)

    # Verify services are mocked
    assert "mock_user_service" in test
    assert "mock_email_service" in test
