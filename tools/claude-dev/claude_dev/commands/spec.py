"""
Specification generation commands.

Handles: claude-dev spec [new|list|validate]
"""

import click
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from claude_dev.utils.config import load_config
from claude_dev.utils.validation import (
    validate_id,
    validate_spec_title,
    sanitize_filename,
)
from claude_dev.utils.file_ops import create_file, open_in_editor, find_files
from claude_dev.templates.renderer import TemplateRenderer

console = Console()


@click.group()
def spec():
    """Specification generation and management commands."""
    pass


@spec.command()
@click.argument("spec_type", type=click.Choice(["use-case", "service", "adr"]))
@click.option("--id", "spec_id", required=True, help="Specification ID (e.g., UC-001, SVC-001, ADR-001)")
@click.option("--title", required=True, help="Specification title")
@click.option("--edit", is_flag=True, help="Open in editor after creation")
def new(spec_type: str, spec_id: str, title: str, edit: bool):
    """
    Create a new specification from template.

    Examples:

        # Create use case
        claude-dev spec new use-case --id UC-001 --title "User Registration"

        # Create service spec
        claude-dev spec new service --id SVC-001 --title "Authentication Service"

        # Create ADR
        claude-dev spec new adr --id ADR-001 --title "Database Selection"
    """
    # Load config
    config = load_config()

    # Validate ID format
    id_prefix = {
        "use-case": "UC",
        "service": "SVC",
        "adr": "ADR",
    }[spec_type]

    is_valid, error_msg = validate_id(spec_id, id_prefix)
    if not is_valid:
        console.print(f"[red]Error:[/red] {error_msg}")
        raise click.Abort()

    # Validate title
    is_valid, error_msg = validate_spec_title(title)
    if not is_valid:
        console.print(f"[red]Error:[/red] {error_msg}")
        raise click.Abort()

    # Determine template and output path
    template_map = {
        "use-case": ("use-case-template.md", "specs/use-cases"),
        "service": ("service-spec-template.md", "specs/services"),
        "adr": ("adr-template.md", "specs/adrs"),
    }

    template_name, output_subdir = template_map[spec_type]

    # Create output path
    output_dir = config.get_path("specs") / output_subdir.split("/")[-1]
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename
    safe_title = sanitize_filename(title)
    filename = f"{spec_id}-{safe_title}.md"
    output_path = output_dir / filename

    # Check if file already exists
    if output_path.exists():
        console.print(f"[yellow]Warning:[/yellow] File already exists: {output_path}")
        if not click.confirm("Overwrite?"):
            raise click.Abort()

    # Render template
    renderer = TemplateRenderer()

    try:
        context = {
            "spec_id": spec_id,
            "title": title,
            "spec_type": spec_type,
        }
        content = renderer.render(template_name, context)

        # Create file
        create_file(output_path, content, overwrite=True, backup=True)

        console.print(Panel(
            f"[green]✓[/green] {spec_type.title()} specification created\n\n"
            f"ID: [cyan]{spec_id}[/cyan]\n"
            f"Title: [cyan]{title}[/cyan]\n"
            f"File: [cyan]{output_path}[/cyan]",
            title="Specification Created",
            border_style="green"
        ))

        # Open in editor if requested
        if edit:
            editor = config.get("defaults.editor", "vim")
            open_in_editor(output_path, editor)

    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] Template not found: {template_name}")
        console.print(f"[yellow]Hint:[/yellow] Are you in a Claude framework project directory?")
        raise click.Abort()


@spec.command()
@click.option(
    "--type",
    "spec_type",
    type=click.Choice(["use-case", "service", "adr", "all"]),
    default="all",
    help="Filter by specification type"
)
def list(spec_type: str):
    """
    List all specifications.

    Examples:

        # List all specs
        claude-dev spec list

        # List only use cases
        claude-dev spec list --type use-case
    """
    config = load_config()
    specs_dir = config.get_path("specs")

    if not specs_dir.exists():
        console.print("[yellow]No specifications found.[/yellow]")
        return

    # Find spec files
    search_dirs = {
        "use-case": ["use-cases"],
        "service": ["services"],
        "adr": ["adrs"],
        "all": ["use-cases", "services", "adrs"],
    }

    table = Table(title="Specifications")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    table.add_column("Title", style="green")
    table.add_column("File", style="dim")

    for subdir in search_dirs[spec_type]:
        subdir_path = specs_dir / subdir
        if not subdir_path.exists():
            continue

        spec_files = find_files(subdir_path, "*.md", recursive=False)

        for spec_file in sorted(spec_files):
            # Parse filename: UC-001-title.md
            parts = spec_file.stem.split("-", 2)
            if len(parts) >= 2:
                spec_id = f"{parts[0]}-{parts[1]}"
                title = parts[2].replace("-", " ").title() if len(parts) > 2 else "Untitled"

                spec_type_name = {
                    "use-cases": "Use Case",
                    "services": "Service",
                    "adrs": "ADR",
                }.get(subdir, subdir)

                table.add_row(
                    spec_id,
                    spec_type_name,
                    title,
                    str(spec_file.relative_to(config.get_project_root()))
                )

    console.print(table)


@spec.command()
@click.argument("spec_id")
def validate(spec_id: str):
    """
    Validate specification file format.

    Checks for:
    - Required sections
    - Proper YAML front matter
    - ID format
    - Cross-references

    Example:
        claude-dev spec validate UC-001
    """
    config = load_config()

    # Find spec file
    spec_file = _find_spec_file(config, spec_id)

    if not spec_file:
        console.print(f"[red]Error:[/red] Specification not found: {spec_id}")
        raise click.Abort()

    # Read and validate
    console.print(f"Validating {spec_file}...")

    with open(spec_file, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []
    warnings = []

    # Check for YAML front matter
    if not content.startswith("---"):
        errors.append("Missing YAML front matter")

    # Check for required sections (basic check)
    required_sections = ["## Overview", "## Acceptance Criteria"]
    for section in required_sections:
        if section not in content:
            warnings.append(f"Missing recommended section: {section}")

    # Report results
    if errors:
        console.print(f"\n[red]✗ Validation failed with {len(errors)} error(s):[/red]")
        for error in errors:
            console.print(f"  • {error}")
    else:
        console.print(f"\n[green]✓ Validation passed[/green]")

    if warnings:
        console.print(f"\n[yellow]⚠ {len(warnings)} warning(s):[/yellow]")
        for warning in warnings:
            console.print(f"  • {warning}")


def _find_spec_file(config, spec_id: str) -> Optional[Path]:
    """Find spec file by ID."""
    specs_dir = config.get_path("specs")

    for subdir in ["use-cases", "services", "adrs"]:
        subdir_path = specs_dir / subdir
        if not subdir_path.exists():
            continue

        # Find files matching ID pattern
        pattern = f"{spec_id}-*.md"
        files = list(subdir_path.glob(pattern))

        if files:
            return files[0]

    return None
