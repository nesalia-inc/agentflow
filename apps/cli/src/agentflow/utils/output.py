"""Output formatting utilities."""

from rich.console import Console
from rich.table import Table
from typing import List, Any

console = Console()


def success(message: str) -> None:
    """Print success message.

    Args:
        message: Message to print
    """
    console.print(f"[green]√[/] {message}", style="bold")


def error(message: str) -> None:
    """Print error message.

    Args:
        message: Message to print
    """
    console.print(f"[red]✗[/] {message}", style="bold")


def warning(message: str) -> None:
    """Print warning message.

    Args:
        message: Message to print
    """
    console.print(f"[yellow]![/] {message}", style="bold")


def info(message: str) -> None:
    """Print info message.

    Args:
        message: Message to print
    """
    console.print(f"[blue]i[/] {message}")


def print_table(columns: List[str], rows: List[List[str]]) -> None:
    """Print a rich table.

    Args:
        columns: List of column headers
        rows: List of rows (each row is a list of strings)
    """
    table = Table(show_header=True, header_style="bold magenta")
    for col in columns:
        table.add_column(col)

    for row in rows:
        table.add_row(*row)

    console.print(table)
