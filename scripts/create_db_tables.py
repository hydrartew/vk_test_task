import logging

from db.base import engine, Base

logger = logging.getLogger(__name__)


def create_db_tables_if_not_exists(drop_all: bool = False) -> None:
    try:

        if drop_all:
            logger.info('Attempting to drop all tables, if they exist.')
            Base.metadata.drop_all(engine)
            logger.info('Database tables dropped successfully.')

        logger.info('Creating new tables if not exists.')
        Base.metadata.create_all(engine)
        logger.info('Tables already exist or created successfully.')

    except Exception as e:
        logger.error(f'Error dropping or/and creating database tables: {e}')
