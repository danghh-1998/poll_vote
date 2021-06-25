from typing import Any, List, Optional
from time import time

from pydantic import BaseModel, Field, validator
from fastapi import status as http_status

from core.config import config


def validate_type(_type: str) -> str:
    assert _type in config.POLL_TYPE, 'type must be post or chat'
    return _type


def validate_end_at(end_at: int) -> int:
    assert end_at > int(time()), 'end_at must be greater than created_at'
    return end_at


class ResponseBM(BaseModel):
    status: str = "success"
    data: Any


class ErrorResponseBM(BaseModel):
    status: str = "failed"
    err_code: int = http_status.HTTP_400_BAD_REQUEST
    err_detail: str


class PollUpdate(BaseModel):
    title: Optional[str] = Field(min_length=config.STRING_LENGTH.start, max_length=config.STRING_LENGTH.stop)
    allow_add_choice: Optional[bool]
    allow_multiple_choice: Optional[bool]


class VoteUpdate(BaseModel):
    title: Optional[str] = Field(min_length=config.STRING_LENGTH.start, max_length=config.STRING_LENGTH.stop)
    image: Optional[str] = Field(max_length=config.STRING_LENGTH.stop)


class Vote(BaseModel):
    title: str = Field(min_length=config.STRING_LENGTH.start, max_length=config.STRING_LENGTH.stop)
    image: Optional[str] = Field(max_length=config.STRING_LENGTH.stop)


class VoteCreate(BaseModel):
    votes: List[Vote] = Field(..., min_items=config.VOTE_LIMIT.start - 1, max_items=config.VOTE_LIMIT.stop)


class PollCreate(BaseModel):
    title: str = Field(..., min_length=config.STRING_LENGTH.start, max_length=config.STRING_LENGTH.stop)
    allow_add_choice: bool = Field(default=True)
    allow_multiple_choice: bool = Field(default=True)
    creator_id: str = Field(...)
    type: str = Field(...)
    votes: List[Vote] = Field(..., min_items=config.VOTE_LIMIT.start, max_items=config.VOTE_LIMIT.stop)
    end_at: Optional[int]

    type_validator = validator('type', allow_reuse=True)(validate_type)
    end_at_validator = validator('end_at', allow_reuse=True)(validate_end_at)


class UserVote(BaseModel):
    vote_id: str
