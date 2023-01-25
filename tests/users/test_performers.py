import pytest
from tests.users.user import User as api
from typing import List


@pytest.mark.asyncio
@pytest.mark.run(order=7)
@pytest.mark.parametrize(
    "email, raiting, count_reviews, count_jobs, page, size, total, assert_json, user_info", 
    [
        (
            "user@example.com", "0", "0", "0", 1, 50, 1, None,
            [
                {
                    "user_name": "ivan2",
                    "user_description": None,
                    "user_img_url": None  
                }
            ]
        ),
        (
            "user@example.com", "5", "0", "0", 1, 50, 0,
            {
                "items": [],
                "total": 0,
                "page": 1,
                "size": 50
            }, 
            None
        ),
        (
            "user@example.com", "0", "5", "0", 1, 50, 0,
            {
                "items": [],
                "total": 0,
                "page": 1,
                "size": 50
            }, 
            None
        ),
        (
            "user@example.com", "0", "0", "5", 1, 50, 0,
            {
                "items": [],
                "total": 0,
                "page": 1,
                "size": 50
            }, 
            None
        ),
        (
            "user@example.com", "0", "0", "0", 2, 3, 1,
            {
                "items": [],
                "total": 1,
                "page": 2,
                "size": 3
            }, 
            None    
        )
    ]
)
async def test_performers(
    email: str,
    raiting: str,
    count_reviews: str,
    count_jobs: str,
    page: int,
    size: int,
    total: int,
    assert_json: dict | None,
    user_info: List | None,
) -> None:
    router = f"/performers/params={raiting}&{count_reviews}"+\
        f"&{count_jobs}?page={page}&size={size}"
    if assert_json:
        await api().performers(
            email,
            router, 
            200,
            page,
            size,
            total,
            None,
            assert_json
        )    
    elif user_info:
        await api().performers(
            email,
            router, 
            200,
            page,
            size,
            total,
            user_info,
            None
        )
    else:
        assert False, "error in parametrs"
