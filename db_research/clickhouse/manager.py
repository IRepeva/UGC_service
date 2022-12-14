from typing import Optional, List, Dict, Union, Tuple

from clickhouse_driver import Client

from db_research.base_manager import BaseDBManager, DEFAULT_TABLE_NAME
from db_research.settings import ch_settings


class ClickhouseManager(BaseDBManager):
    DB_NAME = 'Clickhouse'

    def __init__(self, host=ch_settings.host, port=ch_settings.port):
        self.host = host
        self.port = port

    @property
    def client(self):
        return Client(host=self.host, port=self.port)

    def insert(self, fake_data: List[Union[Dict, Tuple]],
               table_name: Optional[str] = DEFAULT_TABLE_NAME):
        self.client.execute(f'INSERT INTO {table_name} VALUES', fake_data)

    def clear_table(self, table_name: str = DEFAULT_TABLE_NAME):
        self.client.execute(f'TRUNCATE TABLE {table_name}')

    def get_data(self, query: str, table_name=DEFAULT_TABLE_NAME):
        self.client.execute(query.format(table_name))
