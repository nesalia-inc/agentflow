"""Tests for project commands."""

import pytest
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner

from agentflow.commands.project import app

runner = CliRunner()


@pytest.fixture
def temp_dirs(tmp_path: Path):
    """Create temporary directories for testing."""

    def mock_data_dir():
        return tmp_path / ".agentflow"

    def mock_config_dir():
        return tmp_path / ".agentflow"  # Same dir for testing

    with patch("agentflow.storage.DATA_DIR", mock_data_dir()):
        with patch("agentflow.storage.DATA_FILE", mock_data_dir() / "data.json"):
            with patch("agentflow.utils.config.CONFIG_DIR", mock_config_dir()):
                with patch("agentflow.utils.config.CONFIG_FILE", mock_config_dir() / "config.yaml"):
                    yield


@pytest.fixture
def authenticated_user(temp_dirs):
    """Create an authenticated user for testing."""
    from agentflow.commands.auth import app as auth_app

    # Register and login
    runner.invoke(
        auth_app,
        [
            "register",
            "--email",
            "test@example.com",
            "--password",
            "password123",
            "--name",
            "Test User",
        ],
    )
    return "test@example.com"


@pytest.fixture
def with_org(temp_dirs, authenticated_user):
    """Create an organization for testing."""
    from agentflow.commands.org import app as org_app

    runner.invoke(
        org_app, ["create", "--name", "Test Org", "--slug", "test-org"]
    )
    # Set org as active
    runner.invoke(org_app, ["use", "test-org"])
    return "test-org"


class TestProjectList:
    """Tests for project list command."""

    def test_list_when_no_projects(self, temp_dirs, authenticated_user, with_org):
        """Test listing projects when none exist."""
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "No projects found" in result.stdout

    def test_list_with_projects(self, temp_dirs, authenticated_user, with_org):
        """Test listing projects."""
        # Create two projects
        runner.invoke(
            app,
            [
                "create",
                "--name",
                "Project 1",
                "--slug",
                "proj-1",
                "--github-url",
                "https://github.com/test/repo1",
            ],
        )
        runner.invoke(
            app,
            ["create", "--name", "Project 2", "--slug", "proj-2"],
        )

        # List
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "Project 1" in result.stdout
        assert "Project 2" in result.stdout
        assert "proj-1" in result.stdout
        assert "proj-2" in result.stdout

    def test_list_when_not_authenticated(self, temp_dirs):
        """Test listing when not authenticated."""
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 1
        assert "Not authenticated" in result.stdout

    def test_list_when_no_org_set(self, temp_dirs, authenticated_user):
        """Test listing when no organization is selected."""
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 1
        assert "No organization selected" in result.stdout


class TestProjectCreate:
    """Tests for project create command."""

    def test_create_project(self, temp_dirs, authenticated_user, with_org):
        """Test creating a project."""
        result = runner.invoke(
            app,
            [
                "create",
                "--name",
                "Test Project",
                "--slug",
                "test-project",
                "--description",
                "A test project",
                "--github-url",
                "https://github.com/test/repo",
            ],
        )

        assert result.exit_code == 0
        assert "Project created" in result.stdout
        assert "Test Project" in result.stdout
        assert "test-project" in result.stdout

        # Verify project was created
        from agentflow.storage import find_project_by_slug, find_organization_by_slug

        org = find_organization_by_slug("test-org")
        project = find_project_by_slug(org.id, "test-project")
        assert project is not None
        assert project.name == "Test Project"

    def test_create_without_optional_fields(self, temp_dirs, authenticated_user, with_org):
        """Test creating project without optional fields."""
        result = runner.invoke(
            app, ["create", "--name", "Test Project", "--slug", "test-project"]
        )

        assert result.exit_code == 0
        assert "Project created" in result.stdout

    def test_create_with_org_parameter(self, temp_dirs, authenticated_user):
        """Test creating project with explicit org parameter."""
        from agentflow.commands.org import app as org_app

        # Create org but don't set it as active
        runner.invoke(
            org_app, ["create", "--name", "Test Org", "--slug", "test-org"]
        )

        # Create project with explicit org
        result = runner.invoke(
            app,
            ["create", "--name", "Test Project", "--slug", "test-project", "--org", "test-org"],
        )

        assert result.exit_code == 0
        assert "Project created" in result.stdout

    def test_rejects_duplicate_slug(self, temp_dirs, authenticated_user, with_org):
        """Test that duplicate slug is rejected."""
        # Create first project
        runner.invoke(
            app, ["create", "--name", "Project 1", "--slug", "test-project"]
        )

        # Try to create second project with same slug
        result = runner.invoke(
            app, ["create", "--name", "Project 2", "--slug", "test-project"]
        )

        assert result.exit_code == 1
        assert "already exists" in result.stdout

    def test_validates_slug_format(self, temp_dirs, authenticated_user, with_org):
        """Test that invalid slug is rejected."""
        result = runner.invoke(
            app, ["create", "--name", "Test Project", "--slug", "Invalid_Slug"]
        )

        assert result.exit_code == 1
        assert "lowercase" in result.stdout or "hyphens" in result.stdout

    def test_rejects_long_name(self, temp_dirs, authenticated_user, with_org):
        """Test that name over 255 characters is rejected."""
        long_name = "A" * 256
        result = runner.invoke(
            app, ["create", "--name", long_name, "--slug", "test-project"]
        )

        assert result.exit_code == 1
        assert "255 characters" in result.stdout

    def test_requires_authentication(self, temp_dirs):
        """Test that authentication is required."""
        result = runner.invoke(
            app, ["create", "--name", "Test Project", "--slug", "test-project"]
        )

        assert result.exit_code == 1
        assert "Not authenticated" in result.stdout


class TestProjectView:
    """Tests for project view command."""

    def test_view_project(self, temp_dirs, authenticated_user, with_org):
        """Test viewing a project."""
        # Create project
        runner.invoke(
            app,
            [
                "create",
                "--name",
                "Test Project",
                "--slug",
                "test-project",
                "--description",
                "Test description",
            ],
        )

        # View project
        result = runner.invoke(app, ["view", "test-project"])

        assert result.exit_code == 0
        assert "Test Project" in result.stdout
        assert "test-project" in result.stdout
        assert "Test description" in result.stdout

    def test_view_nonexistent_project(self, temp_dirs, authenticated_user, with_org):
        """Test viewing non-existent project."""
        result = runner.invoke(app, ["view", "nonexistent"])

        assert result.exit_code == 1
        assert "not found" in result.stdout


class TestProjectUse:
    """Tests for project use command."""

    def test_set_project(self, temp_dirs, authenticated_user, with_org):
        """Test setting active project."""
        # Create project
        runner.invoke(
            app, ["create", "--name", "Test Project", "--slug", "test-project"]
        )

        # Set as active
        result = runner.invoke(app, ["use", "test-project"])

        assert result.exit_code == 0
        assert "Now using project" in result.stdout
        assert "test-project" in result.stdout

        # Verify it was set
        from agentflow.utils.config import get_current_project

        assert get_current_project() == "test-project"

    def test_use_nonexistent_project(self, temp_dirs, authenticated_user, with_org):
        """Test using non-existent project."""
        result = runner.invoke(app, ["use", "nonexistent"])

        assert result.exit_code == 1
        assert "not found" in result.stdout

    def test_requires_authentication(self, temp_dirs):
        """Test that authentication is required."""
        result = runner.invoke(app, ["use", "test-project"])

        assert result.exit_code == 1
        assert "Not authenticated" in result.stdout
