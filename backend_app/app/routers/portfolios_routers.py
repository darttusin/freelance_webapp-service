from app.schemas.portfolios_schemas import (
    NewPortfolio, 
    UpdatePortfolio, 
    PortfolioInfo
)
from app.schemas.users_schemas import UserLogin
from app.utils.auth_utils import get_current_user
from app.utils.users_utils import generate_post_id

from app.database.portfolios_db import (
    add_new_portfolio, 
    update_portfolio,
    get_current_portfolio, 
    get_portfolios,
    delete_portfolio, 
    get_user_by_portfolio_id
)
from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Page


portfolios_router = APIRouter()


@portfolios_router.post(
    "/portfolio"
)
async def add_new_portfolio_router(
    portfolio_info: NewPortfolio,
    current_user: UserLogin = Depends(get_current_user)
) -> dict:
    portfolio_id = await add_new_portfolio(
        current_user["user_id"],
        await generate_post_id("pr"),
        portfolio_info.portfolio_title,
        portfolio_info.portfolio_description,
        portfolio_info.portfolio_img_url
    )

    return {
        "detail" : "successful add portfolio", 
        "portfolio_id" : portfolio_id
    }


@portfolios_router.put(
    "/portfolio"
)
async def update_portfolio_router(
    portfolio_info: UpdatePortfolio,
    current_user: UserLogin = Depends(get_current_user)
) -> dict:

    return {
        "detail" : await update_portfolio(
            portfolio_info.portfolio_id,
            portfolio_info.portfolio_title,
            portfolio_info.portfolio_description,
            portfolio_info.portfolio_img_url
            )
        }


@portfolios_router.delete(
    "/portfolio/{portfolio_id}"
)
async def delete_portfolio_router(
    portfolio_id: str, 
    current_user: UserLogin = Depends(get_current_user)
) -> dict:

    portfolio_user_id = await get_user_by_portfolio_id(portfolio_id)

    if current_user["user_id"] != portfolio_user_id:
        return {
            "detail" : "not user portfolio"
        }

    return {
        "detail" : await delete_portfolio(portfolio_id)
    }


@portfolios_router.get(
    "/portfolio/{portfolio_id}"
)
async def get_portfolio(
    portfolio_id: str, 
    current_user: UserLogin = Depends(get_current_user)
) -> dict:

    res = await get_current_portfolio(portfolio_id)
    res = res[0] if res != [] else res
    return res


@portfolios_router.get(
    "/portfolios/{user_id}", 
    response_model=Page[PortfolioInfo]
)
async def get_all_portfolios(
    user_id: str, 
    current_user: UserLogin = Depends(get_current_user)
) -> dict:
    return paginate(
        await get_portfolios(user_id)
    )
