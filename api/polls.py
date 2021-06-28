from fastapi import APIRouter, Depends, Request
from box import Box

import crud
from core.exceptions import *
from middlewares import get_user_id
from schemas import PollCreate, PollUpdate, ResponseBM
from utils import split_dict

router = APIRouter()


@router.post('/')
async def create(request: Request, data: PollCreate, user_id=Depends(get_user_id)):
    mysql_pool = request.state.mysql_pool
    async with mysql_pool() as session:
        poll_data, votes_data = split_dict(Box(**data.__dict__), 'votes')
        poll = await crud.create_poll(session=session, data=poll_data, user_id=user_id)
        await crud.create_votes(session=session, poll=poll, data=votes_data)
    return ResponseBM(data=poll | Box(votes=votes_data))


@router.get('/{poll_id}')
async def get(request: Request, poll_id: str, user_id=Depends(get_user_id)):
    mysql_pool = request.state.mysql_pool
    async with mysql_pool() as session:
        poll = await crud.get_poll(session=session, poll_id=poll_id, user_id=user_id)
    return ResponseBM(data=poll)


@router.patch('/{poll_id}')
async def update(request: Request, poll_id: str, data: PollUpdate, user_id=Depends(get_user_id)):
    mysql_pool = request.state.mysql_pool
    async with mysql_pool() as session:
        poll = await crud.get_poll(session=session, poll_id=poll_id, user_id=user_id)
        if data.title:
            user_voted_number = sum([len(vote.user_votes) for vote in poll.votes])
            if user_voted_number > 0:
                raise EditTitleError
        poll = await crud.update_poll(session=session, poll=poll, data=Box(data.__dict__))
    return ResponseBM(data=poll)


@router.delete('/{poll_id}')
async def delete(request: Request, poll_id: str):
    mysql_pool = request.state.mysql_pool
    async with mysql_pool() as session:
        poll_exists = await crud.check_poll_exists(session=session, poll_id=poll_id)
        if not poll_exists.is_exists:
            raise NotFoundError
        await crud.delete_poll(session=session, poll_id=poll_id)
    return ResponseBM(data=Box())
