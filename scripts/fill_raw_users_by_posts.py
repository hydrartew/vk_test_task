import logging

from sqlalchemy.dialects.postgresql import insert

from db.base import session_factory
from db.models import RawPostsTable
from schemas import Post, ListPosts
from utils import retry_settings

logger = logging.getLogger(__name__)


@retry_settings()
def fill_raw_users_by_posts(list_posts: list[Post] | ListPosts) -> None:
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
