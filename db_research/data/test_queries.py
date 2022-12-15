import time
from collections import namedtuple

from faker import Faker
from pymongo import DESCENDING

from db_research.base_manager import DEFAULT_TABLE_NAME
from db_research.data.models import ReviewLikes, Likes, Reviews, Bookmarks
from db_research.mongodb.manager import MongoDBManager
from db_research.settings import base_settings
from db_research.utils import benchmark

faker = Faker()

DEFAULT_USER_ID, DEFAULT_MOVIE_ID = '1', '1'
TEST_BATCH_COUNTS = (100, 1000, 5000)
TEST_BATCH_COUNTS_MONGO = (10, 50)

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


# MONGO TESTS
def get_simple_data(
        manager: MongoDBManager,
        iterations: int = base_settings.iterations_count
) -> None:
    @benchmark(iterations=iterations)
    def run_test(test_data) -> None:
        manager.get_data(test_data.query, test_data.table_name)

    for test in likes_queries:
        run_test(test)
    run_test(bookmark_query)


def get_average_movie_rating(
        manager: MongoDBManager,
        iterations: int = base_settings.iterations_count
) -> None:
    @benchmark(iterations=iterations)
    def run_test(test_data) -> None:
        manager.aggregate(test_data.query, test_data.table_name)

    run_test(avg_rating_test)


def get_movie_reviews_sort_time(
        manager: MongoDBManager,
        iterations: int = base_settings.iterations_count
) -> None:
    @benchmark(iterations=iterations)
    def run_test(test_data) -> None:
        review = manager.aggregate(
            test_data.query, test_data.table_name
        )
        if review:
            review.sort("date", DESCENDING)
        manager.aggregate(avg_rating_test.query, avg_rating_test.table_name)

    run_test(get_review_test)


def get_likes_data_after_insert(
        manager: MongoDBManager,
        iterations: int = base_settings.iterations_count
) -> None:
    def run_test(test_data, prev_count, flag=False) -> None:
        while not flag:
            test_query = test_data.query[0]
            new_count = collection.count_documents(test_query)
            flag = True if new_count == prev_count + 1 else False

    collection = manager.database.get_collection(Likes.table_name)
    for test in likes_queries:
        times = []
        for _ in range(iterations):
            query = test.query[0]
            old_count = collection.count_documents(query)
            data = {
                "user_id": DEFAULT_USER_ID,
                "movie_id": DEFAULT_MOVIE_ID,
                "rating": 10,
            }
            collection.insert_one(data)
            start_time = time.perf_counter()
            run_test(test, old_count)
            times.append(time.perf_counter() - start_time)
        total_time = sum(times)
        avg_time = total_time / iterations
        print(f"Query: {test.name}_after_insert")
        print(f"Number of iterations: {iterations}")
        print(f"Average run time: {avg_time:.4f} sec \n")


def get_average_movie_rating_after_insert(
        manager: MongoDBManager,
        iterations: int = base_settings.iterations_count
) -> None:
    def run_test(test_data, prev_avg, flag=False) -> None:
        while not flag:
            new_count = list(collection.aggregate(test_data.query))
            new_avg = new_count[0].get("avg_rating")
            flag = True if new_avg < prev_avg else False

    collection = manager.database.get_collection(avg_rating_test.table_name)
    times = []
    for _ in range(iterations):
        avg = collection.aggregate(avg_rating_test.query)
        old_avg = list(avg)[0].get("avg_rating")
        data = {
            "user_id": DEFAULT_USER_ID,
            "movie_id": DEFAULT_MOVIE_ID,
            "rating": 1,
        }
        collection.insert_one(data)
        start_time = time.perf_counter()
        run_test(avg_rating_test, old_avg)
        times.append(time.perf_counter() - start_time)
    total_time = sum(times)
    avg_time = total_time / iterations
    print(f"Query: get_average_rating_after_insert")
    print(f"Number of iterations: {iterations}")
    print(f"Average run time: {avg_time:.4f} sec \n")


likes_queries = (
    Test(
        'get_user_likes',
        [
            {"user_id": DEFAULT_USER_ID, 'rating': {'$gte': 6}},
            {"movie_id": 1, "_id": 0}
        ],
        Likes.table_name
    ),
    Test(
        'get_movie_likes',
        [{"movie_id": DEFAULT_MOVIE_ID, 'rating': {'$gte': 6}}],
        Likes.table_name
    )
)

bookmark_query = Test(
    'get_user_bookmarks',
    [{"user_id": DEFAULT_USER_ID}],
    Bookmarks.table_name
)

avg_rating_test = Test(
    'get_average_movie_rating',
    [
        {'$match': {"movie_id": DEFAULT_MOVIE_ID}},
        {"$group": {"_id": None, "avg_rating": {"$avg": "$rating"}}}
    ],
    Likes.table_name
)

get_review_test = Test(
    'get_review_with_sort',
    [
        {'$match': {'movie_id': DEFAULT_MOVIE_ID}},
        {
            '$lookup': {
                'from': ReviewLikes.table_name,
                'localField': 'review_id',
                'foreignField': 'review_id',
                'as': 'review_likes'
            }
        }
    ],
    Reviews.table_name
)

MONGO_TESTS = (
    get_simple_data,
    get_average_movie_rating,
    get_movie_reviews_sort_time,
    get_likes_data_after_insert,
    get_average_movie_rating_after_insert,
)
