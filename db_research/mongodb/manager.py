import logging
from typing import Union, Dict, Optional, List, Tuple, Any

from pymongo import MongoClient

from db_research.base_manager import BaseDBManager, DEFAULT_TABLE_NAME
from db_research.settings import mongo_settings


class MongoDBManager(BaseDBManager):
    DB_NAME = 'MongoDB'

    def __init__(
            self,
            host=mongo_settings.host,
            port=mongo_settings.port,
            db_name=mongo_settings.db_name
    ) -> None:
        self.host = host
        self.port = port
        self.db_name = db_name

    @property
    def database(self):
        client: MongoClient[Any] = MongoClient(self.host, self.port)
        return client.get_database(self.db_name)

    def insert(
            self,
            fake_data: List[Union[Dict[str, Any], Tuple[Any]]],
            collection_name: Optional[str] = DEFAULT_TABLE_NAME
    ):
        collection = self.database.get_collection(collection_name)
        try:
            collection.insert_many(fake_data)
        except Exception as e:
            logging.exception(e)

    def clear_table(self, collection_name: str = DEFAULT_TABLE_NAME):
        collection = self.database.get_collection(collection_name)
        collection.delete_many({})

    def get_data(
            self,
            query: Union[tuple[dict[str, Any]], list[dict[str, Any]]],
            collection_name=DEFAULT_TABLE_NAME
    ):
        collection = self.database.get_collection(collection_name)
        collection.find(*query)

    def aggregate(
            self,
            query: Union[tuple[dict[str, Any]], list[dict[str, Any]]],
            collection_name=DEFAULT_TABLE_NAME
    ):
        collection = self.database.get_collection(collection_name)
        collection.aggregate(query)

    def count_documents(
            self,
            query: Dict[str, Any],
            collection_name=DEFAULT_TABLE_NAME
    ):
        collection = self.database.get_collection(collection_name)
        collection.count_documents(query)
