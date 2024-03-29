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


class VerticaSettings(BaseSettings):
    host: str = Field('127.0.0.1', env='VERTICA_HOST')
    port: int = Field(5433, env='VERTICA_PORT')
    user: str = Field('dbadmin', env='VERTICA_USER')
    password: str = Field('', env='VERTICA_USER_PASS')
    database: str = Field('docker', env='VERTICA_DB')
    autocommit: bool = Field(True, env='VERTICA_AUTOCOMMIT')


class MongoSettings(BaseSettings):
    host: str = Field('127.0.0.1', env='MONGO_HOST')
    port: int = Field(27117, env='MONGO_PORT')
    db_name: str = Field('movies', env='MONGO_DB_NAME')


@lru_cache
def get_base_settings() -> BaseConfig:
    return BaseConfig()


@lru_cache
def get_ch_settings() -> ClickhouseSettings:
    return ClickhouseSettings()


@lru_cache
def get_vertica_settings() -> VerticaSettings:
    return VerticaSettings()


@lru_cache
def get_mongo_settings() -> MongoSettings:
    return MongoSettings()


base_settings: BaseConfig = get_base_settings()
ch_settings: ClickhouseSettings = get_ch_settings()
vertica_settings: VerticaSettings = get_vertica_settings()
mongo_settings: MongoSettings = get_mongo_settings()
