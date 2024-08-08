# -*- coding: utf-8 -*-
from typing import List, Self

from sqlalchemy import Column, INTEGER, VARCHAR, DateTime, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import Base


class PackageTypeModel(Base):
    __tablename__ = 'package_types'

    # Base Columns:
    id = Column('id', INTEGER, primary_key=True, index=True)
    name = Column('name', VARCHAR(128), unique=True, index=True)

    # Settings Columns:
    created_at = Column("created_at", DateTime, default=func.now())
    updated_at = Column("updated_at", DateTime, onupdate=func.now(), default=func.now())

    @classmethod
    async def get_all(cls, session: AsyncSession = None) -> List[Self]:
        return await cls.fetchall(select(cls), session=session)
