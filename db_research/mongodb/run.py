from typing import Union, List, Tuple, Any

from db_research.base_manager import BaseDBManager
from db_research.data.models import (
    Likes, Reviews, Bookmarks, ReviewLikes, BaseDataClass
)
from db_research.data.test_queries import MONGO_TESTS, TEST_BATCH_COUNTS_MONGO
from db_research.mongodb.manager import MongoDBManager
from db_research.settings import base_settings

DB_TO_COMPARE = (MongoDBManager,)
DATA_TO_USE = (Likes, Bookmarks, Reviews, ReviewLikes)


def run(
        manager: BaseDBManager,
        data_to_use: Union[List[BaseDataClass], Tuple[BaseDataClass]],
        tests: Tuple[Any],
        batch_counts: Union[Tuple[int], List[int]] = TEST_BATCH_COUNTS_MONGO,
        iterations: int = base_settings.iterations_count
) -> None:
    manager.create_db()

    print(f'*** Running benchmarks for {manager.DB_NAME} ***')
    for batch_count in batch_counts:
        table_size = batch_count * base_settings.batch_size
        print(f'{table_size} rows:')

        for data_cls in data_to_use:
            fill_db_time = manager.fill_db(data_cls, batch_count)
            print(f'Filling {data_cls.__name__}: {fill_db_time} \n')

        for test in tests:
            test(manager, iterations)

        for data_cls in data_to_use:
            manager.clear_table(data_cls.table_name)

        print("===" * 10)


if __name__ == '__main__':
    for db_manager in DB_TO_COMPARE:
        run(db_manager(), DATA_TO_USE, MONGO_TESTS)
