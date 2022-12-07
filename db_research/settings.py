from functools import lru_cache

from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    iterations_count: int = Field(10, env='ITERATIONS_COUNT')
    batch_size: int = Field(1000, env='BATCH_SIZE')
    batch_count: int = Field(1000, env='BATCH_COUNT')
    max_movie_duration: int = Field(360, env='MAX_MOVIE_DURATION')


class ClickhouseSettings(BaseSettings):
    host: str = Field('127.0.0.1', env='CLICKHOUSE_HOST')
    port: int = Field(9000, env='CLICKHOUSE_PORT')


@lru_cache
def get_base_settings() -> BaseConfig:
    return BaseConfig()


@lru_cache
def get_ch_settings() -> ClickhouseSettings:
    return ClickhouseSettings()


base_settings = get_base_settings()
ch_settings = get_ch_settings()
