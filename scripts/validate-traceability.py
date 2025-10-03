#!/usr/bin/env python3
"""
UC-Service Traceability Validator
Enforces Rule #1: Every use case must reference services

Usage:
    python3 scripts/validate-traceability.py

Returns:
    Exit code 0: All checks passed
    Exit code 1: Issues found
"""

import sys
from pathlib import Path

# Add lib directory to path
script_dir = Path(__file__).parent
lib_dir = script_dir / "lib"
sys.path.insert(0, str(lib_dir))

from traceability import TraceabilityParser, TraceabilityValidator, format_report


def main():
    # Find project root (current working directory)
    project_root = Path.cwd()

    uc_dir = project_root / "specs" / "use-cases"
    services_dir = project_root / "services"

    print("🔍 UC-Service Traceability Validator")
    print("=" * 60)
    print()

    # Check if directories exist
    if not uc_dir.exists():
        print(f"⚠️  Use cases directory not found: {uc_dir}")
        print("   This might be a template or new project.")
        print("   Skipping validation.")
        print()
        return 0

    # Parse files
    print(f"📁 Analyzing project at: {project_root}")
    print(f"   Use cases: {uc_dir}")
    print(f"   Services: {services_dir if services_dir.exists() else '(not created yet)'}")
    print()

    parser = TraceabilityParser()
    use_cases = parser.parse_use_cases(uc_dir)
    services = parser.parse_services(services_dir) if services_dir.exists() else []

    if not use_cases:
        print("ℹ️  No use cases found yet.")
        print("   Create use cases in specs/use-cases/ to enable validation.")
        print()
        return 0

    print(f"📊 Found:")
    print(f"   - {len(use_cases)} use cases")
    print(f"   - {len(services)} services")
    print()

    # Validate
    validator = TraceabilityValidator()
    issues = validator.validate(use_cases, services)

    # Generate report
    report = format_report(use_cases, services, issues)
    print(report)

    # Return exit code
    has_issues = any(issues.values())
    if has_issues:
        print("❌ Traceability validation FAILED")
        print()
        print("Fix these issues before proceeding with implementation.")
        print()
        return 1
    else:
        print("✅ Traceability validation PASSED")
        print()
        return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nValidation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
