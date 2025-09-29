import logging
from datetime import datetime

from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select

from db.base import session_factory

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
    logger.info('Fetching all top users from the database.')

    try:
        with session_factory() as session:
            stmt = select(TopUsersTable)
            result = session.execute(stmt)
            top_users = result.scalars().all()  # Get all the TopUsersTable objects
            logger.info(f'Successfully fetched {len(top_users)} top users.')
            return list(top_users)  # Convert to a list for easier usage

    except Exception as e:
        logger.error(f'Error fetching top users: {e}. Traceback below in the log.')
        if 'session' in locals() and session: # Проверка на существование session
            logger.info('Rollback get_all_top_users session (if applicable).') #более уместный текст
            session.rollback()
        raise
    return JSONResponse(None, status_code=status.HTTP_200_OK)
