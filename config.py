# -*- coding: utf-8 -*-
from os import getenv

from dotenv import load_dotenv
from pydantic.v1 import BaseConfig
from sqlalchemy import URL


class Config(BaseConfig):
    load_dotenv()
    DEBUG: bool = bool(int(getenv('DEBUG')))

    # == SQLAlchemy Variables == #
    DB_CONNECT: str = URL.create(
        drivername='mysql+aiomysql',
        username=getenv('MYSQL_USER'),
        password=getenv('MYSQL_PASSWORD'),
        host=getenv('MYSQL_HOST'),
        port=int(getenv('MYSQL_PORT')),
        database=getenv('MYSQL_DATABASE')
    )

    ALEMBIC_CONNECT = URL.create(
        drivername='mysql+pymysql',
        username=getenv('MYSQL_USER'),
        password=getenv('MYSQL_PASSWORD'),
        host=getenv('MYSQL_HOST'),
        port=int(getenv('MYSQL_PORT')),
        database=getenv('MYSQL_DATABASE')
    )

    REDIS_CONNECT = {
        'host': getenv('REDIS_HOST'),
        'port': int(getenv('REDIS_PORT')),
    }


config = Config()
