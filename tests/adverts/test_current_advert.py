import pytest
import re
from tests.adverts.advert import Advert as api


@pytest.mark.asyncio
@pytest.mark.run(order=16)
@pytest.mark.parametrize(
    "email, first_assert, second_assert, third_assert, four_assert, five_assert",
    [
        (
            "user@example.com", 
            {
                'advert': {
                    'advert_id': 'id', 
                    'advert_title': 'some_title', 
                    'advert_city': 'moscow', 
                    'advert_text': 'some_text', 
                    'advert_price': 2000, 
                    'value': 'some_category', 
                    'description': 'added on website'
                }, 
                'responces': [], 
                'chats': []
            },
            {
                'advert': {
                    'advert_id': 'id', 
                    'advert_title': 'some_title2', 
                    'advert_city': 'moscow2', 
                    'advert_text': 'some_text2', 
                    'advert_price': 4000, 
                    'value': 'some_category2', 
                    'description': 'added on website'
                }, 
                'responces': [], 
                'chats': []
            },
            {
                'advert': {
                    'advert_id': 'id', 
                    'advert_title': 'some_title3', 
                    'advert_city': 'moscow3', 
                    'advert_text': 'some_text3', 
                    'advert_price': 3000, 
                    'value': 'some_category3', 
                    'description': 'added on website'
                }, 
                'responces': [], 
                'chats': []
            },
            {
                'advert': {
                    'advert_id': 'id', 
                    'advert_title': 'some_title4', 
                    'advert_city': 'moscow4', 
                    'advert_text': 'some_text4', 
                    'advert_price': 5000, 
                    'value': 'some_category4',
                    'description': 'added on website'
                },
                'responces': [], 
                'chats': []
            },
            {
                'advert': {
                    'advert_id': 'id', 
                    'advert_title': 'some_title5', 
                    'advert_city': 'moscow5', 
                    'advert_text': 'some_text5', 
                    'advert_price': 30000, 
                    'value': 'some_category5',
                    'description': 'added on website'
                },
                'responces': [], 
                'chats': []
            }
        ),
        (
            "user2@example.com", 
            {
                'advert': {
                    'advert_id': 'id', 
                    'advert_title': 'some_title', 
                    'advert_city': 'moscow', 
                    'advert_text': 'some_text', 
                    'advert_price': 2000, 
                    'value': 'some_category',
                    'description': 'added on website'
                }, 
                'responces': [], 
                'chats': []
            },
            {
                'advert': {
                    'advert_id': 'id', 
                    'advert_title': 'some_title2', 
                    'advert_city': 'moscow2', 
                    'advert_text': 'some_text2', 
                    'advert_price': 4000, 
                    'value': 'some_category2',
                    'description': 'added on website'
                }, 
                'responces': [], 
                'chats': []
            },
            {
                'advert': {
                    'advert_id': 'id', 
                    'advert_title': 'some_title3', 
                    'advert_city': 'moscow3', 
                    'advert_text': 'some_text3', 
                    'advert_price': 3000, 
                    'value': 'some_category3',
                    'description': 'added on website'
                }, 
                'responces': [], 
                'chats': []
            },
            {
                'advert': {
                    'advert_id': 'id', 
                    'advert_title': 'some_title4', 
                    'advert_city': 'moscow4', 
                    'advert_text': 'some_text4', 
                    'advert_price': 5000, 
                    'value': 'some_category4',
                    'description': 'added on website'
                },
                'responces': [], 
                'chats': []
            },
            {
                'advert': {
                    'advert_id': 'id', 
                    'advert_title': 'some_title5', 
                    'advert_city': 'moscow5', 
                    'advert_text': 'some_text5', 
                    'advert_price': 30000, 
                    'value': 'some_category5',
                    'description': 'added on website'
                },
                'responces': [], 
                'chats': []
            }
        )
    ]
)
async def test_adverts(
    email: str,
    first_assert: dict,
    second_assert: dict,
    third_assert: dict,
    four_assert: dict,
    five_assert: dict
) -> None:
    assert_jsons = []
    assert_jsons.append(first_assert)
    assert_jsons.append(second_assert)
    assert_jsons.append(third_assert)
    assert_jsons.append(four_assert)
    assert_jsons.append(five_assert)
    await api().current_advert(
        email,
        200,
        assert_jsons
    )