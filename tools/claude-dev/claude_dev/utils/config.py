"""
Configuration file parsing and management.

Reads and validates .claude/cli-config.yaml configuration files.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml


class Config:
    """Configuration manager for Claude Development Framework CLI."""

    DEFAULT_CONFIG = {
        "project": {
            "name": "my-project",
            "type": "api",
            "version": "1.0.0",
        },
        "paths": {
            "specs": "specs/",
            "src": "src/",
            "tests": "tests/",
            "planning": "planning/",
            "status": "status/",
            "research": "research/",
        },
        "defaults": {
            "coverage_threshold": 90,
            "test_runner": "pytest",
            "editor": os.environ.get("EDITOR", "vim"),
            "auto_open_files": True,
        },
        "agents": {
            "enabled": True,
            "api_key": os.environ.get("CLAUDE_API_KEY", ""),
            "default_model": "claude-sonnet-4",
        },
        "quality": {
            "linter": "pylint",
            "formatter": "black",
            "type_checker": "mypy",
        },
    }

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to config file. If None, searches for .claude/cli-config.yaml
        """
        self.config_path = config_path or self._find_config()
        self.data = self._load_config()

    def _find_config(self) -> Optional[Path]:
        """
        Find .claude/cli-config.yaml by walking up from current directory.

        Returns:
            Path to config file or None if not found
        """
        current = Path.cwd()

        # Walk up directory tree looking for .claude/cli-config.yaml
        for parent in [current] + list(current.parents):
            config_file = parent / ".claude" / "cli-config.yaml"
            if config_file.exists():
                return config_file

        return None

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file or use defaults.

        Returns:
            Configuration dictionary
        """
        if self.config_path and self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                user_config = yaml.safe_load(f) or {}

            # Merge user config with defaults
            return self._merge_configs(self.DEFAULT_CONFIG, user_config)

        # No config file found, use defaults
        return self.DEFAULT_CONFIG.copy()

    def _merge_configs(
        self, default: Dict[str, Any], user: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Recursively merge user config with defaults.

        Args:
            default: Default configuration
            user: User configuration

        Returns:
            Merged configuration
        """
        result = default.copy()

        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-separated key path.

        Args:
            key_path: Dot-separated path (e.g., "project.name")
            default: Default value if key not found

        Returns:
            Configuration value or default

        Example:
            >>> config.get("project.name")
            "my-project"
            >>> config.get("defaults.coverage_threshold")
            90
        """
        keys = key_path.split(".")
        value = self.data

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def get_path(self, path_key: str) -> Path:
        """
        Get path from configuration, resolved relative to project root.

        Args:
            path_key: Path key (e.g., "specs", "src", "tests")

        Returns:
            Absolute path

        Example:
            >>> config.get_path("specs")
            Path("/path/to/project/specs")
        """
        path_value = self.get(f"paths.{path_key}", path_key)
        project_root = self.get_project_root()

        return project_root / path_value

    def get_project_root(self) -> Path:
        """
        Get project root directory (where .claude/ exists).

        Returns:
            Project root path
        """
        if self.config_path:
            # Config file is in .claude/ directory
            return self.config_path.parent.parent

        # No config found, use current directory
        return Path.cwd()

    def save(self, config_data: Optional[Dict[str, Any]] = None) -> None:
        """
        Save configuration to file.

        Args:
            config_data: Configuration data to save. If None, saves current data.
        """
        data = config_data or self.data

        if not self.config_path:
            # Create config file in .claude/ directory
            project_root = Path.cwd()
            claude_dir = project_root / ".claude"
            claude_dir.mkdir(exist_ok=True)
            self.config_path = claude_dir / "cli-config.yaml"

        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def load_config(config_path: Optional[Path] = None) -> Config:
    """
    Load configuration from file or use defaults.

    Args:
        config_path: Optional path to config file

    Returns:
        Config instance
    """
    return Config(config_path)
