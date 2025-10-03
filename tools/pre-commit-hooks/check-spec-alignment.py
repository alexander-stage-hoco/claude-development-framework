#!/usr/bin/env python3
"""
Pre-commit hook: Check spec-code alignment.

Enforces Rule #1: Specifications Are Law
- Every implementation should have a corresponding spec
- UC references in code should have valid spec files
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple


def find_uc_references(filepath: Path) -> List[str]:
    """
    Find UC-XXX references in file.

    Args:
        filepath: Path to file to check

    Returns:
        List of UC IDs found (e.g., ["UC-001", "UC-042"])
    """
    uc_pattern = r"UC-\d{3,4}"
    uc_refs = set()

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            matches = re.findall(uc_pattern, content)
            uc_refs.update(matches)
    except (UnicodeDecodeError, IOError):
        pass

    return sorted(list(uc_refs))


def check_spec_exists(uc_id: str, specs_dir: Path) -> bool:
    """
    Check if spec file exists for UC ID.

    Args:
        uc_id: Use case ID (e.g., "UC-001")
        specs_dir: Path to specs directory

    Returns:
        True if spec file exists
    """
    if not specs_dir.exists():
        return False

    use_cases_dir = specs_dir / "use-cases"
    if not use_cases_dir.exists():
        return False

    # Look for UC-XXX-*.md files
    pattern = f"{uc_id}-*.md"
    matching_files = list(use_cases_dir.glob(pattern))

    return len(matching_files) > 0


def find_project_root() -> Path:
    """
    Find project root (contains .claude/ or specs/ directory).

    Returns:
        Path to project root
    """
    current = Path.cwd()

    # Walk up to find project root
    for parent in [current] + list(current.parents):
        if (parent / ".claude").exists() or (parent / "specs").exists():
            return parent

    return current


def main():
    """Main entry point."""
    # Get command line arguments
    strict_mode = "--strict" in sys.argv
    warn_only = "--warn-only" in sys.argv

    # Find project root
    project_root = find_project_root()
    specs_dir = project_root / "specs"

    # Find all Python files with UC references
    src_dir = project_root / "src"
    if not src_dir.exists():
        # No src directory, skip check
        sys.exit(0)

    missing_specs = []

    # Scan source files for UC references
    for py_file in src_dir.rglob("*.py"):
        uc_refs = find_uc_references(py_file)

        for uc_id in uc_refs:
            if not check_spec_exists(uc_id, specs_dir):
                missing_specs.append((py_file.relative_to(project_root), uc_id))

    if missing_specs:
        if warn_only:
            print("⚠️  Warning: Missing spec files for UC references")
        else:
            print("❌ Missing spec files for UC references!")

        print()
        print("Claude Development Framework Rule #1: Specifications Are Law")
        print("Every UC reference should have a corresponding specification.")
        print()

        for filepath, uc_id in missing_specs:
            print(f"  {filepath}: {uc_id}")
            print(f"    Expected: specs/use-cases/{uc_id}-*.md")
        print()

        if not warn_only:
            print("Please:")
            print("  1. Create spec files for missing UCs")
            print("  2. Or remove UC references from code")
            print("  3. Commit again")
            print()
            print("To bypass (emergency only): git commit --no-verify")

            if not strict_mode:
                # In non-strict mode, allow if only a few missing
                if len(missing_specs) <= 2:
                    print()
                    print("⚠️  Allowing commit (≤2 missing specs in normal mode)")
                    sys.exit(0)

            sys.exit(1)

    if warn_only:
        print("✓ Spec alignment check passed (warning mode)")
    else:
        print("✓ All UC references have corresponding specs")

    sys.exit(0)


if __name__ == "__main__":
    main()
