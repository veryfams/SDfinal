import json
import paho.mqtt.client as mqtt

# Variable global para poder acceder al WebSocketManager desde el callback
ws_manager = None

# Función llamada cuando el cliente MQTT se conecta exitosamente
def on_connect(client, userdata, flags, rc):
    print("🔌 Conectado al broker MQTT")
    # Se suscribe al canal donde llegan las alertas simuladas
    client.subscribe("alertas/general")

# Función llamada cada vez que llega un mensaje MQTT
def on_message(client, userdata, msg):
    # Convierte el payload del mensaje a JSON
    alerta = json.loads(msg.payload.decode())
    print(" Alerta recibida:", alerta)

    # Si el WebSocketManager está definido, reenvía la alerta por WebSocket
    if ws_manager:
        import asyncio
        asyncio.run(ws_manager.broadcast(alerta))

# Inicializa y conecta el cliente MQTT
def start_mqtt(manager):
    global ws_manager
    ws_manager = manager  # Guarda la referencia al WebSocketManager

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Conecta al broker Mosquitto (local o en Docker)
    client.connect("localhost", 1883, 60)
    client.loop_start()  # Mantiene el cliente escuchando en segundo plano
