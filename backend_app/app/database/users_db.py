from typing import List

from sqlalchemy import delete, func, or_, select, update
from sqlalchemy.orm import Session

from app.database.db import async_session

from app.database.models.models import (
    Adverts, 
    Filters, 
    Responses, 
    Reviews,
    Users, 
    UserStats, 
    ChatRooms, 
    TgUsers
)

from app.utils.db_utils import (
    add_to_list, 
    add_to_dict_user,
    add_to_dict_user_info,
    add_to_dict_user_info_for_admin
)


async def add_new_user(
    user_id: str, 
    name: str, 
    email: str, 
    password: str, 
    tg_name: str
) -> None:
    async with async_session() as session:
        async with session.begin():
            new_user = Users(
                user_id=user_id,
                user_name=name,
                user_email=email,
                user_password=password
            )
            session.add(new_user)
            await session.flush()

            new_tg_user = TgUsers(
                user_id=user_id,
                chat_room_id="",
                tg_name=tg_name
            )
            session.add(new_tg_user)
            await session.flush()

            user_stats = UserStats(
                user_id=user_id,
                count_views=0,
                rating=0,
                count_reviews=0,
                count_jobs=0
            )
            session.add(user_stats)
            await session.flush()


async def check_user_by_email(
    email: str
) -> bool:
    async with async_session() as session:
        async with session.begin():
            request_user_id = await session.execute(
                select(
                    Users.user_id
                ).where(
                    Users.user_email==email
                )
            )
            user_id = request_user_id.all()
            if user_id != []: return True
            return False


async def get_user_by_email(
    email: str
) -> dict | bool:
    async with async_session() as session:
        async with session.begin():
            request_user = await session.execute(
                select(
                    Users.user_id,
                    Users.user_email,
                    Users.user_name, 
                    Users.user_password,
                    Users.user_img_url,
                    Users.user_description
                ).where(
                    Users.user_email==email
                )
            )
            user = request_user.all()
            if user == []: return False
            return await add_to_dict_user(user)  


async def check_user_id(
    user_id: str
) -> bool:
    async with async_session() as session:
        async with session.begin():
            request_user_id = await session.execute(
                select(
                    Users.user_id
                ).where(
                    Users.user_id == user_id
                )
            )
            if request_user_id.all() == []: return True
            return False


async def get_user_name(
    user_id: str
) -> str:
    async with async_session() as session:
        async with session.begin():
            request_user_name = await session.execute(
                select(
                    Users.user_name
                ).where(
                    Users.user_id==user_id
                )
            )
            user_name = request_user_name.all()
            if user_name == []: return "incorrect user_id"
            return user_name[0][0]


async def update_profile_info(
    user_id: str, 
    name: str, 
    img_url: str, 
    description: str
) -> str:
    async with async_session() as session:
        async with session.begin():
            if await check_user_id(user_id): 
                return "inccorect user_id"

            request_update_info = \
                update(
                    Users
                ).where(
                    Users.user_id==user_id
                )
            request_update_info = request_update_info.values(
                user_name=name,
                user_img_url=img_url,
                user_description=description
            )
            request_update_info.execution_options(
                synchronize_session="fetch"
            )
            await session.execute(request_update_info)
            
            return "successful changed" 


async def get_user_info(
    user_id: str
) -> dict:
    async with async_session() as session:
        async with session.begin():
            user_data = await session.execute(
                select(
                    Users.user_name,
                    Users.user_description,
                    Users.user_img_url
                )
                .where(
                    Users.user_id==user_id
                )
            )
            return await add_to_dict_user_info(
                user_data.all()
            ) 


async def get_performers(
    raiting_filter: float, 
    count_reviews_filter: int,
    count_jobs_filter: int,
    user_id: str
) -> List:
    async with async_session() as session:
        async with session.begin():
            stats = await session.execute(
                select(
                    UserStats.count_reviews,
                    UserStats.rating,
                    UserStats.user_id,
                    UserStats.count_jobs
                ).where(
                    UserStats.user_id!=user_id
                )
            )

            stats = stats.all()
            raiting = {}
            performers = {}
            performer_num = 1

            for user in stats:
                count = user[0]
                avg = user[1]
                user_id = user[2]
                count_jobs = user[3]

                if int(count_jobs) < int(count_jobs_filter): continue
                if int(avg) < int(raiting_filter): continue
                if int(count) < int(count_reviews_filter): continue

                raiting[str(performer_num)] = \
                    round(((count/(count+10))*avg +\
                        (10/(count+10)))*avg, 4)

                _user = {
                    "user_id" : user_id,
                    "user_info": await get_user_info(user_id),
                    "avg_estimation" : avg,
                    "count_estimation" : count,
                }

                performers[str(performer_num)] = _user
                performer_num += 1

            sorted_raiting = dict(
                sorted(
                    raiting.items(), 
                    key=lambda item: item[1], reverse=True
                )
            )
            sorted_performers = []
            for num in sorted_raiting:
                sorted_performers.append(performers[num])
            
            return sorted_performers
        

