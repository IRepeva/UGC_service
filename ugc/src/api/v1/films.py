from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.models.film import (
    FilmRating, FilmVote, FilmVotePost, ReviewLike, ReviewLikePost, FilmReview,
    FilmReviewPost, FilmReviewDetails
)
from src.models.user import Bookmark
from src.services.bookmark import BookmarkService, get_bookmark_service
from src.services.like import LikeService, get_like_service
from src.services.review import ReviewService, get_review_service
from src.utils.authentication import get_token_payload, security

router = APIRouter()


@router.get('/{film_id}/rating',
            response_model=FilmRating,
            summary="Get movie rating")
async def film_rating(
        film_id: str,
        like_service: LikeService = Depends(get_like_service)
        # ):
) -> FilmRating:
    """
        ### Get detailed information about film rating:
        - _movie_id_
        - _number of likes_
        - _number of dislikes_
        - _rating_
    """
    film = await like_service.get_film_likes(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return film


@router.post("/{film_id}/vote", response_model=FilmVote,
             summary='Set movie rating')
async def rate_film(
        film_id: str,
        film_vote: FilmVotePost,
        like_service: LikeService = Depends(get_like_service),
        token=Depends(security)
) -> FilmVote:
    token_payload = get_token_payload(token.credentials)
    user_id = token_payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    if film_vote.rating > 10 or film_vote.rating < 1:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Rating should be between 1 and 10'
        )

    result = await like_service.rate_film(
        user_id=user_id,
        movie_id=film_id,
        rating=film_vote.rating,
    )
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'The error occurred during rating the movie {film_id}'
        )
    return result


@router.delete("/{film_id}/vote", response_model=FilmVote,
               summary='Delete movie rating')
async def delete_film_vote(
        film_id: str,
        like_service: LikeService = Depends(get_like_service),
        token=Depends(security)
) -> FilmVote:
    token_payload = get_token_payload(token.credentials)
    user_id = token_payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    result = await like_service.delete_film_vote(
        user_id=user_id,
        movie_id=film_id
    )
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'The error occurred during deleting '
                   f'the movie {film_id} rating'
        )
    return result


@router.get('/{film_id}/reviews',
            response_model=List[FilmReviewDetails],
            summary="Get movie reviews")
async def film_reviews(
        film_id: str,
        sort: str | None = None,
        review_service: ReviewService = Depends(get_review_service),
        token=Depends(security)
) -> List[FilmReviewDetails]:
    token_payload = get_token_payload(token.credentials)
    user_id = token_payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    reviews = await review_service.get_film_reviews(user_id, film_id, sort)
    if not reviews:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return reviews


@router.post("/{film_id}/review", response_model=FilmReview,
             summary='Upsert movie review')
async def review_film(
        film_id: str,
        film_review: FilmReviewPost,
        review_service: ReviewService = Depends(get_review_service),
        token=Depends(security)
) -> FilmReview:
    token_payload = get_token_payload(token.credentials)
    user_id = token_payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    result = await review_service.review_film(
        user_id=user_id,
        movie_id=film_id,
        text=film_review.text
    )
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'The error occurred during rating the movie {film_id}'
        )
    return result


@router.delete("/{film_id}/review", response_model=FilmReview,
               summary='Delete movie review')
async def delete_movie_review(
        film_id: str,
        review_service: ReviewService = Depends(get_review_service),
        token=Depends(security)) -> FilmReview:
    token_payload = get_token_payload(token.credentials)
    user_id = token_payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    result = await review_service.delete_film_review(
        user_id=user_id,
        movie_id=film_id
    )
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'The error occurred during rating the movie {film_id}'
        )
    return result


@router.post("/{film_id}/{review_id}", response_model=ReviewLike,
             summary='Rate movie review')
async def rate_review(
        film_id: str,
        review_id: str,
        like_review: ReviewLikePost,
        review_service: ReviewService = Depends(get_review_service),
        token=Depends(security)) -> ReviewLike:
    token_payload = get_token_payload(token.credentials)
    user_id = token_payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    result = await review_service.like_review(
        user_id=user_id,
        review_id=review_id,
        rating=like_review.rating
    )
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'The error occurred during rating the review {review_id}'
        )
    return result


@router.delete("/{film_id}/{review_id}", response_model=ReviewLike,
               summary='Delete review like')
async def delete_review_rating(
        film_id: str,
        review_id: str,
        review_service: ReviewService = Depends(get_review_service),
        token=Depends(security)) -> ReviewLike:
    token_payload = get_token_payload(token.credentials)
    user_id = token_payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    result = await review_service.delete_review_like(
        user_id=user_id,
        review_id=review_id
    )
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'The error occurred during deleting '
                   f'the review {review_id} rating'
        )
    return result


@router.post("{film_id}/bookmark", response_model=Bookmark,
             summary='Add movie to bookmarks')
async def add_movie_bookmark(
        film_id: str,
        bookmark_service: BookmarkService = Depends(get_bookmark_service),
        token=Depends(security)
) -> Bookmark:
    token_payload = get_token_payload(token.credentials)
    user_id = token_payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    result = await bookmark_service.add_bookmark(
        user_id=user_id,
        movie_id=film_id
    )
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'The error occurred during adding '
                   f'movie {film_id} to bookmarks'
        )
    return result


@router.delete("{film_id}/bookmark", response_model=Bookmark,
               summary='Delete movie from bookmarks')
async def delete_movie_bookmark(
        film_id: str,
        bookmark_service: BookmarkService = Depends(get_bookmark_service),
        token=Depends(security)
) -> Bookmark:
    token_payload = get_token_payload(token.credentials)
    user_id = token_payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    result = await bookmark_service.delete_bookmark(
        user_id=user_id,
        movie_id=film_id
    )
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'The error occurred during deleting '
                   f'movie {film_id} from bookmarks'
        )
    return result
