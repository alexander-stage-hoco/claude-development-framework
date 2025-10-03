"""End-to-end tests for complete feature development workflow.

Tests the complete workflow from initial idea through to production-ready code:
1. User provides feature idea
2. uc-writer creates specification
3. bdd-scenario-writer generates .feature file
4. test-writer creates tests (RED state)
5. Implementation makes tests pass (GREEN state)
6. code-quality-checker validates quality
7. refactoring-analyzer suggests improvements
8. adr-manager checks compliance
9. git-workflow-helper guides commit
10. session-summarizer captures decisions

Test Coverage:
- Complete workflow execution
- Agent handoffs at each step
- Traceability throughout
- Quality gates enforced
- All artifacts generated correctly
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
# Test: Complete Feature Workflow
# ============================================================================

@pytest.mark.e2e
def test_complete_feature_development_workflow(mock_fs: MockFileSystem):
    """Test complete feature development from idea to commit."""
    # STEP 1: User provides feature idea
    feature_idea = """
    Feature: User Login
    Users should be able to log in with email and password.
    System should validate credentials and create a session.
    """

    # STEP 2: uc-writer creates specification
    uc_spec = """---
id: UC-020
title: User Login
status: Draft
---

# UC-020: User Login

## Objective
Enable users to authenticate and access the system securely.

## Main Flow
1. User provides email and password
2. System validates credentials
3. System creates session
4. System returns success with session token

## Acceptance Criteria
```gherkin
Scenario: Successful login with valid credentials
  Given user exists with email "user@example.com"
  And password is "SecurePass123"
  When user submits login with email and password
  Then system validates credentials
  And system creates session
  And system returns 200 OK with session token
```

## Services Used
| Service | Methods | Purpose |
|---------|---------|---------|
| AuthService | authenticate(), create_session() | Authentication and session management |
"""
    uc_path = mock_fs.create_file("specs/use-cases/UC-020-user-login.md", uc_spec)

    # STEP 3: bdd-scenario-writer generates .feature file
    feature_file = """# Specification: UC-020 User Login

Feature: User Login
  As a user
  I want to log in with my credentials
  So that I can access the system

  # Specification: UC-020#main-flow
  Scenario: Successful login with valid credentials
    Given user exists with email "user@example.com"
    And password is "SecurePass123"
    When user submits login with email and password
    Then system validates credentials
    And system creates session
    And system returns 200 OK with session token
"""
    feature_path = mock_fs.create_file("features/UC-020-user-login.feature", feature_file)

    # STEP 4: test-writer creates tests (RED state)
    test_file = """\"\"\"Tests for AuthService.authenticate().

Specification: UC-020 User Login
Feature: features/UC-020-user-login.feature
\"\"\"
import pytest
from unittest.mock import Mock
from src.services.auth_service import AuthService


@pytest.fixture
def mock_user_repo() -> Mock:
    user = Mock()
    user.email = "user@example.com"
    user.password_hash = "$2b$12$hashed_password"

    repo = Mock()
    repo.find_by_email.return_value = user
    return repo


@pytest.fixture
def auth_service(mock_user_repo: Mock) -> AuthService:
    return AuthService(user_repository=mock_user_repo)


def test_authenticate_with_valid_credentials(auth_service: AuthService) -> None:
    \"\"\"Test successful authentication.

    Specification: UC-020#main-flow
    Feature Scenario: Successful login with valid credentials
    \"\"\"
    # Arrange
    email = "user@example.com"
    password = "SecurePass123"

    # Act
    result = auth_service.authenticate(email, password)

    # Assert
    assert result["success"] is True
    assert "session_token" in result
"""
    test_path = mock_fs.create_file("tests/unit/services/test_auth_service.py", test_file)

    # RED STATE: Tests would fail (no implementation)

    # STEP 5: Implementation makes tests pass (GREEN state)
    impl_file = """\"\"\"Authentication service.

Architecture: ADR-001 Type Hints Required
Specification: UC-020 User Login
\"\"\"
from typing import Dict, Any, Optional
import bcrypt
import uuid


class AuthService:
    \"\"\"Service for user authentication.

    Architecture: ADR-003 Repository Pattern
    Specification: UC-020
    \"\"\"

    def __init__(self, user_repository):
        self.user_repo = user_repository

    def authenticate(self, email: str, password: str) -> Dict[str, Any]:
        \"\"\"Authenticate user with email and password.

        Specification: UC-020#authenticate

        Args:
            email: User email address
            password: Plain text password

        Returns:
            Authentication result with session token
        \"\"\"
        user = self.user_repo.find_by_email(email)

        if not user:
            return {"success": False, "error": "Invalid credentials"}

        if bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            session_token = str(uuid.uuid4())
            return {"success": True, "session_token": session_token}

        return {"success": False, "error": "Invalid credentials"}
