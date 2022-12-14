from contextlib import contextmanager
from typing import List, Dict, Tuple, Union, Optional

import vertica_python

from db_research.base_manager import (
    BaseDBManager, DEFAULT_TABLE_NAME, DEFAULT_TABLE_FIELDS,
    CREATE_DEFAULT_TABLE
)
from db_research.settings import vertica_settings


class VerticaManager(BaseDBManager):
    DB_NAME = 'Vertica'

    @contextmanager
    def _cursor(self):
        connection = vertica_python.connect(**vertica_settings.dict())
        try:
            cursor = connection.cursor()
            yield cursor
        finally:
            connection.close()

    def create_db(self, create_table_query: str = CREATE_DEFAULT_TABLE):
        with self._cursor() as cursor:
            cursor.execute(create_table_query)

    def clear_table(self, table_name: str = DEFAULT_TABLE_NAME):
        with self._cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {table_name}')

    def insert(self, fake_data: List[Union[Dict, Tuple]],
               table_name: Optional[str] = DEFAULT_TABLE_NAME):
        insert_query = f'''
            INSERT INTO {table_name} {DEFAULT_TABLE_FIELDS} 
            VALUES (%s,%s,%s,%s)
        '''
        if isinstance(fake_data[0], dict):
            fake_data = [tuple(data.values()) for data in fake_data]
        with self._cursor() as cursor:
            cursor.executemany(insert_query, fake_data)

    def get_data(self, query: str, table_name=DEFAULT_TABLE_NAME):
        with self._cursor() as cursor:
            cursor.execute(query.format(table_name))
