#!/usr/bin/env python3
"""
Pre-commit hook: Enforce test-first development.

Enforces Rule #2: Tests Define Correctness
- Every source file should have corresponding tests
- Block commits of untested code
"""

import sys
from pathlib import Path
from typing import List, Tuple


def find_test_file(source_file: Path, project_root: Path) -> Path | None:
    """
    Find corresponding test file for source file.

    Args:
        source_file: Path to source file
        project_root: Project root directory

    Returns:
        Path to test file if it exists, None otherwise
    """
    # Get relative path from src/
    try:
        rel_path = source_file.relative_to(project_root / "src")
    except ValueError:
        return None

    # Construct test file path
    # src/module/file.py -> tests/unit/test_file.py
    test_filename = f"test_{source_file.stem}.py"

    # Check multiple possible locations
    possible_test_paths = [
        project_root / "tests" / "unit" / rel_path.parent / test_filename,
        project_root / "tests" / rel_path.parent / test_filename,
        project_root / "tests" / test_filename,
    ]

    for test_path in possible_test_paths:
        if test_path.exists():
            return test_path

    return None


def is_trivial_file(source_file: Path) -> bool:
    """
    Check if file is trivial (doesn't need tests).

    Args:
        source_file: Path to source file

    Returns:
        True if file is trivial
    """
    trivial_files = [
        "__init__.py",
        "__main__.py",
        "conftest.py",
        "config.py",  # Often just configuration
    ]

    if source_file.name in trivial_files:
        return True

    # Check if file is very small (likely just imports/constants)
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            lines = [
                line.strip()
                for line in f
                if line.strip()
                and not line.strip().startswith('#')
                and not line.strip().startswith('"""')
                and not line.strip().startswith("'''")
            ]

            # If file has < 10 non-comment lines, likely trivial
            if len(lines) < 10:
                return True

    except (UnicodeDecodeError, IOError):
        pass

    return False


def find_project_root() -> Path:
    """Find project root."""
    current = Path.cwd()

    for parent in [current] + list(current.parents):
        if (parent / ".claude").exists() or (parent / "src").exists():
            return parent

    return current


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        sys.exit(0)

    # Get command line arguments
    strict_mode = "--strict" in sys.argv
    filenames = [arg for arg in sys.argv[1:] if not arg.startswith('--')]

    if not filenames:
        sys.exit(0)

    project_root = find_project_root()
    missing_tests = []

    for filepath in filenames:
        source_file = Path(filepath)

        if not source_file.exists():
            continue

        # Skip if not in src/ directory
        if "src/" not in str(source_file):
            continue

        # Skip trivial files
        if is_trivial_file(source_file):
            continue

        # Check for test file
        test_file = find_test_file(source_file, project_root)

        if test_file is None:
            missing_tests.append(source_file)

    if missing_tests:
        print("❌ Source files without corresponding tests!")
        print()
        print("Claude Development Framework Rule #2: Tests Define Correctness")
        print("Write tests BEFORE implementation (Test-Driven Development).")
        print()

        for source_file in missing_tests:
            rel_path = source_file.relative_to(project_root) if source_file.is_absolute() else source_file
            print(f"  {rel_path}")

            # Suggest test file location
            test_name = f"test_{source_file.stem}.py"
            suggested_path = project_root / "tests" / "unit" / test_name
            print(f"    Create: tests/unit/{test_name}")
        print()

        print("Please:")
        print("  1. Create test files for each source file")
        print("  2. Write failing tests first")
        print("  3. Then implement to make tests pass")
        print("  4. Commit again")
        print()

        if not strict_mode:
            # Allow in normal mode if only a few files
            if len(missing_tests) <= 1:
                print("⚠️  Allowing commit (≤1 missing test in normal mode)")
                sys.exit(0)

        print("To bypass (emergency only): git commit --no-verify")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
