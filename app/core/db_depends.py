from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import AsyncSessionLocal


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
