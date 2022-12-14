from collections import namedtuple
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from src.models.user import Bookmarks, UserLikes
from src.services.bookmark import (
    BookmarkService, get_bookmark_service
)
from src.services.like import LikeService, get_like_service
from src.utils.authentication import (
    get_token_payload, security
)

router = APIRouter()


@router.get('/{user_id}/bookmarks',
            response_model=Bookmarks,
            summary="Get user's bookmarks")
async def get_bookmarks(
        user_id: str,
        bookmark_service: BookmarkService = Depends(get_bookmark_service)
) -> Bookmarks:

    bookmarks = await bookmark_service.get_user_bookmarks(user_id)
    if not bookmarks:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return bookmarks


@router.get("/{user_id}/likes", response_model=UserLikes,
            summary="Get user's likes films")
async def rate_film(
        like_service: LikeService = Depends(get_like_service),
        token: namedtuple = Depends(security)
) -> UserLikes:

    token_payload = get_token_payload(token.credentials)
    if not (user_id := token_payload.get('user_id')):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    result = await like_service.get_user_likes(user_id=user_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return result
