import re

from sqlalchemy import Column, String, Boolean, BigInteger, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        table_name = re.sub(r'([a-z])([A-Z])', r'\1_\2', self.__name__).lower()
        return f'{table_name}s'


class Poll(Base):
    _id = Column(String(length=40), name='id', nullable=False, primary_key=True)
    title = Column(String(length=500), nullable=False)
    creator_id = Column(String(length=40), nullable=False)
    _type = Column(String(length=40), name='type', nullable=False)
    allow_add_choice = Column(Boolean, default=True)
    allow_multiple_choice = Column(Boolean, default=True)
    end_at = Column(BigInteger)
    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)


class Vote(Base):
    _id = Column(String(length=40), name='id', nullable=False, primary_key=True)
    title = Column(String(length=500), nullable=False)
    creator_id = Column(String(length=40), nullable=False)
    image = Column(String(length=500))
    last_user_update = Column(String(length=40), nullable=False)
    poll_id = Column(String(length=40), nullable=False, primary_key=True)
    count = Column(Integer, default=0)
    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)


class UserVote(Base):
    vote_id = Column(String(length=40), nullable=False, primary_key=True)
    user_id = Column(String(length=40), nullable=False, primary_key=True)
    created_at = Column(BigInteger)
