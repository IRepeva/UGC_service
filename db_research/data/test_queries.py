from collections import namedtuple

from faker import Faker

from db_research.base_manager import DEFAULT_TABLE_NAME

faker = Faker()
DEFAULT_USER_ID, DEFAULT_MOVIE_ID = '1', '1'
TEST_USER_ID, TEST_MOVIE_ID = 'Harry', 'Potter'
TEST_BATCH_COUNTS = (100, 1000)

Test = namedtuple('Test', ['name', 'query', 'table_name'])

BASE_SELECT_QUERIES = (
    Test(
        "unique_users",
        "select distinct user_id from {0}",
        DEFAULT_TABLE_NAME
    ),
    Test(
        "unique_movies",
        "select distinct movie_id from {0}",
        DEFAULT_TABLE_NAME
    ),
    Test(
        "unique_users_count",
        "select count(distinct user_id) from {0}",
        DEFAULT_TABLE_NAME
    ),
    Test(
        "unique_movies_count",
        "select count(distinct movie_id) from {0}",
        DEFAULT_TABLE_NAME
    ),
    Test(
        "user_frame_stats",
        "SELECT user_id, sum(frame), max(frame) FROM {0} GROUP by user_id",
        DEFAULT_TABLE_NAME
    )
)
