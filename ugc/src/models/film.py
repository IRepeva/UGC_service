import datetime
from typing import List, Any

from pydantic import Field

from src.models.mixin import MixinModel


class FilmRating(MixinModel):
    movie_id: str
    likes: int
    dislikes: int
    rating: float


class FilmVotePost(MixinModel):
    rating: float


class FilmVote(FilmVotePost):
    user_id: str
    movie_id: str


class FilmReviewPost(MixinModel):
    text: str = Field(max_length=800)


class FilmReview(FilmReviewPost):
    user_id: str
    movie_id: str
    review_id: str
    date: datetime.datetime


class FilmReviewDetails(FilmReview):
    rating: float
    review_likes: List[Any] = []


class ReviewLikePost(MixinModel):
    rating: int


class ReviewLike(ReviewLikePost):
    user_id: str
    review_id: str
