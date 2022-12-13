from typing import List

from src.models.mixin import MixinModel


class Bookmarks(MixinModel):
    user_id: str
    movie_ids: List[str] = []


class Bookmark(MixinModel):
    user_id: str
    movie_id: str


class UserLikes(MixinModel):
    user_id: str
    movie_ids: List[str] = []
