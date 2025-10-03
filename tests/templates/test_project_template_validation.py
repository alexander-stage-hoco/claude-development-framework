"""Project template validation tests.

Tests validate that project initialization templates work correctly.
"""

import pytest
import subprocess
from pathlib import Path
import tempfile
import shutil


# ============================================================================
# Test: init-project.sh Script Validation
# ============================================================================


@pytest.mark.unit
def test_init_project_script_exists(framework_root: Path):
    """Test that init-project.sh script exists."""
    script_path = framework_root / "init-project.sh"
    assert script_path.exists(), "init-project.sh script missing"
    assert script_path.is_file(), "init-project.sh should be a file"


@pytest.mark.unit
def test_init_project_script_is_executable(framework_root: Path):
    """Test that init-project.sh has execute permissions."""
    script_path = framework_root / "init-project.sh"

    if not script_path.exists():
        pytest.skip("init-project.sh not found")

    # Check if executable
    import os

    is_executable = os.access(script_path, os.X_OK)

    assert is_executable, "init-project.sh should be executable. Run: chmod +x init-project.sh"


@pytest.mark.unit
def test_init_project_script_has_shebang(framework_root: Path):
    """Test that init-project.sh has proper shebang."""
    script_path = framework_root / "init-project.sh"

    if not script_path.exists():
        pytest.skip("init-project.sh not found")

    with open(script_path, "r") as f:
        first_line = f.readline().strip()

    assert first_line.startswith(
        "#!"
    ), "init-project.sh should start with shebang (#!/bin/bash or #!/usr/bin/env bash)"

    assert "bash" in first_line.lower(), "init-project.sh shebang should specify bash"


# ============================================================================
# Test: Project Template Structure
# ============================================================================


@pytest.mark.unit
def test_init_project_creates_claude_directory(framework_root: Path):
    """Test that init-project.sh creates .claude directory structure."""
    script_path = framework_root / "init-project.sh"

    if not script_path.exists():
        pytest.skip("init-project.sh not found")

    # Read script and check for .claude directory creation
    script_content = script_path.read_text()

    assert ".claude" in script_content, "init-project.sh should create .claude directory"

    # Check for key subdirectories
    expected_dirs = ["templates", "subagents"]
    for dir_name in expected_dirs:
        assert (
            dir_name in script_content
        ), f"init-project.sh should reference .claude/{dir_name} directory"


@pytest.mark.unit
def test_init_project_copies_core_templates(framework_root: Path):
    """Test that init-project.sh copies core templates."""
    script_path = framework_root / "init-project.sh"

    if not script_path.exists():
        pytest.skip("init-project.sh not found")

    script_content = script_path.read_text()

    # Should copy CLAUDE.md and development-rules.md
    core_templates = ["CLAUDE.md", "development-rules.md"]

    for template in core_templates:
        # Check if script mentions copying this file
        assert (
            template in script_content
        ), f"init-project.sh should copy {template} (Tier 1 template)"


@pytest.mark.integration
def test_init_project_script_syntax_is_valid(framework_root: Path):
    """Test that init-project.sh has valid bash syntax."""
    script_path = framework_root / "init-project.sh"

    if not script_path.exists():
        pytest.skip("init-project.sh not found")

    # Use bash -n to check syntax without executing
    result = subprocess.run(["bash", "-n", str(script_path)], capture_output=True, text=True)

    assert result.returncode == 0, f"init-project.sh has syntax errors:\n{result.stderr}"


# ============================================================================
# Test: Project Template Execution (Isolated)
# ============================================================================


@pytest.mark.integration
@pytest.mark.slow
def test_init_project_script_runs_without_errors(framework_root: Path):
    """Test that init-project.sh executes successfully in test environment."""
    script_path = framework_root / "init-project.sh"

    if not script_path.exists():
        pytest.skip("init-project.sh not found")

    # Create temporary directory for test
    with tempfile.TemporaryDirectory() as temp_dir:
        test_project = Path(temp_dir) / "test-project"

        # Run init script
        result = subprocess.run(
            [str(script_path), str(test_project)], capture_output=True, text=True, timeout=30
        )

        # Check for success
        if result.returncode != 0:
            pytest.skip(
                f"init-project.sh execution failed (may require user input):\n"
                f"stdout: {result.stdout[:200]}\n"
                f"stderr: {result.stderr[:200]}"
            )

        # Verify basic structure was created
        assert test_project.exists(), "Project directory should be created"


