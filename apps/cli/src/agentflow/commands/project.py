"""Project commands."""

import typer
from typing import Optional

from agentflow.models import Project, Database
from agentflow.storage import (
    load_database,
    save_database,
    find_organization_by_slug,
    find_project_by_slug,
    find_projects_by_organization,
    slug_exists_in_projects,
)
from agentflow.utils.config import (
    get_current_user_email,
    get_current_organization,
    set_current_organization,
    set_current_project,
)
from agentflow.utils.validators import validate_slug
from agentflow.utils.output import success, error, info, print_table

app = typer.Typer(help="Project commands")


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


def get_org_context(org_slug: Optional[str] = None) -> tuple[str, str]:
    """Get organization context (slug and ID).

    Args:
        org_slug: Optional org slug (uses current if not provided)

    Returns:
        Tuple of (org_slug, org_id)

    Raises:
        typer.Exit if org not found
    """
    # Use provided slug or get from config
    if not org_slug:
        org_slug = get_current_organization()

    if not org_slug:
        error(
            "No organization selected. Use: agentflow org use <slug>\n"
            "Or specify: agentflow project list --org <slug>"
        )
        raise typer.Exit(1)

    # Find organization
    org = find_organization_by_slug(org_slug)
    if not org:
        error(f"Organization '{org_slug}' not found")
        raise typer.Exit(1)

    return org_slug, org.id


@app.command()
def list(
    org: Optional[str] = typer.Option(None, "--org", "-o", help="Organization slug"),
):
    """List all projects in current or specified organization."""
    email = check_authenticated()

    # Get organization context
    org_slug, org_id = get_org_context(org)

    # Get projects
    projects = find_projects_by_organization(org_id)

    if not projects:
        info(f"No projects found in {org_slug}")
        print()
        info("Create one:")
        info(f"  agentflow project create --name 'My Project' --slug 'my-project'")
        return

    # Format data for table
    rows = []
    for project in projects:
        # Format GitHub URL
        github = project.github_url or "-"
        if github != "-" and len(github) > 40:
            github = "..." + github[-37:]

        # Format description
        status = "✓" if project.is_active else "✗"

        rows.append([project.name, project.slug, status, github])

    print_table(
        ["NAME", "SLUG", "ACTIVE", "GITHUB"],
        rows,
    )


@app.command()
def create(
    name: str = typer.Option(..., "--name", "-n", help="Project name"),
    slug: str = typer.Option(..., "--slug", "-s", help="URL-friendly slug"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Project description"),
    github_url: Optional[str] = typer.Option(None, "--github-url", "-g", help="GitHub repository URL"),
    org: Optional[str] = typer.Option(None, "--org", "-o", help="Organization slug"),
):
    """Create a new project."""
    email = check_authenticated()

    # Get organization context
    org_slug, org_id = get_org_context(org)

    # Validate name length
    if len(name) > 255:
        error("Name must be 255 characters or less")
        raise typer.Exit(1)

    # Validate slug
    slug_error = validate_slug(slug)
    if slug_error:
        error(slug_error)
        raise typer.Exit(1)

    # Check if slug already exists in org
    if slug_exists_in_projects(org_id, slug):
        error(f"Project with slug '{slug}' already exists in this organization")
        raise typer.Exit(1)

    # Create project
    project = Project(
        organization_id=org_id,
        name=name,
        slug=slug,
        description=description,
        github_url=github_url,
    )

    # Save to database
    db = load_database()
    db.projects.append(project)
    save_database(db)

    # Set as current project
    set_current_project(slug)

    # Display success
    success(f"Project created in {org_slug}")
    print()
    info(f"  Name:       {name}")
    info(f"  Slug:       {slug}")
    info(f"  GitHub:     {github_url or '(none)'}")
    info(f"  Active:     Yes")
    print()
    info(f"Project is now active")


@app.command()
def view(
    slug: str = typer.Argument(..., help="Project slug"),
    org: Optional[str] = typer.Option(None, "--org", "-o", help="Organization slug"),
):
    """View project details."""
    email = check_authenticated()

    # Get organization context
    org_slug, org_id = get_org_context(org)

    # Find project
    project = find_project_by_slug(org_id, slug)
    if not project:
        error(f"Project '{slug}' not found in {org_slug}")
        raise typer.Exit(1)

    # Get organization name
    org_obj = find_organization_by_slug(org_slug)

    # Display details
    print()
    info(f"Project: {project.name} ({slug})")
    print()
    info(f"Organization:  {org_slug} ({org_obj.name if org_obj else 'Unknown'})")
    info(f"Description:   {project.description or '(none)'}")
    info(f"GitHub URL:    {project.github_url or '(none)'}")
    info(f"Active:        {'Yes' if project.is_active else 'No'}")
    info(f"Created:       {project.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()
    info("Coming in v2:")
    info("  - Create AI agents")
    info("  - Start work sessions")
    info("  - Track agent activities")


@app.command()
def use(
    slug: str = typer.Argument(..., help="Project slug"),
    org: Optional[str] = typer.Option(None, "--org", "-o", help="Organization slug"),
):
    """Set active project."""
    email = check_authenticated()

    # Get organization context
    org_slug, org_id = get_org_context(org)

    # Find project
    project = find_project_by_slug(org_id, slug)
    if not project:
        error(f"Project '{slug}' not found in {org_slug}")
        raise typer.Exit(1)

    # Set org if not already set
    current_org = get_current_organization()
    if current_org != org_slug:
        set_current_organization(org_slug)

    # Set as current project
    set_current_project(slug)

    # Get organization name
    org_obj = find_organization_by_slug(org_slug)

    # Display success
    success(f"Now using project: {slug} ({project.name})")
    print()
    info(f"Working in: [{org_slug} / {slug}]")
    print()
    info("Coming in v2:")
    info("  - Create AI agents")
    info("  - Start work sessions")
