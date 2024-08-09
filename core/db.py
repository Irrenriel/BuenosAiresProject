# -*- coding: utf-8 -*-
import traceback

from loguru import logger
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import config

Engine = create_async_engine(config.DB_CONNECT, echo=config.DEBUG, pool_size=1000, max_overflow=0)
SessionMaker = async_sessionmaker(Engine, class_=AsyncSession, autocommit=False, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    @classmethod
    async def execute(cls, expression, session: AsyncSession = None):
        if session:
            return await session.execute(expression)

        async with SessionContext() as session:
            return await session.execute(expression)

    @classmethod
    async def fetchall(cls, req: Select, session: AsyncSession = None):
        return [item[0] for item in (await cls.execute(req, session=session)).all()]

    @classmethod
    async def fetchone(cls, req: Select, session: AsyncSession = None):
        result = (await cls.execute(req.limit(1), session=session)).one_or_none()
        return result[0] if result else result


async def SessionContext() -> AsyncSession:
    session = SessionMaker()

    try:
        yield session
        await session.commit()

    except Exception:
        logger.error(traceback.format_exc())
        await session.rollback()

    finally:
        await session.close()
