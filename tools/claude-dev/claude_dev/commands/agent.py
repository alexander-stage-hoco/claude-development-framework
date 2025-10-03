"""
Agent invocation commands.

Handles: claude-dev agent [run|list|info]
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
def agent():
    """Agent invocation and management commands."""
    pass


@agent.command()
@click.argument("agent_name")
@click.option("--spec", help="Specification ID for context")
@click.option("--output", type=click.Path(), help="Output file path")
def run(agent_name: str, spec: Optional[str], output: Optional[str]):
    """
    Invoke a specific agent.

    Examples:

        # Invoke test-writer agent
        claude-dev agent run test-writer --spec UC-001

        # Invoke with output file
        claude-dev agent run adr-manager --output specs/adrs/ADR-001.md
    """
    console.print(Panel(
        f"[bold cyan]Invoking Agent[/bold cyan]\n\n"
        f"Agent: [green]{agent_name}[/green]\n"
        f"Context: [green]{spec or 'N/A'}[/green]\n"
        f"Output: [green]{output or 'stdout'}[/green]\n\n"
        f"[yellow]Note:[/yellow] Direct agent invocation requires Claude API access.\n"
        f"This feature is not yet fully implemented.",
        title="Agent Invocation",
        border_style="cyan"
    ))

    # TODO: Implement agent invocation via Claude API
    console.print("\n[yellow]⚠ Agent invocation coming soon![/yellow]")
    console.print("\nFor now, invoke agents from Claude session:")
    console.print(f"  @{agent_name} {spec if spec else ''}")


@agent.command()
@click.option(
    "--tier",
    type=click.Choice(["1", "2", "3", "all"]),
    default="all",
    help="Filter by tier"
)
def list(tier: str):
    """
    List available agents.

    Examples:

        # List all agents
        claude-dev agent list

        # List Tier 1 agents only
        claude-dev agent list --tier 1
    """
    config = load_config()
    project_root = config.get_project_root()

    # Find agent files
    agents_dir = project_root / ".claude" / "agents"

    if not agents_dir.exists():
        console.print("[yellow]No agents directory found.[/yellow]")
        console.print("\nAre you in a Claude Development Framework project?")
        return

    agent_files = find_files(agents_dir, "*.md", recursive=True)

    if not agent_files:
        console.print("[yellow]No agents found.[/yellow]")
        return

    table = Table(title="Available Agents")
    table.add_column("Agent", style="cyan", no_wrap=True)
    table.add_column("Tier", style="magenta")
    table.add_column("Category", style="green")
    table.add_column("File", style="dim")

    for agent_file in sorted(agent_files):
        # Parse agent file name
        agent_name = agent_file.stem

        # Try to read tier from file (basic parsing)
        with open(agent_file, "r", encoding="utf-8") as f:
            content = f.read()

            # Extract tier
            agent_tier = "unknown"
            if "tier: 1" in content.lower() or "tier: critical" in content.lower():
                agent_tier = "1"
            elif "tier: 2" in content.lower() or "tier: high" in content.lower():
                agent_tier = "2"
            elif "tier: 3" in content.lower() or "tier: medium" in content.lower():
                agent_tier = "3"

            # Extract category
            category = "core" if "core-development" in str(agent_file) else "service"

        # Filter by tier
        if tier != "all" and agent_tier != tier:
            continue

        table.add_row(
            agent_name,
            agent_tier,
            category.title(),
            str(agent_file.relative_to(project_root))
        )

    console.print(table)
    console.print(f"\n[dim]Total agents: {len(agent_files)}[/dim]")


@agent.command()
@click.argument("agent_name")
def info(agent_name: str):
    """
    Show information about a specific agent.

    Example:
        claude-dev agent info test-writer
    """
    config = load_config()
    project_root = config.get_project_root()

    # Find agent file
    agents_dir = project_root / ".claude" / "agents"
    agent_file = None

    if agents_dir.exists():
        # Search in all subdirectories
        for candidate in agents_dir.rglob(f"{agent_name}.md"):
            agent_file = candidate
            break

    if not agent_file or not agent_file.exists():
        console.print(f"[red]Error:[/red] Agent not found: {agent_name}")
        console.print("\nAvailable agents:")
        ctx = click.Context(list)
        ctx.invoke(list, tier="all")
        return

    # Read agent file
    with open(agent_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Display agent info (first ~1000 chars)
    console.print(Panel(
        content[:1200] + ("..." if len(content) > 1200 else ""),
        title=f"Agent: {agent_name}",
        border_style="cyan"
    ))

    console.print(f"\nFull agent file: [cyan]{agent_file}[/cyan]")
    console.print(f"\nInvoke agent:")
    console.print(f"  [cyan]claude-dev agent run {agent_name}[/cyan]")
