from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.settings.config import ASYNC_DATABASE_URL


class Base(DeclarativeBase):
    pass


engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db():
    session: AsyncSession = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()
