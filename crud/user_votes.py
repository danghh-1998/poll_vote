from sqlalchemy.ext.asyncio import AsyncConnection
from box import Box

from db import mysql_client
from utils import obj_id, current_time


async def create_user_votes(session: AsyncConnection, user_id: str, data: Box):
    payload = Box(user_id=user_id, created_at=current_time(), **data)
    await mysql_client.create_votes(session=session, payload=payload)
    return payload
