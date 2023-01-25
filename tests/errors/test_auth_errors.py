import pytest
from tests.users.user import User as api


@pytest.mark.asyncio
@pytest.mark.run(order=6)
@pytest.mark.parametrize(
    "assert_json, headers, status",
    [
        (
            {'detail': 'Could not validate credentials'},
            {'Authorization' : 'Bearer INVALIDTOKEN313123'},
            401    
        ),
        (
            {'detail': 'Not authenticated'},
            {'Content-Type' : "application/json"},
            401
        )
    ]
)
async def test_errors_auth(
    assert_json: dict,
    headers: dict,
    status: int
) -> None:
    await api().auth(
        assert_json,
        headers,
        status
    )
