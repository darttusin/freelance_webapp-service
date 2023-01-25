import pytest
from tests.admins.admin import Admin as api
from typing import List



@pytest.mark.asyncio
@pytest.mark.run(order=12)
@pytest.mark.parametrize(
    "email, user_id, assert_json",
    [
        (
            "admin@example.com", False,
            {
                'items': [
                    {
                        'user_id': 'id', 
                        'user_name': 'ivan2', 
                        'user_email': 'user2@example.com', 
                        'user_img_url': None
                    }, 
                    {
                        'user_id': 'id', 
                        'user_name': 'Ivan', 
                        'user_email': 'user@example.com', 
                        'user_img_url': '/img/img_123123.jpg'
                    }
                ], 
                'total': 2, 
                'page': 1, 
                'size': 50
            }
        ),
        (
            "mgr@example.com", False,
            {
                'items': [
                    {
                        'user_id': 'id', 
                        'user_name': 'ivan2', 
                        'user_email': 'user2@example.com', 
                        'user_img_url': None
                    }, 
                    {
                        'user_id': 'id', 
                        'user_name': 'Ivan', 
                        'user_email': 'user@example.com', 
                        'user_img_url': '/img/img_123123.jpg'
                    }
                ], 
                'total': 2, 
                'page': 1, 
                'size': 50
            }
        ),
        (
            "admin@example.com", True,
            {
                'user_info': [
                    {
                        'user_name': 'Ivan', 
                        'user_img_url': '/img/img_123123.jpg', 
                        'user_description': 'desc Ivan', 
                        'user_email': 'user@example.com', 
                        'user_id': 'id'
                    }
                ], 
                'adverts': [], 
                'count_adverts': 0, 
                'raiting': [], 
                'reviews': [], 
                'count_all_offers': 0, 
                'count_all_finished_offers': 0, 
                'count_all_responses': 0, 
                'count_views': 0
            }
        ),
        (
            "mgr@example.com", True,
            {
                'user_info': [
                    {
                        'user_name': 'Ivan', 
                        'user_img_url': '/img/img_123123.jpg', 
                        'user_description': 'desc Ivan', 
                        'user_email': 'user@example.com', 
                        'user_id': 'id'
                    }
                ], 
                'adverts': [], 
                'count_adverts': 0, 
                'raiting': [], 
                'reviews': [], 
                'count_all_offers': 0, 
                'count_all_finished_offers': 0, 
                'count_all_responses': 0, 
                'count_views': 0
            } 
        )
    ]
)
async def test_admin_users(
    email: str,
    user_id: bool,
    assert_json: dict | List
) -> None:
    if user_id:
        await api().users_admin(
            email,
            200,
            assert_json,
            True
        )
    else:    
        await api().users_admin(
            email,
            200,
            assert_json
        )