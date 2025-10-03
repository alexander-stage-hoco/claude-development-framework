#!/usr/bin/env python3
"""
Pre-commit hook: Validate ADR references.

Enforces Rule #7: Technical Decisions Are Binding
- ADR references in code should point to valid ADR files
"""

import sys
import re
from pathlib import Path
from typing import List


def find_adr_references(filepath: Path) -> List[str]:
    """
    Find ADR-XXX references in file.

    Args:
        filepath: Path to file to check

    Returns:
        List of ADR IDs found
    """
    adr_pattern = r"ADR-\d{3,4}"
    adr_refs = set()

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            matches = re.findall(adr_pattern, content)
            adr_refs.update(matches)
    except (UnicodeDecodeError, IOError):
        pass

    return sorted(list(adr_refs))


def check_adr_exists(adr_id: str, specs_dir: Path) -> bool:
    """
    Check if ADR file exists.

    Args:
        adr_id: ADR ID (e.g., "ADR-001")
        specs_dir: Path to specs directory

    Returns:
        True if ADR file exists
    """
    if not specs_dir.exists():
        return False

    adrs_dir = specs_dir / "adrs"
    if not adrs_dir.exists():
        return False

    # Look for ADR-XXX-*.md files
    pattern = f"{adr_id}-*.md"
    matching_files = list(adrs_dir.glob(pattern))

    return len(matching_files) > 0


def find_project_root() -> Path:
    """Find project root."""
    current = Path.cwd()

    for parent in [current] + list(current.parents):
        if (parent / ".claude").exists() or (parent / "specs").exists():
            return parent

    return current


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        sys.exit(0)

    # Get command line arguments
    strict_mode = "--strict" in sys.argv
    filenames = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not filenames:
        sys.exit(0)

    project_root = find_project_root()
    specs_dir = project_root / "specs"

    missing_adrs = []

    for filepath in filenames:
        file_path = Path(filepath)

        if not file_path.exists():
            continue

        adr_refs = find_adr_references(file_path)

        for adr_id in adr_refs:
            if not check_adr_exists(adr_id, specs_dir):
                missing_adrs.append((file_path, adr_id))

    if missing_adrs:
        print("❌ Missing ADR files for references in code!")
        print()
        print("Claude Development Framework Rule #7: Technical Decisions Are Binding")
        print("Every ADR reference should have a corresponding decision record.")
        print()

        for filepath, adr_id in missing_adrs:
            rel_path = filepath.relative_to(project_root) if filepath.is_absolute() else filepath
            print(f"  {rel_path}: {adr_id}")
            print(f"    Expected: specs/adrs/{adr_id}-*.md")
        print()

        if not strict_mode:
            # In normal mode, just warn if only a few missing
            if len(missing_adrs) <= 2:
                print("⚠️  Warning: Missing ADRs (allowing in normal mode)")
                sys.exit(0)

        print("Please:")
        print("  1. Create ADR files for missing references")
        print("  2. Or remove ADR references from code")
        print("  3. Commit again")
        print()
        print("To bypass (emergency only): git commit --no-verify")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
