from typing import List
from datetime import datetime


async def add_to_list(
    request
) -> List:
    data = []
    for row in request:
        data.append(row._asdict())
    return data


async def find_user_id(
    user_ids, 
    advert_id, 
    advert_status
) -> str:
    for id_ in user_ids:
        if id_["advert_id"] == advert_id:
            return id_["user_id"]
    return None


async def add_to_list_adverts(
    request, 
    user_ids
) -> List:
    data = []
    user_ids_list = []

    for row in request:
        data.append(row._asdict())
    for row in user_ids:
        user_ids_list.append(row._asdict())

    for advert in data:
        advert["user_id"] = await find_user_id(
                                        user_ids_list,
                                        advert["advert_id"],
                                        advert["advert_status"])
    return data


async def add_to_dict_user(
    result
) -> dict:
    return {
        "user_id" : result[0][0],
        "user_email" : result[0][1],
        "user_name" : result[0][2],
        "user_password" : result[0][3],
        "user_img_url" : result[0][4],
        "user_description" : result[0][5]
    }


async def add_to_dict_admin(
    result
) -> dict:
    return {
        "admin_id" : result[0][0],
        "admin_email" : result[0][1],
        "admin_login" : result[0][2],
        "admin_password" : result[0][3],
        "admin_role" : result[0][4]
    }


async def add_to_dict_user_info(
    result
) -> dict:
    return {
        "user_name" : result[0][0],
        "user_description" : result[0][1],
        "user_img_url" : result[0][2]
    }


async def add_to_dict_user_info_for_admin(
    result
) -> dict:
    return {
        "user_id": result[0][0],
        "user_email": result[0][1],
        "user_name": result[0][2],
        "user_description": result[0][3],
        "user_img_url": result[0][4]
    }

async def add_to_list_messages_2(
    request, 
    request_data, 
    user_id    
) -> List:
    data = []
    chat_info = {}

    for row in request_data:
        dict_row = row._asdict()
        chat_info = dict_row
        if user_id != "None":
            chat_info["user_id"] = user_id[0]
            chat_info["user_name"] = user_id[1]

    for row in request:
        dict_row = row._asdict()
        data.append(dict_row)

    return chat_info, sorted(data, key=lambda d: d['message_time'])


async def add_to_list_messages(
    request1, 
    request2, 
    request_data, 
    user_id
) -> List:
    data = []
    chat_info = {}

    for row in request_data:
        dict_row = row._asdict()
        chat_info = dict_row
        if user_id != "None":
            chat_info["user_id"] = user_id[0]
            chat_info["user_name"] = user_id[1]

    for row in request1:
        dict_row = row._asdict()
        data.append(dict_row)

    if request2:
        for row in request2:
            dict_row = row._asdict()
            data.append(dict_row)

    return chat_info, sorted(data, key=lambda d: d['message_time']) 


async def add_to_list_rooms(
    request1, 
    request2
) -> List:
    data = []

    for row in request1:
        dict_row = row._asdict()
        data.append(dict_row)

    for row in request2:
        dict_row = row._asdict()
        data.append(dict_row)

    return data


async def add_to_list_chats(
    request1, 
    request2
) -> List:
    data = []

    for row in request1:
        dict_row = row._asdict()
        data.append(dict_row)

    for row in request2:
        dict_row = row._asdict()
        if dict_row not in data:
            data.append(dict_row)

    return data