import aiohttp_cors
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.webhook.aiohttp_server import (SimpleRequestHandler,
                                            setup_application)
from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_request import Request

from aiohttp_cors import setup as cors_setup, ResourceOptions

import api as api
import config as config
from handlers import main_router


async def on_startup(bot: Bot, base_url: str):
    await bot.delete_webhook()
    await bot.set_webhook(f"{base_url}/webhook")


async def on_shutdown(bot: Bot):
    await bot.delete_webhook()


@web.middleware
async def cors_middleware(request, handler):
    response = await handler(request)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

async def main():
    bot = Bot(token=config.BOT_TOKEN)

    dispatcher = Dispatcher()
    dispatcher['base_url'] = f'https://{config.APP_URL}/bot' 
    dispatcher.include_router(main_router)
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)

    app = Application()
    app['bot'] = bot
    app['base_url'] = f'https://{config.APP_URL}/bot'
    app.router.add_post("/sendResponse", api.send_response)
    app.router.add_get("/hi", api.hello_world)

    cors = aiohttp_cors.setup(app, defaults={
        "*": ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*"
        )
    })

    for route in list(app.router.routes()):
        cors.add(route)

    SimpleRequestHandler(
                    dispatcher=dispatcher, 
                    bot=bot
                    ).register(app, path="/webhook")


    setup_application(app, dispatcher, bot=bot)
    return app
