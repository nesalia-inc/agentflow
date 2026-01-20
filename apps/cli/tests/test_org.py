"""Tests for organization commands."""

import pytest
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner

from agentflow.commands.org import app

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


class TestOrgList:
    """Tests for org list command."""

    def test_list_when_no_orgs(self, temp_dirs, authenticated_user):
        """Test listing organizations when none exist."""
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "No organizations found" in result.stdout

    def test_list_with_orgs(self, temp_dirs, authenticated_user):
        """Test listing organizations."""
        # Create two organizations
        runner.invoke(
            app,
            ["create", "--name", "Org 1", "--slug", "org-1", "--description", "First org"],
        )
        runner.invoke(
            app, ["create", "--name", "Org 2", "--slug", "org-2"]
        )

        # List
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "Org 1" in result.stdout
        assert "Org 2" in result.stdout
        assert "org-1" in result.stdout
        assert "org-2" in result.stdout
        assert "0" in result.stdout  # Project count

    def test_list_when_not_authenticated(self, temp_dirs):
        """Test listing when not authenticated."""
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 1
        assert "Not authenticated" in result.stdout


class TestOrgCreate:
    """Tests for org create command."""

    def test_create_organization(self, temp_dirs, authenticated_user):
        """Test creating an organization."""
        result = runner.invoke(
            app,
            ["create", "--name", "Test Org", "--slug", "test-org", "--description", "A test organization"],
        )

        assert result.exit_code == 0
        assert "Organization created" in result.stdout
        assert "Test Org" in result.stdout
        assert "test-org" in result.stdout

        # Verify org was created
        from agentflow.storage import find_organization_by_slug

        org = find_organization_by_slug("test-org")
        assert org is not None
        assert org.name == "Test Org"
        assert org.description == "A test organization"

    def test_create_without_description(self, temp_dirs, authenticated_user):
        """Test creating org without description."""
        result = runner.invoke(
            app, ["create", "--name", "Test Org", "--slug", "test-org"]
        )

        assert result.exit_code == 0
        assert "Organization created" in result.stdout

    def test_rejects_duplicate_slug(self, temp_dirs, authenticated_user):
        """Test that duplicate slug is rejected."""
        # Create first org
        runner.invoke(
            app, ["create", "--name", "Org 1", "--slug", "test-org"]
        )

        # Try to create second org with same slug
        result = runner.invoke(
            app, ["create", "--name", "Org 2", "--slug", "test-org"]
        )

        assert result.exit_code == 1
        assert "already exists" in result.stdout

    def test_validates_slug_format(self, temp_dirs, authenticated_user):
        """Test that invalid slug is rejected."""
        result = runner.invoke(
            app, ["create", "--name", "Test Org", "--slug", "Invalid_Slug"]
        )

        assert result.exit_code == 1
        assert "lowercase" in result.stdout or "hyphens" in result.stdout

    def test_rejects_long_name(self, temp_dirs, authenticated_user):
        """Test that name over 255 characters is rejected."""
        long_name = "A" * 256
        result = runner.invoke(
            app, ["create", "--name", long_name, "--slug", "test-org"]
        )

        assert result.exit_code == 1
        assert "255 characters" in result.stdout

    def test_requires_authentication(self, temp_dirs):
        """Test that authentication is required."""
        result = runner.invoke(
            app, ["create", "--name", "Test Org", "--slug", "test-org"]
        )

        assert result.exit_code == 1
        assert "Not authenticated" in result.stdout


class TestOrgView:
    """Tests for org view command."""

    def test_view_organization(self, temp_dirs, authenticated_user):
        """Test viewing an organization."""
        # Create org
        runner.invoke(
            app,
            ["create", "--name", "Test Org", "--slug", "test-org", "--description", "Test description"],
        )

        # View org
        result = runner.invoke(app, ["view", "test-org"])

        assert result.exit_code == 0
        assert "Test Org" in result.stdout
        assert "test-org" in result.stdout
        assert "Test description" in result.stdout
        assert "Projects: 0" in result.stdout

    def test_view_nonexistent_org(self, temp_dirs, authenticated_user):
        """Test viewing non-existent organization."""
        result = runner.invoke(app, ["view", "nonexistent"])

        assert result.exit_code == 1
        assert "not found" in result.stdout

    def test_view_org_with_projects(self, temp_dirs, authenticated_user):
        """Test viewing org with projects."""
        # Create org
        runner.invoke(
            app, ["create", "--name", "Test Org", "--slug", "test-org"]
        )

        # Set org as active
        runner.invoke(app, ["use", "test-org"])

        # Create a project
        from agentflow.commands.project import app as project_app

        runner.invoke(
            project_app,
            ["create", "--name", "Test Project", "--slug", "test-project"],
        )

        # View org
        result = runner.invoke(app, ["view", "test-org"])

        assert result.exit_code == 0
        assert "Test Project" in result.stdout
        assert "Projects (1):" in result.stdout


class TestOrgUse:
    """Tests for org use command."""

    def test_set_organization(self, temp_dirs, authenticated_user):
        """Test setting active organization."""
        # Create org
        runner.invoke(
            app, ["create", "--name", "Test Org", "--slug", "test-org"]
        )

        # Set as active
        result = runner.invoke(app, ["use", "test-org"])

        assert result.exit_code == 0
        assert "Now using organization" in result.stdout
        assert "test-org" in result.stdout

        # Verify it was set
        from agentflow.utils.config import get_current_organization

        assert get_current_organization() == "test-org"

    def test_clears_project_on_org_change(self, temp_dirs, authenticated_user):
        """Test that changing org clears project context."""
        # Create orgs
        runner.invoke(
            app, ["create", "--name", "Org 1", "--slug", "org-1"]
        )
        runner.invoke(
            app, ["create", "--name", "Org 2", "--slug", "org-2"]
        )

        # Set first org and create a project
        runner.invoke(app, ["use", "org-1"])
        from agentflow.commands.project import app as project_app

        runner.invoke(
            project_app,
            ["create", "--name", "Test Project", "--slug", "test-project"],
        )

        # Verify project is set
        from agentflow.utils.config import get_current_project

        assert get_current_project() == "test-project"

        # Change to second org
        runner.invoke(app, ["use", "org-2"])

        # Project should be cleared
        assert get_current_project() is None

    def test_use_nonexistent_org(self, temp_dirs, authenticated_user):
        """Test using non-existent organization."""
        result = runner.invoke(app, ["use", "nonexistent"])

        assert result.exit_code == 1
        assert "not found" in result.stdout

    def test_requires_authentication(self, temp_dirs):
        """Test that authentication is required."""
        result = runner.invoke(app, ["use", "test-org"])

        assert result.exit_code == 1
        assert "Not authenticated" in result.stdout
