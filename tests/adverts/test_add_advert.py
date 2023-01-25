import pytest
import re
from tests.adverts.advert import Advert as api


@pytest.mark.asyncio
@pytest.mark.run(order=13)
@pytest.mark.parametrize(
    "email, text, title, category, city, price",
    [
        (
            "user@example.com", "some_text", "some_title", 
            "some_category", "moscow", 2000
        ),
        (
            "user@example.com", "some_text2", "some_title2", 
            "some_category2", "moscow2", 4000
        ),
        (
            "user@example.com", "some_text3", "some_title3", 
            "some_category3", "moscow3", 3000
        ),
        (
            "user@example.com", "some_text4", "some_title4", 
            "some_category4", "moscow4", 5000
        ),
        (
            "user@example.com", "some_text5", "some_title5", 
            "some_category5", "moscow5", 30000
        )        
    ]
)
async def test_new_advert(
    email: str,
    text: str,
    title: str,
    category: str,
    city: str,
    price: float  
) -> None:
    data = {
        "advert_text": text,
        "advert_title": title,
        "advert_category": category,
        "advert_city": city,
        "advert_price": price
    }
    assert_json = {
        "detail" : "successful add new advert id", 
        "advert_id" : "id"
    }
    await api().new_advert(
        email,
        data,
        200,
        assert_json
    )