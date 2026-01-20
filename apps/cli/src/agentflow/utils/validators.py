"""Validation utilities."""

import re
from typing import Optional

# Slug regex: lowercase letters, numbers, hyphens
# Must start and end with alphanumeric
SLUG_REGEX = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")


def validate_slug(slug: str) -> Optional[str]:
    """Validate slug format.

    Args:
        slug: Slug to validate

    Returns:
        Error message if invalid, None if valid
    """
    if not 1 <= len(slug) <= 100:
        return "Slug must be between 1 and 100 characters"

    if not SLUG_REGEX.match(slug):
        return (
            "Slug must contain only lowercase letters, numbers, and hyphens, "
            "and must start and end with a letter or number"
        )

    return None


def validate_email(email: str) -> Optional[str]:
    """Validate email format (basic check).

    Args:
        email: Email address to validate

    Returns:
        Error message if invalid, None if valid
    """
    if "@" not in email:
        return "Invalid email format"

    parts = email.split("@")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        return "Invalid email format"

    return None
