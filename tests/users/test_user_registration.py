import pytest
import re
from tests.users.user import User as api

        

@pytest.mark.asyncio
@pytest.mark.run(order=1)
@pytest.mark.parametrize(
    "username, email, password, tg_name, role, error",
    [
        ("ivan", "user@example.com", "pass", "tgname", "user", False),
        ("ivan", "user@example.com", "pass", "tgname", "user", True)
    ]
)
async def test_user_registration(
    username: str,
    email: str,
    password: str,
    tg_name: str,
    role: str,
    error: bool   
) -> None:
    data = {
        "username": username,
        "email": email,
        "password": password,
        "tg_name": tg_name,
        "role": role
    }
    await api().registration_user(
        data,
        200,
        error
    )
