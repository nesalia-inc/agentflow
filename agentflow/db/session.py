"""Database session management utilities."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator, TypeVar

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from agentflow.db.base import get_db_session, get_session_maker


T = TypeVar("T")


class DatabaseSession:
    """Helper class for database session operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize with a database session.

        Args:
            session: SQLAlchemy async session
        """
        self.session = session

    async def add(self, obj: T) -> T:
        """Add an object to the session.

        Args:
            obj: Object to add

        Returns:
            The added object
        """
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(
        self,
        model: type[T],
        id: str | int,
    ) -> T | None:
        """Get an object by ID.

        Args:
            model: Model class
            id: Object ID

        Returns:
            The object or None if not found
        """
        stmt = select(model).where(model.id == id)  # type: ignore[attr-defined]
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        model: type[T],
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[T]:
        """List all objects of a model.

        Args:
            model: Model class
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            List of objects
        """
        stmt = select(model)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def delete(self, obj: T) -> None:
        """Delete an object.

        Args:
            obj: Object to delete
        """
        await self.session.delete(obj)
        await self.session.commit()

    async def execute(self, stmt):
        """Execute a SQL statement.

        Args:
            stmt: SQL statement

        Returns:
            Result object
        """
        return await self.session.execute(stmt)

    async def commit(self) -> None:
        """Commit the session."""
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback the session."""
        await self.session.rollback()


@asynccontextmanager
async def get_db() -> AsyncGenerator[DatabaseSession, None]:
    """
    Get a database session wrapper.

    Yields:
        DatabaseSession: Database session wrapper
    """
    async for session in get_db_session():
        yield DatabaseSession(session)


async def with_db(func):
    """Decorator to run a function with a database session.

    Args:
        func: Async function that takes a DatabaseSession as first argument

    Returns:
        Result of the function
    """

    async def wrapper(*args, **kwargs):
        async with get_db() as db:
            return await func(db, *args, **kwargs)

    return wrapper
