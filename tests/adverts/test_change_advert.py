import pytest
import re
from tests.adverts.advert import Advert as api


@pytest.mark.asyncio
@pytest.mark.run(order=17)
@pytest.mark.parametrize(
    "email, method, data",
    [   
        ("user@example.com", "delete", None),
        ("user2@example.com", "delete", None),
        (
            "user@example.com", "put", {
                "advert_text": "new_text4",
                "advert_title": "new_title4",
                "advert_category": "new_category4",
                "advert_city": "new_city4",
                "advert_price": 0
            }
        ),
        (
            "user2@example.com", "put", {
                "advert_text": "new_text4",
                "advert_title": "new_title4",
                "advert_category": "new_category4",
                "advert_city": "new_city4",
                "advert_price": 0
            }  
        )  
    ]
)
async def test_change_advert(
    email: str,
    method: str,
    data: dict | None
) -> None:
    await api().change_advert(
        email,
        200,
        method,
        data
    )