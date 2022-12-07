from collections import namedtuple
from typing import Union, Tuple, List

from db_research.base_manager import BaseDBManager
from db_research.clickhouse.manager import ClickhouseManager
from db_research.data.models import Views, BaseDataClass
from db_research.data.test_queries import BASE_SELECT_QUERIES, TEST_BATCH_COUNTS
from db_research.settings import base_settings
from db_research.utils import benchmark
from db_research.vertica.manager import VerticaManager

DB_TO_COMPARE = (VerticaManager, ClickhouseManager)
DATA_TO_USE = (Views,)


def run(manager: BaseDBManager,
        data_to_use: Union[List[BaseDataClass], Tuple[BaseDataClass]],
        tests: Tuple[namedtuple],
        batch_counts: Union[Tuple, List] = TEST_BATCH_COUNTS,
        iterations: int = base_settings.iterations_count) -> None:
    manager.create_db()

    print(f'*** Running benchmarks for {manager.DB_NAME} ***')
    for batch_count in batch_counts:
        table_size = batch_count * base_settings.batch_size
        print(f'{table_size} rows: \n')

        for data_cls in data_to_use:
            fill_db_time = manager.fill_db(data_cls, batch_count)
            print(f'Filling {data_cls.__name__}: {fill_db_time} \n')

        @benchmark(iterations=iterations)
        def run_test(test_data):
            manager.get_data(test_data.query, test_data.table_name)

        for test in tests:
            run_test(test)

        for data_cls in data_to_use:
            manager.clear_table(data_cls.TABLE_NAME)

        print("===" * 10)


if __name__ == '__main__':
    for db_manager in DB_TO_COMPARE:
        run(db_manager(), DATA_TO_USE, BASE_SELECT_QUERIES)
