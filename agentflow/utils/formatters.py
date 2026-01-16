"""Output formatting utilities for AgentFlow CLI."""

import datetime
from typing import Any


def format_duration(seconds: int) -> str:
    """Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string like "15m 23s" or "1h 5m 30s"
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s" if secs else f"{minutes}m"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        parts = []
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        if secs and not hours:
            parts.append(f"{secs}s")
        return " ".join(parts)


def format_timestamp(dt: datetime.datetime) -> str:
    """Format datetime to string.

    Args:
        dt: Datetime object

    Returns:
        Formatted timestamp string
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_relative_time(dt: datetime.datetime) -> str:
    """Format datetime as relative time (e.g., "2 minutes ago").

    Args:
        dt: Datetime object

    Returns:
        Relative time string
    """
    now = datetime.datetime.utcnow()
    delta = now - dt

    seconds = int(delta.total_seconds())

    if seconds < 60:
        return f"{seconds} seconds ago"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    else:
        days = seconds // 86400
        return f"{days} day{'s' if days > 1 else ''} ago"
