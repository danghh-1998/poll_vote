from sqlalchemy.ext.asyncio import AsyncConnection
from box import Box

from db import mysql_client
from utils import obj_id, current_time
from core.exceptions import *


async def create_poll(session: AsyncConnection, data: Box, user_id: str) -> Box:
    payload = Box(id=obj_id(),
                  creator_id=user_id,
                  created_at=current_time(),
                  updated_at=current_time(),
                  **data)
    await mysql_client.create_poll(session=session, payload=payload)
    return payload


async def get_poll(session: AsyncConnection, poll_id: str, user_id: str) -> Box:
    payload = Box(id=poll_id)
    results = await mysql_client.get_poll(session=session, payload=payload)
    rows, columns_name = results.fetchall(), tuple(results.keys())
    if not rows:
        raise NotFoundError
    poll_anchor, vote_anchor = 8, 14
    poll = Box(zip((column for column in columns_name[:poll_anchor]), rows[0][:poll_anchor]))
    poll.allow_add_choice = bool(poll.allow_add_choice)
    poll.allow_multiple_choice = bool(poll.allow_multiple_choice)
    votes, myself_votes = [], []
    for row in rows:
        vote = Box(zip((column for column in columns_name[poll_anchor:vote_anchor]), row[poll_anchor:vote_anchor]))
        user_votes = row[-1]
        vote.user_votes = user_votes.split(',') if user_votes else []
        if user_id in vote.user_votes:
            myself_votes.append(vote.id)
        votes.append(vote)
    poll.votes = votes
    poll.myself_votes = myself_votes
    return poll


async def check_poll_exists(session: AsyncConnection, poll_id: str) -> Box:
    payload = Box(id=poll_id)
    result = await mysql_client.check_poll_exists(session=session, payload=payload)
    row, columns_name = result.fetchone(), tuple(result.keys())
    return Box(zip(columns_name, row))


async def update_poll(session: AsyncConnection, data: Box, poll: Box) -> Box:
    data.title = data.title or poll.title
    data.allow_add_choice = data.allow_add_choice \
        if data.allow_add_choice is not None else poll.allow_add_choice
    data.allow_multiple_choice = data.allow_multiple_choice \
        if data.allow_multiple_choice is not None else poll.allow_multiple_choice
    await mysql_client.update_poll(session=session, payload=data | Box(id=poll.id, updated_at=current_time()))
    return poll | data


async def delete_poll(session: AsyncConnection, poll_id: str) -> Box:
    payload = Box(id=poll_id)
    await mysql_client.delete_poll(session=session, payload=payload)
    return payload
