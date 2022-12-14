import random
from functools import lru_cache

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
from src.db.mongo import get_mongo
from src.models.film import FilmRating, FilmVote
from src.models.user import UserLikes
from src.services.base import BaseService
from src.utils.data_generation import get_random_user, get_random_movie


class LikeService(BaseService):
    COLLECTION = 'likes'

    async def get_film_likes(self, movie_id: str):
        film = await self.collection.find_one({'movie_id': movie_id})
        if not film:
            return

        likes = await self.collection.count_documents(
            {'movie_id': movie_id, 'rating': {'$gte': 6}}
        )
        dislikes = await self.collection.count_documents(
            {'movie_id': movie_id, 'rating': {'$lte': 5}}
        )

        avg_rating = await self.get_average_rating(self.collection, movie_id)
        return FilmRating(
            movie_id=movie_id,
            likes=likes,
            dislikes=dislikes,
            rating=round(avg_rating, 2)
        )

    @classmethod
    async def get_average_rating(cls, collection, movie_id: str):
        rating_cursor = collection.aggregate([
            {'$match': {"movie_id": movie_id}},
            {"$group": {"_id": None, "avg_rating": {"$avg": "$rating"}}}
        ])

        avg_rating = await rating_cursor.to_list(length=None)
        print(f'AVERAGE RATING: {avg_rating}, {type(avg_rating)}')
        return float(avg_rating[0]['avg_rating']) if avg_rating else 0.0

    async def get_user_likes(self, user_id: str):
        user_likes_cursor = self.collection.find(
            {"user_id": user_id, 'rating': {'$gte': 6}},
            {"movie_id": 1, "_id": 0}
        )
        if not user_likes_cursor:
            return

        user_likes = UserLikes(user_id=user_id, movie_ids=[])
        for document in await user_likes_cursor.to_list(length=100):
            user_likes.movie_ids.append(document["movie_id"])
        return user_likes

    async def rate_film(self, user_id: str, movie_id: str, rating: float):
        new_rating = await self.collection.find_one_and_replace(
            {'user_id': user_id, 'movie_id': movie_id},
            {'user_id': user_id, 'movie_id': movie_id, 'rating': rating},
            projection={"_id": False},
            return_document=ReturnDocument.AFTER,
            upsert=True,
        )
        print(f'New rating: {new_rating}')
        return FilmVote.parse_obj(new_rating) if rating else None

    async def delete_film_vote(self, user_id: str, movie_id: str):
        deleted_vote = await self.collection.find_one_and_delete(
            {'user_id': user_id, 'movie_id': movie_id},
            projection={"_id": False},
        )
        return FilmVote.parse_obj(deleted_vote) if deleted_vote else None

    @classmethod
    def generate_row(cls):
        return {
            'user_id': get_random_user(),
            'movie_id': get_random_movie(),
            'rating': random.randint(0, 10)
        }


@lru_cache()
def get_like_service(
        mongo: AsyncIOMotorClient = Depends(get_mongo)) -> LikeService:
    return LikeService(mongo)
