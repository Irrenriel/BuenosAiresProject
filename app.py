# -*- coding: utf-8 -*-
import traceback
from contextlib import asynccontextmanager

import alembic.config
from fastapi import FastAPI, Request
from fastapi_pagination import add_pagination
from loguru import logger

from core.redis_db import redis_db
from routers import package_router


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    # Migrations:
    alembic.config.main(argv=['--raiseerr', 'upgrade', 'head'])

    # Startup:
    await redis_db.cron_update_exchange_rate()

    # Work:
    yield

# App:
app = FastAPI(lifespan=lifespan)

add_pagination(app)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"[Request] {request.method} {request.url.path}")
    response = None

    try:
        response = await call_next(request)

    except Exception:
        logger.error(traceback.format_exc())

    finally:
        logger.info(f"[Response] {request.method} {request.url.path} — {response.status_code if response else 'None'}")

    return response

app.include_router(package_router)
