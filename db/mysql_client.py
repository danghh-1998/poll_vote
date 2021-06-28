from typing import Union, List

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncConnection
from box import Box

from core.config import config
from db.queries import Q


class MysqlClient:
    def __init__(self):
        url = f'mysql+aiomysql://' \
              f'{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'
        self.engine = create_async_engine(url, pool_pre_ping=True)

    async def connect(self):
        async with self.engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

    def pool(self):
        return self.engine.connect()


async def create_poll(session: AsyncConnection, payload: Box):
    await session.execute(Q.INSERT__POLL, payload)
    await session.commit()


async def get_poll(session: AsyncConnection, payload: Box):
    return await session.execute(Q.GET_BY_ID__POLL, payload)


async def check_poll_exists(session: AsyncConnection, payload: Box):
    return await session.execute(Q.CHECK_EXISTS__POLL, payload)


async def update_poll(session: AsyncConnection, payload: Box):
    await session.execute(Q.UPDATE__POLL, payload)
    await session.commit()


async def delete_poll(session: AsyncConnection, payload: Box):
    await session.execute(Q.DELETE__POLL, payload)
    await session.commit()


async def create_votes(session: AsyncConnection, payload: Union[Box, List]):
    await session.execute(Q.INSERT__VOTE, payload)
    await session.commit()


async def delete_vote(session: AsyncConnection, payload: Box):
    await session.execute(Q.DELETE__VOTE, payload)
    await session.commit()


async def update_vote(session: AsyncConnection, payload: Box):
    await session.execute(Q.UPDATE__VOTE, payload)
    await session.commit()


async def get_vote(session: AsyncConnection, payload: Box):
    return await session.execute(Q.GET_BY_POLL_ID__VOTE, payload)


async def create_user_votes(session: AsyncConnection, payload: Box):
    await session.execute(Q.INSERT__USER_VOTE, payload)
    await session.commit()
