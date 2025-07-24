# websocket_manager.py

from fastapi import WebSocket
from typing import Set
import asyncio

class WebSocketManager:
    def __init__(self):
        self.connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.add(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.connections.discard(websocket)

    async def broadcast(self, message: str):
        dead_connections = set()

        for ws in self.connections:
            try:
                await ws.send_text(message)
            except Exception as e:
                print("❌ Error al enviar a un cliente WS:", e)
                dead_connections.add(ws)

        # Limpieza de conexiones muertas
        for ws in dead_connections:
            self.connections.discard(ws)

