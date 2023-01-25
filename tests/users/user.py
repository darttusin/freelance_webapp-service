from aiohttp import ClientSession
import re
from types import NoneType
from tests.api import Api
from typing import List
import traceback


class User(Api):
    users_tokens = {}
    users = {}


    @classmethod
    async def registration_user(
        cls,
        data: dict,
        status: int,
        error: bool,
        error_skip: bool = False,
        assert_json: dict = None
    ) -> None:
        response_json = await User.post_json(
            "/registration",
            status,
            data
        )
        if assert_json: assert assert_json == response_json
        try:
            if error:
                assert response_json["detail"] == "Email already used"
            else:
                if data["role"] == "user":
                    assert re.match(r"id_\w{32}", response_json["detail"])
                    cls.users[data["username"]] = {
                        "user_id" : response_json["detail"],
                        "email" : data["email"],
                        "tg_name" : data["tg_name"]
                    }
                elif response_json["detail"]  == "error in data":
                    assert response_json["detail"]  == "error in data"
        except (TypeError, KeyError, AssertionError) as e:
            print(response_json)
            print(cls.users)
            assert error_skip, traceback.format_tb(e.__traceback__)[0]


    @classmethod
    async def login_user(
        cls,
        email: str,
        data: str | dict | None,
        headers: dict,
        status: int,
        error: bool = False,
        assert_json: str = None
    ) -> None:
        response_json = await User.post_login(
            "/login", 
            status, 
            data,
            headers
        )
        if assert_json:
            assert assert_json == response_json
        if error:
            pass
        else:
            assert "access_token" in response_json
            assert "token_type" in response_json
            assert response_json["token_type"] == "bearer"
            cls.users_tokens[email] = response_json["access_token"]


    @classmethod
    async def profile(
        cls,
        email: str,
        router: str,
        method: str,
        data: str | None,
        status: int,
        assert_json: dict | None
    ) -> None:
        headers = {
            'Authorization' : 'Bearer ' + cls.users_tokens[email]
        }
        if method == 'get':
            if data and router == "/profile":
                reg_data = {
                    "username" : "ivan2",
                    "email" : "user2@example.com",
                    "password" : "pass2",
                    "tg_name" : "tgname2",
                    "role" : "user"
                }
                await User.registration_user(
                    reg_data,
                    200,
                    False
                )
                log_data = f'grant_type=&username={reg_data["email"]}'+\
                    f'&password={reg_data["password"]}&'+\
                        'scope=&client_id=&client_secret='
                log_headers = {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
                await User.login_user(
                    reg_data["email"],
                    log_data,
                    log_headers,
                    200
                )
                new_router = router + f"/{cls.users['ivan2']['user_id']}"
                response_json = await User.get_request(
                    new_router, 
                    status,
                    headers
                )
            elif router == "/cabinet":
                response_json = await User.get_request(
                    router, 
                    status,
                    headers
                )
            else:
                assert False, 'error in parameters for testing(router)'
        elif method == 'put' and router == "/profile":
            new = {}
            new["user_id"] = cls.users["ivan"]["user_id"]
            new["email"] = cls.users["ivan"]["email"]
            new["tg_name"] = cls.users["ivan"]["tg_name"]
            cls.users["Ivan"] = new
            cls.users.pop("ivan")
            response_json = await User.put_request(
                router, 
                status, 
                data,
                headers
                )
        else:
            assert False, 'error in parameters for testing'
        if router == "/cabinet" or \
            (router == "/profile" and method == "get"): 
            assert re.match(r'id_\w{32}', response_json["user_id"])
            assert response_json["user_name"] in cls.users 
            assert type(response_json["user_description"]) == NoneType
            assert type(response_json["user_img_url"]) == NoneType
            assert response_json["user_estimations"] == []
            assert response_json["user_portfolios"] == []
        elif router == "/profile" and method == 'put':
            assert assert_json == response_json
        else:
            assert False, 'error in method + router'


    @classmethod
    async def auth(
        cls,
        assert_json: dict,
        headers: dict,
        status: int    
    ) -> None:
        assert await User.get_request(
            "/cabinet", 
            status,
            headers
        ) == assert_json
    

    @classmethod
    async def performers(
        cls,
        email: str,
        router: str,
        status: int,
        page: int,
        size: int,
        total: int,
        user_info: List | None,
        assert_json: dict | None
    ) -> None:
        headers = {
            'Authorization' : 'Bearer ' + cls.users_tokens[email]
        }
        response_json = await User.get_request(
            router, 
            status,
            headers
        )
        if assert_json:
            assert assert_json == response_json
        else:
            assert response_json["total"] == total
            assert response_json["page"] == page
            assert response_json["size"] == size

            for i in range(len(response_json["items"])):
                user = response_json["items"][i]
                assert re.match(r'id_\w{32}', user["user_id"])
                assert user["user_info"] == user_info[i]
                assert user["avg_estimation"] == 0
                assert user["count_estimation"] == 0 
