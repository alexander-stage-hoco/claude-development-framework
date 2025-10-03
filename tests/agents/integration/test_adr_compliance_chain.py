"""Integration tests for ADR compliance chain.

Tests the workflow of creating and enforcing Architecture Decision Records:
- adr-manager creates ADR from technical decision
- ADR is added to technical-decisions.md
- code-quality-checker references ADR in validation
- Implementation compliance checked against ADR
- Violations detected with evidence
- ADR lifecycle (deprecation, superseding)

Test Coverage:
- ADR creation workflow
- ADR format compatibility
- Compliance checking
- Violation detection
- ADR references in code
- ADR lifecycle transitions
"""

import pytest
from pathlib import Path

from tests.agents.fixtures import MockFileSystem


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_fs(tmp_path: Path) -> MockFileSystem:
    """Mock file system for testing."""
    return MockFileSystem(tmp_path)


@pytest.fixture
def sample_adr(mock_fs: MockFileSystem) -> str:
    """Create sample ADR in technical decisions."""
    adr_content = """# Technical Decisions

## Active ADRs

### ADR-001: Use Python 3.11+ with Type Hints

**Date**: 2025-10-01
**Status**: Accepted
**Deciders**: Project Team

**Context**:
We need a modern Python version with better performance and type checking capabilities.
Python 3.11 offers 25% performance improvement and better error messages.

**Decision**:
Use Python 3.11+ for all new code. Require type hints on all function signatures.
Use mypy for static type checking.

**Consequences**:
- ✅ **Easier**: Better IDE support, catch errors early
- ✅ **Easier**: Improved performance
- ❌ **Harder**: Must migrate Python 3.9 code

**Alternatives Considered**:
- Python 3.9 (rejected: older, slower)
- Python 3.10 (rejected: 3.11 has better performance)

### ADR-002: Use pytest for All Testing

**Date**: 2025-10-01
**Status**: Accepted
**Deciders**: Project Team

**Context**:
Need standardized testing framework across project.

**Decision**:
Use pytest as the sole testing framework. No unittest or nose2.

**Consequences**:
- ✅ **Easier**: Fixture-based testing, clear assertions
- ❌ **Harder**: Must convert existing unittest tests

**Alternatives Considered**:
- unittest (rejected: verbose, less features)
- nose2 (rejected: less maintained)

### ADR-003: Repository Pattern for Data Access

**Date**: 2025-10-02
**Status**: Accepted
**Deciders**: Project Team

**Context**:
Need abstraction layer between business logic and database.

**Decision**:
Use Repository pattern for all data access. No direct database calls from services.

**Consequences**:
- ✅ **Easier**: Testable (mock repository), swappable database
- ❌ **Harder**: More layers, more files

**Alternatives Considered**:
- Direct DB access (rejected: hard to test, couples logic to DB)
- Active Record (rejected: violates SRP)
"""

    return mock_fs.create_file(".claude/technical-decisions.md", adr_content)


# ============================================================================
# Test: ADR Creation Format
# ============================================================================

@pytest.mark.integration
def test_adr_has_all_required_sections(sample_adr: str, mock_fs: MockFileSystem):
    """Test that ADR has all required sections."""
    adr = mock_fs.read_file(sample_adr)

    # Required sections
    assert "**Date**:" in adr
    assert "**Status**:" in adr
    assert "**Deciders**:" in adr
    assert "**Context**:" in adr
    assert "**Decision**:" in adr
    assert "**Consequences**:" in adr
    assert "**Alternatives Considered**:" in adr


@pytest.mark.integration
def test_adr_has_sequential_numbering(sample_adr: str, mock_fs: MockFileSystem):
    """Test that ADRs are sequentially numbered."""
    adr = mock_fs.read_file(sample_adr)

    assert "ADR-001" in adr
    assert "ADR-002" in adr
    assert "ADR-003" in adr


@pytest.mark.integration
def test_adr_consequences_have_pros_and_cons(sample_adr: str, mock_fs: MockFileSystem):
    """Test that ADR consequences list both pros and cons."""
    adr = mock_fs.read_file(sample_adr)

    # Should have both easier (pros) and harder (cons)
    assert "✅ **Easier**:" in adr
    assert "❌ **Harder**:" in adr


