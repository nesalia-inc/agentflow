"""Tests for Session entity."""

import pytest
from datetime import datetime, timedelta

from agentflow.entities.session import Session, SessionStatus
from agentflow.entities.workspace import Workspace


@pytest.mark.asyncio
async def test_create_session(db_session):
    """Test creating a session."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    session = await Session.create(
        db,
        workspace_id="test-workspace-1",
        task="Implement authentication",
    )

    assert session.id is not None
    assert session.workspace_id == "test-workspace-1"
    assert session.task == "Implement authentication"
    assert session.status == SessionStatus.ACTIVE
    assert session.started_at is not None
    assert session.completed_at is None


@pytest.mark.asyncio
async def test_session_get_active(db_session):
    """Test retrieving active session for workspace."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    # Create active session
    session1 = await Session.create(db, workspace_id="ws-1", task="Task 1")

    # Get active session
    retrieved = await Session.get_active(db, "ws-1")
    assert retrieved is not None
    assert retrieved.id == session1.id
    assert retrieved.is_active is True


@pytest.mark.asyncio
async def test_session_get_active_none(db_session):
    """Test retrieving active session when none exists."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    retrieved = await Session.get_active(db, "non-existent-ws")
    assert retrieved is None


@pytest.mark.asyncio
async def test_session_log_action(db_session):
    """Test logging an action to a session."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    # Create session
    session = await Session.create(db, workspace_id="ws-1", task="Test task")

    # Log action
    action = await session.log_action(
        db,
        description="Created a file",
        action_type="file_create",
        metadata={"file": "test.py"},
    )

    assert action.id is not None
    assert action.session_id == session.id
    assert action.description == "Created a file"
    assert action.action_type == "file_create"


@pytest.mark.asyncio
async def test_session_complete(db_session):
    """Test completing a session."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    # Create session
    session = await Session.create(db, workspace_id="ws-1", task="Test task")
    session.started_at = datetime.utcnow() - timedelta(seconds=100)
    await db.commit()

    # Complete session
    commit = await session.complete(
        db,
        message="feat: implemented feature",
        description="Detailed description",
    )

    assert commit.id is not None
    assert commit.message == "feat: implemented feature"
    assert commit.description == "Detailed description"
    assert commit.workspace_id == session.workspace_id

    # Check session is updated
    await db_session.refresh(session)
    assert session.status == SessionStatus.COMPLETED
    assert session.completed_at is not None
    assert session.duration_seconds is not None


@pytest.mark.asyncio
async def test_session_abort(db_session):
    """Test aborting a session."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    # Create session
    session = await Session.create(db, workspace_id="ws-1", task="Test task")

    # Abort session
    await session.abort(db)

    # Check session is updated
    await db_session.refresh(session)
    assert session.status == SessionStatus.ABORTED
    assert session.completed_at is not None


@pytest.mark.asyncio
async def test_session_duration(db_session):
    """Test session duration calculation."""
    # Create completed session
    session = Session(
        id="test-session",
        workspace_id="ws-1",
        task="Test task",
        started_at=datetime.utcnow() - timedelta(seconds=150),
        completed_at=datetime.utcnow() - timedelta(seconds=50),
        status=SessionStatus.COMPLETED,
    )

    assert session.duration_seconds == 100


@pytest.mark.asyncio
async def test_session_duration_not_completed(db_session):
    """Test duration is None for active session."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    session = await Session.create(db, workspace_id="ws-1", task="Test task")

    assert session.duration_seconds is None


@pytest.mark.asyncio
async def test_session_is_active(db_session):
    """Test is_active property."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    active_session = await Session.create(db, workspace_id="ws-1", task="Task")
    assert active_session.is_active is True

    completed_session = Session(
        id="test",
        workspace_id="ws-1",
        task="Task",
        status=SessionStatus.COMPLETED,
    )
    assert completed_session.is_active is False


@pytest.mark.asyncio
async def test_session_get_actions(db_session):
    """Test getting session actions."""
    from agentflow.db.session import DatabaseSession

    db = DatabaseSession(db_session)

    # Create session
    session = await Session.create(db, workspace_id="ws-1", task="Test task")

    # Log multiple actions
    await session.log_action(db, "Action 1", "type1")
    await session.log_action(db, "Action 2", "type2")
    await session.log_action(db, "Action 3", "type3")

    # Get actions
    actions = await session.get_actions(db)
    assert len(actions) == 3
    assert [a.description for a in actions] == ["Action 1", "Action 2", "Action 3"]


@pytest.mark.asyncio
async def test_session_repr(db_session):
    """Test session string representation."""
    session = Session(
        id="test-id",
        workspace_id="ws-1",
        task="This is a very long task description that should be truncated",
    )

    repr_str = repr(session)
    assert "Session(id=test-id" in repr_str
    assert "..." in repr_str  # Truncated task
    assert f"status={session.status}" in repr_str
