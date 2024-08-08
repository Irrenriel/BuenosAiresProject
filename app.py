# -*- coding: utf-8 -*-
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from core.redis_db import redis_db
from routers import package_router


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    # Startup:
    await redis_db.cron_update_exchange_rate()

    # Work:
    yield


# App:
app = FastAPI(lifespan=lifespan)

add_pagination(app)

app.include_router(package_router)