async def finish_work(
    advert_id: str
) -> str:
    async with async_session() as session:
        async with session.begin():
            update_filters = \
                update(
                    Filters
                ).where(
                    Filters.advert_id==advert_id
                )
            update_filters = update_filters.values(for_delete=True)
            update_filters.execution_options(
                synchronize_session="fetch"
            )
            await session.execute(update_filters)

            update_adverts = \
                update(
                    Adverts
                ).where(
                    Adverts.advert_id==advert_id
                )
            update_adverts = update_adverts.values(for_delete=True)
            update_adverts = update_adverts.values(advert_status="7")
            update_adverts.execution_options(
                synchronize_session="fetch"
            )
            await session.execute(update_adverts)

            update_responses = \
                update(
                    Responses
                ).where(
                    Responses.advert_id==advert_id
                )
            update_responses = update_responses.values(for_delete=True)
            update_responses = update_responses.values(response_status="7")
            update_responses.execution_options(
                synchronize_session="fetch"
            )
            await session.execute(update_responses)

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

            return "successful finish work"


async def get_all_users() -> List:
    async with async_session() as session:
        async with session.begin():
            request_info = await session.execute(
                select(
                    Users.user_id,
                    Users.user_name,
                    Users.user_email,
                    Users.user_img_url
                )
            )

            return await add_to_list(request_info)


async def add_view(
    user_id: str
) -> List:
    async with async_session() as session:
        async with session.begin():
            request_count_views = await session.execute(
                select(
                    UserStats.count_views
                ).where(
                    UserStats.user_id==user_id
                )
            )

            count = request_count_views.all()[0][0] + 1

            update_views = \
                update(
                    UserStats
                ).where(
                    UserStats.user_id==user_id
                )
            update_views = update_views.values(
                count_views=count
            )
            update_views.execution_options(
                synchronize_session="fetch"
            )
            await session.execute(update_views)


async def get_stats(
    user_id: str
) -> List:
    async with async_session() as session:
        async with session.begin():
            return_data = {}

            user_info = await session.execute(
                select(
                    Users.user_name,
                    Users.user_img_url,
                    Users.user_description,
                    Users.user_email,
                    Users.user_id
                ).where(
                    Users.user_id==user_id
                )
            )

            return_data["user_info"] = await add_to_list(user_info)

            adverts = await session.execute(
                select(
                    Adverts.advert_id,
                    Adverts.advert_title,
                    Adverts.advert_status,
                    Adverts.advert_text,
                    Adverts.advert_price
                ).where(
                    Adverts.user_id==user_id,
                    Adverts.for_delete==False
                )
            )

            return_data["adverts"] = await add_to_list(adverts)
            return_data["count_adverts"] = len(return_data["adverts"])

            rating = await session.execute(
                select(
                    func.count(Reviews.estimation),
                    func.avg(Reviews.estimation)
                ).group_by(
                    Reviews.user_id
                ).having(
                    Reviews.user_id==user_id
                )
            )

            return_data["raiting"] = await add_to_list(rating)

            reviews = await session.execute(
                select(
                    Reviews.review_id,
                    Reviews.review_author_id,
                    Reviews.review_author_comment
                ).where(
                    Reviews.user_id==user_id
                )
            )

            return_data["reviews"] = await add_to_list(reviews)

            all_offers = await session.execute(
                select(
                    Adverts.advert_text
                ).select_from(
                    Responses, 
                    Filters,
                    Adverts
                ).where(
                    Responses.response_status=='6',
                    Responses.user_id==user_id,
                    Adverts.advert_id==Filters.advert_id,
                    Responses.for_delete==True
                ).group_by(
                    Adverts.advert_text
                )
            )

            all_offers = all_offers.all()
            return_data["count_all_offers"] = len(all_offers)

            all_finished_offers = await session.execute(
                select(
                    Adverts.advert_text
                ).select_from(
                    Responses, 
                    Filters,
                    Adverts
                ).where(
                    Responses.response_status=='5',
                    Responses.user_id==user_id,
                    Adverts.advert_id==Filters.advert_id,
                    Responses.for_delete==True
                ).group_by(
                    Adverts.advert_text
                )
            )
            all_finished_offers = all_finished_offers.all()
            return_data["count_all_finished_offers"] = \
                                                len(all_finished_offers)

            all_responses = await session.execute(
                select(
                    Adverts.advert_text
                ).select_from(
                    Responses, 
                    Filters,
                    Adverts
                ).where(
                    or_(Responses.response_status=='5',
                    Responses.response_status=="2"),
                    Responses.user_id==user_id,
                    Adverts.advert_id==Filters.advert_id,
                    Responses.for_delete==True
                ).group_by(
                    Adverts.advert_text
                )
            )
            all_responses = all_responses.all()
            return_data["count_all_responses"] = len(all_responses)

            views = await session.execute(
                select(
                    UserStats.count_views
                ).where(
                    UserStats.user_id==user_id
                )
            )
            views = views.all()
            if views == []: return_data["count_views"] = 0
            else: return_data["count_views"] = views[0][0]

            return return_data 


async def get_all_user_chats(
    user_id: str
) -> List:
    async with async_session() as session:
        async with session.begin():
            request_chats = await session.execute(
                select(
                    ChatRooms.chat_room_id,
                    ChatRooms.performer_id,
                    ChatRooms.customer_id,
                    Users.user_img_url,
                    Users.user_name
                ).join(
                    Users,
                    or_(ChatRooms.customer_id==Users.user_id,
                    ChatRooms.performer_id==Users.user_id)
                ).where(
                    Users.user_id==user_id
                )
            )

            return await add_to_list(request_chats)       