from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from core.config import config


class MysqlClient:
    def __init__(self):
        url = f'mysql+aiomysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}'
        self.engine = create_async_engine(url, pool_pre_ping=True)

    async def connect(self):
        async with self.engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

    def pool(self):
        return self.engine.connect()
