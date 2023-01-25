from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate

from app.database.users_db import finish_work
from app.database.adverts_db import (
    add_new_advert, 
    check_user_advert,
    get_adverts, 
    get_current_advert, 
    delete_advert,
    update_advert, 
    get_user_adverts
)
from app.database.responses_db import (
    get_responses_by_advert, 
    get_responses_by_advert_for_user
)
from app.database.chats_db import (
    get_chats_by_advert,
    get_chats_by_advert_for_user
)

from app.schemas.users_schemas import UserLogin
from app.schemas.adverts_schemas import (
    NewAdvert, 
    AdvertUpdate, 
    AdvertInfo, 
    MyAdvertInfo
)

from app.utils.users_utils import generate_post_id
from app.utils.auth_utils import get_current_user


adverts_router = APIRouter()


@adverts_router.post("/advert")
async def add_new_advert_router(
    advert_info: NewAdvert, 
    current_user: UserLogin = Depends(get_current_user)
) -> dict:
    
    advert_id = await add_new_advert(
        current_user["user_id"],
        await generate_post_id("ad"),
        advert_info.advert_text,
        advert_info.advert_title,
        advert_info.advert_category,
        advert_info.advert_city,
        advert_info.advert_price,
        await generate_post_id("filt")
    )

    return {
        "detail" : "successful add new advert id", 
        "advert_id" : advert_id
    }


@adverts_router.get(
    "/adverts/params={category}&{city}", 
    response_model=Page[AdvertInfo]
)
async def all_adverts(
    city: str, 
    category: str,
    current_user: UserLogin = Depends(get_current_user)
) -> dict:
    return paginate(
        await get_adverts(
            city=city, 
            category=category, 
            user_id=current_user["user_id"]
        )
    )


@adverts_router.get(
    "/myAdverts"
)
async def my_adverts(
    current_user: UserLogin = Depends(get_current_user)
) -> dict:
    return await get_user_adverts(
        current_user["user_id"]
    )


@adverts_router.get("/advert/{advert_id}")
async def current_advert(
    advert_id: str, 
    current_user: UserLogin = Depends(get_current_user)
) -> dict:

    if await check_user_advert(
        current_user["user_id"], 
        advert_id
    ):
        responces = await get_responses_by_advert(advert_id)
        chats = await get_chats_by_advert(advert_id)
    else:
        responces = await get_responses_by_advert_for_user(
            advert_id, 
            current_user["user_id"]
        )
        chats = await get_chats_by_advert_for_user(
            advert_id,
            current_user["user_id"]
        )

    advert = await get_current_advert(advert_id)  
    advert = advert[0] if advert != [] else advert
    
    return {
        "advert" : advert,
        "responces" : responces,
        "chats" : chats
    }


@adverts_router.delete("/advert/{advert_id}")
async def delete_advert_router(
    advert_id: str, 
    current_user: UserLogin = Depends(get_current_user)
) -> dict:
    if not await check_user_advert(
        current_user["user_id"], 
        advert_id
    ):
        return {
            "detail" : "not user advert"
        }
    return {
        "detail" : await delete_advert(advert_id)
    }


@adverts_router.put("/advert/{advert_id}")
async def update_advert_router(
    advert_id: str, 
    advert_info: AdvertUpdate,
    current_user: UserLogin = Depends(get_current_user)
) -> dict:
    if not await check_user_advert(
        current_user["user_id"], 
        advert_id
    ):
        return {
            "detail" : "not user advert"
        }
    return {
        "detail" : await update_advert(
            current_user["user_id"],
            advert_id,
            advert_info.advert_text,
            advert_info.advert_title,
            advert_info.advert_category,
            advert_info.advert_city,
            advert_info.advert_price
            )
        }


@adverts_router.put(
    "/finishWork/{advert_id}"
)
async def performers(
    advert_id: str,
    current_user: UserLogin = Depends(get_current_user)
) -> dict:
    return {
        "detail" : await finish_work(advert_id)
    }
