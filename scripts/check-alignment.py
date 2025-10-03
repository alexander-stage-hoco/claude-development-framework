#!/usr/bin/env python3
"""
Claude Development Framework - Spec-Code Alignment Checker
Version: 2.0
Purpose: Validate alignment between use case specifications and BDD tests

This tool detects spec-code drift by comparing:
- Use case acceptance criteria vs BDD scenarios
- Scenario counts vs criteria counts
- Orphaned implementations (tests without specs)

Exit Codes:
    0 - Perfect alignment (no issues)
    1 - Alignment issues found (drift detected)
    2 - Invalid usage or file system errors

Usage:
    ./scripts/check-alignment.py
    ./scripts/check-alignment.py --specs specs/use-cases --bdd tests/bdd
    ./scripts/check-alignment.py --verbose
"""

import sys
from pathlib import Path
from typing import List

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from alignment import UseCase, BDDFeature, AlignmentParser, AlignmentValidator, AlignmentIssue


def print_header():
    """Print validation header."""
    print("=" * 60)
    print("Claude Framework - Spec-Code Alignment Checker")
    print("=" * 60)
    print()


def print_summary(use_cases: dict, bdd_features: dict):
    """Print summary of parsed files."""
    print(f"📋 Use Cases Found: {len(use_cases)}")
    for uc_id, uc in sorted(use_cases.items()):
        print(f"   - {uc_id}: {len(uc.acceptance_criteria)} acceptance criteria")
    print()

    print(f"🧪 BDD Features Found: {len(bdd_features)}")
    for feature_name, feature in sorted(bdd_features.items()):
        uc_ref = f" (→ {feature.uc_reference})" if feature.uc_reference else ""
        print(f"   - {feature_name}: {len(feature.scenarios)} scenarios{uc_ref}")
    print()


def print_issues(issues: List[AlignmentIssue]):
    """Print alignment issues grouped by type."""
    if not issues:
        print("✅ PERFECT ALIGNMENT - No issues found!")
        print()
        print("All use cases have corresponding BDD files with matching scenario counts.")
        return

    print(f"⚠️  ALIGNMENT ISSUES FOUND: {len(issues)}")
    print()

    # Group by issue type
    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]

    if errors:
        print("🚨 ERRORS (must fix):")
        print()
        for issue in errors:
            print(f"  ❌ {issue.message}")
            if issue.uc_id:
                print(f"     UC: {issue.uc_id}")
            if issue.feature_name:
                print(f"     Feature: {issue.feature_name}")
            print()

    if warnings:
        print("⚠️  WARNINGS (review recommended):")
        print()
        for issue in warnings:
            print(f"  ⚠️  {issue.message}")
            if issue.uc_id:
                print(f"     UC: {issue.uc_id}")
            if issue.feature_name:
                print(f"     Feature: {issue.feature_name}")
            print()


def print_issue_explanations():
    """Print explanations for each issue type."""
    print("=" * 60)
    print("Issue Type Explanations")
    print("=" * 60)
    print()
    print("📖 missing_bdd (ERROR):")
    print("   Use case has acceptance criteria but no BDD feature file.")
    print("   Fix: Create BDD feature file in tests/bdd/ with scenarios.")
    print()
    print("📖 orphaned_feature (WARNING):")
    print("   BDD feature exists but doesn't reference any use case.")
    print("   Fix: Add UC reference to feature file or use case spec.")
    print()
    print("📖 count_mismatch (WARNING):")
    print("   Number of BDD scenarios doesn't match acceptance criteria count.")
    print("   Fix: Ensure each criterion has a corresponding scenario.")
    print()
    print("📖 broken_bdd_ref (ERROR):")
    print("   Use case references a BDD file that doesn't exist.")
    print("   Fix: Create the referenced file or update the reference.")
    print()
    print("📖 broken_uc_ref (ERROR):")
    print("   BDD feature references a use case that doesn't exist.")
    print("   Fix: Create the use case or update the BDD file reference.")
    print()


def print_usage():
    """Print usage information."""
    print("Usage:")
    print("  ./scripts/check-alignment.py [options]")
    print()
    print("Options:")
    print("  --specs DIR      Use case directory (default: specs/use-cases)")
    print("  --bdd DIR        BDD feature directory (default: tests/bdd)")
    print("  --verbose        Show detailed output")
    print("  --explain        Show issue type explanations")
    print("  --help           Show this help message")
    print()
    print("Examples:")
    print("  ./scripts/check-alignment.py")
    print("  ./scripts/check-alignment.py --verbose")
    print("  ./scripts/check-alignment.py --specs planning/use-cases --bdd tests/features")
    print()


def main():
    """Main validation routine."""
    # Parse arguments
    args = sys.argv[1:]

    if "--help" in args:
        print_usage()
        return 0

    if "--explain" in args:
        print_issue_explanations()
        return 0

    verbose = "--verbose" in args

    # Determine directories
    uc_dir = Path("specs/use-cases")
    bdd_dir = Path("tests/bdd")

    if "--specs" in args:
        idx = args.index("--specs")
        if idx + 1 < len(args):
            uc_dir = Path(args[idx + 1])

    if "--bdd" in args:
        idx = args.index("--bdd")
        if idx + 1 < len(args):
            bdd_dir = Path(args[idx + 1])

    # Validate directories exist
    if not uc_dir.exists():
        print(f"❌ ERROR: Use case directory not found: {uc_dir}")
        print(f"   This might be a template repository without project files yet.")
        print(f"   Run this command from a project root directory.")
        print()
        return 2

    if not bdd_dir.exists():
        print(f"⚠️  WARNING: BDD directory not found: {bdd_dir}")
        print(f"   Creating placeholder directory...")
        bdd_dir.mkdir(parents=True, exist_ok=True)

    # Print header
    print_header()

    # Parse files
    print("🔍 Parsing use case specifications...")
    parser = AlignmentParser()
    use_cases = parser.parse_use_cases(uc_dir)
    print(f"   Found {len(use_cases)} use cases")
    print()

    print("🔍 Parsing BDD feature files...")
    bdd_features = parser.parse_bdd_features(bdd_dir)
    print(f"   Found {len(bdd_features)} features")
    print()

    # Show summary if verbose
    if verbose:
        print_summary(use_cases, bdd_features)

    # Validate alignment
    print("🔬 Validating alignment...")
    validator = AlignmentValidator()
    issues = validator.validate(use_cases, bdd_features)
    print()

    # Print results
    print("=" * 60)
    print("Validation Results")
    print("=" * 60)
    print()

    print_issues(issues)

    # Print footer
    print("=" * 60)

    if not issues:
        print("Status: ✅ ALIGNED")
        print()
        print("Recommendation: No action needed. Specs and tests are in sync.")
        return 0
    else:
        errors = [i for i in issues if i.severity == "error"]
        warnings = [i for i in issues if i.severity == "warning"]

        print(f"Status: ⚠️  DRIFT DETECTED ({len(errors)} errors, {len(warnings)} warnings)")
        print()
        print("Recommendation:")
        if errors:
            print("  1. Fix all errors (missing BDD files, broken references)")
        if warnings:
            print("  2. Review warnings (count mismatches, orphaned features)")
        print("  3. Run again to verify fixes")
        print()
        print("Run './scripts/check-alignment.py --explain' for issue type details")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print()
        print("❌ Validation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print()
        print(f"❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(2)
