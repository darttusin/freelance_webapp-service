from app.schemas.responses_schemas import (
    AddResponse, 
    UpdateStatus, 
    ResponseInfo, 
    OfferJob, 
    PortfolioInfo,
    UpdateStatusOffer
)
from app.schemas.users_schemas import UserLogin
from app.utils.users_utils import generate_post_id
from app.utils.auth_utils import get_current_user
from app.database.responses_db import (
    add_new_response, 
    add_offer_job,
    all_offers, 
    delete_response,
    get_my_responses,
    update_status_response,
    update_status_offer
)
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params, paginate

responses_router = APIRouter()


@responses_router.post(
    "/responce"
)
async def add_responce_router(
    response_info: AddResponse,
    current_user: UserLogin = Depends(get_current_user)
) -> dict:
    
    result = await add_new_response(
        await generate_post_id("resp"),
        current_user["user_id"],
        response_info.advert_id,
        response_info.price,
        response_info.responce_text
    )
    return {
        "detail" : result
    }


@responses_router.get(
    "/myResponces", 
    response_model=Page[ResponseInfo]
)
async def my_responces_router(
    current_user: UserLogin = Depends(get_current_user)
) -> dict:
    return paginate(
        await get_my_responses(
            current_user["user_id"]
        )
    )


@responses_router.put(
    "/statusResponce"
)
async def update_status_router(
    advert_info: UpdateStatus,
    current_user: UserLogin = Depends(get_current_user)
) -> dict:
    result = await update_status_response(
        advert_info.advert_id, 
        advert_info.response_status,
        advert_info.user_id
    )
    
    if result:
        return {
            "detail" : "incorrect advert_id"
        }
    return {
        "detail": f"Status updated for {advert_info.response_status}"
    }


@responses_router.delete(
    "/response/{advert_id}/{user_id}"
)
async def delete_response_by_advert_router(
    advert_id: str, 
    user_id: str,
    current_user: UserLogin = Depends(get_current_user)
) -> dict:
    return {
        "detail" : await delete_response(
            advert_id, 
            user_id
        )
    }


@responses_router.post(
    "/jobOffering"
)
async def offer_job_by_advert_router(
    job_info: OfferJob,
    current_user: UserLogin = Depends(get_current_user)
) -> dict:
    return {
        "detail" : await add_offer_job(
            job_info.user_id,
            job_info.advert_id
            )
        }


@responses_router.get(
    "/offers", 
    response_model=Page[PortfolioInfo]
)
async def all_users_offers_router(
    current_user: UserLogin = Depends(get_current_user)
) -> dict:
    return paginate(
        await all_offers(current_user['user_id'])
    )


@responses_router.put(
    "/statusOffer"
)
async def change_status_offer(
    offer_info: UpdateStatusOffer,
    current_user: UserLogin = Depends(get_current_user)
) -> str:
    result = await update_status_offer(
        offer_info.advert_id, 
        offer_info.offer_status,
        offer_info.user_id
    )

    if result:
        return {
            "detail" : "incorrect advert_id or user_id"
        }
    return {
        "detail": f"Status updated for {offer_info.offer_status}"
    }
