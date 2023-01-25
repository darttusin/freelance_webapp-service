from app.schemas.users_schemas import (
    UserRegistration, 
    UserLogin, 
    ChangeInfo,
    PerformerInfo
)
from app.utils.users_utils import ( 
    get_password_hash, 
    generate_user_id,
    create_access_token
)
from app.utils.auth_utils import (
    authenticate_user, 
    get_current_user
)
import app.constants.constants as const

from app.database.reviews_db import get_user_estimations
from app.database.portfolios_db import get_portfolios
from app.database.admins_db import add_new_admin, get_admin_by_email
from app.database.users_db import (
    add_new_user, 
    check_user_by_email,
    get_user_by_email, 
    get_user_name, 
    update_profile_info,
    get_performers,  
    get_user_info, 
    add_view
)

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi_pagination import Page, paginate
from fastapi.security import OAuth2PasswordRequestForm

from datetime import datetime, timedelta
from typing import List


users_router = APIRouter()


@users_router.post(
    "/registration"
)
async def registration(
    user: UserRegistration
) -> dict:
    if user.role == "user":
        if await check_user_by_email(user.email):
            return {
                "detail" : "Email already used"
            }

        user_id = await generate_user_id("id")

        await add_new_user(
            user_id, 
            user.username, 
            user.email, 
            get_password_hash(user.password),
            user.tg_name
        )
        return {
            "detail": user_id
        }

    elif user.role == "admin" or user.role == "manager":
        if type(
            await get_admin_by_email(
                user.email
        )) != bool:
            return {
                "detail" : "Email already used"
            }
            
        admin_id = await generate_user_id(user.role)
        await add_new_admin(
                user.email,
                user.username,
                user.password,
                user.role, 
                admin_id
                )
        return {
            'admin_id': admin_id
            }

    return {
        "detail": "error in data"
    }


@users_router.post(
    "/login"
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    user = await authenticate_user(
        form_data.username, 
        form_data.password
    )
    if not user:
        return {
            "detail": "Incorrect username or password"
        }
    access_token = await create_access_token(
        data={"sub": user['user_email']}
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }


@users_router.get(
    "/cabinet"
)
async def cabinet(
    current_user: UserLogin = Depends(get_current_user)
) -> dict:
    estimations = await get_user_estimations(
        current_user["user_id"]
    )

    count = 0
    sum_estimations = 0

    for estimation in estimations:
        count += 1
        sum_estimations += estimation["estimation"]

    avg = 0 if count == 0 else sum_estimations/count

    return {
        "user_id": current_user["user_id"],
        "user_name": current_user["user_name"],
        "user_img_url" : current_user['user_img_url'],
        "user_description" : current_user['user_description'],
        "user_estimations": estimations,
        "user_portfolios": await get_portfolios(
            current_user["user_id"]
        ),
        "avg_estimation": avg,
        "count_estimations": count
    }


@users_router.get(
    "/profile/{user_id}"
)
async def profile_router(
    user_id: str, 
    current_user: UserLogin = Depends(get_current_user)
) -> dict:

    if user_id == current_user["user_id"]: 
        return RedirectResponse(
            "/cabinet", 
            status_code=302
        )

    user_name = await get_user_name(user_id)
    if user_name == "incorrect user_id": 
        return {
            "detail": "incorrect user_id"
        }
    
    user_info = await get_user_info(user_id)
    estimations = await get_user_estimations(user_id)

    count = 0
    sum_estimations = 0

    for estimation in estimations:
        count += 1
        sum_estimations += estimation["estimation"]

    avg = 0 if count == 0 else sum_estimations/count

    await add_view(user_id)

    return {
        "user_id": user_id,
        "user_name": user_name,
        "user_img_url" : user_info['user_img_url'],
        "user_description" : user_info['user_description'],
        "user_estimations": estimations,
        "user_portfolios": await get_portfolios(user_id),
        "avg_estimation": avg,
        "count_estimations": count
    }


@users_router.put(
    "/profile"
)
async def change_profile(
    changed_info: ChangeInfo,
    current_user: UserLogin = Depends(get_current_user)
) -> dict:
    return {
        "detail" : await update_profile_info(
            current_user['user_id'], 
            changed_info.user_name,
            changed_info.img_url, 
            changed_info.description
        )
    }


@users_router.get(
    "/performers/params={raiting}&{count_reviews}&{count_jobs}",
    response_model=Page[PerformerInfo]
)
async def performers(
    raiting: str,
    count_reviews: str, 
    count_jobs: str,
    current_user: UserLogin = Depends(get_current_user)
) -> List:
    
    return paginate(
        await get_performers(
            raiting,
            count_reviews,
            count_jobs,
            current_user["user_id"]
        )
    )
