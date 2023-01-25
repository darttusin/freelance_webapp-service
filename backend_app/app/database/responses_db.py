from app.database.adverts_db import (
    check_advert_id, 
    check_user_advert
)
from app.database.db import async_session
from app.database.models.models import (
    Adverts, 
    Filters, 
    Parameters,
    Responses, 
    Statuses, 
    Users,
    ChatRooms,
    Messages,
    Offers,
    UserStats
)

from app.utils.db_utils import add_to_list

from sqlalchemy import and_, delete, or_, select, update
from sqlalchemy.orm import Session, join

import aiohttp
from app.utils.bot_connection import BotConnection
import pytz
from typing import List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime



async def check_user_response(
    user_id: str, 
    advert_id: str
) -> bool:
    async with async_session() as session:
        async with session.begin():
            request = await session.execute(
                select(
                    Responses.response_text
                ).where(
                    Responses.advert_id==advert_id,
                    Responses.user_id==user_id,
                    Responses.for_delete==False
                )
            )
            result = request.all()
            if result == []: return False
            return True


async def add_new_response(
    response_id: str,
    user_id: str, 
    advert_id: str, 
    price: int, 
    response_text: str
) -> str:
    async with async_session() as session:
        async with session.begin():

            if await check_advert_id(advert_id): 
                return "incorrect advert_id"
            if await check_user_response(user_id, advert_id): 
                return "responce already added"
            if await check_user_advert(user_id, advert_id):
                return "user can't ad responce for his advert"

            request = Responses(
                        response_id=response_id,
                        user_id=user_id,
                        advert_id=advert_id,
                        response_text=response_text,
                        response_status="2",
                        response_price=price,
                        for_delete=False
                        )

            session.add(request)
            await session.flush()

            await create_chat(
                user_id, 
                advert_id, 
                session, 
                "Вам пришёл отклик на обьявление"
            )

            # request_user_id = await session.execute(
            #     select(
            #         Adverts.user_id,
            #         Adverts.advert_title
            #     ).where(
            #         Adverts.advert_id==advert_id
            #     )
            # )
            # advert_info = request_user_id.all()
            # if advert_info == []: return "successful ad responce"
            # else: 
            #     user_id = advert_info[0][0]
            #     advert_title = advert_info[0][1]

            # data = {
            #         "user_id" : user_id,
            #         "advert_title": advert_title,
            #         "advert_url": f"advert/{advert_id}",
            #         "response_text": response_text,
            #         "response_price": price
            #         }
            # bot_connection = BotConnection()
            # res = bot_connection.send_response(data)

            return "successful ad responce"


async def create_chat(
    user_id: str, 
    advert_id: str,
    session: AsyncSession,
    message_text: str
) -> None:
    request_customer_id = await session.execute(
        select(
            Adverts.user_id
        ).where(
            Adverts.advert_id==advert_id
        )
    )
    customer_id = request_customer_id.all()[0][0]
    performer_id = user_id

    new_chat_room = ChatRooms(
        advert_id=advert_id,
        customer_id=customer_id,
        performer_id=performer_id,
        last_message=message_text,
        chat_opened=False
    )   
    session.add(new_chat_room)
    await session.flush()

    request_chat_room_id = await session.execute(
        select(
            ChatRooms.chat_room_id
        ).where(
            ChatRooms.advert_id==advert_id,
            ChatRooms.customer_id==customer_id,
            ChatRooms.performer_id==performer_id
        )
    )
    chat_room_id = request_chat_room_id.all()[0][0]
    if message_text == "Вам пришёл отклик на обьявление":
        message_sender = performer_id
    else:
        message_sender = customer_id
    tz = pytz.timezone("Europe/Moscow") 
    message_time = datetime.now(tz)
    message_time = message_time.strftime(
	    "%m/%d/%Y, %H:%M:%S"
    )

    new_message = Messages(
        chat_room_id=chat_room_id,
        message_sender=message_sender,
        message_text=message_text,
        message_time=message_time
    )
    session.add(new_message)
    await session.flush()


async def get_my_responses(
    user_id: str
) -> List:
    async with async_session() as session:
        async with session.begin():
            request_responses = await session.execute(
                select(
                    Responses.advert_id,
                    Adverts.advert_title,
                    Adverts.advert_text,
                    Adverts.advert_price,
                    Adverts.advert_city,
                    Statuses.description.label("response_status")
                ).select_from(
                    Statuses, 
                    Responses,
                    Adverts,
                ).where(
                    Responses.response_status==Statuses.status_id,
                    Responses.advert_id==Adverts.advert_id,
                    Responses.user_id==user_id,
                    Responses.for_delete==False,
                    or_(Responses.response_status=='2',
                        Responses.response_status=='3',
                        Responses.response_status=='4'
                    )
                )
            ) 
            return await add_to_list(request_responses)

async def update_status_response(
    advert_id: str, 
    response_status_new: str,
    user_id: str
) -> bool:
    async with async_session() as session:
        async with session.begin():
            if await check_advert_id(advert_id):
                return True
            
            request_resp = \
                update(
                    Responses
                ).where(
                    Responses.advert_id==advert_id,
                    Responses.user_id==user_id
                )

            if response_status_new == '4':
                request_ads = \
                    update(
                        Adverts
                    ).where(
                        Adverts.advert_id==advert_id
                    )
                request_ads = request_ads.values(
                    advert_status=response_status_new
                )
                request_ads.execution_options(
                    synchronize_session="fetch"
                )
                await session.execute(request_ads)

            request_resp = request_resp.values(
                response_status=response_status_new
            )
            request_resp.execution_options(
                synchronize_session="fetch"
            )
            await session.execute(request_resp)
            return False


