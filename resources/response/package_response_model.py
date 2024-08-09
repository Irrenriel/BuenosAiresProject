# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel


class PackageResponseModel(BaseModel):
    id: int
    name: str
    weight: float
    type: dict
    value: float
    delivery_cost: Optional[float] = None
