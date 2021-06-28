from fastapi import APIRouter, Depends, Request
from box import Box

import crud
from core.exceptions import *
from middlewares import get_user_id
from schemas import ResponseBM, UserVote
from core.config import config

router = APIRouter()


@router.post('/{poll_id}/vote')
async def create_user_votes(request: Request, poll_id: str, data: UserVote, user_id: Depends(get_user_id)):
    mysql_pool = request.state.mysql_pool
    async with mysql_pool() as session:
        await crud.check_poll_exists(session=session, poll_id=poll_id)
        await crud.create_user_votes(session=session, user_id=user_id, data=Box(**data.__dict__))
    return ResponseBM(data=Box())


@router.delete('/{poll_id}/vote')
async def create_user_votes(request: Request, poll_id: str, data: UserVote, user_id: Depends(get_user_id)):
    mysql_pool = request.state.mysql_pool
    async with mysql_pool() as session:
        await crud.check_poll_exists(session=session, poll_id=poll_id)
        await crud.create_user_votes(session=session, user_id=user_id, data=Box(**data.__dict__))
    return ResponseBM(data=Box())
