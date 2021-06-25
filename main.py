from time import time

from fastapi import FastAPI, Request

from db.mysql_client import MysqlClient
from loguru import logger

from core.logger import init_logging
from api.polls import router as polls_router

app = FastAPI()
client = MysqlClient()


@app.middleware("http")
async def init_resource(request: Request, call_next):
    request.state.mysql_pool = client.pool
    start_time = time()
    response = await call_next(request)
    end_time = time()
    logger.info(f'{request.method} {request.url.path} take {end_time - start_time:.2f}s')
    return response


app.include_router(
    polls_router,
    prefix="/internal/polls",
    tags=["Polls"],
    responses={404: {"message": "Not found"}},
)


@app.on_event("startup")
async def startup_event():
    init_logging()
    await client.connect()
