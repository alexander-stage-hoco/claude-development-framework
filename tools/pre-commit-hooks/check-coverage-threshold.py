#!/usr/bin/env python3
"""
Pre-commit hook: Check test coverage threshold.

Enforces Rule #2: Tests Define Correctness
- Maintain minimum test coverage (default: 90%)
"""

import sys
import subprocess
from pathlib import Path


def find_project_root() -> Path:
    """Find project root."""
    current = Path.cwd()

    for parent in [current] + list(current.parents):
        if (parent / ".claude").exists() or (parent / "tests").exists():
            return parent

    return current


def run_coverage(threshold: int = 90) -> tuple[bool, str]:
    """
    Run pytest with coverage.

    Args:
        threshold: Minimum coverage percentage

    Returns:
        Tuple of (passed, output)
    """
    project_root = find_project_root()
    tests_dir = project_root / "tests"
    src_dir = project_root / "src"

    # Check if tests directory exists
    if not tests_dir.exists():
        return True, "No tests directory found (skipping coverage check)"

    # Check if src directory exists
    if not src_dir.exists():
        return True, "No src directory found (skipping coverage check)"

    # Run pytest with coverage
    cmd = [
        "pytest",
        str(tests_dir),
        f"--cov={src_dir}",
        f"--cov-fail-under={threshold}",
        "--cov-report=term-missing:skip-covered",
        "-q",  # Quiet mode
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(project_root),
        )

        output = result.stdout + result.stderr

        return result.returncode == 0, output

    except FileNotFoundError:
        return True, "pytest not found (skipping coverage check)"


def main():
    """Main entry point."""
    # Parse arguments
    threshold = 90  # default
    warn_only = False

    for arg in sys.argv[1:]:
        if arg.startswith("--threshold="):
            threshold = int(arg.split("=")[1])
        elif arg == "--warn-only":
            warn_only = True

    # Run coverage
    passed, output = run_coverage(threshold)

    if not passed:
        if warn_only:
            print(f"⚠️  Warning: Test coverage below {threshold}%")
        else:
            print(f"❌ Test coverage below {threshold}%!")

        print()
        print("Claude Development Framework Rule #2: Tests Define Correctness")
        print(f"Maintain at least {threshold}% test coverage.")
        print()
        print(output)
        print()

        if not warn_only:
            print("Please:")
            print("  1. Add tests to increase coverage")
            print(f"  2. Ensure coverage ≥ {threshold}%")
            print("  3. Commit again")
            print()
            print("To bypass (emergency only): git commit --no-verify")
            sys.exit(1)

    if warn_only:
        print(f"✓ Coverage check passed (warning mode, threshold: {threshold}%)")
    else:
        print(f"✓ Test coverage meets threshold ({threshold}%)")

    sys.exit(0)


if __name__ == "__main__":
    main()
