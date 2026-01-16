"""Tests for Workspace entity."""

import pytest

from agentflow.entities.workspace import Workspace


@pytest.mark.asyncio
async def test_create_workspace(db_session):
    """Test creating a workspace."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    workspace = await Workspace.create(
        db,
        name="test-workspace",
        description="A test workspace",
    )

    assert workspace.id is not None
    assert workspace.name == "test-workspace"
    assert workspace.description == "A test workspace"
    assert workspace.created_at is not None


@pytest.mark.asyncio
async def test_create_workspace_duplicate_name(db_session):
    """Test creating a workspace with duplicate name raises error."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    # Create first workspace
    await Workspace.create(db, name="test-workspace")

    # Try to create second workspace with same name
    with pytest.raises(ValueError, match="already exists"):
        await Workspace.create(db, name="test-workspace")


@pytest.mark.asyncio
async def test_get_by_id(db_session):
    """Test retrieving workspace by ID."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    # Create workspace
    workspace = await Workspace.create(db, name="test-workspace")

    # Retrieve by ID
    retrieved = await Workspace.get_by_id(db, workspace.id)
    assert retrieved is not None
    assert retrieved.id == workspace.id
    assert retrieved.name == "test-workspace"


@pytest.mark.asyncio
async def test_get_by_id_not_found(db_session):
    """Test retrieving non-existent workspace by ID."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    retrieved = await Workspace.get_by_id(db, "non-existent-id")
    assert retrieved is None


@pytest.mark.asyncio
async def test_get_by_name(db_session):
    """Test retrieving workspace by name."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    # Create workspace
    await Workspace.create(db, name="test-workspace")

    # Retrieve by name
    retrieved = await Workspace.get_by_name(db, "test-workspace")
    assert retrieved is not None
    assert retrieved.name == "test-workspace"


@pytest.mark.asyncio
async def test_get_by_name_not_found(db_session):
    """Test retrieving non-existent workspace by name."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    retrieved = await Workspace.get_by_name(db, "non-existent")
    assert retrieved is None


@pytest.mark.asyncio
async def test_list_all(db_session):
    """Test listing all workspaces."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    # Create multiple workspaces
    await Workspace.create(db, name="workspace-1")
    await Workspace.create(db, name="workspace-2")
    await Workspace.create(db, name="workspace-3")

    # List all
    workspaces = await Workspace.list_all(db)
    assert len(workspaces) == 3
    workspace_names = [w.name for w in workspaces]
    assert "workspace-1" in workspace_names
    assert "workspace-2" in workspace_names
    assert "workspace-3" in workspace_names


@pytest.mark.asyncio
async def test_workspace_repr(db_session):
    """Test workspace string representation."""
    workspace = Workspace(
        id="test-id",
        name="test-workspace",
    )

    repr_str = repr(workspace)
    assert "Workspace(id=test-id" in repr_str
    assert "name=test-workspace)" in repr_str
