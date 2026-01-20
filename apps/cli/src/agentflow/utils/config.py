"""Configuration file management."""

import yaml
from pathlib import Path
from typing import Optional

# Config file path
CONFIG_DIR = Path.home() / ".agentflow"
CONFIG_FILE = CONFIG_DIR / "config.yaml"


def load_config() -> dict:
    """Load configuration from YAML file.

    Returns:
        Configuration dictionary (empty if file doesn't exist)
    """
    if not CONFIG_FILE.exists():
        return {}

    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f) or {}


def save_config(config: dict) -> None:
    """Save configuration to YAML file.

    Args:
        config: Configuration dictionary to save
    """
    CONFIG_DIR.mkdir(exist_ok=True)

    with open(CONFIG_FILE, "w") as f:
        yaml.dump(config, f, default_flow_style=False)


def get_current_user_email() -> Optional[str]:
    """Get current user email from config.

    Returns:
        User email if set, None otherwise
    """
    config = load_config()
    return config.get("current_user_email")


def set_current_user_email(email: str) -> None:
    """Set current user email in config.

    Args:
        email: User email address
    """
    config = load_config()
    config["current_user_email"] = email
    save_config(config)


def get_current_api_key() -> Optional[str]:
    """Get current API key from config.

    Returns:
        API key if set, None otherwise
    """
    config = load_config()
    return config.get("current_api_key")


def set_current_api_key(api_key: str) -> None:
    """Set current API key in config.

    Args:
        api_key: API key string
    """
    config = load_config()
    config["current_api_key"] = api_key
    save_config(config)


def get_current_organization() -> Optional[str]:
    """Get current organization slug from config.

    Returns:
        Organization slug if set, None otherwise
    """
    config = load_config()
    return config.get("current_organization")


def set_current_organization(slug: str) -> None:
    """Set current organization in config.

    Args:
        slug: Organization slug
    """
    config = load_config()
    config["current_organization"] = slug
    save_config(config)


def get_current_project() -> Optional[str]:
    """Get current project slug from config.

    Returns:
        Project slug if set, None otherwise
    """
    config = load_config()
    return config.get("current_project")


def set_current_project(slug: str) -> None:
    """Set current project in config.

    Args:
        slug: Project slug
    """
    config = load_config()
    config["current_project"] = slug
    save_config(config)


def clear_current_project() -> None:
    """Clear current project from config."""
    config = load_config()
    if "current_project" in config:
        del config["current_project"]
    save_config(config)


def get_context_string() -> str:
    """Get formatted context string for prompt.

    Returns:
        Context string like "[org]" or "[org / project]"
    """
    org = get_current_organization()
    project = get_current_project()

    if org and project:
        return f"[{org} / {project}]"
    elif org:
        return f"[{org}]"
    else:
        return ""
