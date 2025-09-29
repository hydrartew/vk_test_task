import logging

import requests

from config_reader import settings
from db import add_row_posts_to_db
from utils import retry_settings
from schemas import Post, ListPosts

logger = logging.getLogger(__name__)


@retry_settings()
def get_posts_data() -> list[Post] | ListPosts:
    logger.info(f'Attempting to get raw posts from the url API {settings.POSTS_URL_API}.')

    response = requests.get(settings.POSTS_URL_API)

    response.raise_for_status()

    response_json = response.json()

    _data = ListPosts.model_validate(response_json)

    logger.info('Posts received and validated successfully.')

    return _data


def fill_raw_users_by_posts() -> None:
    list_posts = get_posts_data()
    add_row_posts_to_db(list_posts)
