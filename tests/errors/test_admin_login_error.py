import pytest
from tests.admins.admin import Admin as api


@pytest.mark.asyncio
@pytest.mark.run(order=10)
@pytest.mark.parametrize(
    "email, password",
    [
        ("wrong@mail.ru", "wrongpass")
    ]
)
async def test_login_admin_with_error(
    email: str,
    password: str
) -> None:
    assert_json = {
        "detail": "Incorrect adminname or password"
    }
    data = f'grant_type=&username={email}'+\
            f'&password={password}&scope=&client_id=&client_secret='
    headers = {
            'Content-Type' : 'application/x-www-form-urlencoded'
    }
    await api().login_admin(
        email,
        data,
        headers, 
        200,
        True,
        assert_json
    )