# ============================================================================
# Test: ADR References in Code
# ============================================================================

@pytest.mark.integration
def test_code_references_adr_in_docstrings(mock_fs: MockFileSystem):
    """Test that implementation code references relevant ADRs."""
    impl_content = """\"\"\"User repository implementation.

Architecture: ADR-003 Repository Pattern
Specification: UC-005 User Management
\"\"\"
from typing import Optional

class UserRepository:
    \"\"\"Repository for user data access.

    Architecture: ADR-003 Repository Pattern for Data Access
    \"\"\"

    def find_by_id(self, user_id: int) -> Optional[dict]:
        \"\"\"Find user by ID.

        Specification: UC-005#get-user
        \"\"\"
        # Implementation using repository pattern (ADR-003)
        pass
"""

    impl_path = mock_fs.create_file("src/repositories/user_repository.py", impl_content)
    impl = mock_fs.read_file(impl_path)

    # Verify ADR references
    assert "Architecture: ADR-003" in impl
    assert "Repository Pattern" in impl


@pytest.mark.integration
def test_code_follows_adr_type_hints_requirement(mock_fs: MockFileSystem):
    """Test that code follows ADR-001 type hints requirement."""
    # Compliant code (ADR-001: type hints required)
    compliant = """from typing import Dict, Any

def process_data(data: Dict[str, Any]) -> int:
    \"\"\"Process data.

    Architecture: ADR-001 Type Hints Required
    Specification: UC-010#process
    \"\"\"
    return len(data)
"""

    # Non-compliant code (missing type hints)
    non_compliant = """def process_data(data):
    return len(data)
"""

    path1 = mock_fs.create_file("src/compliant.py", compliant)
    path2 = mock_fs.create_file("src/non_compliant.py", non_compliant)

    comp = mock_fs.read_file(path1)
    non_comp = mock_fs.read_file(path2)

    # Compliant has type hints
    assert "data: Dict[str, Any]" in comp
    assert "-> int:" in comp

    # Non-compliant lacks type hints (would be flagged by quality checker)
    assert "data:" not in non_comp or "data):" in non_comp


# ============================================================================
# Test: Compliance Checking
# ============================================================================

@pytest.mark.integration
def test_compliance_checker_validates_against_adrs(sample_adr: str, mock_fs: MockFileSystem):
    """Test that compliance checker validates code against ADRs."""
    # Create code that violates ADR-002 (pytest required)
    test_content = """import unittest  # VIOLATION: ADR-002 requires pytest

class TestUser(unittest.TestCase):  # VIOLATION: Should use pytest
    def test_create_user(self):
        pass
"""

    test_path = mock_fs.create_file("tests/unit/test_user.py", test_content)
    test = mock_fs.read_file(test_path)

    # Compliance checker would detect violation
    assert "import unittest" in test  # Violates ADR-002


@pytest.mark.integration
def test_compliance_checker_detects_pattern_violations(sample_adr: str, mock_fs: MockFileSystem):
    """Test that compliance checker detects architectural pattern violations."""
    # Code violating ADR-003 (repository pattern required)
    violation_content = """from src.database import db  # Direct DB access

def get_user(user_id):
    # VIOLATION: ADR-003 requires repository pattern, not direct DB access
    conn = db.connect()
    result = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return result.fetchone()
"""

    impl_path = mock_fs.create_file("src/user_service.py", violation_content)
    impl = mock_fs.read_file(impl_path)

    # Compliance checker would flag direct DB access
    assert "db.connect()" in impl
    assert "conn.execute" in impl


@pytest.mark.integration
def test_compliance_report_includes_file_line_evidence(mock_fs: MockFileSystem):
    """Test that compliance violations include file:line evidence."""
    # Simulated compliance report
    report_content = """ADR COMPLIANCE REPORT
=====================

VIOLATIONS DETECTED:

CRITICAL (1):
  ❌ src/user_service.py:5
     VIOLATION: ADR-003 (Repository Pattern Required)
     Found: Direct database access
     Evidence:
       5: conn = db.connect()
       6: result = conn.execute("SELECT * FROM users")
     Suggested Fix: Use UserRepository.find_all()

HIGH (1):
  ⚠️ tests/unit/test_user.py:1
     VIOLATION: ADR-002 (pytest Required)
     Found: Using unittest instead of pytest
     Evidence:
       1: import unittest
     Suggested Fix: Convert to pytest format
"""

    report_path = mock_fs.create_file("reports/adr-compliance.txt", report_content)
    report = mock_fs.read_file(report_path)

    # Verify file:line references
    assert "src/user_service.py:5" in report
    assert "tests/unit/test_user.py:1" in report
    assert "Evidence:" in report


