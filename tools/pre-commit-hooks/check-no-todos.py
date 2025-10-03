#!/usr/bin/env python3
"""
Pre-commit hook: Block TODO comments in source code.

Enforces Rule #6: No Shortcuts
- TODO comments should become issues/tasks
- Prevents technical debt from accumulating
"""

import sys
import re
from pathlib import Path


def check_file_for_todos(filepath: str) -> tuple[bool, list[str]]:
    """
    Check file for TODO comments.

    Args:
        filepath: Path to file to check

    Returns:
        Tuple of (has_todos, list of TODO lines)
    """
    todos = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                # Match TODO comments (case-insensitive)
                if re.search(r"#\s*TODO", line, re.IGNORECASE):
                    todos.append(f"  Line {line_num}: {line.strip()}")

    except (UnicodeDecodeError, IOError):
        # Skip binary files or files we can't read
        return False, []

    return len(todos) > 0, todos


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: check-no-todos.py <file1> [file2 ...]")
        sys.exit(0)

    files_with_todos = []

    for filepath in sys.argv[1:]:
        if not Path(filepath).exists():
            continue

        has_todos, todo_lines = check_file_for_todos(filepath)

        if has_todos:
            files_with_todos.append((filepath, todo_lines))

    if files_with_todos:
        print("❌ TODO comments found in source code!")
        print()
        print("Claude Development Framework Rule #6: No Shortcuts")
        print("TODO comments should become issues or tasks instead.")
        print()

        for filepath, todo_lines in files_with_todos:
            print(f"File: {filepath}")
            for line in todo_lines:
                print(line)
            print()

        print("Please:")
        print("  1. Create an issue for each TODO")
        print("  2. Remove TODO comments from code")
        print("  3. Commit again")
        print()
        print("To bypass (emergency only): git commit --no-verify")

        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
