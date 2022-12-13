import datetime
import random
from functools import lru_cache
from typing import Optional

from faker import Faker
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
from src.db.mongo import get_mongo
from src.models.film import FilmReview, FilmReviewDetails, ReviewLike
from src.services.base import BaseService
from src.services.like import LikeService
from src.utils.data_generation import (
    get_random_user, get_random_movie, get_random_date
)
from src.utils.parser import parse_sort

faker = Faker()


class ReviewService(BaseService):
    COLLECTION = 'reviews'
    DEPENDENT_COLLECTION = 'review_likes'

    async def get_film_reviews(self, user_id: Optional[str],
                               movie_id: str, sort: str):
        aggregate_pipeline = [
            {'$match': {'movie_id': movie_id}},
            {
                '$lookup': {
                    'from': self.DEPENDENT_COLLECTION,
                    'localField': 'review_id',
                    'foreignField': 'review_id',
                    'as': 'review_likes'
                }
            }
        ]
        if sort:
            aggregate_pipeline.append({'$sort': parse_sort(sort)})

        reviews_cursor = self.collection.aggregate(aggregate_pipeline)
        if not reviews_cursor:
            return

        likes_collection = self.database.get_collection(LikeService.COLLECTION)

        user_rating = await likes_collection.find_one(
            {'movie_id': movie_id, 'user_id': user_id}
        )
        rating = (
            user_rating['rating'] if user_rating else
            await LikeService.get_average_rating(likes_collection, movie_id)
        )
        reviews = await reviews_cursor.to_list(length=100)
        print(f"review likes: {reviews[0].get('review_likes')}")
        return [
            FilmReviewDetails(
                user_id=review['user_id'],
                movie_id=movie_id,
                review_id=review['review_id'],
                text=review.get('text'),
                date=review.get('date'),
                rating=round(rating, 2),
                review_likes=[d['rating'] for d in review.get('review_likes')]
            )
            for review in reviews
        ]

    async def review_film(self, user_id: str, movie_id: str, text: str):
        new_review = await self.collection.find_one_and_replace(
            {'user_id': user_id, 'movie_id': movie_id},
            {
                'review_id': self.COLLECTION + ':' + user_id + ':' + movie_id,
                'user_id': user_id,
                'movie_id': movie_id,
                'text': text,
                'date': datetime.datetime.now()
            },
            projection={"_id": False},
            return_document=ReturnDocument.AFTER,
            upsert=True,
        )

        return FilmReview.parse_obj(new_review) if new_review else None

    async def delete_film_review(self, user_id: str, movie_id: str):
        deleted_review = await self.collection.find_one_and_delete(
            {'user_id': user_id, 'movie_id': movie_id},
            projection={"_id": False},
        )
        return FilmReview.parse_obj(deleted_review) if deleted_review else None

    async def like_review(self, user_id: str, review_id: str, rating: int):
        review = await self.collection.find_one({'review_id': review_id})
        if not review:
            return

        review_likes = self.database.get_collection(self.DEPENDENT_COLLECTION)
        new_review_like = await review_likes.find_one_and_replace(
            {'user_id': user_id, 'review_id': review_id},
            {'user_id': user_id, 'review_id': review_id, 'rating': rating},
            projection={"_id": False},
            return_document=ReturnDocument.AFTER,
            upsert=True,
        )
        return ReviewLike.parse_obj(
            new_review_like) if new_review_like else None

    async def delete_review_like(self, user_id: str, review_id: str):
        review = await self.collection.find_one({'review_id': review_id})
        if not review:
            return

        review_likes = self.database.get_collection(self.DEPENDENT_COLLECTION)
        deleted = await review_likes.find_one_and_delete(
            {'user_id': user_id, 'review_id': review_id},
            projection={"_id": False}
        )
        return ReviewLike.parse_obj(deleted) if deleted else None

    @classmethod
    def generate_row(cls):
        user_id, movie_id = get_random_user(), get_random_movie()
        return {
            'review_id': cls.COLLECTION + ':' + user_id + ':' + movie_id,
            'user_id': user_id,
            'movie_id': movie_id,
            'text': faker.text(),
            'date': get_random_date(),
        }

    @classmethod
    def generate_dependent_row(cls):
        user_id, movie_id = get_random_user(), get_random_movie()
        return {
            'user_id': get_random_user(),
            'review_id': cls.COLLECTION + ':' + user_id + ':' + movie_id,
            'rating': random.randint(0, 1)
        }


@lru_cache()
def get_review_service(
        mongo: AsyncIOMotorClient = Depends(get_mongo)) -> ReviewService:
    return ReviewService(mongo)
