from typing import Any, Union, List

from pydantic import BaseModel
from gapoic.app_config import load_config_as_class


class AppConfig(BaseModel):
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SENTRY_DNS: str
    VIOLATION_WORDS: Union[str, List]
    LOG_FILE: str = 'app.log'
    LOG_ROTATION: str = '500 MB'
    VOTE_LIMIT: range = range(2, 10)
    STRING_LENGTH: range = range(1, 255)
    POLL_TYPE: tuple = ('post', 'chat')

    def __init__(self, **data: Any):
        data['VIOLATION_WORDS'] = [f' {word} ' for word in data.get('VIOLATION_WORDS').split(',')]
        super(AppConfig, self).__init__(**data)

    class Config:
        arbitrary_types_allowed = True


config = load_config_as_class(validator_cls=AppConfig)
