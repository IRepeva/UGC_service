import datetime
import random
from abc import abstractmethod
from typing import Optional, Any

from faker import Faker

from db_research.settings import base_settings
from db_research.utils import (
    generate_random_string, get_random_user, get_random_movie, get_random_date
)

faker = Faker()


class BaseDataClass:
    table_name: Optional[str] = None

    @classmethod
    @abstractmethod
    def generate_row(cls, *args) -> dict[str, Any]:
        ...


class Views(BaseDataClass):
    table_name = 'views'

    @classmethod
    def generate_row(cls, *args):
        return {
            'user_id': generate_random_string(),
            'movie_id': generate_random_string(),
            'frame': random.randint(1, base_settings.max_movie_duration),
            'time_created': datetime.datetime.now()
        }


class Likes(BaseDataClass):
    table_name = 'likes'

    @classmethod
    def generate_row(cls, *args):
        return {
            'user_id': get_random_user(),
            'movie_id': get_random_movie(),
            'rating': random.randint(0, 10)
        }


class Bookmarks(BaseDataClass):
    table_name = 'bookmarks'

    @classmethod
    def generate_row(cls, *args):
        return {
            'user_id': get_random_user(),
            'movie_id': get_random_movie()
        }


class Reviews(BaseDataClass):
    PREFIX = 'reviews'
    table_name = 'reviews'

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
    table_name = 'review_likes'

    @classmethod
    def generate_row(cls, *args):
        user_id, movie_id = get_random_user(), get_random_movie()
        return {
            'user_id': get_random_user(),
            'review_id': Reviews.PREFIX + ':' + user_id + ':' + movie_id,
            'rating': random.randint(0, 1)
        }
