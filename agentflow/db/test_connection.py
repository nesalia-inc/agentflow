"""Test database connection."""

import asyncio
from sqlalchemy import text

from agentflow.db.base import get_db_session
from agentflow.config.database import get_database_settings


async def test_connection() -> bool:
    """Test database connection.

    Returns:
        True if connection successful, False otherwise
    """
    try:
        settings = get_database_settings()
        print(f"Testing connection to: {settings.db_url}")

        async for session in get_db_session():
            result = await session.execute(text("SELECT 1"))
            value = result.scalar()
            print(f"✅ Connection successful! Query result: {value}")
            return True

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


if __name__ == "__main__":
    asyncio.run(test_connection())
