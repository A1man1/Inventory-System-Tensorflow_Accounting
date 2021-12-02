import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
import logging

from core.settings import get_app_settings

# configure settings object for global settings.
settings = get_app_settings()

# initialize logger, its level and format.
log_format = "%(asctime)s - %(levelname)s - %(message)s - %(filename)s - %(lineno)d"

log_level = logging.INFO
if settings.debug:
    log_level = logging.DEBUG

logging.basicConfig(format=log_format, level=log_level)

log = logging.getLogger(__name__)

def generate_uuid():
    """Function to generate uuid for unique id fields.

    Returns:
        str: Generated unique uuid.
    """
    return str(uuid.uuid4())


def utc_now() -> datetime:
    """Fuction get UTC timestamp.

    Returns:
        datetime: Datetime in UTC timezone.
    """
    return datetime.now(tz=timezone.utc)


async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = settings.default_page_limit):
    """Common Request query parameters.

    Args:
        q (Optional[str], optional): [description]. Defaults to None.
        skip (int, optional): [description]. Defaults to 0.
        limit (int, optional): [description]. Defaults to 100.

    Returns:
        dict: Query Parameters for GET requests to apply pagination.
    """
    return {"q": q, "skip": skip, "limit": limit}


def sort_list_of_dictionaries_by_key_and_pivot(pivot, list: list, key: str) -> list:
    list = sorted(list, key=lambda i: i[key], reverse=True)
    index = 0
    closer = float("inf")
    for j in list:
        j[key] = float(j[key])
        if j[key] == pivot:
            break
        elif ((j[key] > pivot) and (j[key] < closer)):
            index += 1
            closer = j[key]
        else:
            break
    list = list[index:] + list[0:index][::-1]
    return list

def filter_by_issue(key_search:bool):
    return key_search

def try_parsing_date(text):
    for fmt in ('%Y-%m-%d', '%d.%m.%Y','%m.%d.%Y','%Y.%d.%m','%Y.%m.%d' ,'%d/%m/%Y','%d/%m/%Y', '%m-%d-%Y'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")