"""
Project initialization command.

Handles: claude-dev init <project-name>
"""

import click
import subprocess
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from claude_dev.utils.validation import validate_project_name
from claude_dev.utils.file_ops import ensure_dir
from claude_dev.utils.config import Config

console = Console()


@click.command()
@click.argument("project_name")
@click.option(
    "--path",
    type=click.Path(),
    default=None,
    help="Parent directory path (defaults to current directory)",
)
@click.option(
    "--template",
    type=click.Choice(["api", "cli", "data-pipeline", "web", "ml"], case_sensitive=False),
    default=None,
    help="Project template to use",
)
@click.option(
    "--no-git",
    is_flag=True,
    default=False,
    help="Skip git initialization",
)
def init(project_name: str, path: Optional[str], template: Optional[str], no_git: bool):
    """
    Initialize a new Claude Development Framework project.

    Creates project structure, copies framework files, and sets up initial configuration.

    Examples:

        # Initialize project in current directory
        claude-dev init my-project

        # Initialize with template
        claude-dev init my-api --template api

        # Initialize in specific path
        claude-dev init my-project --path /path/to/parent
    """
    # Validate project name
    is_valid, error_msg = validate_project_name(project_name)
    if not is_valid:
        console.print(f"[red]Error:[/red] {error_msg}")
        raise click.Abort()

    # Determine project path
    parent_path = Path(path) if path else Path.cwd()
    project_path = parent_path / project_name

    # Check if project already exists
    if project_path.exists():
        console.print(f"[red]Error:[/red] Directory already exists: {project_path}")
        raise click.Abort()

    console.print(Panel(
        f"[bold cyan]Initializing Claude Development Framework Project[/bold cyan]\n\n"
        f"Project: [green]{project_name}[/green]\n"
        f"Path: [green]{project_path}[/green]\n"
        f"Template: [green]{template or 'default'}[/green]",
        title="Project Initialization",
        border_style="cyan"
    ))

    # Find framework root (where init-project.sh lives)
    framework_root = _find_framework_root()

    if not framework_root:
        console.print(
            "[yellow]Warning:[/yellow] Could not find framework root. "
            "Using manual setup instead of init-project.sh"
        )
        _manual_init(project_path, project_name, template, no_git)
    else:
        _script_init(framework_root, project_path, project_name, no_git)

    console.print(f"\n[green]✓[/green] Project initialized successfully!")
    console.print(f"\nNext steps:")
    console.print(f"  1. cd {project_name}")
    console.print(f"  2. Read .claude/CLAUDE.md")
    console.print(f"  3. Create your first use case:")
    console.print(f"     [cyan]claude-dev spec new use-case --id UC-001 --title \"Your Feature\"[/cyan]")


def _find_framework_root() -> Optional[Path]:
    """
    Find framework root directory (contains init-project.sh).

    Returns:
        Path to framework root or None if not found
    """
    # Try to find init-project.sh by walking up from current directory
    current = Path(__file__).resolve()

    for parent in current.parents:
        init_script = parent / "init-project.sh"
        if init_script.exists():
            return parent

    # Also check if we're in a framework installation
    # Look for .claude/templates/
    for parent in [Path.cwd()] + list(Path.cwd().parents):
        templates_dir = parent / ".claude" / "templates"
        if templates_dir.exists():
            return parent

    return None


def _script_init(
    framework_root: Path, project_path: Path, project_name: str, no_git: bool
):
    """
    Initialize project using init-project.sh script.

    Args:
        framework_root: Path to framework root
        project_path: Path to new project
        project_name: Project name
        no_git: Whether to skip git init
    """
    init_script = framework_root / "init-project.sh"

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Running init-project.sh...", total=None)

        try:
            # Run init-project.sh
            result = subprocess.run(
                [str(init_script), project_name],
                cwd=project_path.parent,
                capture_output=True,
                text=True,
                check=True,
            )

            progress.update(task, completed=True)

            # Show output if verbose
            if result.stdout:
                console.print(result.stdout)

        except subprocess.CalledProcessError as e:
            progress.stop()
            console.print(f"[red]Error running init-project.sh:[/red]\n{e.stderr}")
            raise click.Abort()


def _manual_init(
    project_path: Path, project_name: str, template: Optional[str], no_git: bool
):
    """
    Manually initialize project (fallback if init-project.sh not found).

    Args:
        project_path: Path to new project
        project_name: Project name
        template: Template name
        no_git: Whether to skip git init
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Create directory structure
        task = progress.add_task("Creating project structure...", total=5)

        # Create main directories
        for dir_name in [".claude", "specs", "src", "tests", "planning", "status", "research", "docs"]:
            ensure_dir(project_path / dir_name)
        progress.advance(task)

        # Create subdirectories
        for dir_name in ["use-cases", "services", "adrs"]:
            ensure_dir(project_path / "specs" / dir_name)
        progress.advance(task)

        # Create .claude subdirectories (we'll populate with templates later)
        for dir_name in ["templates", "guides", "quick-ref", "agents"]:
            ensure_dir(project_path / ".claude" / dir_name)
        progress.advance(task)

        # Create initial config file
        config = Config()
        config.data["project"]["name"] = project_name
        if template:
            config.data["project"]["type"] = template
        config.config_path = project_path / ".claude" / "cli-config.yaml"
        config.save()
        progress.advance(task)

        # Create placeholder README
        readme_content = f"""# {project_name}

Project initialized with Claude Development Framework v2.1

## Quick Start

1. Read `.claude/CLAUDE.md` for framework overview
2. Create your first use case: `claude-dev spec new use-case --id UC-001`
3. Start development session

## Framework Rules

See `.claude/development-rules.md` for the 12 Non-Negotiable Rules.
"""
        (project_path / "README.md").write_text(readme_content)
        progress.advance(task)

        # Git init
        if not no_git:
            progress.update(task, description="Initializing git repository...")
            subprocess.run(
                ["git", "init"],
                cwd=project_path,
                capture_output=True,
                check=False,
            )

        progress.update(task, completed=True, description="Project structure created!")
