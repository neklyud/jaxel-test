from aiokafka import AIOKafkaConsumer
from typing import Optional
import asyncio
from app.models.item import Item
import json
from tortoise.transactions import atomic

@atomic()
async def write_or_update(self, item) -> None:
    event = await Item.get(id=item['id'])
    if not event:
        await Item.create(**item)
        return


class Consumer(object):
    def __init__(self, server: str, topic: str, loop: Optional[asyncio.BaseEventLoop] = None):
        self.topic: str = topic
        self.loop = loop if loop else asyncio.get_running_loop()
        self.consumer = AIOKafkaConsumer(self.topic, bootstrap_servers=server, loop=loop)

    async def run(self):
        await self.consumer.start()
        try:
            while True:
                data = await self.consumer.getmany(timeout_ms=10000)
                for tp, messages in data.items():
                    for message in messages:
                        data = json.loads(message.value)
                        if 'item_list' not in data:
                            continue
                        for i_item in data['item_list']:
                            await Item.update_or_create(**i_item)
        finally:
            await self.consumer.stop()
