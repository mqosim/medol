from typing import AsyncGenerator

from fastapi_cli.cli import logger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine

from src.medol.core.config import Settings
from src.medol.models.base_model import Base

POSTGRES_DB_URL = Settings.postgres_db_url()

engine: AsyncEngine = create_async_engine(POSTGRES_DB_URL, echo=True, future=True, pool_pre_ping=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def init_db():
    async with engine.begin() as conn:
        logger.info("Initializing the database...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully.")


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
