import logging

import requests

from config_reader import settings
from schemas import ListPosts
from utils import retry_settings

logger = logging.getLogger(__name__)


@retry_settings()
def get_raw_posts() -> ListPosts:
    logger.info(f'Attempting to get raw posts from the url API {settings.POSTS_URL_API}.')

    response = requests.get(settings.POSTS_URL_API)

    response.raise_for_status()

    response_json = response.json()

    _data = ListPosts.model_validate(response_json)

    logger.info('Posts received and validated successfully.')

    return _data
