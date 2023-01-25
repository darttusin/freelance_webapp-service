import pytest
import re
from tests.adverts.advert import Advert as api


@pytest.mark.asyncio
@pytest.mark.run(order=14)
@pytest.mark.parametrize(
    "category, city, email, assert_json",
    [ 
        (
            "None", "None", "user@example.com", 
            {
                "items": [],
                "total": 0,
                "page": 1,
                "size": 50
            }
        ),
        (
            "None", "None", "user2@example.com", 
            {
                'items': [
                    {
                        'advert_id': 'id', 
                        'advert_title': 'some_title', 
                        'advert_city': 'moscow', 
                        'advert_text': 'some_text', 
                        'advert_price': 2000.0, 
                        'value': 'some_category', 
                        'response': False, 
                        'user_img_url': '/img/img_123123.jpg'
                    }, 
                    {
                        'advert_id': 'id', 
                        'advert_title': 'some_title2', 
                        'advert_city': 'moscow2', 
                        'advert_text': 'some_text2', 
                        'advert_price': 4000.0, 
                        'value': 'some_category2', 
                        'response': False, 
                        'user_img_url': '/img/img_123123.jpg'
                    }, 
                    {
                        'advert_id': 'id', 
                        'advert_title': 'some_title3', 
                        'advert_city': 'moscow3', 
                        'advert_text': 'some_text3', 
                        'advert_price': 3000.0, 
                        'value': 'some_category3', 
                        'response': False, 
                        'user_img_url': '/img/img_123123.jpg'
                    }, 
                    {
                        'advert_id': 'id', 
                        'advert_title': 'some_title4', 
                        'advert_city': 'moscow4', 
                        'advert_text': 'some_text4', 
                        'advert_price': 5000.0, 
                        'value': 'some_category4', 
                        'response': False, 
                        'user_img_url': '/img/img_123123.jpg'
                    }, 
                    {
                        'advert_id': 'id', 
                        'advert_title': 'some_title5', 
                        'advert_city': 'moscow5', 
                        'advert_text': 'some_text5', 
                        'advert_price': 30000.0, 
                        'value': 'some_category5', 
                        'response': False, 
                        'user_img_url': '/img/img_123123.jpg'
                    }
                ], 
                'total': 5, 
                'page': 1, 
                'size': 50
            }
        ),
        (
            "some_category", "None", "user2@example.com", 
            {
                'items': [
                    {
                        'advert_id': 'id', 
                        'advert_title': 'some_title', 
                        'advert_city': 'moscow', 
                        'advert_text': 'some_text', 
                        'advert_price': 2000, 
                        'value': 'some_category', 
                        'response': False, 
                        'user_img_url': '/img/img_123123.jpg'
                    }
                ], 
                'total': 1, 
                'page': 1, 
                'size': 50
            }
        ),
        (
            "some_category", "moscow", "user2@example.com", 
            {
                'items': [
                    {
                        'advert_id': 'id', 
                        'advert_title': 'some_title', 
                        'advert_city': 'moscow', 
                        'advert_text': 'some_text', 
                        'advert_price': 2000, 
                        'value': 'some_category', 
                        'response': False, 
                        'user_img_url': '/img/img_123123.jpg'
                    }
                ], 
                'total': 1, 
                'page': 1, 
                'size': 50
            }
        ),
        (
            "None", "moscow", "user2@example.com", 
            {
                'items': [
                    {
                        'advert_id': 'id', 
                        'advert_title': 'some_title', 
                        'advert_city': 'moscow', 
                        'advert_text': 'some_text', 
                        'advert_price': 2000, 
                        'value': 'some_category', 
                        'response': False, 
                        'user_img_url': '/img/img_123123.jpg'
                    }
                ], 
                'total': 1, 
                'page': 1, 
                'size': 50
            }
        )             
    ]
)
async def test_adverts(
    category: str,
    city: str,
    email: str,
    assert_json: dict
) -> None:
    await api().test_adverts(
        category,
        city,
        email,
        200,
        assert_json
    )


@pytest.mark.asyncio
@pytest.mark.run(order=15)
@pytest.mark.parametrize(
    "email, assert_json",
    [ 
        (
            "user@example.com", 
            [
                {
                    'advert_id': 'id', 
                    'advert_title': 'some_title', 
                    'advert_city': 'moscow', 
                    'advert_text': 'some_text', 
                    'advert_price': 2000, 
                    'value': 'some_category', 
                    'advert_status': 'added on website', 
                    'user_id': None
                }, 
                {
                    'advert_id': 'id', 
                    'advert_title': 'some_title2', 
                    'advert_city': 'moscow2', 
                    'advert_text': 'some_text2', 
                    'advert_price': 4000, 
                    'value': 'some_category2', 
                    'advert_status': 'added on website', 
                    'user_id': None
                }, 
                {
                    'advert_id': 'id', 
                    'advert_title': 'some_title3', 
                    'advert_city': 'moscow3', 
                    'advert_text': 'some_text3', 
                    'advert_price': 3000, 
                    'value': 'some_category3', 
                    'advert_status': 'added on website', 
                    'user_id': None
                }, 
                {
                    'advert_id': 'id', 
                    'advert_title': 'some_title4', 
                    'advert_city': 'moscow4', 
                    'advert_text': 'some_text4', 
                    'advert_price': 5000, 
                    'value': 'some_category4', 
                    'advert_status': 'added on website', 
                    'user_id': None
                }, 
                {
                    'advert_id': 'id', 
                    'advert_title': 'some_title5', 
                    'advert_city': 'moscow5', 
                    'advert_text': 'some_text5', 
                    'advert_price': 30000, 
                    'value': 'some_category5', 
                    'advert_status': 'added on website', 
                    'user_id': None
                }
            ]
        ),
        ("user2@example.com", [])        
    ]
)
async def test_my_adverts(
    email: str,
    assert_json: dict
) -> None:
    await api().test_adverts(
        "None",
        "None",
        email,
        200,
        assert_json,
        True
    )