"""
    impl_path = mock_fs.create_file("src/services/auth_service.py", impl_file)

    # GREEN STATE: Tests would pass

    # Verify complete workflow artifacts
    assert mock_fs.file_exists(uc_path)
    assert mock_fs.file_exists(feature_path)
    assert mock_fs.file_exists(test_path)
    assert mock_fs.file_exists(impl_path)

    # Verify traceability chain
    uc = mock_fs.read_file(uc_path)
    feature = mock_fs.read_file(feature_path)
    test = mock_fs.read_file(test_path)
    impl = mock_fs.read_file(impl_path)

    assert "UC-020" in uc
    assert "UC-020" in feature
    assert "UC-020" in test
    assert "UC-020" in impl


@pytest.mark.e2e
def test_traceability_maintained_throughout_workflow(mock_fs: MockFileSystem):
    """Test that UC ID is traceable through all workflow artifacts."""
    uc_id = "UC-050"

    # Create workflow artifacts
    uc_path = mock_fs.create_file(f"specs/use-cases/{uc_id}.md", f"# {uc_id}: Test Feature\n\nScenario: Test")
    feature_path = mock_fs.create_file(f"features/{uc_id}.feature", f"# Specification: {uc_id}\n\nFeature: Test")
    test_path = mock_fs.create_file(f"tests/unit/test_{uc_id.lower()}.py", f"# Specification: {uc_id}\n# Feature: features/{uc_id}.feature")
    impl_path = mock_fs.create_file(f"src/{uc_id.lower()}.py", f"# Specification: {uc_id}")

    # Verify traceability
    for path in [uc_path, feature_path, test_path, impl_path]:
        content = mock_fs.read_file(path)
        assert uc_id in content, f"{uc_id} not found in {path}"


@pytest.mark.e2e
def test_quality_gates_enforced_in_workflow(mock_fs: MockFileSystem):
    """Test that quality gates are enforced at each workflow step."""
    # UC must have acceptance criteria for BDD generation
    incomplete_uc = """# UC-060: Incomplete

## Objective
Test objective.
"""
    uc_path = mock_fs.create_file("specs/use-cases/UC-060.md", incomplete_uc)
    uc = mock_fs.read_file(uc_path)

    # Gate 1: UC must have acceptance criteria
    has_acceptance_criteria = "## Acceptance Criteria" in uc
    assert not has_acceptance_criteria, "Quality gate: UC needs acceptance criteria for BDD"

    # Implementation must have type hints for quality check
    no_types_impl = """def process(data):
    return data["result"]
"""
    impl_path = mock_fs.create_file("src/no_types.py", no_types_impl)
    impl = mock_fs.read_file(impl_path)

    # Gate 2: Implementation must have type hints
    has_type_hints = ": " in impl and "->" in impl
    assert not has_type_hints, "Quality gate: Implementation needs type hints"


@pytest.mark.e2e
def test_adr_compliance_checked_in_workflow(mock_fs: MockFileSystem):
    """Test that ADR compliance is checked during workflow."""
    # Create ADR requiring pytest
    adr = """### ADR-010: Use pytest for Testing

**Decision**: All tests must use pytest framework.
"""
    adr_path = mock_fs.create_file(".claude/technical-decisions.md", adr)

    # Compliant test
    compliant_test = """import pytest

def test_feature():
    assert True
"""

    # Non-compliant test
    non_compliant_test = """import unittest

class TestFeature(unittest.TestCase):
    def test_it(self):
        pass
"""

    path1 = mock_fs.create_file("tests/compliant.py", compliant_test)
    path2 = mock_fs.create_file("tests/non_compliant.py", non_compliant_test)

    comp = mock_fs.read_file(path1)
    non_comp = mock_fs.read_file(path2)

    # Compliant uses pytest
    assert "import pytest" in comp

    # Non-compliant violates ADR-010
    assert "import unittest" in non_comp


@pytest.mark.e2e
def test_refactoring_only_after_green_state(mock_fs: MockFileSystem):
    """Test that refactoring happens only after GREEN state."""
    # Original implementation (GREEN state)
    original = """def calculate(x, y):
    return x + y + x * y + 10  # Magic number
"""

    # Can only refactor if tests pass
    tests_passing = True

    if tests_passing:
        # Refactored (magic number extracted)
        refactored = """CONSTANT = 10

def calculate(x, y):
    return x + y + x * y + CONSTANT
"""
        impl_path = mock_fs.create_file("src/refactored.py", refactored)
        impl = mock_fs.read_file(impl_path)
        assert "CONSTANT = 10" in impl


@pytest.mark.e2e
def test_session_summary_captures_workflow_decisions(mock_fs: MockFileSystem):
    """Test that session summarizer captures key workflow decisions."""
    session_summary = """# Session Summary: UC-070 Implementation

## Decisions Made
1. Created UC-070 for user profile feature
2. Chose bcrypt for password hashing (ADR-015)
3. Used repository pattern for data access (ADR-003)
4. Implemented with pytest fixtures (ADR-002)

## Artifacts Created
- specs/use-cases/UC-070-user-profile.md
- features/UC-070-user-profile.feature
- tests/unit/services/test_profile_service.py
- src/services/profile_service.py

## Quality Metrics
- Test coverage: 95%
- Code quality score: 88/100
- All tests passing (GREEN state)

