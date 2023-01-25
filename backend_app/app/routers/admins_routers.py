from app.database.admins_db import (
    add_new_admin, 
    get_admin_by_email
)
from app.database.adverts_db import (
    get_current_advert, 
    get_user_id_by_advert
)
from app.database.chats_db import (
    get_all_chat_messages_admin,
    get_all_chat_rooms,
    get_all_chats_for_admins
)
from app.database.responses_db import (
    get_responses_by_advert
)
from app.database.users_db import (
    get_all_user_chats, 
    get_all_users, 
    get_stats
)
from app.schemas.admins_schemas import AdminLogin
from app.schemas.users_schemas import UserInfo
from app.schemas.adverts_schemas import (
    AdvertUpdate, 
    NewAdvert
)

from app.utils.auth_utils import (
    authenticate_admin, 
    get_current_admin
)
from app.utils.users_utils import create_access_token

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import Page, paginate


admins_router = APIRouter()


@admins_router.post(
    "/admin/login"
)
async def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    admin = \
        await authenticate_admin(
            form_data.username, 
            form_data.password
        )
    if not admin:
        return {
            "detail": "Incorrect adminname or password"
        }

    access_token = \
        await create_access_token(
            data={"sub": admin['admin_email']}
        )
    admin = {
        "admin_id" : admin["admin_id"],
        "admin_email" : admin["admin_email"],
        "admin_login": admin["admin_login"],
        "admin_role": admin["admin_role"]
    }

    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "admin_info": admin
    }


@admins_router.get(
    "/admin/chats"
)
async def all_chat(
    current_admin: AdminLogin = Depends(get_current_admin)
):
    return await get_all_chats_for_admins()


@admins_router.get(
    "/admin/user={user_id}"
)
async def get_user(
    user_id: str, 
    current_admin: AdminLogin = Depends(get_current_admin)
):
    return await get_stats(user_id)


@admins_router.get(
    "/admin/users", 
    response_model=Page[UserInfo]
)
async def get_users(
    current_admin: AdminLogin = Depends(get_current_admin)
):
    return paginate(
        await get_all_users()
    )

@admins_router.get(
    "/admin/chats/user={user_id}"
)
async def get_user_chats(
    user_id: str, 
    current_admin: AdminLogin = Depends(get_current_admin)
):
    return await get_all_user_chats(user_id)


@admins_router.get(
    "/admin/advert={advert_id}"
)
async def get_all_advert_info(
    advert_id: str, 
    current_admin: AdminLogin = Depends(get_current_admin)
):
    advert = await get_current_advert(advert_id)  
    responces = await get_responses_by_advert(advert_id)
    user_id = await get_user_id_by_advert(advert_id)
    if user_id == []:
        chats = "error in user_id"
    else:
        user_id = user_id[0][0]
        chats = await get_all_chat_rooms(user_id)
    return {
            "advert_info": advert,
            "responces": responces,
            "chats": chats 
    }


@admins_router.get(
    "/admin/chat={chat_room_id}"
)
async def get_chat_admin(
    chat_room_id: str,
    current_admin: AdminLogin = Depends(get_current_admin)
):
    return await get_all_chat_messages_admin(int(chat_room_id))

# @admins_router.get("/admin/stats")
# async def get_stats_router(current_admin: AdminLogin = Depends(
#                                         users_utils.get_current_admin)):
#     return await get_stats()