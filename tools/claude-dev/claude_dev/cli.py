"""
Main CLI entry point for claude-dev tool.

Provides the main command group and imports all subcommands.
"""

import os
import click
from rich.console import Console
from rich.panel import Panel
from typing import Optional

from claude_dev import __version__

# Initialize rich console for beautiful output
console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="claude-dev")
@click.pass_context
def cli(ctx):
    """
    Claude Development Framework CLI Tool

    A command-line interface for managing projects using the Claude Development Framework.
    Simplifies project initialization, specification generation, testing, planning, and quality checks.

    Examples:

        # Initialize a new project
        claude-dev init my-project

        # Create a new use case specification
        claude-dev spec new use-case --id UC-001 --title "User Registration"

        # Generate tests from specification
        claude-dev test generate UC-001

        # Check spec-code alignment
        claude-dev check alignment

    For more information on a specific command, run:
        claude-dev <command> --help
    """
    # Ensure that ctx.obj exists and is a dict
    ctx.ensure_object(dict)


@cli.command()
def version():
    """Display version information."""
    console.print(
        Panel(
            f"[bold cyan]Claude Development Framework CLI[/bold cyan]\n"
            f"Version: [green]{__version__}[/green]\n\n"
            f"Part of the Claude Development Framework v2.1",
            title="Version Info",
            border_style="cyan",
        )
    )


@cli.command()
@click.option(
    "--shell",
    type=click.Choice(["bash", "zsh", "fish"]),
    help="Shell type (auto-detected if not specified)",
)
def completion(shell: Optional[str]):
    """
    Install shell completion.

    Examples:
        # Auto-detect shell and install
        claude-dev completion

        # Install for specific shell
        claude-dev completion --shell bash
    """
    import subprocess

    # Auto-detect shell if not specified
    if not shell:
        shell_env = os.environ.get("SHELL", "")
        if "bash" in shell_env:
            shell = "bash"
        elif "zsh" in shell_env:
            shell = "zsh"
        elif "fish" in shell_env:
            shell = "fish"
        else:
            console.print("[red]Error:[/red] Could not detect shell. Use --shell option.")
            return

    console.print(f"Installing completion for [cyan]{shell}[/cyan]...")

    # Click supports built-in completion
    # Generate completion script
    if shell == "bash":
        console.print("\nAdd this to your ~/.bashrc:")
        console.print('[dim]eval "$(_CLAUDE_DEV_COMPLETE=bash_source claude-dev)"[/dim]')
    elif shell == "zsh":
        console.print("\nAdd this to your ~/.zshrc:")
        console.print('[dim]eval "$(_CLAUDE_DEV_COMPLETE=zsh_source claude-dev)"[/dim]')
    elif shell == "fish":
        console.print("\nAdd this to your ~/.config/fish/completions/claude-dev.fish:")
        console.print("[dim]_CLAUDE_DEV_COMPLETE=fish_source claude-dev | source[/dim]")

    console.print("\n[green]✓[/green] Then restart your shell or source the file.")


# Import command modules
# These will be registered as subcommands
from claude_dev.commands import init_cmd, spec, test, plan, check, session, agent

# Register command groups
cli.add_command(init_cmd.init)
cli.add_command(spec.spec)
cli.add_command(test.test)
cli.add_command(plan.plan)
cli.add_command(check.check)
cli.add_command(session.session)
cli.add_command(agent.agent)


if __name__ == "__main__":
    cli()
