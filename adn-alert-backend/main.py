from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from websocket_manager import WebSocketManager
from mqtt_client import MQTTClient
from db import Database
import asyncio

app = FastAPI()

# Base de datos local
db = Database(
    dbname="adn_alert_db",
    user="postgres",
    password="tu_password",  # reemplaza por la real
    host="postgres-master",
    port=5432
)

# WebSocket manager
ws_manager = WebSocketManager()

# Cliente MQTT
mqtt = MQTTClient("mosquitto", 1883, "alertas/general", db)

# Cada vez que llega un mensaje MQTT, se reenvía por WebSocket
mqtt.set_on_message_callback(
    lambda topic, payload, timestamp: asyncio.run(ws_manager.broadcast(payload))
)
mqtt.start()

# Endpoint WebSocket para clientes
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("👤 Cliente WebSocket intentando conectar...")
    await ws_manager.connect(websocket)
    print("✅ Cliente WebSocket conectado.")
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        print("❌ Cliente WebSocket desconectado.")
        await ws_manager.disconnect(websocket)


# Endpoint para obtener alertas almacenadas
@app.get("/alertas")
def get_alertas():
    return db.get_alerts()

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}