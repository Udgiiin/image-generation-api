from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from typing import Any, Dict
import humps

engine = create_async_engine(settings.DATABASE_URI)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with SessionLocal() as session:
        yield session


Base = declarative_base()

