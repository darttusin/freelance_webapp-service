from app.schemas.reviews_schemas import AddReview
from app.schemas.users_schemas import UserLogin

import app.utils.users_utils as users_utils
from app.utils.auth_utils import get_current_user

from app.database.reviews_db import (
    add_review, 
    get_current_review, 
    update_review
)

from fastapi import APIRouter, Depends
from typing import List


reviews_router = APIRouter()


@reviews_router.post(
    "/review"
)
async def add_review_router(
    review_info: AddReview,
    current_user: UserLogin = Depends(get_current_user)
) -> dict:
    
    review_id = await users_utils.generate_post_id("rew")
    result = await add_review(
        review_id,
        review_info.user_id,
        review_info.advert_id,
        current_user["user_id"],
        review_info.review_author_comment,
        review_info.estimation
    )

    return {
        "detail" : result, 
        "review_id" : review_id
    }
    

@reviews_router.get(
    "/review/{review_id}"
)
async def current_review_router(
    review_id: str,
    current_user: UserLogin = Depends(get_current_user)
) -> List:
    return await get_current_review(review_id)


@reviews_router.put(
    "/review/{review_id}/{new_review_text}"
)
async def update_review_router(
    review_id: str, 
    new_review_text: str
) -> dict:
    await update_review(
        review_id, 
        new_review_text
    )
    return {
        "detail" : "ok"
    }