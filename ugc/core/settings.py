from functools import lru_cache
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

# LOGGING
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    # PROJECT
    PROJECT_NAME = Field('movies', env='PROJECT_NAME')
    BATCH_SIZE: int = Field(1000, env='BATCH_SIZE')
    BATCH_COUNT: int = Field(50, env='BATCH_COUNT')

    # MONGO
    MONGO_HOST: str = Field('127.0.0.1', env='MONGO_HOST')
    MONGO_PORT: int = Field(27017, env='MONGO_PORT')
    MONGO_DB: str = Field('movies', env='MONGO_DB')

    # LOGS
    SENTRY_DSN: str = Field(..., env='SENTRY_DSN')


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: BaseSettings = get_settings()
