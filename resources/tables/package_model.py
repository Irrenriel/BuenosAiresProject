# -*- coding: utf-8 -*-
from typing import List, Self, Optional

from sqlalchemy import Column, INTEGER, VARCHAR, Float, ForeignKey, DateTime, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from core.db import Base
from resources.tables.package_type_model import PackageTypeModel


class PackageModel(Base):
    __tablename__ = 'packages'

    # Base Columns:
    id = Column('id', INTEGER, primary_key=True, index=True)
    name = Column('name', VARCHAR(255), index=True)

    # Data Columns:
    weight = Column('weight', Float)
    type_id = Column(INTEGER, ForeignKey(PackageTypeModel.id))
    value = Column(Float)
    delivery_cost = Column(Float, nullable=True)

    # Settings Columns:
    created_at = Column("created_at", DateTime, default=func.now())
    updated_at = Column("updated_at", DateTime, onupdate=func.now(), default=func.now())

    # ORM:
    type = relationship(PackageTypeModel, lazy='selectin')

    @classmethod
    async def get_all(cls, session: AsyncSession = None) -> List[Self]:
        return await cls.fetchall(select(cls), session=session)

    @classmethod
    def get_delivery_cost(cls, weight: float, value: float, exchange_rate: float) -> Optional[float]:
        return (weight * 0.5 + value * 0.01) * exchange_rate if exchange_rate else None