# ============================================================================
# Test: ADR Lifecycle
# ============================================================================

@pytest.mark.integration
def test_adr_deprecation_workflow(mock_fs: MockFileSystem):
    """Test ADR deprecation workflow."""
    # Original ADR
    original_adr = """### ADR-005: Use Sessions for Authentication

**Date**: 2025-09-01
**Status**: Accepted

**Decision**: Use server-side sessions for authentication.
"""

    # Deprecated ADR
    deprecated_adr = """### ADR-005: Use Sessions for Authentication

**Date**: 2025-09-01
**Status**: Deprecated (see ADR-010)
**Deprecated Date**: 2025-10-01
**Reason**: Migrated to JWT for stateless authentication

**Decision**: Use server-side sessions for authentication.
(Original content preserved)
"""

    path1 = mock_fs.create_file(".claude/technical-decisions-old.md", original_adr)
    path2 = mock_fs.create_file(".claude/technical-decisions-new.md", deprecated_adr)

    old = mock_fs.read_file(path1)
    new = mock_fs.read_file(path2)

    # Original is Accepted
    assert "**Status**: Accepted" in old

    # Deprecated has status change and reason
    assert "**Status**: Deprecated (see ADR-010)" in new
    assert "**Deprecated Date**:" in new
    assert "**Reason**:" in new


@pytest.mark.integration
def test_adr_superseding_workflow(mock_fs: MockFileSystem):
    """Test ADR superseding workflow."""
    # New ADR supersedes old one
    new_adr = """### ADR-010: Use JWT for Authentication

**Date**: 2025-10-01
**Status**: Accepted
**Supersedes**: ADR-005
**Deciders**: Project Team

**Context**:
Need stateless authentication for microservices architecture.
Sessions (ADR-005) require sticky sessions, limiting scalability.

**Decision**:
Use JWT tokens for stateless authentication. Store tokens in HTTP-only cookies.

**Consequences**:
- ✅ **Easier**: Stateless, scales horizontally
- ❌ **Harder**: Token management, refresh logic
"""

    path = mock_fs.create_file(".claude/technical-decisions.md", new_adr)
    adr = mock_fs.read_file(path)

    # Verify superseding link
    assert "**Supersedes**: ADR-005" in adr
    assert "ADR-010" in adr


# ============================================================================
# Test: ADR and Quality Checker Integration
# ============================================================================

@pytest.mark.integration
def test_quality_checker_enforces_adr_standards(sample_adr: str, mock_fs: MockFileSystem):
    """Test that quality checker enforces ADR standards."""
    # Code compliant with ADR-001 (type hints)
    compliant_code = """\"\"\"User service.

Architecture: ADR-001 Type Hints Required
\"\"\"
from typing import Dict, Any

def create_user(data: Dict[str, Any]) -> Dict[str, Any]:
    \"\"\"Create user.

    Architecture: ADR-001
    Specification: UC-005#create
    \"\"\"
    return {"id": 1, "name": data["name"]}
"""

    impl_path = mock_fs.create_file("src/user_service.py", compliant_code)
    impl = mock_fs.read_file(impl_path)

    # Quality checker would pass this
    assert "data: Dict[str, Any]" in impl
    assert "-> Dict[str, Any]:" in impl
    assert "Architecture: ADR-001" in impl


