from typing import Dict, Any, Tuple
from time import time
from uuid import uuid4

from box import Box


def current_time() -> int:
    return int(time())


def obj_id() -> str:
    return uuid4().hex


def split_dict(_dict: Box, _key: str) -> Tuple[Box, Any]:
    if _key not in _dict:
        raise KeyError
    return Box({key: val for key, val in _dict.items() if key != _key}), _dict.get(_key)
