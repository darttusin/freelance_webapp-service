from typing import List

from sqlalchemy import select, update, delete, or_, and_
from sqlalchemy.orm import Session

from app.database.db import async_session
from app.database.models.models import (
    ChatRooms,
    Messages,
    Users,
    Adverts,
    Statuses,
    Responses
)

from app.utils.db_utils import (
    add_to_list, 
    add_to_list_messages,
    add_to_list_messages_2,  
    add_to_list_rooms, 
    add_to_list_chats
)




async def add_new_chat(
    advert_id: str, 
    customer_id: str, 
    performer_id: str
) -> int | str:
    async with async_session() as session:
        async with session.begin():
            request_check = await session.execute(
                select(
                    ChatRooms.chat_room_id
                ).where(
                   and_(
                    ChatRooms.advert_id==advert_id,
                    ChatRooms.performer_id==performer_id
                   )
                )
            )

            check = request_check.all()
            if check != []: return "chat already exists"

            new_chat_room = ChatRooms(
                advert_id=advert_id,
                customer_id=customer_id,
                performer_id=performer_id,
                last_message=""
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

            return request_chat_room_id.all()[0][0]


async def add_new_message(
    chat_room_id: int,
    message_sender: str,
    message_text: str,
    message_time: str
) -> None:
    async with async_session() as session:
        async with session.begin():
            new_message = Messages(
                chat_room_id=chat_room_id,
                message_sender=message_sender,
                message_text=message_text,
                message_time=message_time
            )
            session.add(new_message)
            await session.flush()

            update_last_message = \
                update(
                    ChatRooms
                ).where(
                    ChatRooms.chat_room_id==chat_room_id
                )

            update_last_message = update_last_message.values(
                last_message=message_text
            )
            update_last_message.execution_options(
                synchronize_session="fetch"
            )
            await session.execute(update_last_message)  


async def get_all_chat_messages(
    chat_room_id: str,
    message_sender: str
) -> List:
    async with async_session() as session:
        async with session.begin():
            chat_room_id = int(chat_room_id)

            request_messages = await session.execute(
                select(
                    Messages.message_id,
                    Messages.message_text,
                    Messages.message_time,
                    Users.user_name,
                    Users.user_id,
                    Users.user_img_url
                ).join(
                    Users,
                    Users.user_id==Messages.message_sender
                ).where(
                    Messages.chat_room_id==chat_room_id
                )
            )

            request_chat_data = await session.execute(
                select(
                    ChatRooms.advert_id,
                    Adverts.advert_title,
                    ChatRooms.chat_opened,
                    Statuses.description.label("response_status"),
                    Responses.response_text,
                    Responses.response_price
                ).select_from(
                    Adverts,
                    ChatRooms,
                    Statuses,
                    Responses
                ).where(
                    Adverts.advert_id==ChatRooms.advert_id,
                    ChatRooms.chat_room_id==chat_room_id,
                    Responses.advert_id==ChatRooms.advert_id,
                    Statuses.status_id==Responses.response_status
                )
            )

            request_id = await session.execute(
                select(
                    ChatRooms.customer_id,
                    ChatRooms.performer_id
                ).where(
                    ChatRooms.chat_room_id==chat_room_id
                )
            )

            twos_ids = request_id.all()[0]
            res_id = twos_ids[0] if twos_ids[0] != message_sender else twos_ids[1]

            request_name = await session.execute(
                select(
                    Users.user_name
                ).where(
                    Users.user_id==res_id
                )
            )

            name = request_name.all()[0][0]
            res_id = [res_id, name]

            messages = await add_to_list_messages_2(
                                                request_messages,
                                                request_chat_data,
                                                res_id)
            return messages


async def get_all_chat_rooms(
    user_id: str,
    role: str
) -> List:
    async with async_session() as session:
        async with session.begin():
            request_customer = await session.execute(
                select(
                    ChatRooms.chat_room_id,
                    ChatRooms.performer_id,
                    Users.user_img_url,
                    Users.user_name,
                    Users.user_id,
                    ChatRooms.last_message,
                    ChatRooms.chat_opened,
                    Adverts.advert_title
                ).join(
                    Users,
                    ChatRooms.performer_id==Users.user_id
                ).join(
                    Adverts,
                    ChatRooms.advert_id==Adverts.advert_id
                ).where(
                    ChatRooms.customer_id==user_id,
                    Adverts.advert_status=="4"
                )
            )

            request_performer = await session.execute(
                select(
                    ChatRooms.chat_room_id,
                    ChatRooms.customer_id,
                    Users.user_img_url,
                    Users.user_id,
                    Users.user_name,
                    ChatRooms.last_message,
                    ChatRooms.chat_opened,
                    Adverts.advert_title
                ).join(
                    Users,
                    ChatRooms.customer_id==Users.user_id
                ).join(
                    Adverts,
                    ChatRooms.advert_id==Adverts.advert_id
                ).where(
                    ChatRooms.performer_id==user_id,
                    Adverts.advert_status=="4"
                )
            )

            if role == "performer": return await add_to_list(
                request_performer
            )
            if role == "customer": return await add_to_list(
                request_customer
            ) 
            if role == "admin" : return await add_to_list_chats(
                request_customer, 
                request_performer
            )


async def get_all_chats_for_admins() -> List:

    async with async_session() as session:
        async with session.begin():
            request_customer = await session.execute(
                select(
                    ChatRooms.chat_room_id,
                    ChatRooms.customer_id,
                    ChatRooms.performer_id,
                    Users.user_img_url,
                    Users.user_name,
                    ChatRooms.chat_opened
                ).join(
                    Users,
                    ChatRooms.customer_id==Users.user_id
                )
            )

            request_performer = await session.execute(
                select(
                    ChatRooms.chat_room_id,
                    ChatRooms.customer_id,
                    ChatRooms.performer_id,
                    Users.user_img_url,
                    Users.user_name,
                    ChatRooms.chat_opened
                ).join(
                    Users,
                    ChatRooms.performer_id==Users.user_id
                )
            )

            return await add_to_list_chats(
                request_customer, 
                request_performer
            )   


async def get_all_chat_messages_admin(
    chat_room_id: int
) -> List:
    async with async_session() as session:
        async with session.begin():
            request_sender = await session.execute(
                select(
                    Messages.message_id,
                    Messages.message_text,
                    Messages.message_time,
                    Users.user_name,
                    Users.user_id,
                    Users.user_img_url
                ).join(
                    Users,
                    Users.user_id==Messages.message_sender
                ).where(
                    Messages.chat_room_id==chat_room_id
                )
            )

            request_chat_data = await session.execute(
                select(
                    ChatRooms.advert_id,
                    Adverts.advert_title,
                    Adverts.advert_price,
                    ChatRooms.chat_opened
                ).join(
                    Adverts,
                    Adverts.advert_id==ChatRooms.advert_id
                ).where(
                    ChatRooms.chat_room_id==chat_room_id
                )
            )

            messages = await add_to_list_messages(
                request_sender, 
                None,
                request_chat_data,
                "None"
            )
            return messages


async def open_chat(
    chat_room_id: int
) -> str:
    async with async_session() as session:
        async with session.begin():
            request_chat_check = await session.execute(
                select(
                    ChatRooms.chat_opened
                ).where(
                    ChatRooms.chat_room_id==chat_room_id
                )
            )
            flag = request_chat_check.all()
            if flag == []: 
                return "chat doesnot exists"
            else:
                if flag[0][0]:
                    return "chat already opened"

            request_chat = \
                update(
                    ChatRooms
                ).where(
                    ChatRooms.chat_room_id==chat_room_id
                )
            request_chat = request_chat.values(chat_opened=True)
            request_chat.execution_options(synchronize_session="fetch")
            await session.execute(request_chat) 

            return "chat opened" 


async def get_chats_by_advert(
    advert_id: str
) -> List:
    async with async_session() as session:
        async with session.begin():
            request_chats = await session.execute(
                select(
                    ChatRooms.chat_room_id,
                    ChatRooms.performer_id,
                    ChatRooms.chat_opened,
                    ChatRooms.last_message,
                    Users.user_img_url            
                ).join(
                    Users,
                    Users.user_id==ChatRooms.performer_id
                ).where(
                    ChatRooms.advert_id==advert_id
                )
            )

            return await add_to_list(request_chats)


async def get_chats_by_advert_for_user(
    advert_id: str,
    performer_id: str
) -> List:
    async with async_session() as session:
        async with session.begin():
            request_chats = await session.execute(
                select(
                    ChatRooms.chat_room_id,
                    ChatRooms.customer_id,
                    ChatRooms.chat_opened,
                    ChatRooms.last_message,
                    Users.user_img_url            
                ).join(
                    Users,
                    Users.user_id==ChatRooms.customer_id
                ).where(
                    and_(
                        ChatRooms.advert_id==advert_id,
                        ChatRooms.performer_id==performer_id
                    )
                )
            )

            return await add_to_list(request_chats)
            