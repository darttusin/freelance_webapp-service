import pytest
import re
from tests.admins.admin import Admin as api


@pytest.mark.asyncio
@pytest.mark.run(order=8)
@pytest.mark.parametrize(
    "username, email, password, tg_name, role, error",
    [
        ("ivan_admin", "admin@example.com", "pass", "tgname", "admin", False),
        ("ivan_admin", "admin@example.com", "pass", "tgname", "admin", True),
        ("ivan_manager", "mgr@example.com", "pass", "tgname", "manager", False),
        ("ivan_manager", "mgr@example.com", "pass", "tgname", "manager", True)
    ]
)
async def test_admin_registration(
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
    await api().registration_admin(
        data,
        200,
        error
    )