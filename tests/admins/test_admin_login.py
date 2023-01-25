import pytest
from tests.admins.admin import Admin as api



@pytest.mark.asyncio
@pytest.mark.run(order=9)
@pytest.mark.parametrize(
    "email, password",
    [
        ("admin@example.com", "pass"),
        ("mgr@example.com", "pass")
    ]
)
async def test_admin_login(
    email: str,
    password: str
) -> None:
    data = f'grant_type=&username={email}'+\
        f'&password={password}&scope=&client_id=&client_secret='
    headers = {
        'Content-Type' : 'application/x-www-form-urlencoded'
    }
    await api().login_admin(
        email,
        data,
        headers,
        200
    )