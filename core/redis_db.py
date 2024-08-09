# -*- coding: utf-8 -*-
import json
from logging import INFO

from fastapi_utilities import repeat_every
from loguru import logger
from redis import Redis
from aiohttp import ClientSession

from config import config


class RedisConnector(Redis):
    EXCHANGE_RATE_URL = 'https://www.cbr-xml-daily.ru/daily_json.js'

    @logger.catch
    async def update_exchange_rate(self):
        async with ClientSession() as session:
            for i in range(3):
                async with session.get(self.EXCHANGE_RATE_URL) as resp:
                    if resp.status != 200:
                        self.log(f'Wrong `cbr-xml-daily` API response status! (Status: {resp.status})', level=30)
                        continue

                    data = json.loads(await resp.text())

                    if not (exchange_rate := data.get('Valute', {}).get('USD', {}).get('Value')):
                        self.log('Wrong `cbr-xml-daily` API values!', level=30)
                        self.log(data, level=30)
                        continue

                    if not isinstance(exchange_rate, float):
                        exchange_rate = float(exchange_rate)

                    self.set('exchange_rate', exchange_rate)  # noqa
                    self.log('Successfully updated exchange rate!')
                    break

            else:
                self.log('Failed to update exchange rate!', level=30)

    async def get_exchange_rate(self):
        if exchange_rate := self.get('exchange_rate'):
            return float(exchange_rate)

    @repeat_every(seconds=300)
    async def cron_update_exchange_rate(self):
        await self.update_exchange_rate()

    def log(self, msg, level=INFO):
        {
            50: logger.critical,
            40: logger.error,
            30: logger.warning,
            20: logger.info,
            10: logger.debug,
        }.get(level, logger.error)(f'[{self.__class__.__name__}] {msg}')


redis_db = RedisConnector(**config.REDIS_CONNECT)
