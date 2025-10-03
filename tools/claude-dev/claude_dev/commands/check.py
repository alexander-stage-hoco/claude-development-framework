"""
Quality check commands.

Handles: claude-dev check [alignment|coverage|quality|all]
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
def check():
    """Quality check commands."""
    pass


@check.command()
@click.option("--report", is_flag=True, help="Generate detailed report")
def alignment(report: bool):
    """
    Check spec-code alignment.

    Verifies:
    - Every use case has a specification
    - Every implementation has corresponding tests
    - BDD features match use cases

    Example:
        claude-dev check alignment --report
    """
    config = load_config()
    project_root = config.get_project_root()

    console.print("[cyan]Checking spec-code alignment...[/cyan]\n")

    # Check if validation script exists
    validation_script = project_root / "scripts" / "validate-traceability.py"

    if validation_script.exists():
        # Run existing validation script
        result = subprocess.run(
            ["python3", str(validation_script)],
            capture_output=True,
            text=True,
        )

        console.print(result.stdout)

        if result.returncode != 0:
            console.print("\n[red]✗ Alignment check failed[/red]")
            if result.stderr:
                console.print(result.stderr)
        else:
            console.print("\n[green]✓ All specs aligned with code[/green]")

    else:
        # Basic manual check
        console.print("[yellow]⚠ Validation script not found. Performing basic check...[/yellow]\n")

        specs_dir = config.get_path("specs")
        tests_dir = config.get_path("tests")

        # Count specs and tests
        uc_specs = (
            list((specs_dir / "use-cases").glob("UC-*.md"))
            if (specs_dir / "use-cases").exists()
            else []
        )
        test_files = list(tests_dir.rglob("test_*.py")) if tests_dir.exists() else []

        console.print(f"Use Cases: {len(uc_specs)}")
        console.print(f"Test Files: {len(test_files)}")

        if len(uc_specs) > 0 and len(test_files) == 0:
            console.print("\n[red]✗ No tests found for use cases[/red]")
        else:
            console.print("\n[green]✓ Basic alignment check passed[/green]")


@check.command()
@click.option("--fail-under", type=int, default=None, help="Fail if coverage is below threshold")
def coverage(fail_under: Optional[int]):
    """
    Check test coverage against threshold.

    Example:
        claude-dev check coverage --fail-under 90
    """
    config = load_config()
    threshold = fail_under or config.get("defaults.coverage_threshold", 90)

    console.print(f"[cyan]Checking test coverage (threshold: {threshold}%)...[/cyan]\n")

    cmd = [
        "pytest",
        "--cov=src",
        f"--cov-fail-under={threshold}",
        "--cov-report=term-missing",
        "tests/",
    ]

    try:
        result = subprocess.run(cmd, check=False)

        if result.returncode == 0:
            console.print(f"\n[green]✓ Coverage meets threshold ({threshold}%)[/green]")
        else:
            console.print(f"\n[red]✗ Coverage below threshold ({threshold}%)[/red]")

    except FileNotFoundError:
        console.print("[red]Error:[/red] pytest not found. Install: pip install pytest pytest-cov")
        raise click.Abort()


@check.command()
@click.option("--fix", is_flag=True, help="Auto-fix issues where possible")
def quality(fix: bool):
    """
    Check code quality (linting, type checking).

    Example:
        claude-dev check quality --fix
    """
    config = load_config()
    linter = config.get("quality.linter", "pylint")
    formatter = config.get("quality.formatter", "black")
    type_checker = config.get("quality.type_checker", "mypy")

    console.print("[cyan]Running code quality checks...[/cyan]\n")

    passed = True

    # Run formatter
    if fix:
        console.print(f"[dim]Running {formatter}...[/dim]")
        try:
            subprocess.run([formatter, "src/", "tests/"], check=False)
            console.print(f"[green]✓ {formatter} completed[/green]")
        except FileNotFoundError:
            console.print(f"[yellow]⚠ {formatter} not found[/yellow]")

    # Run linter
    console.print(f"\n[dim]Running {linter}...[/dim]")
    try:
        result = subprocess.run([linter, "src/"], check=False)
        if result.returncode == 0:
            console.print(f"[green]✓ {linter} passed[/green]")
        else:
            console.print(f"[red]✗ {linter} found issues[/red]")
            passed = False
    except FileNotFoundError:
        console.print(f"[yellow]⚠ {linter} not found[/yellow]")

    # Run type checker
    console.print(f"\n[dim]Running {type_checker}...[/dim]")
    try:
        result = subprocess.run([type_checker, "src/", "--ignore-missing-imports"], check=False)
        if result.returncode == 0:
            console.print(f"[green]✓ {type_checker} passed[/green]")
        else:
            console.print(f"[yellow]⚠ {type_checker} found issues (non-blocking)[/yellow]")
    except FileNotFoundError:
        console.print(f"[yellow]⚠ {type_checker} not found[/yellow]")

    if passed:
        console.print("\n[green]✓ Code quality checks passed[/green]")
    else:
        console.print("\n[red]✗ Some quality checks failed[/red]")


@check.command()
def all():
    """
    Run all quality checks.

    Example:
        claude-dev check all
    """
    console.print(Panel("[bold cyan]Running All Quality Checks[/bold cyan]", border_style="cyan"))

    # Run alignment check
    console.print("\n[bold]1. Spec-Code Alignment[/bold]")
    ctx = click.Context(alignment)
    ctx.invoke(alignment, report=False)

    # Run coverage check
    console.print("\n[bold]2. Test Coverage[/bold]")
    ctx = click.Context(coverage)
    ctx.invoke(coverage, fail_under=None)

    # Run quality check
    console.print("\n[bold]3. Code Quality[/bold]")
    ctx = click.Context(quality)
    ctx.invoke(quality, fix=False)

    console.print("\n[bold cyan]All checks completed![/bold cyan]")
