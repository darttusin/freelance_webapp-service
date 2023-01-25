import pytest
from tests.admins.admin import Admin as api



@pytest.mark.asyncio
@pytest.mark.run(order=11)
@pytest.mark.parametrize(
    "email, user_id",
    [
        ("admin@example.com", False),
        ("mgr@example.com", False),
        ("admin@example.com", True),
        ("mgr@example.com", True)
    ]
)
async def test_admin_chats(
    email: str,
    user_id: bool
) -> None:
    if user_id:
        await api().chats_admin(
            email,
            200,
            [],
            True
        )
    else:    
        await api().chats_admin(
            email,
            200,
            []
        )
