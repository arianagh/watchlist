from asyncio import current_task
from typing import AsyncGenerator, Type

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine, AsyncEngine,
)
from sqlalchemy.orm import DeclarativeBase

from movie.src.core.config import settings

AsyncPostgreSQLEngine: AsyncEngine = create_async_engine(settings.full_database_url, future=True, echo=True)


AsyncPostgreSQLScopedSession = async_scoped_session(
    async_sessionmaker(
        AsyncPostgreSQLEngine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
        class_=AsyncSession,
    ),
    scopefunc=current_task,
)


async def initialize_postgres_db(declarative_base: Type[DeclarativeBase]):
    async_engine = AsyncPostgreSQLEngine
    metadata = declarative_base.metadata

    async with async_engine.begin() as connection:
        if settings.RESET_DB:
            await connection.run_sync(metadata.drop_all)

        await connection.run_sync(metadata.create_all)

    await async_engine.dispose()


def get_async_postgresql_session() -> AsyncSession:
    return AsyncPostgreSQLScopedSession()


async def async_postgresql_session_context_manager() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncPostgreSQLScopedSession() as session:
        yield session