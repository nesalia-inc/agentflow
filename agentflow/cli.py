"""AgentFlow CLI - Main entry point."""

import asyncio
from pathlib import Path

import questionary
import typer

from agentflow.config import (
    config_exists,
    get_database_config,
    save_database_config,
    save_user,
    set_current_workspace,
)
from agentflow.config.database import DatabaseSettings
from agentflow.db.base import init_db, close_db
from agentflow.entities import Workspace
from agentflow.db.session import DatabaseSession, get_db
from agentflow.utils.id_generator import generate_id

app = typer.Typer(help="AgentFlow - Git-like workflow management for AI agents")

config_app = typer.Typer(help="Configuration management")
app.add_typer(config_app, name="config")


@app.command()
def init(
    db_url: str = typer.Option(None, "--db-url", help="Direct database URL (skips prompts)"),
    create_workspace: bool = typer.Option(False, "--workspace", "-w", help="Create a workspace after init"),
) -> None:
    """Initialize AgentFlow configuration.

    Interactively configure database connection and create initial workspace.
    """
    if db_url:
        # Direct mode - use provided URL
        _init_direct(db_url, create_workspace)
    else:
        # Interactive mode
        _init_interactive()


def _init_direct(db_url: str, create_ws: bool = False) -> None:
    """Initialize with direct database URL.

    Args:
        db_url: Database connection URL
        create_ws: Whether to create a workspace
    """
    typer.echo(f"[*] Configuring AgentFlow with provided database URL...")

    # Create database settings
    db_settings = DatabaseSettings(db_url=db_url)

    # Test connection
    if not _test_connection_sync(db_settings):
        typer.echo("[!] Failed to connect to database. Please check your URL and try again.")
        raise typer.Exit(1)

    # Save configuration
    save_database_config(db_settings)

    # Generate user ID
    user_id = generate_id()
    save_user(user_id, "CLI User")

    typer.echo("[*] Configuration saved to ~/.agentflow/config.json")

    # Create workspace if requested
    if create_ws:
        workspace_name = typer.prompt("Workspace name", default="my-project")
        _create_workspace_sync(workspace_name)
    else:
        typer.echo("[*] Setup complete! Use 'agentflow --help' to see available commands.")


def _init_interactive() -> None:
    """Initialize with interactive prompts."""
    typer.echo("Welcome to AgentFlow! Let's configure your connection.\n")

    # Ask database type
    db_type = questionary.select(
        "Database type:",
        choices=["PostgreSQL", "SQLite"],
        default="PostgreSQL",
    ).ask()

    if db_type == "PostgreSQL":
        # PostgreSQL configuration
        host = questionary.text("Host", default="localhost").ask()
        port = questionary.text("Port", default="5432").ask()
        database = questionary.text("Database name", default="agentflow").ask()
        username = questionary.text("Username", default="postgres").ask()
        password = questionary.password("Password").ask()

        # Build URL
        db_url = f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"
    else:
        # SQLite configuration
        db_path = questionary.text("Database file path", default="agentflow.db").ask()
        db_url = f"sqlite+aiosqlite:///{db_path}"

    typer.echo("")
    typer.echo("[*] Testing connection...")

    # Create database settings
    db_settings = DatabaseSettings(db_url=db_url)

    # Test connection
    if not _test_connection_sync(db_settings):
        typer.echo("[!] Failed to connect to database. Please check your credentials and try again.")
        raise typer.Exit(1)

    typer.echo("[*] Connection successful!\n")

    # Save configuration
    save_database_config(db_settings)

    # Get user info
    user_id = generate_id()
    user_name = questionary.text("Your name", default="Developer").ask()
    save_user(user_id, user_name)

    typer.echo("[*] Configuration saved to ~/.agentflow/config.json\n")

    # Ask about workspace
    create_workspace = questionary.confirm("Create a workspace?", default=False).ask()

    if create_workspace:
        workspace_name = questionary.text("Workspace name", default="my-project").ask()
        _create_workspace_sync(workspace_name)

    typer.echo("\n[*] You're ready! Use 'agentflow --help' to see available commands.")


def _test_connection_sync(db_settings: DatabaseSettings) -> bool:
    """Test database connection synchronously.

    Args:
        db_settings: Database settings to test

    Returns:
        True if connection successful, False otherwise
    """
    try:
        # Run async init_db in sync context
        asyncio.run(_test_connection_async(db_settings))
        return True
    except Exception as e:
        typer.echo(f"[!] Connection error: {e}")
        return False


async def _test_connection_async(db_settings: DatabaseSettings) -> None:
    """Test database connection asynchronously.

    Args:
        db_settings: Database settings to test
    """
    await init_db()
    await close_db()


def _create_workspace_sync(workspace_name: str) -> None:
    """Create workspace synchronously.

    Args:
        workspace_name: Name for the workspace
    """
    try:
        asyncio.run(_create_workspace_async(workspace_name))
    except Exception as e:
        typer.echo(f"[!] Failed to create workspace: {e}")
        raise typer.Exit(1)


async def _create_workspace_async(workspace_name: str) -> None:
    """Create workspace asynchronously.

    Args:
        workspace_name: Name for the workspace
    """
    await init_db()

    async with get_db() as db:
        db_session = DatabaseSession(db.session)
        workspace = await Workspace.create(db_session, workspace_name)
        set_current_workspace(workspace.id)

    await close_db()
    typer.echo(f"[*] Workspace '{workspace_name}' created")


@config_app.command("show")
def config_show() -> None:
    """Show current configuration."""
    if not config_exists():
        typer.echo("[!] No configuration found. Run 'agentflow init' first.")
        raise typer.Exit(1)

    config = get_database_config()
    if not config:
        typer.echo("[!] No database configuration found.")
        raise typer.Exit(1)

    typer.echo("[*] Current configuration:")
    typer.echo(f"  Database URL: {config.db_url}")
    typer.echo(f"  Schema: {config.db_schema}")
    typer.echo(f"  Pool size: {config.db_pool_size}")
    typer.echo(f"  Max overflow: {config.db_max_overflow}")


@config_app.command("test")
def config_test() -> None:
    """Test database connection."""
    db_config = get_database_config()
    if not db_config:
        typer.echo("[!] No database configuration found. Run 'agentflow init' first.")
        raise typer.Exit(1)

    typer.echo("[*] Testing connection...")
    if _test_connection_sync(db_config):
        typer.echo("[*] Connection successful!")
    else:
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
