"""
Planning commands for iterations and milestones.

Handles: claude-dev plan [iteration|milestone|current|list]
"""

import click
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from claude_dev.utils.config import load_config
from claude_dev.utils.file_ops import find_files

console = Console()


@click.group()
def plan():
    """Planning commands for iterations and milestones."""
    pass


@plan.command()
@click.option("--milestone", help="Parent milestone ID")
@click.option("--scope", help="Brief scope description")
def iteration(milestone: Optional[str], scope: Optional[str]):
    """
    Plan a new iteration (1-3 hour scope).

    Examples:

        # Plan new iteration
        claude-dev plan iteration

        # Plan iteration for specific milestone
        claude-dev plan iteration --milestone M1

        # Plan with scope
        claude-dev plan iteration --scope "Implement user authentication"
    """
    console.print(Panel(
        f"[bold cyan]Planning New Iteration[/bold cyan]\n\n"
        f"Milestone: [green]{milestone or 'N/A'}[/green]\n"
        f"Scope: [green]{scope or 'To be defined'}[/green]\n\n"
        f"[yellow]Note:[/yellow] This command will invoke the iteration-planner agent.\n"
        f"Agent integration is not yet fully implemented.",
        title="Iteration Planning",
        border_style="cyan"
    ))

    # TODO: Integrate with iteration-planner agent
    console.print("\n[yellow]⚠ Agent integration coming soon![/yellow]")
    console.print("For now, manually invoke iteration-planner agent from Claude session:")
    console.print(f"  @iteration-planner create iteration{f' for milestone {milestone}' if milestone else ''}")


@plan.command()
@click.option("--use-cases", help="Comma-separated list of use case IDs")
@click.option("--title", help="Milestone title")
def milestone(use_cases: Optional[str], title: Optional[str]):
    """
    Plan a new milestone.

    Examples:

        # Plan new milestone
        claude-dev plan milestone

        # Plan milestone with scope
        claude-dev plan milestone --use-cases UC-001,UC-002 --title "Authentication"
    """
    console.print(Panel(
        f"[bold cyan]Planning New Milestone[/bold cyan]\n\n"
        f"Title: [green]{title or 'To be defined'}[/green]\n"
        f"Use Cases: [green]{use_cases or 'To be defined'}[/green]\n\n"
        f"[yellow]Note:[/yellow] This command will invoke the iteration-planner agent.\n"
        f"Agent integration is not yet fully implemented.",
        title="Milestone Planning",
        border_style="cyan"
    ))

    # TODO: Integrate with iteration-planner agent
    console.print("\n[yellow]⚠ Agent integration coming soon![/yellow]")
    console.print("For now, manually create milestone file in planning/milestones/")


@plan.command()
def current():
    """
    Show current iteration details.

    Example:
        claude-dev plan current
    """
    config = load_config()
    planning_dir = config.get_path("planning")

    current_file = planning_dir / "current-iteration.md"

    if not current_file.exists():
        console.print("[yellow]No current iteration.[/yellow]")
        console.print("\nStart a new iteration with:")
        console.print("  [cyan]claude-dev plan iteration[/cyan]")
        return

    # Read current iteration
    with open(current_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Display content
    console.print(Panel(
        content[:1000] + ("..." if len(content) > 1000 else ""),
        title="Current Iteration",
        border_style="cyan"
    ))

    console.print(f"\nFull file: [cyan]{current_file}[/cyan]")


@plan.command()
@click.option(
    "--status",
    type=click.Choice(["active", "completed", "all"]),
    default="all",
    help="Filter by status"
)
def list(status: str):
    """
    List all iterations.

    Examples:

        # List all iterations
        claude-dev plan list

        # List only active iterations
        claude-dev plan list --status active

        # List completed iterations
        claude-dev plan list --status completed
    """
    config = load_config()
    planning_dir = config.get_path("planning")

    if not planning_dir.exists():
        console.print("[yellow]No planning directory found.[/yellow]")
        return

    # Find iteration files
    iteration_files = find_files(planning_dir, "iteration-*.md", recursive=False)

    if not iteration_files:
        console.print("[yellow]No iterations found.[/yellow]")
        return

    table = Table(title="Iterations")
    table.add_column("Iteration", style="cyan", no_wrap=True)
    table.add_column("Status", style="magenta")
    table.add_column("File", style="dim")

    for iteration_file in sorted(iteration_files):
        iteration_name = iteration_file.stem

        # Try to read status from file (basic parsing)
        with open(iteration_file, "r", encoding="utf-8") as f:
            content = f.read()
            if "Status: Completed" in content or "Status: ✓" in content:
                iter_status = "completed"
            elif "Status: Active" in content or "Status: In Progress" in content:
                iter_status = "active"
            else:
                iter_status = "unknown"

        # Filter by status
        if status != "all" and iter_status != status:
            continue

        table.add_row(
            iteration_name,
            iter_status.title(),
            str(iteration_file.relative_to(config.get_project_root()))
        )

    console.print(table)
