import pytest
from types import NoneType
import re
from tests.users.user import User as api


@pytest.mark.asyncio
@pytest.mark.run(order=5)
@pytest.mark.parametrize(
    "email, router, method, data, status, assert_json",
    [
        ("user@example.com", "/cabinet", "get", None, 200, None),
        ("user@example.com", '/profile', 'get', 'user_id', 200, None),
        ("user@example.com", '/profile', 'put', {
            "user_name": "Ivan",
            "img_url": "/img/img_123123.jpg",
            "description": "desc Ivan"
            }, 
            200, 
            {
                "detail": "successful changed"
            }
        )
    ]
)
async def test_profile(
    email: str,
    router: str,
    method: str,
    data: str | None | dict,
    status: int,
    assert_json: None | dict
) -> None:
    await api().profile(
        email,
        router,
        method,
        data,
        status,
        assert_json
    )
