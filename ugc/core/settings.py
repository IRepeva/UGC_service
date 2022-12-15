from functools import lru_cache
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

# LOGGING
logging_config.dictConfig(LOGGING)


class MongoSettings(BaseSettings):
    HOST: str = Field('127.0.0.1')
    PORT: int = Field(27017)
    DB: str = Field('movies')


class Settings(BaseSettings):
    # PROJECT
    project_name = Field('movies', env='PROJECT_NAME')
    batch_size: int = Field(1000, env='BATCH_SIZE')
    batch_count: int = Field(50, env='BATCH_COUNT')

    # LOGS
    sentry_dsn: str = Field(..., env='SENTRY_DSN')

    # MONGO
    DATABASE: MongoSettings = MongoSettings()

    class Config:
        env_prefix = 'MONGO_'


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
