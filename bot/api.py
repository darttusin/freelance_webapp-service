from database.bot_db import get_chat_id
from aiohttp.web_request import Request
import config as config
import keyboards as keyboards
from aiogram import Bot
from aiohttp.web_response import json_response


async def send_response(request: Request):
    data = await request.json()

    user_id = data.get("user_id")
    advert_url = data.get("advert_url")
    advert_title = data.get("advert_title")
    text = data.get("response_text")
    price = data.get("response_price")
    chat_id = await get_chat_id(user_id)
    
    if chat_id == 'no chat': return json_response("TgUser undefined")

    response_text = \
        f"Вам поступил отклик на обьявление {advert_title}!\n" +\
        f"Текст отправленный исполнителем:\n{text}\n" +\
        f"Цена предложенная исполнителем:\n{price}\n" +\
        "Для просмотра откликов на обьявление перейдите "+\
        "по кнопке снизу сообщения."


    bot: Bot = request.app['bot']
    await bot.send_message(int(chat_id), response_text, 
        reply_markup=await keyboards.generate_keyboard_webapp(
                                                        advert_url))

    return json_response("Response sended")


async def hello_world(request: Request):
    return json_response({'ok': True, 'text': 'Hello World'})
