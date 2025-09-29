import logging.config

from vk_test_task.api import get_raw_posts
from vk_test_task.db import recreate_database

logger = logging.getLogger(__name__)
logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logging.getLogger('sqlalchemy.engine').propagate = False


def main():
    get_raw_posts()
    recreate_database()


if __name__ == '__main__':
    main()
