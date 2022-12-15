from typing import Any, Generator

from db_research.data.models import BaseDataClass
from db_research.settings import base_settings


class BaseDataGenerator:
    def __init__(
            self,
            data_cls: BaseDataClass,
            batch_count: int = base_settings.batch_count,
            batch_size: int = base_settings.batch_size
    ):
        self.data_cls = data_cls
        self.batch_size = batch_size
        self.batch_count = batch_count

    def generate_batch(self, batch_size: int):
        return [self.data_cls.generate_row() for _ in range(batch_size)]

    def generate_data(self) -> Generator[list[dict[str, Any]], Any, None]:
        return (
            self.generate_batch(self.batch_size) for _ in
            range(self.batch_count)
        )
