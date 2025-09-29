import logging
from datetime import datetime

from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from db import get_all_top_users

logger = logging.getLogger(__name__)


class TopUsers(BaseModel):
    user_id: int
    posts_cnt: int
    calculated_at: datetime


router = APIRouter()


@router.get('/top',
            name='Get table data top_users_by_posts',
            description='Get table top_users_by_posts in JSON format',
            responses={
                200: {"model": TopUsers, "description": "List top users"},
                500: {"description": "Server error"}
            })
def get_top_users() -> JSONResponse:
    try:
        top_users = get_all_top_users()
        return JSONResponse(top_users, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(e, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
