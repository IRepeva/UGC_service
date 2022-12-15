import logging
import sys
import time
from typing import Any

from pymongo import MongoClient

sys.path.append('.')
from core.settings import settings
from src.services.bookmark import BookmarkService
from src.services.like import LikeService
from src.services.review import ReviewService
from src.utils.data_generation import BaseDataGenerator

logger = logging.getLogger(__name__)


def fill_db(
        batch_count: int = settings.batch_count,
        batch_size: int = settings.batch_size
):
    mongo_client: MongoClient[Any] = MongoClient(settings.DATABASE.HOST,
                                                 settings.DATABASE.PORT)
    mongo_database = mongo_client.get_database(settings.DATABASE.DB)

    for mongo_service in (LikeService, ReviewService, BookmarkService):
        start = time.perf_counter()
        data_generator = BaseDataGenerator(
            mongo_service, batch_count, batch_size
        )

        collections_to_fill = [(mongo_service.collection_name, False)]
        if mongo_service.dependent_coll_name:
            collections_to_fill.append(
                (mongo_service.dependent_coll_name, True)
            )

        for collection_name, dependent in collections_to_fill:
            collection = mongo_database.get_collection(collection_name)
            collection.delete_many({})

            for fake_data in data_generator.generate_data(dependent=dependent):
                mongo_service.insert(fake_data, collection)

        logger.info(
            f'Filled {mongo_service.__name__}: {time.perf_counter() - start}'
        )


if __name__ == '__main__':
    fill_db()
