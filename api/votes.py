from fastapi import APIRouter, Depends, Request
from box import Box

import crud
from core.exceptions import *
from middlewares import get_user_id
from schemas import VoteCreate, VoteUpdate, ResponseBM
from core.config import config

router = APIRouter()


@router.post('/{poll_id}/votes')
async def create_votes(request: Request, poll_id: str, data: VoteCreate, user_id=Depends(get_user_id)):
    mysql_pool = request.state.mysql_pool
    async with mysql_pool() as session:
        poll = await crud.get_poll(session=session, poll_id=poll_id, user_id=user_id)
        if len(data.votes) + len(poll.votes) > config.VOTE_LIMIT.stop:
            raise VoteLimitationError
        if not poll.allow_add_choice:
            raise PollConfigError
        votes = await crud.create_votes(session=session, poll=poll, data=data.votes)
    return ResponseBM(data=[Box(id=vote.id,
                                title=vote.title,
                                image=vote.image,
                                creator_id=user_id,
                                last_user_update=user_id) for vote in votes])


@router.patch('/{poll_id}/votes/{vote_id}')
async def update_vote(request: Request, poll_id: str, vote_id: str, data: VoteUpdate, user_id=Depends(get_user_id)):
    mysql_pool = request.state.mysql_pool
    async with mysql_pool() as session:
        vote = await crud.get_vote(session=session, poll_id=poll_id, vote_id=vote_id)
        if vote.count > 0:
            raise EditTitleError
        vote = crud.update_vote(session=session, vote=vote, data=Box(**data.__dict__), user_id=user_id)
    return ResponseBM(data=vote)


@router.delete('/{poll_id}/votes/{vote_id}')
async def delete_vote(request: Request, poll_id: str, vote_id: str, user_id=Depends(get_user_id)):
    mysql_pool = request.state.mysql_pool
    async with mysql_pool() as session:
        poll = await crud.get_poll(session=session, poll_id=poll_id, user_id=user_id)
        if len(poll.votes) == 2:
            raise VoteLimitationError
        await crud.get_vote(session=session, poll_id=poll_id, vote_id=vote_id)
        await crud.delete_vote(session=session, vote_id=vote_id)
    return ResponseBM(data=Box())
