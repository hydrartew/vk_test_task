import logging

from vk_test_task.db.base import engine, Base, session_factory
from vk_test_task.db.models import RawPostsTable, TopUsersTable  # для создания таблицы
from vk_test_task.schemas import Post, ListPosts

logger = logging.getLogger(__name__)


def recreate_database() -> None:
    logger.info('Attempting to drop all tables, if they exist, and create new ones.')
    try:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
    except Exception as e:
        logger.error(f'Error dropping or/and creating database tables: {e}')
    else:
        logger.info('Database tables recreated successfully!')


def add_posts(list_posts: list[Post] | ListPosts):
    instances_to_add = []
    for p in list_posts:
        instances_to_add.append(
            RawPostsTable(
                id=p.id,
                user_id=p.user_id,
                title=p.title,
                body=p.body
            )
        )
    with session_factory() as session:
        session.add_all(instances_to_add)
        session.commit()
