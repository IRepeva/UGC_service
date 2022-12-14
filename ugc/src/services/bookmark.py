from functools import lru_cache

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from src.db.mongo import get_mongo
from src.models.user import Bookmarks, Bookmark
from src.services.base import BaseService
from src.utils.data_generation import get_random_user, get_random_movie


class BookmarkService(BaseService):
    COLLECTION = 'bookmarks'

    async def get_user_bookmarks(self, user_id: str):
        bookmarks_cursor = self.collection.find({'user_id': user_id})
        if not bookmarks_cursor:
            return

        bookmarks = Bookmarks(user_id=user_id, movie_ids=[])
        for document in await bookmarks_cursor.to_list(length=100):
            bookmarks.movie_ids.append(document["movie_id"])
        return bookmarks

    async def add_bookmark(self, user_id: str, movie_id: str):
        bookmark = await self.collection.find_one(
            {'user_id': user_id, 'movie_id': movie_id}
        )
        if not bookmark:
            await self.collection.insert_one(
                {"user_id": user_id, "movie_id": movie_id}
            )
        return Bookmark(user_id=user_id, movie_id=movie_id)

    async def delete_bookmark(self, user_id: str, movie_id: str):
        del_bookmark = await self.collection.find_one_and_delete(
            {'user_id': user_id, 'movie_id': movie_id},
            projection={"_id": False},
        )

        return Bookmark.parse_obj(del_bookmark) if del_bookmark else None

    @classmethod
    def generate_row(cls):
        return {
            'user_id': get_random_user(),
            'movie_id': get_random_movie()
        }


@lru_cache()
def get_bookmark_service(
        mongo: AsyncIOMotorClient = Depends(get_mongo)) -> BookmarkService:
    return BookmarkService(mongo)
