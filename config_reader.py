from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: str = str(Path(__file__).parents[0])

    model_config = SettingsConfigDict(env_file=f'{BASE_DIR}/.env', extra='allow')

    POSTS_URL_API: str
    CRON_FREQ_IN_HOURS: int

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr


settings = Settings()
