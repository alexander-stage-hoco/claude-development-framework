"""
Session management commands.

Handles: claude-dev session [start|end|status]
"""

import click
from datetime import datetime
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel

from claude_dev.utils.config import load_config
from claude_dev.utils.file_ops import create_file

console = Console()


@click.group()
def session():
    """Session management commands."""
    pass


@session.command()
@click.option("--iteration", help="Iteration ID for this session")
def start(iteration: Optional[str]):
    """
    Start a new development session.

    Creates/updates session state file with timestamp and context.

    Example:
        claude-dev session start --iteration iteration-01
    """
    config = load_config()
    status_dir = config.get_path("status")
    status_dir.mkdir(parents=True, exist_ok=True)

    session_file = status_dir / "session-state.md"

    # Create session state content
    content = f"""# Session State

**Date**: {datetime.now().strftime("%Y-%m-%d")}
**Time Started**: {datetime.now().strftime("%H:%M")}
**Iteration**: {iteration or "N/A"}

## Session Goals

- [ ] TODO: Define session goals

## Current Progress

_Session just started_

## Next Steps

1. Review current iteration plan
2. Define session goals
3. Start implementation

## Notes

_Add notes as you work_

---
Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
"""

    create_file(session_file, content, overwrite=True, backup=True)

    console.print(
        Panel(
            f"[green]✓[/green] Session started\n\n"
            f"Time: [cyan]{datetime.now().strftime('%H:%M')}[/cyan]\n"
            f"Iteration: [cyan]{iteration or 'N/A'}[/cyan]\n"
            f"State file: [cyan]{session_file}[/cyan]",
            title="Session Started",
            border_style="green",
        )
    )

    console.print("\n[bold]Next steps:[/bold]")
    console.print("1. Review .claude/CLAUDE.md")
    console.print("2. Check planning/current-iteration.md")
    console.print("3. Start work on current task")


@session.command()
@click.option("--summarize", is_flag=True, help="Invoke session-summarizer agent")
def end(summarize: bool):
    """
    End current development session.

    Updates session state and optionally generates summary.

    Example:
        claude-dev session end --summarize
    """
    config = load_config()
    status_dir = config.get_path("status")
    session_file = status_dir / "session-state.md"

    if not session_file.exists():
        console.print("[yellow]No active session found.[/yellow]")
        return

    # Read current session
    with open(session_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Update with end time
    end_time = datetime.now().strftime("%H:%M")
    content += f"\n\n**Time Ended**: {end_time}\n"

    # Write back
    with open(session_file, "w", encoding="utf-8") as f:
        f.write(content)

    console.print(
        Panel(
            f"[green]✓[/green] Session ended\n\n" f"Time: [cyan]{end_time}[/cyan]",
            title="Session Ended",
            border_style="green",
        )
    )

    if summarize:
        console.print("\n[yellow]⚠ Agent integration coming soon![/yellow]")
        console.print("For now, manually invoke session-summarizer agent:")
        console.print("  @session-summarizer summarize this session")


@session.command()
def status():
    """
    Show current session status.

    Example:
        claude-dev session status
    """
    config = load_config()
    status_dir = config.get_path("status")
    session_file = status_dir / "session-state.md"

    if not session_file.exists():
        console.print("[yellow]No active session.[/yellow]")
        console.print("\nStart a session with:")
        console.print("  [cyan]claude-dev session start[/cyan]")
        return

    # Read session state
    with open(session_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Display content
    console.print(
        Panel(
            content[:800] + ("..." if len(content) > 800 else ""),
            title="Current Session",
            border_style="cyan",
        )
    )

    console.print(f"\nFull file: [cyan]{session_file}[/cyan]")
