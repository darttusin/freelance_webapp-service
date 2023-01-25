from typing import List
from fastapi import WebSocket
from fastapi.websockets import WebSocketState
from collections import defaultdict



class ConnectionManager:
    def __init__(self):
        self.connections = defaultdict(dict)

    def get_members(self, chat_room_id: str):
        try:
            return self.connections[chat_room_id]
        except Exception:
            return None
    
    async def connect(self, websocket: WebSocket, chat_room_id: str):
        await websocket.accept()
        if self.connections[chat_room_id] == {} \
            or len(self.connections[chat_room_id]) == 0:
            self.connections[chat_room_id] = []
        self.connections[chat_room_id].append(websocket)
    
    def remove(self, websocket: WebSocket, chat_room_id: str):
        self.connections[chat_room_id].remove(websocket)

    async def send_private_message(self, message: str, chat_room_id: str):
        live_connections = []
        while len(self.connections[chat_room_id]) > 0:
            websocket = self.connections[chat_room_id].pop()
            await websocket.send_text(message)
            live_connections.append(websocket)
            
        self.connections[chat_room_id] = live_connections
