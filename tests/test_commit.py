"""Tests for Commit entity."""

import pytest
from datetime import datetime, timedelta

from agentflow.entities.commit import Commit
from agentflow.entities.workspace import Workspace
from agentflow.entities.session import Session


@pytest.mark.asyncio
async def test_commit_fields(db_session):
    """Test commit fields."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    # Create workspace and session
    workspace = await Workspace.create(db, name="test-ws")
    session = await Session.create(db, workspace.id, "Test task")
    session.started_at = datetime.utcnow() - timedelta(seconds=100)
    session.completed_at = datetime.utcnow() - timedelta(seconds=50)
    await db.commit()

    # Create commit
    commit = Commit(
        id="test-commit",
        session_id=session.id,
        workspace_id=workspace.id,
        message="feat: add authentication",
        description="Implemented login and registration",
        duration_seconds=50,
    )

    await db.add(commit)

    assert commit.id == "test-commit"
    assert commit.session_id == session.id
    assert commit.workspace_id == workspace.id
    assert commit.message == "feat: add authentication"
    assert commit.description == "Implemented login and registration"
    assert commit.duration_seconds == 50
    assert commit.created_at is not None


@pytest.mark.asyncio
async def test_get_by_id(db_session):
    """Test retrieving commit by ID."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    # Create workspace, session and commit
    workspace = await Workspace.create(db, name="test-ws")
    session = await Session.create(db, workspace.id, "Test task")

    commit = Commit(
        id="test-commit",
        session_id=session.id,
        workspace_id=workspace.id,
        message="Test commit",
    )
    await db.add(commit)

    # Retrieve by ID
    retrieved = await Commit.get_by_id(db, "test-commit")
    assert retrieved is not None
    assert retrieved.id == "test-commit"
    assert retrieved.message == "Test commit"


@pytest.mark.asyncio
async def test_get_by_id_not_found(db_session):
    """Test retrieving non-existent commit."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    retrieved = await Commit.get_by_id(db, "non-existent")
    assert retrieved is None


@pytest.mark.asyncio
async def test_list_for_workspace(db_session):
    """Test listing commits for a workspace."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    # Create workspace
    workspace = await Workspace.create(db, name="test-ws")

    # Create multiple sessions and commits
    for i in range(3):
        session = await Session.create(db, workspace.id, f"Task {i}")

        commit = Commit(
            id=f"commit-{i}",
            session_id=session.id,
            workspace_id=workspace.id,
            message=f"Commit {i}",
        )
        # Add delay to ensure different created_at
        commit.created_at = datetime.utcnow() + timedelta(seconds=i)
        await db.add(commit)

    # List commits
    commits = await Commit.list_for_workspace(db, workspace.id)
    assert len(commits) == 3
    # Should be ordered by created_at desc (newest first)
    assert commits[0].id == "commit-2"
    assert commits[1].id == "commit-1"
    assert commits[2].id == "commit-0"


@pytest.mark.asyncio
async def test_list_for_workspace_with_limit(db_session):
    """Test listing commits with limit."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    # Create workspace
    workspace = await Workspace.create(db, name="test-ws")

    # Create multiple commits
    for i in range(5):
        session = await Session.create(db, workspace.id, f"Task {i}")

        commit = Commit(
            id=f"commit-{i}",
            session_id=session.id,
            workspace_id=workspace.id,
            message=f"Commit {i}",
        )
        await db.add(commit)

    # List with limit
    commits = await Commit.list_for_workspace(db, workspace.id, limit=3)
    assert len(commits) == 3


@pytest.mark.asyncio
async def test_get_session(db_session):
    """Test getting session from commit."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    # Create workspace and session
    workspace = await Workspace.create(db, name="test-ws")
    session = await Session.create(db, workspace.id, "Test task")

    # Create commit
    commit = Commit(
        id="test-commit",
        session_id=session.id,
        workspace_id=workspace.id,
        message="Test commit",
    )
    await db.add(commit)

    # Get session
    retrieved_session = await commit.get_session(db)
    assert retrieved_session is not None
    assert retrieved_session.id == session.id


@pytest.mark.asyncio
async def test_get_actions(db_session):
    """Test getting actions from commit."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    # Create workspace and session
    workspace = await Workspace.create(db, name="test-ws")
    session = await Session.create(db, workspace.id, "Test task")

    # Add actions to session
    await session.log_action(db, "Action 1", "type1")
    await session.log_action(db, "Action 2", "type2")

    # Create commit
    commit = Commit(
        id="test-commit",
        session_id=session.id,
        workspace_id=workspace.id,
        message="Test commit",
    )
    await db.add(commit)

    # Get actions
    actions = await commit.get_actions(db)
    assert len(actions) == 2
    assert [a.description for a in actions] == ["Action 1", "Action 2"]


@pytest.mark.asyncio
async def test_short_message(db_session):
    """Test short_message property."""
    # Short message
    commit1 = Commit(
        id="test-1",
        session_id="session-1",
        workspace_id="ws-1",
        message="Short",
    )
    assert commit1.short_message == "Short"

    # Long message
    long_message = "This is a very long message that should be truncated"
    commit2 = Commit(
        id="test-2",
        session_id="session-1",
        workspace_id="ws-1",
        message=long_message,
    )
    assert commit2.short_message == long_message[:47] + "..."


@pytest.mark.asyncio
async def test_has_parent(db_session):
    """Test has_parent property."""
    # Commit without parent
    commit1 = Commit(
        id="commit-1",
        session_id="session-1",
        workspace_id="ws-1",
        message="First commit",
        parent_id=None,
    )
    assert commit1.has_parent is False

    # Commit with parent
    commit2 = Commit(
        id="commit-2",
        session_id="session-1",
        workspace_id="ws-1",
        message="Second commit",
        parent_id="commit-1",
    )
    assert commit2.has_parent is True


@pytest.mark.asyncio
async def test_commit_repr(db_session):
    """Test commit string representation."""
    commit = Commit(
        id="test-commit",
        session_id="session-1",
        workspace_id="ws-1",
        message="feat: add authentication",
    )

    repr_str = repr(commit)
    assert "Commit(id=test-commit" in repr_str
    assert "message=" in repr_str


@pytest.mark.asyncio
async def test_get_last_for_workspace(db_session):
    """Test _get_last_for_workspace class method."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    # Create workspace
    workspace = await Workspace.create(db, name="test-ws")

    # Create multiple commits
    for i in range(3):
        session = await Session.create(db, workspace.id, f"Task {i}")

        commit = Commit(
            id=f"commit-{i}",
            session_id=session.id,
            workspace_id=workspace.id,
            message=f"Commit {i}",
        )
        # Add delay to ensure order
        commit.created_at = datetime.utcnow() + timedelta(seconds=i)
        await db.add(commit)

    # Get last commit
    last = await Commit._get_last_for_workspace(db, workspace.id)
    assert last is not None
    assert last.id == "commit-2"


@pytest.mark.asyncio
async def test_get_last_for_workspace_empty(db_session):
    """Test _get_last_for_workspace when no commits exist."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    # Create workspace without commits
    workspace = await Workspace.create(db, name="test-ws")

    last = await Commit._get_last_for_workspace(db, workspace.id)
    assert last is None
