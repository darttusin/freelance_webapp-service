import pytest
from tests.users.user import User as api


@pytest.mark.asyncio
@pytest.mark.run(order=2)
@pytest.mark.parametrize(
    "username, email, password, tg_name, role, status, assert_json",
    [
        (
            "ivan_test", "user222@example.com", "pass", 
            "tgname", "err", 200, {"detail" : "error in data"}
        ),
        (
            "ivan_test", "errmail.com", "pass", 
            "tgname", "user", 422, {'detail': [{'loc': ['body', 'email'], 
                            'msg': 'value is not a valid email address', 
                            'type': 'value_error.email'}]}
        )
    ]
)
async def test_regisration_with_error(
    username: str,
    email: str,
    password: str,
    tg_name: str,
    role: str,
    status: int,
    assert_json: dict  
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
        status,
        False,
        True,
        assert_json
    )  
