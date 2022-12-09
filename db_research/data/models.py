import datetime
import random
from abc import abstractmethod

from faker import Faker

from db_research.settings import base_settings
from db_research.utils import (
    generate_random_string, get_random_user, get_random_movie, get_random_date
)

faker = Faker()


class BaseDataClass:
    TABLE_NAME = None

    @classmethod
    @abstractmethod
    def generate_row(cls, *args):
        ...


class Views(BaseDataClass):
    TABLE_NAME = 'views'

    @classmethod
    def generate_row(cls, *args):
        return {
            'user_id': generate_random_string(),
            'movie_id': generate_random_string(),
            'frame': random.randint(1, base_settings.max_movie_duration),
            'time_created': datetime.datetime.now()
        }


class Likes(BaseDataClass):
    TABLE_NAME = 'likes'

    @classmethod
    def generate_row(cls, *args):
        return {
            'user_id': get_random_user(),
            'movie_id': get_random_movie(),
            'rating': random.randint(0, 10)
        }


class Bookmarks(BaseDataClass):
    TABLE_NAME = 'bookmarks'

    @classmethod
    def generate_row(cls, *args):
        return {
            'user_id': get_random_user(),
            'movie_id': get_random_movie()
        }


class Reviews(BaseDataClass):
    PREFIX = 'reviews'
    TABLE_NAME = 'reviews'

    @classmethod
    def generate_row(cls, *args):
        user_id, movie_id = get_random_user(), get_random_movie()
        return {
            'review_id': cls.PREFIX + ':' + user_id + ':' + movie_id,
            'user_id': user_id,
            'movie_id': movie_id,
            'text': faker.text(),
            'date': get_random_date(),
        }


class ReviewLikes(BaseDataClass):
    TABLE_NAME = 'review_likes'

    @classmethod
    def generate_row(cls, *args):
        user_id, movie_id = get_random_user(), get_random_movie()
        return {
            'user_id': get_random_user(),
            'review_id': Reviews.PREFIX + ':' + user_id + ':' + movie_id,
            'rating': random.randint(0, 1)
        }
