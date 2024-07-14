from typing import AsyncGenerator
from sqlalchemy.ext.asyncio.session import AsyncSession
from ...database import async_session


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session
