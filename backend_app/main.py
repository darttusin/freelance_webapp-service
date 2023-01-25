from fastapi import (FastAPI, WebSocket, WebSocketDisconnect)
from fastapi.middleware.cors import CORSMiddleware
from app.routers import *
from app.database.db import db_create
from app.utils.connection_manager import ConnectionManager
from app.database.chats_db import add_new_message
from fastapi_pagination import add_pagination
from datetime import datetime, timedelta
from fastapi.responses import HTMLResponse
import json
import pytz


app = FastAPI()
origins = [
    "http://localhost", 
    "http://localhost:8080", 
    "http://localhost:3000", 
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
add_pagination(app)
app.include_router(users_router)
app.include_router(adverts_router)
app.include_router(responses_router)
app.include_router(reviews_router)
app.include_router(portfolios_router)
app.include_router(chat_routers)
app.include_router(checks_routers)
app.include_router(admins_router)


@app.on_event("startup")
async def startup():
    db_create()


manager = ConnectionManager()


@app.websocket("/ws/{chat_room_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    chat_room_id: str
) -> None:
    await manager.connect(
        websocket, 
        chat_room_id
    )

    try:
        while True:
            data = await websocket.receive_text()
            data = data.replace('"', "\"")
            data_json = json.loads(data)

            room_members = (
                manager.get_members(chat_room_id)
                if manager.get_members(chat_room_id) is not None
                else []
            )
            if websocket not in room_members:
                await manager.connect(websocket, chat_room_id)

            tz = pytz.timezone("Europe/Moscow")
            now = datetime.now(tz)

            await add_new_message(
                int(chat_room_id), 
                data_json["user_id"],
                data_json["message_text"],
                now.strftime("%m/%d/%Y, %H:%M:%S")
            )

            await manager.send_private_message(
                json.dumps(data_json),
                chat_room_id
            )

    except WebSocketDisconnect:
        manager.remove(
            websocket, 
            chat_room_id
        )
