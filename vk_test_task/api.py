import logging
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log, RetryError

from config_reader import settings
from vk_test_task.schemas import PostList

logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(min=1, max=4),
    before_sleep=before_sleep_log(logger, logging.INFO, exc_info=True)
)
def get_raw_posts() -> PostList:
    logger.info(f'Attempting to get raw posts from the url API {settings.POSTS_URL_API}.')

    response = requests.get(settings.POSTS_URL_API)

    response.raise_for_status()

    response_json = response.json()

    _data = PostList.model_validate(response_json)

    logger.info('Successfully get and validated posts.')

    return _data
