from typing import List

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session, join

from app.database.db import async_session
from app.database.models.models import (
    Adverts, 
    Filters, 
    Responses, 
    Statuses,
    Users
)
from app.utils.db_utils import (
    add_to_list, 
    add_to_list_adverts
)


async def add_new_advert(
    user_id: str,
    advert_id: str,
    text: str, 
    title: str, 
    category: str, 
    city: str, 
    price: int,
    filter_id: str
) -> str:
    async with async_session() as session:
        async with session.begin():
            request_add_advert = Adverts(
                user_id=user_id,
                advert_id=advert_id,
                advert_text=text,
                advert_title=title,
                advert_status='1',
                advert_city=city,
                advert_price=price,
                for_delete=False
            )
            
            session.add(request_add_advert)
            await session.flush()

            request_add_filter = Filters(
                filter_id=filter_id,
                advert_id=advert_id,
                parameter_id='category',
                value=category,
                for_delete=False
            )

            session.add(request_add_filter)
            await session.flush()

            return advert_id


async def check_advert_id(
    advert_id: str
) -> bool:
    async with async_session() as session:
        async with session.begin():
            request_advert_id = await session.execute(
                select(
                    Adverts.advert_id
                ).where(
                    Adverts.advert_id == advert_id,
                    Adverts.for_delete == False
                )
            )
            advert_id_db = request_advert_id.all()
            if advert_id_db == []: return True
            return False  


async def get_adverts(
    user_id: str, 
    city: str, 
    category: str
) -> List:
    async with async_session() as session:
        async with session.begin():
            if city == "None" and category == "None":
                request_adverts = await session.execute(
                    select(
                        Adverts.advert_id,
                        Adverts.advert_title,
                        Adverts.advert_city,
                        Adverts.advert_text,
                        Adverts.advert_price,
                        Filters.value,
                        Users.user_img_url
                    ).select_from(
                        Filters, 
                        Users,
                        Adverts
                    ).where(
                        Adverts.advert_status=='1',
                        Adverts.for_delete==False,
                        Filters.advert_id==Adverts.advert_id,
                        Users.user_id==Adverts.user_id,
                        Adverts.user_id!=user_id
                    )
                )
            elif city == "None" and category != "None":
                request_adverts = await session.execute(
                    select(
                        Adverts.advert_id,
                        Adverts.advert_title,
                        Adverts.advert_city,
                        Adverts.advert_text,
                        Adverts.advert_price,
                        Filters.value,
                        Users.user_img_url
                    ).select_from(
                        Filters, 
                        Users,
                        Adverts
                    ).where(
                        Adverts.advert_status=='1',
                        Adverts.for_delete==False,
                        Filters.advert_id==Adverts.advert_id,
                        Filters.value==category,
                        Users.user_id==Adverts.user_id,
                        Adverts.user_id!=user_id
                    )
                )    
            elif city != "None" and category == "None":
                request_adverts = await session.execute(
                    select(
                        Adverts.advert_id,
                        Adverts.advert_title,
                        Adverts.advert_city,
                        Adverts.advert_text,
                        Adverts.advert_price,
                        Filters.value,
                        Users.user_img_url
                    ).select_from(
                        Filters,
                        Users,
                        Adverts
                    ).where(
                        Adverts.advert_status=='1',
                        Adverts.for_delete==False,
                        Filters.advert_id==Adverts.advert_id,
                        Adverts.advert_city==city,
                        Users.user_id==Adverts.user_id,
                        Adverts.user_id!=user_id
                    )
                )
            else:
                request_adverts = await session.execute(
                    select(
                        Adverts.advert_id,
                        Adverts.advert_title,
                        Adverts.advert_city,
                        Adverts.advert_text,
                        Adverts.advert_price,
                        Filters.value,
                        Users.user_img_url
                    ).select_from(
                        Filters,
                        Users,
                        Adverts
                    ).where(
                        Adverts.advert_status=='1',
                        Adverts.for_delete==False,
                        Filters.advert_id==Adverts.advert_id,
                        Adverts.advert_city==city,
                        Filters.value==category,
                        Users.user_id==Adverts.user_id,
                        Adverts.user_id!=user_id
                    )
                )

            adverts = []
            for row in request_adverts:
                data = row._asdict()
                request_status = await session.execute(
                    select(
                        Responses.advert_id
                    ).where(
                        Responses.advert_id==data["advert_id"]
                    )
                )
                status = request_status.all()
                data["response"] = False if status == [] else True
                adverts.append(data)
            return adverts


