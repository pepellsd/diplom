from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Callable, Type
from fastapi import Depends

from app.services.database.repository.base_repository import BaseRepository
from app.config import Settings, get_settings


settings: Settings = get_settings()

engine = create_async_engine(settings.DATABASE_URI, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession, autocommit=False, autoflush=False)
Base = declarative_base()


async def get_session() -> Callable[[], AsyncSession]:
    async with async_session() as session:
        yield session


async def get_session_stub():
    raise NotImplementedError


def get_repository(Repo_type: Type[BaseRepository]) -> Callable:
    def get_repo(db: AsyncSession = Depends(get_session)) -> BaseRepository:
        return Repo_type(db)
    return get_repo

