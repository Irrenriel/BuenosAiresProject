# -*- coding: utf-8 -*-
from pydantic import BaseModel


class PackageTypeCreateModel(BaseModel):
    name: str
