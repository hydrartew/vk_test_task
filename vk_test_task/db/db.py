import logging

import psycopg2
from sqlalchemy.dialects.postgresql import insert

from vk_test_task.db.base import engine, Base, session_factory
from vk_test_task.db.models import RawPostsTable, TopUsersTable  # для создания таблицы
from vk_test_task.schemas import Post, ListPosts

from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log, RetryError

logger = logging.getLogger(__name__)


def recreate_database() -> None:
    logger.info('Attempting to drop all tables, if they exist, and create new ones.')
    try:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
    except Exception as e:
        logger.error(f'Error dropping or/and creating database tables: {e}')
    else:
        logger.info('Database tables recreated successfully.')


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(min=1, max=4),
    before_sleep=before_sleep_log(logger, logging.INFO, exc_info=True)
)
def add_posts(list_posts: list[Post] | ListPosts) -> None:
    logger.info(f'Attempting to add/update {len(list_posts)} posts.')

    try:

        with session_factory() as session:
            for p in list_posts:
                insert_stmt = insert(RawPostsTable).values(
                    id=p.id,
                    user_id=p.user_id,
                    title=p.title,
                    body=p.body
                )

                do_update_stmt = insert_stmt.on_conflict_do_update(
                    index_elements=['id'],
                    set_=dict(title=p.title, body=p.body)
                )

                session.execute(do_update_stmt)

            session.commit()
            logger.info(f'Posts were added/updated successfully.')

    except Exception:
        logger.error(f'Error adding posts. Traceback below in the log.')
        if session:
            logger.info('Rollback add_posts session.')
            session.rollback()
        raise
