from tortoise import Tortoise, run_async
from config import config
import logging
import asyncpg

logging.basicConfig(level=logging.INFO)

async def connect_create_if_not_exists():
    try:
        conn = await asyncpg.connect(
            user=config.postgres_user,
            password=config.postgres_password,
            database=config.market_db,
            host=config.postgres_host,
            port=config.postgres_port
        )
    except asyncpg.InvalidCatalogNameError:
        # Database does not exist, create it.
        sys_conn = await asyncpg.connect(
            database='template1',
            user=config.postgres_user,
            password=config.postgres_password,
            host=config.postgres_host,
            port=config.postgres_port,
        )
        await sys_conn.execute(
            f'CREATE DATABASE "{config.market_db}" OWNER "{config.postgres_user}"'
        )
        await sys_conn.close()

        # Connect to the newly created database.
        conn = await asyncpg.connect(
            user=config.postgres_user,
            password=config.postgres_password,
            host=config.postgres_host,
            port=config.postgres_port,
            database=config.market_db,
        )

    return conn

async def init():
    logging.info(f'Connect to {config.postgres_host}:{config.postgres_port} with user - {config.postgres_user}')
    await connect_create_if_not_exists()
    await Tortoise.init(
        config={
            'connections': {
                'default': {
                    "engine": "tortoise.backends.asyncpg",
                    "credentials": {
                        'database': config.market_db,
                        "host": config.postgres_host,
                        "password": config.postgres_password,
                        "port": config.postgres_port,
                        "user": config.postgres_user,
                    },
                },
            },
            'apps': {
                'models': {
                    'models': ['app.models.item'],
                    'default_connection': 'default'
                },
            }
        },
    )

    await Tortoise.generate_schemas()
    

if __name__ == '__main__':
    run_async(init())
