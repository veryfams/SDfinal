from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from db import Database
from mqtt_client import MQTTClient
from websocket_manager import WebSocketManager
import asyncio

app = FastAPI()
ws_manager = WebSocketManager()

# Configuración de la base de datos (ajusta los valores según tu entorno)
DB_CONFIG = {
    'dbname': 'adn_alert_db',
    'user': 'postgres',
    'password': 'tu_password',
    'host': 'postgres',  # Usar el nombre del servicio de docker-compose
    'port': 5432
}
db = Database(**DB_CONFIG)

# Inicializa la tabla si no existe
from models import CREATE_TABLE_ALERTS
db.cur.execute(CREATE_TABLE_ALERTS)
db.conn.commit()

# Configuración MQTT
MQTT_BROKER = 'mosquitto'  # Usar el nombre del servicio de docker-compose
MQTT_PORT = 1883
MQTT_TOPIC = 'alertas/#'
import json
import asyncio

mqtt_client = MQTTClient(MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, db)

def mqtt_to_ws(topic, payload, timestamp):
    
    msg = json.dumps({
        'topic': topic,
        'payload': payload,
        'timestamp': timestamp.isoformat()
    })
    asyncio.create_task(ws_manager.broadcast(msg))



mqtt_client.set_on_message_callback(mqtt_to_ws)
mqtt_client.start()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket)
