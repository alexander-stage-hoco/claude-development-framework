"""Mock helpers for agent testing.

Provides utilities to mock file operations, git commands, and agent behaviors.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
from unittest.mock import Mock, MagicMock


class MockFileSystem:
    """Mock file system for testing agent file operations."""

    def __init__(self, base_path: Path):
        """Initialize mock file system.

        Args:
            base_path: Base directory for mock file system
        """
        self.base = base_path
        self.files: Dict[str, str] = {}

    def create_file(self, relative_path: str, content: str) -> str:
        """Create a mock file.

        Args:
            relative_path: Path relative to base
            content: File content

        Returns:
            The relative path to the created file
        """
        full_path = self.base / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding='utf-8')
        self.files[relative_path] = content
        return relative_path

    def read_file(self, relative_path: str) -> Optional[str]:
        """Read mock file content.

        Args:
            relative_path: Path relative to base

        Returns:
            File content or None if not found
        """
        full_path = self.base / relative_path
        if full_path.exists():
            return full_path.read_text(encoding='utf-8')
        return self.files.get(relative_path)

    def file_exists(self, relative_path: str) -> bool:
        """Check if mock file exists.

        Args:
            relative_path: Path relative to base

        Returns:
            True if file exists
        """
        return (self.base / relative_path).exists() or relative_path in self.files

    def create_uc_spec(self, uc_id: str, title: str, services: Optional[List[str]] = None) -> str:
        """Create a mock use case specification.

        Args:
            uc_id: Use case ID (e.g., "UC-001")
            title: Use case title
            services: Optional list of required services

        Returns:
            Path to created file
        """
        services_section = ""
        if services:
            services_section = "\n## Services Required\n" + "\n".join(f"- {svc}" for svc in services)

        content = f"""---
id: {uc_id}
title: {title}
status: Draft
priority: High
---

# {uc_id}: {title}

## Objective
Test objective for {title}.

## Main Flow
1. User initiates action
2. System processes request
3. System returns response

## Acceptance Criteria
```gherkin
Feature: {title}
  Scenario: Success
    When action is performed
    Then result is successful
```
{services_section}
"""
        file_path = f"specs/use-cases/{uc_id}-{title.lower().replace(' ', '-')}.md"
        self.create_file(file_path, content)
        return file_path

    def create_service_spec(self, service_id: str, service_name: str) -> str:
        """Create a mock service specification.

        Args:
            service_id: Service ID (e.g., "SVC-001")
            service_name: Service name

        Returns:
            Path to created file
        """
        content = f"""# {service_name} Specification

## Service ID
{service_id}

## Purpose
Test service for {service_name}.

## Dependencies
- Database

## Interface

### operation() -> Result
Test operation.
"""
        file_path = f"specs/services/{service_id}-{service_name.lower()}.md"
        self.create_file(file_path, content)
        return file_path

    def create_adr(self, adr_id: str, title: str, decision: str) -> str:
        """Create a mock ADR.

        Args:
            adr_id: ADR ID (e.g., "ADR-001")
            title: ADR title
            decision: Decision text

        Returns:
            Path to created file
        """
        content = f"""# {adr_id}: {title}

## Status
Accepted

## Context
Test context for {title}.

## Decision
{decision}

## Consequences
Test consequences.
"""
        file_path = f"specs/adrs/{adr_id}-{title.lower().replace(' ', '-')}.md"
        self.create_file(file_path, content)
        return file_path


class MockGitRepo:
    """Mock git repository for testing."""

    def __init__(self):
        """Initialize mock git repo."""
        self.commits: List[Dict[str, Any]] = []
        self.current_branch = "main"
        self.branches: List[str] = ["main"]
        self.staged_files: List[str] = []

    def create_branch(self, branch_name: str):
        """Create a new branch.

        Args:
            branch_name: Name of branch to create
        """
        if branch_name not in self.branches:
            self.branches.append(branch_name)

    def checkout(self, branch_name: str):
        """Checkout a branch.

        Args:
            branch_name: Branch to checkout
        """
        if branch_name in self.branches:
            self.current_branch = branch_name

    def stage(self, file_path: str):
        """Stage a file.

        Args:
            file_path: Path to file to stage
        """
        if file_path not in self.staged_files:
            self.staged_files.append(file_path)

    def commit(self, message: str) -> str:
        """Create a commit.

        Args:
            message: Commit message

        Returns:
            Commit hash (mock)
        """
        commit_hash = f"abc{len(self.commits):04d}"
        self.commits.append({
            "hash": commit_hash,
            "message": message,
            "branch": self.current_branch,
            "files": self.staged_files.copy()
        })
        self.staged_files.clear()
        return commit_hash

    def get_commits(self, branch: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get commits.

        Args:
            branch: Optional branch filter

        Returns:
            List of commits
        """
        if branch:
            return [c for c in self.commits if c["branch"] == branch]
        return self.commits


class MockAgentResponse:
    """Mock agent response for testing agent behaviors."""

    def __init__(self, success: bool = True, output: str = "", files_created: Optional[List[str]] = None):
        """Initialize mock agent response.

        Args:
            success: Whether agent succeeded
            output: Agent output/message
            files_created: List of files created by agent
        """
        self.success = success
        self.output = output
        self.files_created = files_created or []
        self.errors: List[str] = []

    def add_error(self, error: str):
        """Add an error message.

        Args:
            error: Error message
        """
        self.errors.append(error)
        self.success = False


def create_mock_agent(agent_name: str, behavior: Optional[Dict[str, Any]] = None) -> Mock:
    """Create a mock agent with specified behavior.

    Args:
        agent_name: Name of agent to mock
        behavior: Optional dict specifying mock behavior
            - "success": bool (default True)
            - "output": str
            - "files": List[str] of files to create
            - "side_effect": callable

    Returns:
        Mock agent object
    """
    behavior = behavior or {}

    agent = MagicMock(name=agent_name)
    agent.name = agent_name

    # Default behavior: success with empty output
    response = MockAgentResponse(
        success=behavior.get("success", True),
        output=behavior.get("output", f"{agent_name} executed successfully"),
        files_created=behavior.get("files", [])
    )

    if "side_effect" in behavior:
        agent.execute.side_effect = behavior["side_effect"]
    else:
        agent.execute.return_value = response

    return agent


def create_agent_chain(*agent_mocks: Mock) -> List[Mock]:
    """Create a chain of agents that execute in sequence.

    Args:
        *agent_mocks: Agent mocks to chain

    Returns:
        List of chained agents
    """
    return list(agent_mocks)


def simulate_agent_workflow(agents: List[Mock], initial_state: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate a workflow of multiple agents.

    Args:
        agents: List of agent mocks
        initial_state: Initial workflow state

    Returns:
        Final workflow state
    """
    state = initial_state.copy()

    for agent in agents:
        result = agent.execute(state)
        if hasattr(result, 'success') and not result.success:
            state["failed_agent"] = agent.name
            state["errors"] = getattr(result, 'errors', [])
            break
        if hasattr(result, 'files_created'):
            state.setdefault("files_created", []).extend(result.files_created)

    return state
