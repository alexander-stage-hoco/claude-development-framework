"""
Test generation and execution commands.

Handles: claude-dev test [generate|run|coverage]
"""

import click
import subprocess
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel

from claude_dev.utils.config import load_config

console = Console()


@click.group()
def test():
    """Test generation and execution commands."""
    pass


@test.command()
@click.argument("spec_id")
@click.option(
    "--type",
    "test_type",
    type=click.Choice(["unit", "integration", "bdd", "all"]),
    default="all",
    help="Type of tests to generate"
)
def generate(spec_id: str, test_type: str):
    """
    Generate tests from specification using test-writer agent.

    Examples:

        # Generate all tests for UC-001
        claude-dev test generate UC-001

        # Generate only unit tests
        claude-dev test generate UC-001 --type unit
    """
    console.print(Panel(
        f"[bold cyan]Generating Tests[/bold cyan]\n\n"
        f"Specification: [green]{spec_id}[/green]\n"
        f"Test Type: [green]{test_type}[/green]\n\n"
        f"[yellow]Note:[/yellow] This command will invoke the test-writer agent.\n"
        f"Agent integration is not yet fully implemented.",
        title="Test Generation",
        border_style="cyan"
    ))

    # TODO: Integrate with test-writer agent
    # For now, show placeholder message
    console.print("\n[yellow]⚠ Agent integration coming soon![/yellow]")
    console.print("For now, manually invoke test-writer agent from Claude session:")
    console.print(f"  @test-writer generate tests for {spec_id}")


@test.command()
@click.argument("path", type=click.Path(exists=True), required=False)
@click.option("--coverage", is_flag=True, help="Show coverage report")
@click.option("--watch", is_flag=True, help="Watch mode for TDD")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def run(path: Optional[str], coverage: bool, watch: bool, verbose: bool):
    """
    Run tests using pytest.

    Examples:

        # Run all tests
        claude-dev test run

        # Run specific test file
        claude-dev test run tests/test_auth.py

        # Run with coverage
        claude-dev test run --coverage

        # Watch mode for TDD
        claude-dev test run --watch
    """
    config = load_config()

    # Determine test path
    if path:
        test_path = Path(path)
    else:
        test_path = config.get_path("tests")

    # Build pytest command
    cmd = ["pytest", str(test_path)]

    if verbose:
        cmd.append("-v")

    if coverage:
        cmd.extend(["--cov=src", "--cov-report=term-missing", "--cov-report=html"])

    if watch:
        # Use pytest-watch if available
        cmd = ["ptw", str(test_path)] + cmd[1:]

    console.print(f"Running: [cyan]{' '.join(cmd)}[/cyan]\n")

    try:
        result = subprocess.run(cmd, check=False)

        if result.returncode == 0:
            console.print("\n[green]✓ All tests passed![/green]")
        else:
            console.print(f"\n[red]✗ Tests failed with exit code {result.returncode}[/red]")

    except FileNotFoundError:
        console.print("[red]Error:[/red] pytest not found. Install it with:")
        console.print("  pip install pytest pytest-cov")
        raise click.Abort()


@test.command()
@click.option(
    "--fail-under",
    type=int,
    default=None,
    help="Fail if coverage is below threshold (default: from config)"
)
def coverage(fail_under: Optional[int]):
    """
    Check test coverage.

    Examples:

        # Check coverage with default threshold
        claude-dev test coverage

        # Check with custom threshold
        claude-dev test coverage --fail-under 90
    """
    config = load_config()

    # Get threshold from config or option
    threshold = fail_under or config.get("defaults.coverage_threshold", 90)

    console.print(f"Checking coverage (threshold: {threshold}%)...\n")

    cmd = [
        "pytest",
        "--cov=src",
        f"--cov-fail-under={threshold}",
        "--cov-report=term-missing",
        "--cov-report=html",
        "tests/"
    ]

    try:
        result = subprocess.run(cmd, check=False)

        if result.returncode == 0:
            console.print(f"\n[green]✓ Coverage meets threshold ({threshold}%)[/green]")
            console.print(f"View detailed report: file://{Path.cwd()}/htmlcov/index.html")
        else:
            console.print(f"\n[red]✗ Coverage below threshold ({threshold}%)[/red]")

    except FileNotFoundError:
        console.print("[red]Error:[/red] pytest not found. Install it with:")
        console.print("  pip install pytest pytest-cov")
        raise click.Abort()
