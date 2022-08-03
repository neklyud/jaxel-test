import asyncio
from app.components.consumer import Consumer
from config import config
from tortoise import Tortoise

async def init_db():
    uri = 'postgres://{user}:{password}@{host}:{port}/{db}'.format(
        user=config.postgres_user,
        password=config.postgres_password,
        host=config.postgres_host,
        port=config.postgres_port,
        db=config.market_db,
    )
    await Tortoise.init(db_url=uri, modules={"models": ["app.models.item"]})

async def run():
    await init_db()
    await Consumer(config.kafka_host, loop=loop, topic=config.kafka_transfer_topik).run()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
