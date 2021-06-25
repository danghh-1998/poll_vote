from fastapi import APIRouter, Depends, Request
from gapoic.app_config import load_config_as_class

from core.config import config
from middlewares import get_user_id
from schemas import PollCreate, PollUpdate, ResponseBM

import crud

router = APIRouter()


# @router.get('/{poll_id}')
# async def get(poll_id: str, user_id=Depends(get_user_id)):
#     result = client.get_poll_by_id(_id=poll_id, user_id=user_id)
#     return ResponseBM(data=result)


@router.post('/')
async def create(request: Request, data: PollCreate):
    mysql_pool = request.state.mysql_pool
    async with mysql_pool() as conn:
        await crud.create_poll(conn, data)

# @router.patch('/{poll_id}')
# async def update(poll_id: str, data: PollUpdate, user_id=Depends(get_user_id)):
#     result = client.update_poll(data=data, poll_id=poll_id, user_id=user_id)
#     return ResponseBM(data=result)
#
#
# @router.delete('/{poll_id}')
# async def delete(poll_id: str, user_id=Depends(get_user_id)):
#     result = client.delete_poll(_id=poll_id, user_id=user_id)
#     return ResponseBM(data=result)
