from database.models.models import TgUsers
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session, join
from typing import List


class BotDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    async def add_new_chat_room_id(self, chat_room_id: str, 
                                    tg_name: str) -> bool:
        

        request_check_tg_name = await self.db_session.execute(
            select(
                TgUsers.tg_name
            ).where(
                TgUsers.tg_name==tg_name
            )
        )
        check_tg_name = request_check_tg_name.all()

        if check_tg_name == []: return False


        request_set_chat_room_id = update(TgUsers).where(
                                        TgUsers.tg_name==tg_name)
        request_set_chat_room_id = request_set_chat_room_id.values(
                                        chat_room_id=str(chat_room_id))
        request_set_chat_room_id.execution_options(
                                        synchronize_session="fetch")
        await self.db_session.execute(request_set_chat_room_id)

        return True


    async def get_chat_id(self, user_id: str) -> str:
        request_chat_room_id = await self.db_session.execute(
            select(
                TgUsers.chat_room_id
            ).where(
                TgUsers.user_id==user_id
            )
        )
        
        res = request_chat_room_id.all()
        if res == []: return "no chat"
        return res[0][0]