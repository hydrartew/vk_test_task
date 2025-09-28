import logging.config

from vk_test_task.api import get_raw_posts

logger = logging.getLogger(__name__)
logging.config.fileConfig('logging.ini', disable_existing_loggers=False)


def main():
    get_raw_posts()


if __name__ == '__main__':
    main()
