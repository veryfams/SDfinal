from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from mqtt_client import start_mqtt         # Importa el módulo que escucha alertas MQTT
from websocket_manager import WebSocketManager  # Administra conexiones WebSocket

# Crea la app FastAPI
app = FastAPI()

# Instancia un gestor de conexiones WebSocket
ws_manager = WebSocketManager()

# Inicia la suscripción al broker MQTT, pasándole el manager para reenviar mensajes
start_mqtt(ws_manager)

# Ruta WebSocket donde se conectarán los clientes (React)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)  # Acepta y registra la conexión
    try:
        while True:
            await websocket.receive_text()  # Espera mensajes, aunque no se procesan
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)  # Quita la conexión si se desconecta el cliente
