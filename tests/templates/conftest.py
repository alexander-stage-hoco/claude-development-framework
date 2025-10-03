"""Pytest configuration and fixtures for template tests."""

import pytest
from pathlib import Path
from typing import List

from tests.templates.fixtures.template_parser import (
    TemplateParser,
    get_all_template_paths,
)


@pytest.fixture(scope="session")
def template_paths() -> List[Path]:
    """Get all template file paths.

    Returns:
        List of paths to all template files
    """
    return get_all_template_paths()


@pytest.fixture(scope="session")
def template_parsers(template_paths: List[Path]) -> List[TemplateParser]:
    """Get TemplateParser instances for all templates.

    Returns:
        List of TemplateParser instances
    """
    return [TemplateParser(path) for path in template_paths]


@pytest.fixture(
    params=get_all_template_paths(),
    ids=lambda p: p.stem,
)
def template_parser(request) -> TemplateParser:
    """Parametrized fixture providing TemplateParser for each template.

    This allows writing a single test that runs against all templates.
    """
    return TemplateParser(request.param)


@pytest.fixture
def use_case_template_parser() -> TemplateParser:
    """Get parser for use-case-template.md specifically.

    Returns:
        TemplateParser for use case template
    """
    templates_dir = Path(__file__).parent.parent.parent / ".claude" / "templates"
    uc_template_path = templates_dir / "use-case-template.md"

    if not uc_template_path.exists():
        pytest.skip(f"Use case template not found at {uc_template_path}")

    return TemplateParser(uc_template_path)


@pytest.fixture
def claude_template_parser() -> TemplateParser:
    """Get parser for CLAUDE.md template specifically.

    Returns:
        TemplateParser for CLAUDE template
    """
    templates_dir = Path(__file__).parent.parent.parent / ".claude" / "templates"
    claude_template_path = templates_dir / "CLAUDE.md"

    if not claude_template_path.exists():
        pytest.skip(f"CLAUDE template not found at {claude_template_path}")

    return TemplateParser(claude_template_path)


@pytest.fixture
def service_spec_template_parser() -> TemplateParser:
    """Get parser for service-spec.md template specifically.

    Returns:
        TemplateParser for service spec template
    """
    templates_dir = Path(__file__).parent.parent.parent / ".claude" / "templates"
    service_template_path = templates_dir / "service-spec.md"

    if not service_template_path.exists():
        pytest.skip(f"Service spec template not found at {service_template_path}")

    return TemplateParser(service_template_path)


@pytest.fixture
def framework_root() -> Path:
    """Get path to framework root directory.

    Returns:
        Path to framework root
    """
    return Path(__file__).parent.parent.parent
