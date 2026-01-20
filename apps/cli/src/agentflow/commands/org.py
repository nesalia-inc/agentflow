"""Organization commands."""

import typer
from typing import Optional

from agentflow.models import Organization, Database
from agentflow.storage import (
    load_database,
    save_database,
    find_organization_by_slug,
    find_organizations_by_owner,
    find_projects_by_organization,
    slug_exists_in_organizations,
)
from agentflow.utils.config import (
    get_current_user_email,
    set_current_organization,
    get_current_organization,
)
from agentflow.utils.validators import validate_slug
from agentflow.utils.output import success, error, info, print_table

app = typer.Typer(help="Organization commands")


def check_authenticated() -> str:
    """Check if user is authenticated.

    Returns:
        User email if authenticated

    Raises:
        typer.Exit if not authenticated
    """
    email = get_current_user_email()
    if not email:
        error("Not authenticated. Run: agentflow auth login")
        raise typer.Exit(1)
    return email


@app.command()
def list(
    all_users: bool = typer.Option(False, "--all", "-a", help="Show all organizations (admin only)"),
):
    """List all organizations for current user."""
    email = check_authenticated()

    # Load database and find user
    db = load_database()
    user_id = None
    for user in db.users:
        if user.email == email:
            user_id = user.id
            break

    if not user_id:
        error("User not found")
        raise typer.Exit(1)

    # Filter by current user
    user_orgs = [org for org in db.organizations if org.owner_id == user_id]

    if not user_orgs:
        info("No organizations found")
        print()
        info("Create one:")
        info("  agentflow org create --name 'My Org' --slug 'my-org'")
        return

    # Format data for table
    rows = []
    for org in user_orgs:
        # Count projects
        project_count = len(find_projects_by_organization(org.id))

        # Format description
        description = org.description or "-"
        if len(description) > 50:
            description = description[:47] + "..."

        rows.append([org.name, org.slug, description, str(project_count)])

    print_table(
        ["NAME", "SLUG", "DESCRIPTION", "PROJECTS"],
        rows,
    )


@app.command()
def create(
    name: str = typer.Option(..., "--name", "-n", help="Organization name"),
    slug: str = typer.Option(..., "--slug", "-s", help="URL-friendly slug"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Organization description"),
):
    """Create a new organization."""
    email = check_authenticated()

    # Validate name length
    if len(name) > 255:
        error("Name must be 255 characters or less")
        raise typer.Exit(1)

    # Validate slug
    slug_error = validate_slug(slug)
    if slug_error:
        error(slug_error)
        raise typer.Exit(1)

    # Check if slug already exists
    if slug_exists_in_organizations(slug):
        error(f"Organization with slug '{slug}' already exists")
        raise typer.Exit(1)

    # Load database and find user
    db = load_database()

    # Find user by email to get their ID
    user_id = None
    for user in db.users:
        if user.email == email:
            user_id = user.id
            break

    if not user_id:
        error("User not found")
        raise typer.Exit(1)

    # Create organization
    org = Organization(
        owner_id=user_id, name=name, slug=slug, description=description
    )

    # Save to database
    db.organizations.append(org)
    save_database(db)

    # Display success
    success("Organization created")
    print()
    info(f"  Name:     {name}")
    info(f"  Slug:     {slug}")
    info(f"  Projects: 0")
    print()
    info("Set as active:")
    info(f"  agentflow org use {slug}")


@app.command()
def view(
    slug: str = typer.Argument(..., help="Organization slug"),
):
    """View organization details."""
    email = check_authenticated()

    # Find organization
    org = find_organization_by_slug(slug)
    if not org:
        error(f"Organization '{slug}' not found")
        raise typer.Exit(1)

    # Check ownership (for Phase 0, allow viewing own orgs only)
    db = load_database()
    user_id = None
    for user in db.users:
        if user.email == email:
            user_id = user.id
            break

    if org.owner_id != user_id:
        error("Access denied")
        raise typer.Exit(1)

    # Get projects
    projects = find_projects_by_organization(org.id)

    # Display details
    print()
    info(f"Organization: {org.name} ({slug})")
    print()
    info(f"Description:    {org.description or '(none)'}")
    info(f"Created:        {org.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()

    if projects:
        info(f"Projects ({len(projects)}):")
        print()
        rows = []
        for project in projects:
            status = "✓" if project.is_active else "✗"
            rows.append([project.name, project.slug, status])

        print_table(["NAME", "SLUG", "ACTIVE"], rows)
    else:
        info("Projects: 0")
    print()

    info("Manage projects:")
    info(f"  agentflow project create --org {slug} --name 'New Project'")


@app.command()
def use(
    slug: str = typer.Argument(..., help="Organization slug"),
):
    """Set active organization."""
    email = check_authenticated()

    # Find organization
    org = find_organization_by_slug(slug)
    if not org:
        error(f"Organization '{slug}' not found")
        raise typer.Exit(1)

    # Check ownership
    db = load_database()
    user_id = None
    for user in db.users:
        if user.email == email:
            user_id = user.id
            break

    if org.owner_id != user_id:
        error("Access denied")
        raise typer.Exit(1)

    # Set as current organization
    set_current_organization(slug)

    # Clear current project (org change invalidates project context)
    from agentflow.utils.config import clear_current_project

    clear_current_project()

    # Display success
    success(f"Now using organization: {slug} ({org.name})")
    print()
    info("Next steps:")
    info("  agentflow project list")
    info("  agentflow project create --name 'My Project'")