async def get_responses_by_advert(
    advert_id: str
) -> List:
    async with async_session() as session:
        async with session.begin():
            request_responses = await session.execute(
                select(
                    Responses.user_id,
                    Users.user_img_url,
                    Users.user_name,
                    Responses.response_text,
                    Responses.response_price,
                    Statuses.description.label("response_status")
                ).select_from(
                    Responses,
                    Users,
                    Statuses
                ).where(
                    Statuses.status_id==Responses.response_status,
                    Responses.user_id==Users.user_id,
                    Responses.advert_id==advert_id,
                    Responses.for_delete==False
                )
            )
            return await add_to_list(request_responses)


async def get_responses_by_advert_for_user(
    advert_id: str, 
    user_id: str
) -> List:
    async with async_session() as session:
        async with session.begin():
            request_responses = await session.execute(
                select(
                    Responses.user_id,
                    Users.user_img_url,
                    Users.user_name,
                    Responses.response_text,
                    Responses.response_price,
                    Statuses.description.label("response_status")
                ).select_from(
                    Responses,
                    Users,
                    Statuses
                ).where(
                    Statuses.status_id==Responses.response_status,
                    Responses.user_id==Users.user_id,
                    and_(Responses.advert_id==advert_id,
                    Responses.user_id==user_id,
                    Responses.for_delete==False)
                )
            )
            return await add_to_list(request_responses)    


async def delete_response(
    advert_id: str, 
    user_id: str
) -> str:
    async with async_session() as session:
        async with session.begin():
            request_responses = \
                update(
                    Responses
                ).where(
                    Responses.advert_id==advert_id,
                    Responses.user_id==user_id,
                    Responses.advert_id==advert_id
                )
            request_responses = request_responses.values(
                for_delete=True
            )
            request_responses.execution_options(
                synchronize_session="fetch"
            )
            await session.execute(request_responses)

            return f"delete response for {advert_id}"+\
                f" by user {user_id}"


async def add_offer_job(
    user_id: str, 
    advert_id: str
) -> str:
    async with async_session() as session:
        async with session.begin():

            request = Offers(
                user_id=user_id,
                advert_id=advert_id,
                offer_status="5",
                for_delete=False
            )
            
            session.add(request)
            await session.flush()
            return "successful offer a job"

                                        
async def all_offers(
    user_id: str
) -> List:
    async with async_session() as session:
        async with session.begin():
            request = await session.execute(
                select(
                    Offers.advert_id,
                    Adverts.advert_title,
                    Adverts.advert_text,
                    Adverts.advert_city,
                    Adverts.advert_price,
                    Filters.value,
                    Statuses.description.label("offer_status")
                ).select_from(
                    Offers, 
                    Filters,
                    Adverts,
                    Statuses
                ).where(
                    Offers.offer_status=="5",
                    Offers.offer_status==Statuses.status_id,
                    Offers.user_id==user_id,
                    Offers.advert_id==Adverts.advert_id,
                    Adverts.advert_id==Filters.advert_id,
                    Adverts.for_delete==False,
                    Offers.for_delete==False
                ).group_by(
                    Offers.advert_id,
                    Adverts.advert_title,
                    Adverts.advert_text,
                    Adverts.advert_city,
                    Adverts.advert_price,
                    Filters.value,
                    Statuses.description.label("offer_status")
                )
            )
            return await add_to_list(request)


async def update_status_offer(
    advert_id: str, 
    offer_status_new: str,
    user_id: str
) -> bool:
    async with async_session() as session:
        async with session.begin():
            request_offer = \
                update(
                    Offers
                ).where(
                    Offers.advert_id==advert_id,
                    Offers.user_id==user_id
                )

            if offer_status_new == '4':
                request_ads = \
                    update(
                        Adverts
                    ).where(
                        Adverts.advert_id==advert_id
                    )
                request_ads = request_ads.values(
                    advert_status=offer_status_new
                )
                request_ads.execution_options(
                    synchronize_session="fetch"
                )
                await session.execute(request_ads)
            
            if offer_status_new == "7":
                request_ads = \
                    update(
                        Adverts
                    ).where(
                        Adverts.advert_id==advert_id
                    )
                request_ads = request_ads.values(
                    for_delete=True
                )
                request_ads.execution_options(
                    synchronize_session="fetch"
                )
                await session.execute(request_ads)

                request_offer = request_offer.values(
                    offer_status=offer_status_new,
                    for_delete=True
                )
                request_offer.execution_options(
                    synchronize_session="fetch"
                )
                await session.execute(request_offer)

                request_stats = await session.execute(
                    select(
                        UserStats.count_jobs,
                        UserStats.user_id
                    ).select_from(
                        Responses,
                        UserStats,
                        Adverts
                    ).where(
                        UserStats.user_id==Responses.user_id,
                        Adverts.advert_id==Responses.advert_id
                    )
                )
                result = request_stats.all()[0]
                count_jobs = result[0] + 1
                user_id = result[1]

                update_stats = \
                    update(
                        UserStats
                    ).where(
                        UserStats.user_id==user_id
                    )
                update_stats = update_stats.values(count_jobs=count_jobs)
                update_stats.execution_options(synchronize_session="fetch")
                await session.execute(update_stats)
            
            request_offer = request_offer.values(
                    offer_status=offer_status_new
                )
            request_offer.execution_options(
                synchronize_session="fetch"
            )
            await session.execute(request_offer)

            return False
