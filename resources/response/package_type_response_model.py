# -*- coding: utf-8 -*-
from pydantic import BaseModel


class PackageTypeResponseModel(BaseModel):
    id: int
    name: str