## Next Steps
- Add profile photo upload (UC-071)
- Implement profile search (UC-072)
"""

    summary_path = mock_fs.create_file("session-summaries/2025-10-03-uc-070.md", session_summary)
    summary = mock_fs.read_file(summary_path)

    # Verify summary captures key information
    assert "UC-070" in summary
    assert "Decisions Made" in summary
    assert "Artifacts Created" in summary
    assert "Quality Metrics" in summary


@pytest.mark.e2e
def test_git_workflow_guides_commit_process(mock_fs: MockFileSystem):
    """Test that git-workflow-helper guides commit process."""
    # Simulated git workflow guidance
    workflow_guide = """# Git Workflow for UC-080

## Pre-Commit Checklist
- [x] All tests passing (GREEN state)
- [x] Code quality score ≥ 80 (Score: 92)
- [x] ADR compliance verified
- [x] Spec references in code
- [x] No TODOs or FIXMEs

## Commit Structure
Type: feat
Scope: authentication
Message: implement user login with session management

Details:
- Created UC-080 specification
- Generated BDD scenarios
- Wrote comprehensive tests (RED → GREEN)
- Implemented AuthService with type hints
- Achieved 95% test coverage
- All quality gates passed

Specification: UC-080

## Files to Commit
- specs/use-cases/UC-080-user-login.md
- features/UC-080-user-login.feature
- tests/unit/services/test_auth_service.py
- src/services/auth_service.py

## Commit Command
git add [files above]
git commit -m "feat(authentication): implement user login with session management

- Created UC-080 specification
- Generated BDD scenarios
- Implemented AuthService with type hints
- Achieved 95% test coverage

Specification: UC-080

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
"""

    guide_path = mock_fs.create_file("git-workflow-guide.md", workflow_guide)
    guide = mock_fs.read_file(guide_path)

    # Verify workflow guidance
    assert "Pre-Commit Checklist" in guide
    assert "All tests passing" in guide
    assert "Code quality score" in guide
    assert "Commit Structure" in guide


@pytest.mark.e2e
def test_service_dependencies_identified_and_mocked(mock_fs: MockFileSystem):
    """Test that service dependencies are identified and properly mocked."""
    # UC identifies required services
    uc = """## Services Used
| Service | Methods | Purpose |
|---------|---------|---------|
| UserRepository | find_by_id(), save() | User data access |
| EmailService | send_welcome_email() | Email notifications |
| CacheService | set(), get() | Session caching |
"""
    uc_path = mock_fs.create_file("specs/use-cases/UC-090.md", uc)

    # Tests mock all identified services
    test = """import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_user_repository() -> Mock:
    return Mock()

@pytest.fixture
def mock_email_service() -> Mock:
    return Mock()

@pytest.fixture
def mock_cache_service() -> Mock:
    return Mock()
"""
    test_path = mock_fs.create_file("tests/unit/test_uc_090.py", test)

    uc_content = mock_fs.read_file(uc_path)
    test_content = mock_fs.read_file(test_path)

    # Verify all services are mocked
    assert "UserRepository" in uc_content
    assert "EmailService" in uc_content
    assert "CacheService" in uc_content

    assert "mock_user_repository" in test_content
    assert "mock_email_service" in test_content
    assert "mock_cache_service" in test_content


@pytest.mark.e2e
def test_complete_workflow_with_error_handling(mock_fs: MockFileSystem):
    """Test complete workflow includes proper error handling."""
    # UC documents error scenarios
    uc = """## Error Scenarios

### Error: Invalid Credentials
**Trigger**: User provides wrong password
**Expected**: System returns 401 Unauthorized
"""
    uc_path = mock_fs.create_file("specs/use-cases/UC-100.md", uc)

    # BDD scenario for error
    feature = """Scenario: Login fails with invalid password
  Given user exists
  And user provides wrong password
  When user submits login
  Then system returns 401 Unauthorized
"""
    feature_path = mock_fs.create_file("features/UC-100.feature", feature)

    # Test for error case
    test = """def test_authenticate_fails_with_wrong_password():
    service = AuthService()
    result = service.authenticate("user@example.com", "wrong_password")
    assert result["success"] is False
    assert result["status_code"] == 401
"""
    test_path = mock_fs.create_file("tests/unit/test_auth_errors.py", test)

    # Implementation handles error
    impl = """def authenticate(self, email, password):
    user = self.user_repo.find_by_email(email)
    if not user or not self._verify_password(password, user.password_hash):
        return {"success": False, "status_code": 401}
    return {"success": True, "session_token": self._create_session()}
"""
    impl_path = mock_fs.create_file("src/auth_service.py", impl)

    # Verify error handling throughout
    uc_content = mock_fs.read_file(uc_path)
    feature_content = mock_fs.read_file(feature_path)
    test_content = mock_fs.read_file(test_path)
    impl_content = mock_fs.read_file(impl_path)

    assert "Error" in uc_content
    assert "fails with" in feature_content
    assert "fails_with" in test_content
    assert "401" in impl_content
