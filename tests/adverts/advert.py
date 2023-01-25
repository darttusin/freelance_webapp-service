from aiohttp import ClientSession
import re
from types import NoneType
from tests.api import Api
from tests.users.user import User
from typing import List
import traceback


class Advert(User, Api):
    adverts = {}


    @classmethod
    async def new_advert(
        cls,
        email: str,
        data: dict,
        status: int,
        assert_json: dict
    ) -> None:
        headers = {
            'Authorization' : 'Bearer ' + cls.users_tokens[email]
        }
        response_json = await Advert.post_request(
            "/advert", 
            status, 
            data,
            headers
        )

        assert_json["advert_id"] = response_json["advert_id"]
        assert assert_json == response_json
        cls.adverts[response_json["advert_id"]] = data


    @classmethod
    async def test_adverts(
        cls,
        category: str,
        city: str,
        email: str,
        status: int,
        assert_json: dict,
        my: bool = False
    ) -> None:
        headers = {
            'Authorization' : 'Bearer ' + cls.users_tokens[email]
        }
        router = "/myAdverts" if my else "/adverts/params="+\
            f"{category}&{city}?page=1&size=50"
        
        response_json = await Advert.get_request(
            router, 
            status, 
            headers
        )

        if email == "user2@example.com":
            if my:
                pass
            else:
                for i in range(len(response_json["items"])):
                    assert_json["items"][i]["advert_id"] =\
                        response_json["items"][i]["advert_id"]
        elif email == "user@example.com":
            if my:
                for i in range(len(response_json)):
                    assert_json[i]["advert_id"] =\
                        response_json[i]["advert_id"]
        assert assert_json == response_json

    
    @classmethod
    async def current_advert(
        cls,
        email: str,
        status: int,
        assert_jsons: List
    ) -> None:
        adverts_ids = list(cls.adverts.keys())
        headers = {
            'Authorization' : 'Bearer ' + cls.users_tokens[email]
        }
        for i in range(len(adverts_ids)):
            responce_json = await Advert.get_request(
                f"/advert/{adverts_ids[i]}", 
                status,
                headers
            )
            assert_jsons[i]["advert"]["advert_id"] = adverts_ids[i]
            assert assert_jsons[i] == responce_json


    @classmethod
    async def change_advert(
        cls,
        email: str,
        status: int,
        method: str,
        data: dict | None,
    ) -> None:
        headers = {
            'Authorization' : 'Bearer ' + cls.users_tokens[email]
        }   
        if method == "delete":
            advert_id = list(cls.adverts.keys())[-1]
            responce_json = await Advert.delete_request(
                f"/advert/{advert_id}", 
                status,
                headers
            )
            if email == "user2@example.com":
                assert responce_json == {
                    "detail" : "not user advert"
                }
            else:
                assert responce_json == {
                    "detail" : "successful delete advert and "+\
                        "all responses"+ f" - {advert_id}"
                }
                cls.adverts.pop(advert_id)
        elif method == "put":
            advert_id = list(cls.adverts.keys())[-1]
            responce_json = await Advert.put_request(
                f"/advert/{advert_id}", 
                status, 
                data,
                headers
            )
            if email == "user2@example.com":
                assert responce_json == {'detail': 'not user advert'}
            else:
                assert responce_json == {
                    "detail" : f"successful update advert - {advert_id}"
                }
                cls.adverts.pop(advert_id)
        else:
            assert False, "error in method"
           



    

        