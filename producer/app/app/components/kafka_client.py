from aiokafka import AIOKafkaProducer
from components.common import Singleton
from typing import Optional, Any

import asyncio

class KafkaProducer(object, metaclass=Singleton):
    def __init__(self, server: str, topic: str, loop: Optional[Any] = None):
        self._loop = loop if loop else asyncio.get_event_loop()
        self._producer: AIOKafkaProducer = AIOKafkaProducer(loop=self._loop, bootstrap_servers=server)
        self.topic: str = topic

    async def start(self) -> None:
        await self._producer.start()

    async def stop(self) -> None:
        await self._producer.stop()
    
    async def push(self, message: bytes) -> None:
        await self._producer.send_and_wait(self.topic, value=message, timestamp_ms=10000)
