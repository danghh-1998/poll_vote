from sqlalchemy.ext.asyncio import AsyncConnection

from db.queries import Q


async def create_votes(session: AsyncConnection, *args):
    await session.execute(Q.INSERT__VOTE, *args)
