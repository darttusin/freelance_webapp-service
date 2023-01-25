from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends

from app.database.chats_db import (
    add_new_chat, 
    add_new_message,
    get_all_chat_messages, 
    get_all_chat_rooms,
    open_chat
)
                                   
from app.schemas.chats_schemas import NewChat
from app.utils.auth_utils import get_current_user
from app.schemas.users_schemas import UserLogin


chat_routers = APIRouter()  


@chat_routers.post("/chat")
async def new_chat_router(
    chat_room_info: NewChat
) -> int | str:
    res = await add_new_chat(
        chat_room_info.advert_id,
        chat_room_info.customer_id,
        chat_room_info.performer_id
    )

    if type(res) == int: 
        return {
        "chat_id": res
        }
    else: 
        return {
        "detail": res
        }


@chat_routers.get("/chats/mode={role}")
async def all_chats(
    role: str,
    current_user: UserLogin = Depends(get_current_user)
) -> List:
    return await get_all_chat_rooms(
        current_user['user_id'], 
        role
    )  


@chat_routers.get("/chat/{chat_room_id}")
async def get_chat(
    chat_room_id: str,
    current_user: UserLogin = Depends(get_current_user)
) -> List:
    return await get_all_chat_messages(
        chat_room_id, 
        current_user['user_id']
    )


@chat_routers.put("/openChat={chat_room_id}")
async def open_chat_router(
    chat_room_id: str, 
    current_user: UserLogin = Depends(get_current_user)
) -> dict:
    await open_chat(int(chat_room_id))
    return {
        "detail" : await open_chat(
            int(chat_room_id)
        )
    }