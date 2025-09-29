import logging.config
import time

import schedule

from config_reader import settings
from db import create_db_tables_if_not_exists
from scripts import fill_raw_users_by_posts, fill_top_users_by_posts

logger = logging.getLogger(__name__)
logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logging.getLogger('sqlalchemy.engine').propagate = False


def launch_scripts():
    logger.info('Launch scripts.')

    fill_raw_users_by_posts()
    fill_top_users_by_posts()

    logger.info('End scripts.')


def cron_scripts():
    create_db_tables_if_not_exists()

    schedule.every(settings.CRON_FREQ_IN_SEC).seconds.do(launch_scripts)

    while True:
        schedule.run_pending()
        time.sleep(1)


def main():
    cron_scripts()


if __name__ == '__main__':
    main()
