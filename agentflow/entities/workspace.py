"""Workspace entity for organizing work."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import String, DateTime, Text, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from agentflow.db.base import Base
from agentflow.db.session import DatabaseSession
from agentflow.utils.id_generator import generate_id

if TYPE_CHECKING:
    from agentflow.entities.session import Session
    from agentflow.entities.commit import Commit


class Workspace(Base):
    """Represents a workspace for organizing work."""

    __tablename__ = "workspaces"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_id)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    sessions: Mapped[List["Session"]] = relationship(  # type: ignore[name-defined]
        back_populates="workspace",
        cascade="all, delete-orphan",
    )
    commits: Mapped[List["Commit"]] = relationship(  # type: ignore[name-defined]
        back_populates="workspace",
        cascade="all, delete-orphan",
    )

    @classmethod
    async def create(cls, db: DatabaseSession, name: str, description: str | None = None) -> "Workspace":
        """Create a new workspace.

        Args:
            db: Database session
            name: Workspace name
            description: Optional description

        Returns:
            The created Workspace instance

        Raises:
            ValueError: If workspace name already exists
        """
        # Check if workspace with same name exists
        existing = await cls.get_by_name(db, name)
        if existing:
            raise ValueError(f"Workspace with name '{name}' already exists")

        workspace = cls(
            id=generate_id(),
            name=name,
            description=description,
            created_at=datetime.utcnow(),
        )
        return await db.add(workspace)

    @classmethod
    async def get_by_id(cls, db: DatabaseSession, workspace_id: str) -> "Workspace | None":
        """Retrieve a workspace by ID.

        Args:
            db: Database session
            workspace_id: Workspace ID

        Returns:
            Workspace instance or None if not found
        """
        return await db.get(cls, workspace_id)

    @classmethod
    async def get_by_name(cls, db: DatabaseSession, name: str) -> "Workspace | None":
        """Retrieve a workspace by name.

        Args:
            db: Database session
            name: Workspace name

        Returns:
            Workspace instance or None if not found
        """
        stmt = select(cls).where(cls.name == name)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def list_all(cls, db: DatabaseSession) -> list["Workspace"]:
        """List all workspaces.

        Args:
            db: Database session

        Returns:
            List of workspaces ordered by creation date (newest first)
        """
        stmt = select(cls).order_by(cls.created_at.desc())
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def add_session(self, db: DatabaseSession, task: str) -> "Session":
        """Create a new session in this workspace.

        Args:
            db: Database session
            task: Task description

        Returns:
            The created Session instance
        """
        from agentflow.entities.session import Session
        session = Session.create(self.id, task)
        return await db.add(session)

    async def get_commits(self, db: DatabaseSession, limit: int | None = None) -> list["Commit"]:
        """Get commits from this workspace.

        Args:
            db: Database session
            limit: Maximum number of commits to return

        Returns:
            List of commits ordered by creation date (newest first)
        """
        from agentflow.entities.commit import Commit

        stmt = select(Commit).where(
            Commit.workspace_id == self.id
        ).order_by(Commit.created_at.desc())

        if limit:
            stmt = stmt.limit(limit)

        result = await db.execute(stmt)
        return list(result.scalars().all())

    def __repr__(self) -> str:
        return f"Workspace(id={self.id}, name={self.name})"
