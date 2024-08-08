# -*- coding: utf-8 -*-
from pydantic import BaseModel, field_validator


class PackageCreateModel(BaseModel):
    name: str
    weight: float
    type_id: int
    value: float

    @field_validator('weight', 'value')
    def positive_weight_check(cls, value):  # noqa
        if not isinstance(value, float):
            value = float(value)

        if value < 0:
            raise ValueError('Must be positive')

        return value
