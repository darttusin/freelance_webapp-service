from typing import List

import config as config
from database.dals.bot_dal import BotDAL


async def add_new_chat_room_id(chat_room_id: str, 
                                tg_name: str) -> bool:

    async with config.async_session() as session:
        async with session.begin():
            bot_dal = BotDAL(session)
            return await bot_dal.add_new_chat_room_id(
                                                chat_room_id, 
                                                tg_name
                                                )       


async def get_chat_id(user_id: str) -> bool:

    async with config.async_session() as session:
        async with session.begin():
            bot_dal = BotDAL(session)
            return await bot_dal.get_chat_id(user_id)