"""Main module."""

import aiohttp
import logging
import asyncio
import http
import json
from models.item import Item, ItemList
from typing import List
from pydantic import parse_raw_as
from aiokafka import AIOKafkaProducer
from components.kafka_client import KafkaProducer
from components.http_client import PersistentClient
from config import config

logging.basicConfig(level=logging.INFO)
    

class Observer(object):
    """Class that provede methods to get data from resource."""

    def __init__(self, http_client: PersistentClient, kafka_client: KafkaProducer, url: str, interval: int = 5):
        """Observer constructor."""

        self.client: PersistentClient = http_client
        self.producer: KafkaProducer = kafka_client
        self.interval: int = interval
        self.last_trade: int | None
        self.base_url: str = url

    async def run(self, pair: str) -> None:
        pair_dict = {'market': pair}
        await self.producer.start()
        try:
            while True:
                try:
                    market_data = await self.client.get(endpoint=self.base_url, query_parameters=pair_dict)
                    logging.info('New message received')
                    await self.producer.push(market_data.json().encode())
                    logging.info('Message send to kafka.')
                    await asyncio.sleep(self.interval)
                except Exception as ex:
                    logging.info(str(ex))
                    continue
        finally:
            await self.client.close()
            await self.producer.stop()

def run():
    http_client = PersistentClient()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    kafka_producer = KafkaProducer(server=config.kafka_host, topic=config.kafka_transfer_topik, loop=loop)
    observer = Observer(
        http_client=http_client,
        kafka_client=kafka_producer, 

        interval=config.listen_timeout, 
        url=f'{config.garantex_api_host}/trades',
    )
    loop.run_until_complete(observer.run('usdtrub'))


if __name__ == '__main__':
    run()
