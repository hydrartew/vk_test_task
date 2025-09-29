import logging

from sqlalchemy import select, func, column
from sqlalchemy.dialects.postgresql import insert

from db.base import session_factory
from db.models import RawPostsTable, TopUsersTable
from utils import retry_settings

logger = logging.getLogger(__name__)


@retry_settings()
def fill_top_users_by_posts() -> None:
    logger.info('Calculating top users by posts.')

    try:
        with session_factory() as session:
            subquery = (
                select(
                    RawPostsTable.user_id,
                    func.count().label('posts_cnt')
                )
                .group_by(RawPostsTable.user_id)
                .order_by(column('posts_cnt').desc(), column('user_id'))
            )

            stmt = insert(TopUsersTable).from_select(
                ['user_id', 'posts_cnt'],
                select(
                    subquery.c.user_id,
                    subquery.c.posts_cnt
                )
            )

            do_update_stmt = stmt.on_conflict_do_update(
                index_elements=[TopUsersTable.user_id],
                set_=dict(
                    posts_cnt=stmt.excluded.posts_cnt,
                    calculated_at=func.now()
                )
            )

            session.execute(do_update_stmt)

            session.commit()
            logger.info('Top users calculated and updated successfully.')

    except Exception:
        logger.error('Error calculating top users. Traceback below in the log.')
        if session:
            logger.info('Rollback add_posts session.')
            session.rollback()
        raise
