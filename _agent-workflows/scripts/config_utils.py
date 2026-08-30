"""Shared strict TOML loading for the central workflow configuration."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any


class ConfigError(ValueError):
    """Raised when a present configuration layer cannot be used safely."""


def load_toml(path: Path, *, required: bool = False) -> dict[str, Any]:
    """Load a TOML table, allowing absence only for optional layers."""
    if not path.exists():
        if required:
            raise ConfigError(f"required TOML file not found: {path}")
        return {}
    if not path.is_file():
        raise ConfigError(f"TOML layer is not a file: {path}")
    try:
        with path.open("rb") as stream:
            parsed = tomllib.load(stream)
    except tomllib.TOMLDecodeError as error:
        raise ConfigError(f"failed to parse {path}: {error}") from error
    except OSError as error:
        raise ConfigError(f"failed to read {path}: {error}") from error
    if not isinstance(parsed, dict):
        raise ConfigError(f"TOML layer did not parse to a table: {path}")
    return parsed


def load_central_config(project_root: Path) -> dict[str, Any]:
    config_path = project_root / "_agent-workflows" / "_config" / "config.toml"
    return load_toml(config_path, required=True)


def expand_project_path(value: str, project_root: Path) -> Path:
    """Expand a central-config path from the selected project root.

    Central paths use ``{project-root}`` so the same configuration can be
    consumed from a checkout, a temporary test project, or a worktree.
    """
    expanded = value.replace("{project-root}", str(project_root.resolve()))
    return Path(expanded).expanduser().resolve()


def central_path(
    project_root: Path,
    dotted_key: str,
    *,
    required: bool = True,
) -> Path:
    """Return one path-valued central config key resolved against the project."""
    config = load_central_config(project_root)
    current: Any = config
    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            if required:
                raise ConfigError(f"required config key not found: {dotted_key}")
            return Path()
        current = current[part]
    if not isinstance(current, str) or not current.strip():
        raise ConfigError(f"config key is not a non-empty path: {dotted_key}")
    return expand_project_path(current, project_root)


def load_customization(project_root: Path | None, skill_dir: Path) -> dict[str, Any]:
    return load_toml(skill_dir / "customize.toml", required=True)
