from aiohttp import ClientSession
import re
from types import NoneType
from tests.api import Api
from tests.users.user import User
from typing import List
import traceback


class Admin(User):
    admins_tokens = {}
    admins = {}


    @classmethod
    async def registration_admin(
        cls,
        data: dict,
        status: int,
        error: bool
    ) -> None:
        response_json = await User.post_json(
            "/registration",
            200,
            data
        )
        try:
            if error:
                assert response_json["detail"] == "Email already used"
            else:
                if data["role"] == "admin":
                    assert re.match(
                        r'admin_\w{32}', 
                        response_json["admin_id"]
                    )
                elif data["role"] == "manager":
                    assert re.match(
                        r'manager_\w{32}', 
                        response_json["admin_id"]
                    )
                else:
                    assert response_json["detail"]  == "error in data"
                cls.admins[data["username"]] = {
                    "admin_id" : response_json["admin_id"],
                    "admin_email" : data["email"],
                    "admin_role": data["role"]
                }
        except (KeyError, TypeError, AssertionError) as e:
            print(response_json)
            print(cls.admins)
            assert False, traceback.format_tb(e.__traceback__)[0]


    @classmethod
    async def login_admin(
        cls,
        email: str,
        data: str | dict | None,
        headers: dict,
        status: int,
        error: bool = False,
        assert_json: str = None
    ) -> None:
        response_json = await Admin.post_request(
            "/admin/login", 
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
            if email[0:5] == "admin":
                assert len(response_json["access_token"]) == 140
            elif email[0:3] == "mgr":
                assert len(response_json["access_token"]) == 137
            assert response_json["token_type"] == "bearer"
            cls.admins_tokens[email] = response_json["access_token"]
            admin_info = response_json['admin_info']
            admin_login = admin_info["admin_login"]
            admin_info.pop("admin_login")
            assert admin_info == cls.admins[admin_login]


    @classmethod
    async def chats_admin(
        cls, 
        email: str,
        status: int,
        assert_json: dict | List,
        user_id: bool = False
    ) -> None:
        headers = {
            'Authorization' : 'Bearer ' + cls.admins_tokens[email]
        }
        router = "/admin/chats" 
        if user_id:
            user_id = cls.users["Ivan"]["user_id"]
            router += f"/user={user_id}"

        assert assert_json == await Admin.get_request(
            router, 
            status,
            headers
        )

    @classmethod
    async def users_admin(
        cls, 
        email: str,
        status: int,
        assert_json: dict | List,
        user_id: bool = False
    ) -> None:
        headers = {
            'Authorization' : 'Bearer ' + cls.admins_tokens[email]
        }
        router = "/admin/users" 
        if user_id:
            user_id_cls = cls.users["Ivan"]["user_id"]
            router = "/admin" + f"/user={user_id_cls}"

        response_json = await Admin.get_request(
            router, 
            status,
            headers
        )
        if user_id:
            assert_json["user_info"][0]["user_id"] = cls.users[
                assert_json["user_info"][0]["user_name"]
            ]["user_id"]
            assert assert_json == response_json
        else:
            assert_json["items"][0]["user_id"] = cls.users[
                assert_json["items"][0]["user_name"]
            ]["user_id"]
            assert_json["items"][1]["user_id"] = cls.users[
                assert_json["items"][1]["user_name"]
            ]["user_id"]
            assert assert_json == response_json


    


