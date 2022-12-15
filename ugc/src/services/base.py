import logging
from abc import abstractmethod
from typing import Optional

from core.settings import settings
from motor.motor_asyncio import AsyncIOMotorClient


class BaseService:
    COLLECTION: Optional[str] = None
    DEPENDENT_COLLECTION: Optional[str] = None

    def __init__(self, mongo: AsyncIOMotorClient):
        self.database = mongo.get_database(settings.MONGO_DB)
        self.collection = self.database.get_collection(self.COLLECTION)

    @classmethod
    @abstractmethod
    def generate_row(cls):
        ...

    @classmethod
    def generate_dependent_row(cls):
        ...

    @classmethod
    def insert(cls, fake_data: dict, collection):
        try:
            collection.insert_many(fake_data)
        except Exception as exc:
            logging.exception(exc)
