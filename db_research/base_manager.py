import time
from abc import abstractmethod
from typing import Optional, List, Union, Dict, Tuple, Any

from db_research.data.models import BaseDataClass
from db_research.data_generator import BaseDataGenerator
from db_research.settings import base_settings

DEFAULT_TABLE_NAME = 'views'
DEFAULT_TABLE_FIELDS = '(user_id, movie_id, frame, time_created)'
CREATE_DEFAULT_TABLE = f'''
    CREATE TABLE IF NOT EXISTS {DEFAULT_TABLE_NAME} (
        user_id         VARCHAR(256)    NOT NULL,
        movie_id        VARCHAR(256)    NOT NULL,
        frame           VARCHAR(256)    NOT NULL,
        time_created    TIMESTAMP       NOT NULL
    );
'''


class BaseDBManager:
    DB_NAME: Optional[str] = None

    def create_db(self, create_table_query: str = CREATE_DEFAULT_TABLE):
        ...

    def clear_database(self):
        ...

    @abstractmethod
    def clear_table(self, table_name: str = DEFAULT_TABLE_NAME):
        ...

    @abstractmethod
    def insert(
            self,
            fake_data: List[Union[Dict[str, Any], Tuple[Any]]],
            table_name: Optional[str] = DEFAULT_TABLE_NAME
    ):
        ...

    def fill_db(
            self,
            data_class: BaseDataClass,
            batch_count: int,
            batch_size: int = base_settings.batch_size
    ):
        start = time.perf_counter()
        data_generator = BaseDataGenerator(
            data_class, batch_count, batch_size
        )
        for fake_data in data_generator.generate_data():
            self.insert(fake_data, data_class.TABLE_NAME)
        return time.perf_counter() - start

    @abstractmethod
    def get_data(
            self,
            query: Union[tuple[dict[str, Any]], list[dict[str, Any]], str],
            table_name: str = DEFAULT_TABLE_NAME
    ):
        ...
