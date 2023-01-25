from aiohttp import ClientSession
import re
from types import NoneType
from typing import List


class Api():
    url = "http://localhost:8000"
    headers = {
        'accept' : 'application/json',
        'content-type' : 'application/json'
    }


    @classmethod
    async def post_json(
        cls,
        router: str,
        status: int,
        data: dict
    ) -> dict:
        async with ClientSession() as session:
            url = cls.url + router
            async with session.post(
                url, 
                json=data,
                ssl=False
            ) as response:
                assert response.status == status
                response_json = await response.json()
                return response_json


    @classmethod
    async def post_request(
        cls,
        router: str,
        status: int,
        data: dict,
        headers: dict
    ) -> dict:
        async with ClientSession() as session:
            url = cls.url + router
            async with session.post(
                url, 
                json=data,
                headers=headers,
                ssl=False
            ) as response:
                assert response.status == status
                response_json = await response.json()
                return response_json

    
    @classmethod
    async def post_login(
        cls,
        router: str,
        status: int,
        data: str,
        headers: dict = {}
    ) -> dict:
        async with ClientSession() as session:
            url = cls.url + router
            if headers == {}: headers = cls.headers
            async with session.post(
                url,
                data=data,
                headers=headers,
                ssl=False
            ) as response:
                response_json = await response.json()
                assert response.status == status
                return response_json
    

    @classmethod
    async def get_request(
        cls,
        router: str,
        status: int,
        headers: dict = {}
    ) -> dict:
        async with ClientSession() as session:
            url = cls.url + router
            if headers == {}: headers = cls.headers
            async with session.get(
                url,
                headers=headers,
                ssl=False
            ) as response:
                response_json = await response.json()
                assert response.status == status
                return response_json


    @classmethod
    async def put_request(
        cls,
        router: str,
        status: int,
        data: str,
        headers: dict = {}
    ) -> dict:
        async with ClientSession() as session:
            url = cls.url + router
            if headers == {}: headers = cls.headers
            async with session.put(
                url,
                json=data,
                headers=headers,
                ssl=False
            ) as response:
                response_json = await response.json()
                assert response.status == status
                return response_json
    
    @classmethod
    async def delete_request(
        cls,
        router: str,
        status: int,
        headers: dict = {}
    ) -> dict:
        async with ClientSession() as session:
            url = cls.url + router
            if headers == {}: headers = cls.headers
            async with session.delete(
                url,
                headers=headers,
                ssl=False
            ) as response:
                response_json = await response.json()
                assert response.status == status
                return response_json
