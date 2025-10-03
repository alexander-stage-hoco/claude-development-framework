"""
Template rendering using Jinja2.

Renders templates from .claude/templates/ directory with provided context.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import jinja2


class TemplateRenderer:
    """Template renderer for Claude Development Framework templates."""

    def __init__(self, template_dir: Optional[Path] = None):
        """
        Initialize template renderer.

        Args:
            template_dir: Path to templates directory. If None, uses .claude/templates/
        """
        self.template_dir = template_dir or self._find_template_dir()

        if self.template_dir:
            self.env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(str(self.template_dir)),
                autoescape=False,  # Templates are markdown, not HTML
                trim_blocks=True,
                lstrip_blocks=True,
            )
        else:
            self.env = None

    def _find_template_dir(self) -> Optional[Path]:
        """
        Find .claude/templates/ directory by walking up from current directory.

        Returns:
            Path to templates directory or None if not found
        """
        current = Path.cwd()

        # Walk up directory tree looking for .claude/templates/
        for parent in [current] + list(current.parents):
            template_dir = parent / ".claude" / "templates"
            if template_dir.exists() and template_dir.is_dir():
                return template_dir

        return None

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Render template with context.

        Args:
            template_name: Template filename (e.g., "use-case-template.md")
            context: Template context variables

        Returns:
            Rendered template content

        Raises:
            FileNotFoundError: If template directory or template file not found
            jinja2.TemplateError: If template rendering fails
        """
        if not self.env:
            raise FileNotFoundError(
                "Template directory not found. Are you in a Claude framework project?"
            )

        # Add common context variables
        full_context = {
            "now": datetime.now(),
            "today": datetime.now().strftime("%Y-%m-%d"),
            **context,
        }

        template = self.env.get_template(template_name)
        return template.render(full_context)

    def render_string(self, template_string: str, context: Dict[str, Any]) -> str:
        """
        Render template from string.

        Args:
            template_string: Template content as string
            context: Template context variables

        Returns:
            Rendered template content
        """
        # Add common context variables
        full_context = {
            "now": datetime.now(),
            "today": datetime.now().strftime("%Y-%m-%d"),
            **context,
        }

        template = jinja2.Template(
            template_string,
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        return template.render(full_context)

    def list_templates(self) -> list[str]:
        """
        List available templates.

        Returns:
            List of template filenames
        """
        if not self.template_dir:
            return []

        return [
            f.name
            for f in self.template_dir.iterdir()
            if f.is_file() and f.suffix in [".md", ".yaml", ".yml", ".txt"]
        ]

    def template_exists(self, template_name: str) -> bool:
        """
        Check if template exists.

        Args:
            template_name: Template filename

        Returns:
            True if template exists
        """
        if not self.template_dir:
            return False

        return (self.template_dir / template_name).exists()

    def get_template_path(self, template_name: str) -> Optional[Path]:
        """
        Get full path to template file.

        Args:
            template_name: Template filename

        Returns:
            Path to template file or None if not found
        """
        if not self.template_dir:
            return None

        template_path = self.template_dir / template_name
        return template_path if template_path.exists() else None


def render_template(template_name: str, context: Dict[str, Any]) -> str:
    """
    Convenience function to render template.

    Args:
        template_name: Template filename
        context: Template context variables

    Returns:
        Rendered template content
    """
    renderer = TemplateRenderer()
    return renderer.render(template_name, context)
