import sys
import time

from pymongo import MongoClient

sys.path.append('.')
from src.core.config import settings
from src.services.bookmark import BookmarkService
from src.services.like import LikeService
from src.services.review import ReviewService
from src.utils.data_generation import BaseDataGenerator


def fill_db(batch_count: int = settings.BATCH_COUNT,
            batch_size: int = settings.BATCH_SIZE):
    mongo_client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
    mongo_database = mongo_client.get_database(settings.MONGO_DB)

    for mongo_service in (LikeService, ReviewService, BookmarkService):
        start = time.perf_counter()
        data_generator = BaseDataGenerator(
            mongo_service, batch_count, batch_size
        )

        collections_to_fill = [(mongo_service.COLLECTION, False)]
        if mongo_service.DEPENDENT_COLLECTION:
            collections_to_fill.append(
                (mongo_service.DEPENDENT_COLLECTION, True)
            )

        for collection_name, dependent in collections_to_fill:
            collection = mongo_database.get_collection(collection_name)
            collection.delete_many({})

            for fake_data in data_generator.generate_data(dependent=dependent):
                mongo_service.insert(fake_data, collection)
            print(f'Collection {collection_name}: {collection.count_documents({})}')

        print(f'Filled {mongo_service.__name__}: {time.perf_counter() - start}')


if __name__ == '__main__':
    fill_db()
