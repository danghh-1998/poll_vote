from typing import Union, List

from sqlalchemy.ext.asyncio import AsyncConnection
from box import Box

from db import mysql_client
from utils import current_time, obj_id
from core.exceptions import NotFoundError


async def create_votes(session: AsyncConnection, data: List, poll: Box) -> List[Box]:
    payload = [Box(id=obj_id(),
                   creator_id=poll.creator_id,
                   last_user_update=poll.creator_id,
                   poll_id=poll.id,
                   created_at=current_time(),
                   updated_at=current_time(),
                   count=0,
                   **vote.__dict__) for vote in data]
    await mysql_client.create_votes(session=session, payload=payload)
    return payload


async def get_vote(session: AsyncConnection, poll_id: str, vote_id: str) -> Box:
    payload = Box(poll_id=poll_id, vote_id=vote_id)
    result = await mysql_client.get_vote(session=session, payload=payload)
    row, columns_name = result.fetchone(), tuple(result.keys())
    if not row:
        raise NotFoundError
    return Box(zip(columns_name, row))


async def update_vote(session: AsyncConnection, vote: Box, data: Box, user_id: str) -> Box:
    payload = Box(title=data.title or vote.title,
                  image=data.image or vote.image,
                  id=vote.id,
                  last_user_update=user_id,
                  updated_at=current_time())
    await mysql_client.update_vote(session=session, payload=payload)
    return vote | payload


async def delete_vote(session: AsyncConnection, vote_id: str) -> Box:
    payload = Box(id=vote_id)
    await mysql_client.delete_vote(session=session, payload=payload)
    return payload
