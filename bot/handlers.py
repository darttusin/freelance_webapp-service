from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

import config as config
import const_answers as answer
from database.bot_db import add_new_chat_room_id

main_router = Router()


@main_router.message(Command(commands=["start"]))
async def command_start_bot(message: Message, 
                            command: CommandObject, bot: Bot):

    if await add_new_chat_room_id(message.chat.id, 
                                message.from_user.username):
        await message.answer(answer.POSITIVE_ANSWER)
    else:
        await message.answer(answer.NEGATIVE_ANSWER)
    
