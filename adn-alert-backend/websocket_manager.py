from fastapi import WebSocket
from typing import List

class WebSocketManager:
    def __init__(self):
        # Lista de conexiones WebSocket activas
        self.active_connections: List[WebSocket] = []

    # Acepta una nueva conexión WebSocket y la agrega a la lista
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    # Elimina una conexión cerrada
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # Envía un mensaje JSON a todos los clientes conectados
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)
