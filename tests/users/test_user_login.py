import pytest
from tests.users.user import User as api



@pytest.mark.asyncio
@pytest.mark.run(order=3)
@pytest.mark.parametrize(
    "email, password",
    [
        ("user@example.com", "pass")
    ]
)
async def test_login(
    email: str,
    password: str
) -> None:
    data = f'grant_type=&username={email}'+\
        f'&password={password}&scope=&client_id=&client_secret='
    headers = {
        'Content-Type' : 'application/x-www-form-urlencoded'
    }
    await api().login_user(
        email,
        data,
        headers,
        200
    )