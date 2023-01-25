from typing import List

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.database.db import async_session
from app.database.users_db import check_user_id
from app.database.models.models import Reviews, Users, UserStats, Adverts

from app.utils.db_utils import add_to_list


async def check_user_id_in_reviews(
    user_id: str, 
    review_author_id: str,
    advert_id: str
) -> bool:
    async with async_session() as session:
        async with session.begin():
            request_user_id = await session.execute(
                select(
                    Reviews.review_author_id
                ).where(
                    Reviews.review_author_id==review_author_id,
                    Reviews.user_id==user_id,
                    Reviews.advert_id==advert_id
                )
            )
            user_id = request_user_id.all()
            if user_id != []: return True
            return False


async def add_review(
    review_id: str,
    user_id: str, 
    advert_id: str,
    review_author_id: str, 
    review_author_comment: str,
    estimation: int
) -> str:
    async with async_session() as session:
        async with session.begin():

            if await check_user_id(user_id):
                return "inccorrect user_id"
        
            if user_id == review_author_id:
                return "user can't add review for yourself"

            if await check_user_id_in_reviews(
                user_id, 
                review_author_id,
                advert_id
            ):
                return "user added review on this user"

            new_review = Reviews(
                review_id=review_id,
                advert_id=advert_id,
                user_id=user_id,
                review_author_comment=review_author_comment,
                review_author_id=review_author_id,
                estimation=estimation
            )
            session.add(new_review)
            await session.flush()

            request_stats = await session.execute(
                select(
                    UserStats.rating,
                    UserStats.count_reviews
                ).where(
                    UserStats.user_id==user_id
                )
            )
            res_stats = request_stats.all()[0]
            rating = res_stats[0]
            count = res_stats[1]

            new_rating = ((rating*count) + estimation) / (count+1)
            count+=1

            request = \
                update(
                    UserStats
                ).where(
                    UserStats.user_id==user_id
                )
            request = request.values(
                rating=new_rating,
                count_reviews=count
            )
            request.execution_options(synchronize_session="fetch")
            await session.execute(request)

            return "successful add review"


async def get_user_estimations(
    user_id: str
) -> List:
    async with async_session() as session:
        async with session.begin():
            request_estimations= await session.execute(
                select(
                    Reviews.review_id,
                    Reviews.review_author_comment,
                    Reviews.estimation,
                    Reviews.review_author_id,
                    Users.user_name,
                    Users.user_img_url,
                    Adverts.advert_id,
                    Adverts.advert_title
                ).join(
                    Adverts,
                    Reviews.advert_id==Adverts.advert_id
                ).join(
                    Users,
                    Reviews.review_author_id==Users.user_id
                ).where(
                    Reviews.user_id==user_id
                )
            )
            return await add_to_list(request_estimations)
            

async def get_current_review(
    review_id: str
) -> List:
    async with async_session() as session:
        async with session.begin():
            request_review = await session.execute(
                select(
                    Reviews.review_id,
                    Reviews.review_author_comment,
                    Reviews.estimation,
                    Reviews.review_author_id,
                    Users.user_name,
                    Users.user_img_url,
                    Adverts.advert_id,
                    Adverts.advert_title
                ).join(
                    Adverts,
                    Reviews.advert_id==Adverts.advert_id
                ).join(
                    Users,
                    Reviews.review_author_id==Users.user_id
                ).where(
                    Reviews.review_id==review_id
                )
            )

            return await add_to_list(request_review)


async def update_review(
    review_id: str, 
    new_review_text: str
) -> None:
    async with async_session() as session:
        async with session.begin():
            request = \
                update(
                    Reviews
                ).where(
                    Reviews.review_id==review_id
                )
            request.values(review_author_comment==new_review_text)
            request.execution_options(synchronize_session="fetch")
            await session.execute(request)
