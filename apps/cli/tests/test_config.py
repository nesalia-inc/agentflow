"""Tests for config management."""

import pytest
from pathlib import Path
from unittest.mock import patch

from agentflow.utils.config import (
    load_config,
    save_config,
    get_current_user_email,
    set_current_user_email,
    get_current_api_key,
    set_current_api_key,
    get_current_organization,
    set_current_organization,
    get_current_project,
    set_current_project,
    clear_current_project,
    get_context_string,
    CONFIG_DIR,
    CONFIG_FILE,
)


@pytest.fixture
def temp_config_dir(tmp_path: Path):
    """Create temporary config directory for testing."""

    def mock_config_dir():
        return tmp_path / ".agentflow"

    with patch("agentflow.utils.config.CONFIG_DIR", mock_config_dir()):
        with patch("agentflow.utils.config.CONFIG_FILE", mock_config_dir() / "config.yaml"):
            yield


class TestLoadConfig:
    """Tests for load_config function."""

    def test_returns_empty_dict_if_file_not_exists(self, temp_config_dir):
        """Test that load_config returns empty dict if file doesn't exist."""
        config = load_config()
        assert config == {}

    def test_loads_existing_config(self, temp_config_dir):
        """Test that load_config loads existing config."""
        import agentflow.utils.config

        # Create test config
        agentflow.utils.config.CONFIG_DIR.mkdir(exist_ok=True)
        test_config = {"key": "value", "number": 42}
        with open(agentflow.utils.config.CONFIG_FILE, "w") as f:
            import yaml

            yaml.dump(test_config, f)

        # Load config
        config = load_config()

        assert config["key"] == "value"
        assert config["number"] == 42


class TestSaveConfig:
    """Tests for save_config function."""

    def test_saves_config_to_file(self, temp_config_dir):
        """Test that save_config writes to file."""
        import agentflow.utils.config
        import yaml

        test_config = {"key": "value", "nested": {"item": "test"}}
        save_config(test_config)

        # Verify file exists
        assert agentflow.utils.config.CONFIG_FILE.exists()

        # Load and verify
        with open(agentflow.utils.config.CONFIG_FILE, "r") as f:
            loaded_config = yaml.safe_load(f)

        assert loaded_config["key"] == "value"
        assert loaded_config["nested"]["item"] == "test"


class TestCurrentUserEmail:
    """Tests for current user email functions."""

    def test_get_returns_none_if_not_set(self, temp_config_dir):
        """Test that get_current_user_email returns None if not set."""
        result = get_current_user_email()
        assert result is None

    def test_set_and_get(self, temp_config_dir):
        """Test setting and getting user email."""
        set_current_user_email("test@example.com")
        result = get_current_user_email()
        assert result == "test@example.com"


class TestCurrentAPIKey:
    """Tests for current API key functions."""

    def test_get_returns_none_if_not_set(self, temp_config_dir):
        """Test that get_current_api_key returns None if not set."""
        result = get_current_api_key()
        assert result is None

    def test_set_and_get(self, temp_config_dir):
        """Test setting and getting API key."""
        set_current_api_key("afk_test_key")
        result = get_current_api_key()
        assert result == "afk_test_key"


class TestCurrentOrganization:
    """Tests for current organization functions."""

    def test_get_returns_none_if_not_set(self, temp_config_dir):
        """Test that get_current_organization returns None if not set."""
        result = get_current_organization()
        assert result is None

    def test_set_and_get(self, temp_config_dir):
        """Test setting and getting organization."""
        set_current_organization("test-org")
        result = get_current_organization()
        assert result == "test-org"


class TestCurrentProject:
    """Tests for current project functions."""

    def test_get_returns_none_if_not_set(self, temp_config_dir):
        """Test that get_current_project returns None if not set."""
        result = get_current_project()
        assert result is None

    def test_set_and_get(self, temp_config_dir):
        """Test setting and getting project."""
        set_current_project("test-project")
        result = get_current_project()
        assert result == "test-project"

    def test_clear_removes_project(self, temp_config_dir):
        """Test that clear_current_project removes project from config."""
        set_current_project("test-project")
        assert get_current_project() == "test-project"

        clear_current_project()
        assert get_current_project() is None


class TestGetContextString:
    """Tests for get_context_string function."""

    def test_returns_empty_string_if_no_context(self, temp_config_dir):
        """Test that get_context_string returns empty string if no context."""
        result = get_context_string()
        assert result == ""

    def test_returns_org_only(self, temp_config_dir):
        """Test that get_context_string returns org when only org is set."""
        set_current_organization("my-org")
        result = get_context_string()
        assert result == "[my-org]"

    def test_returns_org_and_project(self, temp_config_dir):
        """Test that get_context_string returns both when set."""
        set_current_organization("my-org")
        set_current_project("my-project")
        result = get_context_string()
        assert result == "[my-org / my-project]"

    def test_handles_project_without_org(self, temp_config_dir):
        """Test that get_context_string handles project without org."""
        # This shouldn't happen in normal usage, but test defensive behavior
        set_current_project("my-project")
        result = get_context_string()
        # Since org is not set, it should return empty or just the project
        # Current implementation returns empty when org is not set
        assert result == ""
