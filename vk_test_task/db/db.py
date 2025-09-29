import logging

from vk_test_task.db.base import engine, Base, session_factory
from vk_test_task.db.models import RawPostsTable, TopUsersTable  # для создания таблицы

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


if __name__ == "__main__":
    recreate_database()
