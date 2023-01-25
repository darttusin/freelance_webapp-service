from app.database.models.models import Portfolios
from app.database.db import async_session

from app.utils.db_utils import add_to_list

from typing import List

from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session




async def add_new_portfolio(
    user_id: str, 
    portfolio_id: str, 
    portfolio_title: str, 
    portfolio_desc: str,
    portfolio_img_url: str
) -> str:
    async with async_session() as session:
        async with session.begin():
            request = Portfolios(
                user_id=user_id,
                portfolio_id=portfolio_id,
                portfolio_title=portfolio_title,
                portfolio_description=portfolio_desc,
                portfolio_img_url=portfolio_img_url,
                for_delete=False
            )

            session.add(request)
            await session.flush()
            return portfolio_id


async def update_portfolio(
    portfolio_id: str, 
    portfolio_title: str, 
    portfolio_desc: str,
    portfolio_img_url: str
) -> str:
    async with async_session() as session:
        async with session.begin():
            request = \
                update(
                    Portfolios
                ).where(
                    Portfolios.portfolio_id==portfolio_id
                )
            request = request.values(
                portfolio_title=portfolio_title,
                portfolio_description=portfolio_desc,
                portfolio_img_url=portfolio_img_url
            )
            request.execution_options(synchronize_session="fetch")
            await session.execute(request)

            return "successful update portfolio"


async def get_current_portfolio(
    portfolio_id: str
) -> List:
    async with async_session() as session:
        async with session.begin():
            request = await session.execute(
                select(
                    Portfolios.user_id,
                    Portfolios.portfolio_id,
                    Portfolios.portfolio_title,
                    Portfolios.portfolio_description,
                    Portfolios.portfolio_img_url   
                ).where(
                    Portfolios.portfolio_id==portfolio_id,
                    Portfolios.for_delete==False
                )
            )

            return await add_to_list(request)


async def get_portfolios(
    user_id: str
) -> List:
    async with async_session() as session:
        async with session.begin():
            request_portfolios = await session.execute(
                select(
                    Portfolios.portfolio_id,
                    Portfolios.portfolio_title,
                    Portfolios.portfolio_description,
                    Portfolios.portfolio_img_url   
                ).where(
                    Portfolios.user_id==user_id,
                    Portfolios.for_delete==False
                )
            )        
            return await add_to_list(request_portfolios)


async def delete_portfolio(
    portfolio_id: str
) -> str:
    async with async_session() as session:
        async with session.begin():
            request = \
                update(
                    Portfolios
                ).where(
                    Portfolios.portfolio_id==portfolio_id
                )
            request = request.values(for_delete=True)
            request.execution_options(synchronize_session="fetch")

            await session.execute(request)
            return f"successful delete portfolio - {portfolio_id}"

        
async def get_user_by_portfolio_id(
    portfolio_id: str
) -> str:
    async with async_session() as session:
        async with session.begin():
            request = await session.execute(
                select(
                    Portfolios.user_id
                ).where(
                    Portfolios.portfolio_id==portfolio_id,
                    Portfolios.for_delete==False
                )
            )
            res = request.all()
            if res == []: return 'error in portfolio_id'
            return res[0][0]
