from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           WebAppInfo)

import config as config


async def generate_keyboard_webapp(advert_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text='Перейти на объявление',
                        web_app=WebAppInfo(
                            url=f'https://{config.APP_URL}/{advert_url}')
                    )]
                ]
            )