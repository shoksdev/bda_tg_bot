import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.models import Base

engine = create_async_engine(os.getenv('DATABASE_ENGINE'), echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_database():
    """Создаём базу данных"""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_database():
    """Очищаем базу данных"""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)