import logging

import requests
from sqlalchemy.dialects.postgresql import insert

from config_reader import settings
from db.base import session_factory
from db.models import RawPostsTable
from schemas import Post, ListPosts
from utils import retry_settings

logger = logging.getLogger(__name__)


@retry_settings()
def get_posts_data() -> list[Post] | ListPosts:
    logger.info(f'Attempting to get raw posts from the url API {settings.POSTS_URL_API}.')

    response = requests.get(settings.POSTS_URL_API)

    response.raise_for_status()

    response_json = response.json()

    _data = ListPosts.model_validate(response_json)

    logger.info('Posts received and validated successfully.')

    return _data


@retry_settings()
def fill_raw_users_by_posts() -> None:
    list_posts = get_posts_data()

    logger.info(f'Attempting to add/update {len(list_posts)} posts.')

    try:

        with session_factory() as session:
            for p in list_posts:
                stmt = insert(RawPostsTable).values(
                    id=p.id,
                    user_id=p.user_id,
                    title=p.title,
                    body=p.body
                )

                do_update_stmt = stmt.on_conflict_do_update(
                    index_elements=[RawPostsTable.id],
                    set_=dict(title=p.title, body=p.body)
                )

                session.execute(do_update_stmt)

            session.commit()
            logger.info(f'Posts were added/updated successfully.')

    except Exception:
        logger.error('Error adding posts. Traceback below in the log.')
        if session:
            logger.info('Rollback add_posts session.')
            session.rollback()
        raise
