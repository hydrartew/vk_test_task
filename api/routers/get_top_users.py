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
        top_users_sqlalchemy = get_all_top_users()
        top_users_dict = [
            {
                "user_id": user.user_id,
                "posts_cnt": user.posts_cnt,
                "calculated_at": user.calculated_at.isoformat(),
            }
            for user in top_users_sqlalchemy
        ]
        return JSONResponse(top_users_dict, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
