"""
File operation utilities.

Provides helpers for creating directories, files, and handling templates.
"""

import os
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime


def ensure_dir(path: Path) -> Path:
    """
    Ensure directory exists, create if necessary.

    Args:
        path: Directory path

    Returns:
        Path to directory
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def create_file(path: Path, content: str, overwrite: bool = False, backup: bool = True) -> bool:
    """
    Create file with content.

    Args:
        path: File path
        content: File content
        overwrite: Whether to overwrite existing file
        backup: Whether to create backup of existing file

    Returns:
        True if file was created, False if file exists and overwrite=False

    Raises:
        FileExistsError: If file exists and overwrite=False
    """
    if path.exists() and not overwrite:
        return False

    # Create backup if file exists and backup=True
    if path.exists() and backup:
        backup_path = path.with_suffix(path.suffix + ".bak")
        shutil.copy2(path, backup_path)

    # Ensure parent directory exists
    ensure_dir(path.parent)

    # Write content
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return True


def read_file(path: Path) -> Optional[str]:
    """
    Read file content.

    Args:
        path: File path

    Returns:
        File content or None if file doesn't exist
    """
    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def copy_directory(src: Path, dst: Path, exclude: Optional[list] = None) -> None:
    """
    Copy directory recursively.

    Args:
        src: Source directory
        dst: Destination directory
        exclude: List of patterns to exclude
    """
    exclude = exclude or []

    if not src.exists():
        raise FileNotFoundError(f"Source directory not found: {src}")

    ensure_dir(dst)

    for item in src.iterdir():
        # Check if item should be excluded
        if any(pattern in str(item) for pattern in exclude):
            continue

        dst_item = dst / item.name

        if item.is_dir():
            copy_directory(item, dst_item, exclude)
        else:
            shutil.copy2(item, dst_item)


def find_files(root: Path, pattern: str = "*", recursive: bool = True) -> list[Path]:
    """
    Find files matching pattern.

    Args:
        root: Root directory to search
        pattern: Glob pattern
        recursive: Whether to search recursively

    Returns:
        List of matching file paths
    """
    if not root.exists():
        return []

    if recursive:
        return list(root.rglob(pattern))
    else:
        return list(root.glob(pattern))


def open_in_editor(path: Path, editor: Optional[str] = None) -> None:
    """
    Open file in editor.

    Args:
        path: File path
        editor: Editor command (defaults to $EDITOR or vim)
    """
    editor = editor or os.environ.get("EDITOR", "vim")

    # Use os.system to open editor
    os.system(f"{editor} {path}")


def get_relative_path(path: Path, base: Path) -> Path:
    """
    Get relative path from base.

    Args:
        path: Absolute path
        base: Base path

    Returns:
        Relative path
    """
    try:
        return path.relative_to(base)
    except ValueError:
        # Path is not relative to base
        return path


def format_file_size(size: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size: Size in bytes

    Returns:
        Formatted size string
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def get_file_age(path: Path) -> str:
    """
    Get file age as human-readable string.

    Args:
        path: File path

    Returns:
        Age string (e.g., "2 hours ago", "3 days ago")
    """
    if not path.exists():
        return "unknown"

    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    now = datetime.now()
    delta = now - mtime

    if delta.days > 365:
        years = delta.days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"
    elif delta.days > 30:
        months = delta.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    elif delta.days > 0:
        return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
    elif delta.seconds > 3600:
        hours = delta.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif delta.seconds > 60:
        minutes = delta.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "just now"
