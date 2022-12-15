import datetime
import functools
import random
import string
import time

from db_research.settings import base_settings

NOW = '01/12/2022 19:03:43'

USERS_COUNT = 1000
USER_IDS = [str(i) for i in range(USERS_COUNT)]

MOVIES_COUNT = 1000
MOVIE_IDS = [str(i) for i in range(MOVIES_COUNT)]


def generate_random_string(char_num=16) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for _ in range(char_num))


def get_random_user(amount=len(USER_IDS)) -> str:
    return random.choice(USER_IDS[:amount])


def get_random_movie(amount=len(MOVIE_IDS)) -> str:
    return random.choice(MOVIE_IDS[:amount])


def get_random_date() -> datetime.datetime:
    now_datetime = datetime.datetime.strptime(NOW, "%d/%m/%Y %H:%M:%S")
    delta = 60*24*365*7
    random_delta_minutes = datetime.timedelta(minutes=random.randint(0, delta))
    return now_datetime - random_delta_minutes


def benchmark(iterations: int = base_settings.iterations_count):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            times = []
            for _ in range(iterations):
                start_time = time.perf_counter()
                func(*args, **kwargs)
                end_time = time.perf_counter()
                times.append(end_time - start_time)

            total_time = sum(times)
            avg_time = total_time / iterations

            print(f"Query: {args[0].name}")
            print(f"Number of iterations: {iterations}")
            print(f"Average run time: {avg_time:.4f} sec \n")

        return inner

    return wrapper
