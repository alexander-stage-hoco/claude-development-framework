"""
Input validation utilities.

Validates user inputs like IDs, names, paths, etc.
"""

import re
from pathlib import Path
from typing import Optional


def validate_id(id_value: str, id_type: str = "UC") -> tuple[bool, Optional[str]]:
    """
    Validate ID format (UC-001, SVC-001, ADR-001, etc.).

    Args:
        id_value: ID to validate
        id_type: Expected ID type (UC, SVC, ADR, etc.)

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Pattern: TYPE-NNN or TYPE-NNNN
    pattern = rf"^{id_type}-\d{{3,4}}$"

    if not re.match(pattern, id_value):
        return False, f"Invalid {id_type} ID format. Expected: {id_type}-001 to {id_type}-9999"

    return True, None


def validate_project_name(name: str) -> tuple[bool, Optional[str]]:
    """
    Validate project name.

    Args:
        name: Project name to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Must be valid directory name
    # Only lowercase letters, numbers, hyphens, underscores
    pattern = r"^[a-z0-9][a-z0-9_-]*[a-z0-9]$"

    if not name:
        return False, "Project name cannot be empty"

    if len(name) < 2:
        return False, "Project name must be at least 2 characters"

    if len(name) > 50:
        return False, "Project name must be less than 50 characters"

    if not re.match(pattern, name):
        return False, (
            "Project name must contain only lowercase letters, numbers, "
            "hyphens, and underscores. Must start and end with letter or number."
        )

    return True, None


def validate_spec_title(title: str) -> tuple[bool, Optional[str]]:
    """
    Validate specification title.

    Args:
        title: Title to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not title:
        return False, "Title cannot be empty"

    if len(title) < 5:
        return False, "Title must be at least 5 characters"

    if len(title) > 100:
        return False, "Title must be less than 100 characters"

    return True, None


def validate_path(
    path: Path, must_exist: bool = False, must_be_dir: bool = False
) -> tuple[bool, Optional[str]]:
    """
    Validate file/directory path.

    Args:
        path: Path to validate
        must_exist: Whether path must exist
        must_be_dir: Whether path must be a directory

    Returns:
        Tuple of (is_valid, error_message)
    """
    if must_exist and not path.exists():
        return False, f"Path does not exist: {path}"

    if must_be_dir and path.exists() and not path.is_dir():
        return False, f"Path is not a directory: {path}"

    return True, None


def validate_coverage_threshold(threshold: int) -> tuple[bool, Optional[str]]:
    """
    Validate coverage threshold.

    Args:
        threshold: Coverage threshold (0-100)

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(threshold, int):
        return False, "Coverage threshold must be an integer"

    if threshold < 0 or threshold > 100:
        return False, "Coverage threshold must be between 0 and 100"

    return True, None


def validate_iteration_scope(hours: float) -> tuple[bool, Optional[str]]:
    """
    Validate iteration scope is within framework limits (1-3 hours).

    Args:
        hours: Estimated hours

    Returns:
        Tuple of (is_valid, error_message)
    """
    if hours < 1:
        return False, "Iteration scope must be at least 1 hour"

    if hours > 3:
        return False, "Iteration scope must not exceed 3 hours (framework rule)"

    return True, None


def validate_agent_name(name: str, valid_agents: Optional[list[str]] = None) -> tuple[bool, Optional[str]]:
    """
    Validate agent name.

    Args:
        name: Agent name to validate
        valid_agents: Optional list of valid agent names

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Agent name cannot be empty"

    if valid_agents and name not in valid_agents:
        return False, f"Unknown agent: {name}. Valid agents: {', '.join(valid_agents)}"

    return True, None


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', "", filename)

    # Replace spaces with hyphens
    filename = filename.replace(" ", "-")

    # Remove consecutive hyphens
    filename = re.sub(r"-+", "-", filename)

    # Remove leading/trailing hyphens
    filename = filename.strip("-")

    return filename


def parse_id(id_value: str) -> tuple[str, int]:
    """
    Parse ID into type and number.

    Args:
        id_value: ID to parse (e.g., "UC-001")

    Returns:
        Tuple of (type, number)

    Example:
        >>> parse_id("UC-001")
        ("UC", 1)
        >>> parse_id("SVC-042")
        ("SVC", 42)
    """
    parts = id_value.split("-")
    if len(parts) != 2:
        raise ValueError(f"Invalid ID format: {id_value}")

    id_type = parts[0]
    id_number = int(parts[1])

    return id_type, id_number


def format_id(id_type: str, number: int, width: int = 3) -> str:
    """
    Format ID with proper padding.

    Args:
        id_type: ID type (UC, SVC, ADR, etc.)
        number: ID number
        width: Number width (default: 3)

    Returns:
        Formatted ID

    Example:
        >>> format_id("UC", 1)
        "UC-001"
        >>> format_id("SVC", 42)
        "SVC-042"
    """
    return f"{id_type}-{number:0{width}d}"