async def get_user_adverts(user_id: str) -> List:
    async with async_session() as session:
        async with session.begin():
            request_adverts = await session.execute(
                select(
                    Adverts.advert_id,
                    Adverts.advert_title,
                    Adverts.advert_city,
                    Adverts.advert_text,
                    Adverts.advert_price,
                    Filters.value,
                    Statuses.description.label("advert_status")
                ).select_from(
                    Filters, 
                    Statuses,
                    Adverts
                ).where(
                    Adverts.user_id==user_id,
                    Filters.advert_id==Adverts.advert_id,
                    Statuses.status_id==Adverts.advert_status
                )
            )

            request_user_id = await session.execute(
                select(
                    Adverts.advert_id,
                    Responses.user_id
                ).join(
                    Adverts,
                    Adverts.advert_status==Responses.response_status
                ).where(
                    Adverts.user_id==user_id,
                    Adverts.advert_status=='4'
                )
            )

            return await add_to_list_adverts(
                request_adverts, 
                request_user_id
            )


async def get_current_advert(
    advert_id: str
) -> List:
    async with async_session() as session:
        async with session.begin():
            request_advert = await session.execute(
                select(
                    Adverts.advert_id,
                    Adverts.advert_title,
                    Adverts.advert_city,
                    Adverts.advert_text,
                    Adverts.advert_price,
                    Filters.value,
                    Statuses.description
                ).select_from(
                    Filters, 
                    Statuses,
                    Adverts
                ).where(
                    Adverts.for_delete==False,
                    Adverts.advert_id==advert_id,
                    Filters.advert_id==Adverts.advert_id,
                    Statuses.status_id==Adverts.advert_status
                )
            )

            return await add_to_list(request_advert)


async def check_user_advert(
    user_id: str, 
    advert_id: str
) -> bool:
    async with async_session() as session:
        async with session.begin():
            request_user_id = await session.execute(
                select(
                    Adverts.user_id
                ).where(
                    Adverts.advert_id==advert_id,
                    Adverts.for_delete==False
                )
            )
            user_id_db = request_user_id.all()
            if user_id_db == []:
                return False
            if user_id_db[0][0] == user_id: return True
            return False

async def delete_advert(
    advert_id: str
) -> str:
    async with async_session() as session:
        async with session.begin():
            request_adverts = \
                update(
                    Adverts
                ).where(
                    Adverts.advert_id==advert_id
                )
            request_adverts = request_adverts.values(for_delete=True)
            request_adverts.execution_options(
                synchronize_session="fetch"
            )
            await session.execute(request_adverts)

            request_filters = \
                update(
                    Filters
                ).where(
                    Filters.advert_id==advert_id
                )
            request_filters = request_filters.values(for_delete=True)
            request_filters.execution_options(
                synchronize_session="fetch"
            )
            await session.execute(request_filters)

            request_responses = \
                update(
                    Responses
                ).where(
                    Responses.advert_id==advert_id
                )
            request_responses = request_responses.values(
                for_delete=True
            )
            request_responses.execution_options(
                ynchronize_session="fetch"
            )
            await session.execute(request_responses)

            return "successful delete advert and all responses"+\
                f" - {advert_id}"


async def update_advert(
    user_id: str, 
    advert_id: str,
    advert_text: str, 
    advert_title: str, 
    category: str, 
    advert_city: str, 
    advert_price: int
) -> str:
    async with async_session() as session:
        async with session.begin():
            request_advert_update = \
                update(
                    Adverts
                ).where(
                    Adverts.advert_id==advert_id,
                    Adverts.user_id==user_id,
                    Adverts.for_delete==False
                )

            request_advert_update = request_advert_update.values(
                advert_text=advert_text,
                advert_title=advert_title,
                advert_price=advert_price,
                advert_city=advert_city
            )
            request_advert_update.execution_options(synchronize_session="fetch")
            await session.execute(request_advert_update)

            request_filters = \
                update(
                    Filters
                ).where(
                    Filters.advert_id==advert_id
                )
            request_filters = request_filters.values(value=category)
            request_filters.execution_options(
                synchronize_session="fetch"
            )
            await session.execute(request_filters)

            return f"successful update advert - {advert_id}"


async def get_user_id_by_advert(
    advert_id: str
) -> str:
    async with async_session() as session:
        async with session.begin():
            request_user_id = await session.execute(
                select(
                    Adverts.user_id
                ).where(
                    Adverts.advert_id==advert_id
                )
            )
            return request_user_id.all()