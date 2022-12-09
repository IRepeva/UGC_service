from collections import namedtuple
from collections import namedtuple
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.models.film import (
    FilmRating, FilmVote, FilmVotePost
)
from src.services.like import LikeService, get_like_service
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
        token: namedtuple = Depends(security)
) -> FilmVote:
    token_payload = get_token_payload(token.credentials)
    if not (user_id := token_payload.get('user_id')):
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
        token: namedtuple = Depends(security)
) -> FilmVote:
    token_payload = get_token_payload(token.credentials)
    if not (user_id := token_payload.get('user_id')):
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