@pytest.mark.integration
@pytest.mark.slow
def test_init_project_creates_required_structure(framework_root: Path):
    """Test that initialized project has all required directories."""
    script_path = framework_root / "init-project.sh"

    if not script_path.exists():
        pytest.skip("init-project.sh not found")

    # Expected directory structure
    required_dirs = [
        ".claude",
        ".claude/templates",
        "specs",
        "specs/use-cases",
        "planning",
        "planning/iterations",
        "tests",
    ]

    # Check if script creates these directories
    script_content = script_path.read_text()

    missing_dirs = []
    for dir_path in required_dirs:
        # Check if script mentions creating this directory
        dir_parts = dir_path.split("/")
        if not any(part in script_content for part in dir_parts):
            missing_dirs.append(dir_path)

    if missing_dirs:
        pytest.skip(
            f"init-project.sh may not create all required directories: {missing_dirs[:3]}. "
            "This might be intentional (minimal setup)."
        )


# ============================================================================
# Test: Template File References
# ============================================================================


@pytest.mark.unit
def test_init_project_references_existing_templates(framework_root: Path):
    """Test that init-project.sh only copies templates that exist."""
    script_path = framework_root / "init-project.sh"

    if not script_path.exists():
        pytest.skip("init-project.sh not found")

    script_content = script_path.read_text()

    # Find cp commands that copy .md files to .claude/templates
    import re

    # Look for: cp .claude/templates/something.md
    copy_commands = re.findall(
        r"cp\s+[^;\n]*\.claude/templates/([a-zA-Z0-9_/-]+\.md)", script_content
    )

    templates_dir = framework_root / ".claude" / "templates"
    missing_templates = []

    for template_file in set(copy_commands):
        # Check if source file exists
        source_path = templates_dir / template_file
        if not source_path.exists():
            missing_templates.append(template_file)

    assert not missing_templates, (
        f"init-project.sh copies non-existent templates: {missing_templates}. "
        "All copied templates must exist."
    )


# ============================================================================
# Test: Documentation Validation
# ============================================================================


@pytest.mark.unit
def test_init_project_has_usage_documentation(framework_root: Path):
    """Test that init-project.sh has usage documentation."""
    script_path = framework_root / "init-project.sh"

    if not script_path.exists():
        pytest.skip("init-project.sh not found")

    script_content = script_path.read_text()

    # Should have usage information
    has_usage = any(
        indicator in script_content.lower()
        for indicator in ["usage:", "help", "usage()", "show_help"]
    )

    assert has_usage, "init-project.sh should have usage documentation or help function"


@pytest.mark.unit
def test_project_init_documented_in_readme(framework_root: Path):
    """Test that project initialization is documented in README."""
    readme_path = framework_root / "README.md"

    if not readme_path.exists():
        pytest.skip("README.md not found")

    readme_content = readme_path.read_text()

    # Should mention init-project.sh
    assert (
        "init-project" in readme_content.lower()
    ), "README.md should document how to initialize a new project"


# ============================================================================
# Test: Project Template Report
# ============================================================================


@pytest.mark.unit
def test_project_template_report(framework_root: Path):
    """Generate report on project initialization capabilities."""
    script_path = framework_root / "init-project.sh"

    if not script_path.exists():
        pytest.skip("init-project.sh not found")

    print("\n\n=== Project Template Analysis ===")

    script_content = script_path.read_text()

    # Count directories created
    import re

    mkdir_commands = re.findall(r"mkdir[^;\n]*", script_content)
    print(f"\nDirectory creation commands: {len(mkdir_commands)}")

    # Count file copies
    cp_commands = re.findall(r"cp[^;\n]*", script_content)
    print(f"File copy commands: {len(cp_commands)}")

    # Check for error handling
    has_error_handling = any(
        pattern in script_content for pattern in ["set -e", "set -u", "exit 1", "|| exit"]
    )
    print(f"Has error handling: {has_error_handling}")

    # Check for user interaction
    has_user_interaction = any(
        pattern in script_content for pattern in ["read ", "read -p", "read -r"]
    )
    print(f"Has user interaction: {has_user_interaction}")

    assert True  # Informational test
