"""Pytest configuration and shared fixtures for agent testing.

This module provides:
- Pytest configuration
- Shared fixtures for all test modules
- Test utilities and helpers
"""

import pytest
from pathlib import Path
from typing import Dict, List, Any
import yaml


# ============================================================================
# Path Configuration
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
AGENTS_DIR = PROJECT_ROOT / ".claude" / "subagents"
TEMPLATES_DIR = PROJECT_ROOT / ".claude" / "templates"
SPECS_DIR = PROJECT_ROOT / "specs"


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return project root directory path."""
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def agents_dir() -> Path:
    """Return agents directory path."""
    return AGENTS_DIR


@pytest.fixture(scope="session")
def templates_dir() -> Path:
    """Return templates directory path."""
    return TEMPLATES_DIR


# ============================================================================
# Agent Discovery
# ============================================================================


@pytest.fixture(scope="session")
def all_agent_files() -> List[Path]:
    """Return list of all agent markdown files."""
    return list(AGENTS_DIR.glob("*.md"))


@pytest.fixture(scope="session")
def agent_names() -> List[str]:
    """Return list of all agent names (without .md extension)."""
    return [f.stem for f in AGENTS_DIR.glob("*.md")]


@pytest.fixture
def agent_file(request) -> Path:
    """Parametrized fixture that provides individual agent files.

    Usage:
        @pytest.mark.parametrize("agent_file", all_agent_files, indirect=True)
        def test_something(agent_file):
            ...
    """
    return request.param


# ============================================================================
# Agent Content Parsing
# ============================================================================


def parse_agent_file(agent_path: Path) -> Dict[str, Any]:
    """Parse agent markdown file into structured data.

    Args:
        agent_path: Path to agent markdown file

    Returns:
        Dictionary with:
        - metadata: Parsed YAML front matter
        - content: Main content sections
        - raw: Raw file content
    """
    with open(agent_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split front matter and content
    parts = content.split("---", 2)

    if len(parts) < 3:
        return {"metadata": {}, "content": content, "raw": content, "has_frontmatter": False}

    # Parse YAML front matter
    try:
        metadata = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        metadata = {}

    main_content = parts[2].strip()

    return {
        "metadata": metadata or {},
        "content": main_content,
        "raw": content,
        "has_frontmatter": True,
    }


@pytest.fixture
def parsed_agent(agent_file: Path) -> Dict[str, Any]:
    """Return parsed agent data for testing.

    Requires agent_file fixture.
    """
    return parse_agent_file(agent_file)


# ============================================================================
# Mock File System
# ============================================================================


@pytest.fixture
def mock_fs(tmp_path: Path) -> Path:
    """Create a mock file system for testing.

    Creates temporary directory with standard project structure:
    - specs/use-cases/
    - specs/services/
    - specs/adrs/
    - src/
    - tests/unit/
    - tests/integration/
    - planning/
    - research/
    """
    # Create directory structure
    (tmp_path / "specs" / "use-cases").mkdir(parents=True)
    (tmp_path / "specs" / "services").mkdir(parents=True)
    (tmp_path / "specs" / "adrs").mkdir(parents=True)
    (tmp_path / "src").mkdir(parents=True)
    (tmp_path / "tests" / "unit").mkdir(parents=True)
    (tmp_path / "tests" / "integration").mkdir(parents=True)
    (tmp_path / "planning").mkdir(parents=True)
    (tmp_path / "research").mkdir(parents=True)
    (tmp_path / "status").mkdir(parents=True)
    (tmp_path / "docs").mkdir(parents=True)

    return tmp_path


# ============================================================================
# Test Data Fixtures
# ============================================================================


@pytest.fixture
def sample_uc_content() -> str:
    """Return sample use case content for testing."""
    return """---
id: UC-001
title: Create User
status: Draft
priority: High
estimated_effort: Small (<3h)
dependencies: None
---

# UC-001: Create User

## Objective
Allow new users to register for the system.

## User Value
Users can create an account to access system features.

## Primary Actor
End User

## Preconditions
- User has valid email address
- Email not already registered

## Postconditions
- User account created in database
- Confirmation email sent
- User can log in

## Main Flow
1. User provides email, username, password
2. System validates input data
3. System checks email uniqueness
4. System creates user account
5. System sends confirmation email
6. System returns success message

## Acceptance Criteria

```gherkin
Feature: User Registration

  Scenario: Successfully create new user
    Given I am on the registration page
    When I provide valid email "user@example.com"
    And I provide username "johndoe"
    And I provide password "SecurePass123!"
    Then user account should be created
    And confirmation email should be sent
```

## Services Required
- UserService (create_user)
- EmailService (send_confirmation)
"""


@pytest.fixture
def sample_service_spec() -> str:
    """Return sample service specification for testing."""
    return """# UserService Specification

## Service ID
SVC-001

## Purpose
Manage user account creation, retrieval, and updates.

## Dependencies
- Database (PostgreSQL)
- EmailService (for notifications)

## Interface

### create_user(data: Dict) -> User
Creates new user account.

**Input:**
- email: str (required, unique, valid format)
- username: str (required, unique)
- password: str (required, min 8 chars)

**Output:**
- User object with id, email, username, created_at

**Errors:**
- ValidationError: Invalid input
- DuplicateEmailError: Email already exists
"""


# ============================================================================
# Pytest Configuration
# ============================================================================


def pytest_configure(config):
    """Pytest configuration hook."""
    config.addinivalue_line("markers", "unit: Unit tests for individual agents")
    config.addinivalue_line("markers", "integration: Integration tests for agent chains")
    config.addinivalue_line("markers", "e2e: End-to-end workflow tests")
    config.addinivalue_line("markers", "performance: Performance and benchmarking tests")
    config.addinivalue_line("markers", "slow: Tests that take more than 1 second")


# ============================================================================
# Test Utilities
# ============================================================================


class AgentTestHelper:
    """Helper class for agent testing."""

    @staticmethod
    def extract_sections(content: str) -> Dict[str, str]:
        """Extract markdown sections from agent content.

        Returns dict mapping section headers to content.
        """
        sections = {}
        current_section = None
        current_content = []

        for line in content.split("\n"):
            if line.startswith("## "):
                if current_section:
                    sections[current_section] = "\n".join(current_content).strip()
                current_section = line[3:].strip()
                current_content = []
            elif current_section:
                current_content.append(line)

        if current_section:
            sections[current_section] = "\n".join(current_content).strip()

        return sections

    @staticmethod
    def find_code_blocks(content: str) -> List[str]:
        """Extract all code blocks from markdown content."""
        blocks = []
        in_block = False
        current_block = []

        for line in content.split("\n"):
            if line.strip().startswith("```"):
                if in_block:
                    blocks.append("\n".join(current_block))
                    current_block = []
                    in_block = False
                else:
                    in_block = True
            elif in_block:
                current_block.append(line)

        return blocks

    @staticmethod
    def find_checkboxes(content: str) -> List[str]:
        """Extract checkbox items from content."""
        checkboxes = []
        for line in content.split("\n"):
            if "- [ ]" in line or "- [x]" in line or "- [X]" in line:
                checkboxes.append(line.strip())
        return checkboxes


@pytest.fixture
def agent_helper() -> AgentTestHelper:
    """Return AgentTestHelper instance."""
    return AgentTestHelper()
