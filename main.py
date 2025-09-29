import logging.config

from vk_test_task.api import get_raw_posts
from vk_test_task.db import recreate_database, add_posts, collect_top_users

logger = logging.getLogger(__name__)
logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logging.getLogger('sqlalchemy.engine').propagate = False


def main():
    recreate_database()

    list_posts = get_raw_posts()
    add_posts(list_posts)

    collect_top_users()


if __name__ == '__main__':
    main()
