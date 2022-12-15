import datetime
import random

from core.settings import settings
from src.services.base import BaseService

NOW = '01/12/2022 19:03:43'

USERS_COUNT = 1000
USER_IDS = [str(i) for i in range(USERS_COUNT)]

MOVIES_COUNT = 1000
MOVIE_IDS = [str(i) for i in range(MOVIES_COUNT)]


class BaseDataGenerator:
    def __init__(
            self,
            service: BaseService,
            batch_count: int = settings.batch_count,
            batch_size: int = settings.batch_size
    ):
        self.service = service
        self.batch_size = batch_size
        self.batch_count = batch_count

    def generate_batch(self, dependent: bool = False):
        if dependent:
            return [
                self.service.generate_dependent_row() for _ in
                range(self.batch_size)
            ]

        return [self.service.generate_row() for _ in range(self.batch_size)]

    def generate_data(self, dependent: bool = False):
        return (
            self.generate_batch(dependent=dependent) for _ in
            range(self.batch_count)
        )


def get_random_user(amount=len(USER_IDS)):
    return random.choice(USER_IDS[:amount])


def get_random_movie(amount=len(MOVIE_IDS)):
    return random.choice(MOVIE_IDS[:amount])


def get_random_date():
    now_datetime = datetime.datetime.strptime(NOW, '%d/%m/%Y %H:%M:%S')
    delta = 60 * 24 * 365 * 7
    random_delta_minutes = datetime.timedelta(minutes=random.randint(0, delta))
    return now_datetime - random_delta_minutes
