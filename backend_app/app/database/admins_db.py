from typing import List

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session, join

from app.database.db import async_session
from app.database.models.models import Admins
from app.utils.db_utils import add_to_dict_admin
from app.utils.users_utils import get_password_hash


async def add_new_admin(
    email: str,
    username: str,
    password: str,
    role: str, 
    admin_id: str
) -> None:
    async with async_session() as session:
        async with session.begin():
            request = Admins(
                admin_id=admin_id,
                admin_email=email,
                admin_login=username,
                admin_password=get_password_hash(password),
                admin_role=role
            )
            session.add(request)
            await session.flush()


async def get_admin_by_email(
    email: str
) -> List | bool:
    async with async_session() as session:
        async with session.begin():
            request = await session.execute(
                select(
                    Admins.admin_id,
                    Admins.admin_email,
                    Admins.admin_login,
                    Admins.admin_password,
                    Admins.admin_role
                ).where(
                    Admins.admin_email==email
                )
            )
            result = request.all()
            if result == []: return False
            return await add_to_dict_admin(result) 