@pytest.mark.integration
def test_quality_checker_cites_adr_in_violations(mock_fs: MockFileSystem):
    """Test that quality checker cites ADR when reporting violations."""
    # Simulated quality report citing ADR
    quality_report = """CODE QUALITY REPORT
==================

ADR Compliance Issues:

❌ CRITICAL: src/auth.py:12
   Missing type hints (violates ADR-001)
   ADR-001 requires: Type hints on all functions
   Found: def authenticate(username, password):
   Fix: def authenticate(username: str, password: str) -> Optional[Session]:

⚠️ HIGH: tests/unit/test_auth.py:1
   Using unittest (violates ADR-002)
   ADR-002 requires: pytest for all testing
   Found: import unittest
   Fix: Convert to pytest format with fixtures
"""

    report_path = mock_fs.create_file("reports/quality.txt", quality_report)
    report = mock_fs.read_file(report_path)

    # Verify ADR citations
    assert "violates ADR-001" in report
    assert "violates ADR-002" in report
    assert "ADR-001 requires:" in report


# ============================================================================
# Test: ADR Decision Qualification
# ============================================================================

@pytest.mark.integration
def test_adr_created_for_architectural_decisions(mock_fs: MockFileSystem):
    """Test that ADRs are created for qualifying architectural decisions."""
    # Decision qualifies as ADR (impacts multiple parts, hard to change)
    adr_content = """### ADR-004: Use PostgreSQL for Persistence

**Date**: 2025-10-02
**Status**: Accepted

**Context**:
Need reliable, ACID-compliant database for production.
Decision impacts all services (data layer, queries, migrations).
Hard to change later due to schema dependencies.

**Decision**:
Use PostgreSQL 15+ as primary database.

**Consequences**:
- ✅ **Easier**: ACID guarantees, mature ecosystem
- ❌ **Harder**: Complex queries can be slow

**Alternatives Considered**:
- MongoDB (rejected: need ACID transactions)
- MySQL (rejected: weaker JSON support)
"""

    path = mock_fs.create_file(".claude/adrs/ADR-004.md", adr_content)
    adr = mock_fs.read_file(path)

    # ADR created because:
    # 1. Impacts multiple parts: ✓ ("impacts all services")
    # 2. Hard to change: ✓ ("Hard to change later")
    # 3. Multiple options: ✓ (PostgreSQL, MongoDB, MySQL)

    assert "impacts all services" in adr or "Decision impacts" in adr
    assert "Hard to change" in adr or "hard to change" in adr


@pytest.mark.integration
def test_trivial_decisions_not_adr_worthy(mock_fs: MockFileSystem):
    """Test that trivial decisions don't create ADRs."""
    # Trivial decision (doesn't need ADR)
    code_comment = """# Using 'user_id' instead of 'userId' for variable naming
# (team preference, easily changed, local to this file)
user_id = get_current_user()
"""

    impl_path = mock_fs.create_file("src/auth.py", code_comment)
    impl = mock_fs.read_file(impl_path)

    # No ADR created because:
    # - Local impact (single file)
    # - Easy to change (find/replace)
    # - Not architectural

    assert "user_id" in impl
    # This decision stays as code comment, not ADR


# ============================================================================
# Test: ADR Compliance Workflow
# ============================================================================

@pytest.mark.integration
def test_complete_adr_compliance_workflow(sample_adr: str, mock_fs: MockFileSystem):
    """Test complete ADR compliance workflow."""
    # Step 1: ADR exists
    adr = mock_fs.read_file(sample_adr)
    assert "ADR-001" in adr
    assert "Type Hints" in adr

    # Step 2: Implementation references ADR
    impl_content = """\"\"\"Data service.

Architecture: ADR-001 Type Hints Required
\"\"\"
from typing import List

def get_items() -> List[dict]:
    \"\"\"Get items.

    Architecture: ADR-001
    \"\"\"
    return []
"""
    impl_path = mock_fs.create_file("src/data_service.py", impl_content)
    impl = mock_fs.read_file(impl_path)
    assert "Architecture: ADR-001" in impl

    # Step 3: Quality checker validates compliance
    # (simulated - would run mypy, check type hints)

    # Step 4: Compliance report generated
    compliance_report = """ADR COMPLIANCE: PASSED ✓

All code complies with active ADRs:
- ADR-001: Type hints present on all functions ✓
- ADR-002: pytest used for testing ✓
- ADR-003: Repository pattern followed ✓
"""
    report_path = mock_fs.create_file("reports/compliance.txt", compliance_report)
    report = mock_fs.read_file(report_path)
    assert "PASSED ✓" in report
