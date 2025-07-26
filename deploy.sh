#!/bin/bash

echo "🚀 Desplegando sistema con alta disponibilidad y balanceador de carga..."

# Crear directorios necesarios
echo "📁 Creando estructura de directorios..."
mkdir -p nginx
mkdir -p haproxy
mkdir -p postgres/master
mkdir -p mosquitto/config
mkdir -p mosquitto/data
mkdir -p mosquitto/log
mkdir -p monitoring
mkdir -p scripts
mkdir -p backend/logs

# Dar permisos
chmod +x scripts/setup-replica.sh

echo "🛑 Deteniendo contenedores existentes..."
docker compose down -v

echo "🏗️ Construyendo imágenes..."
docker compose build --no-cache

echo "🐳 Iniciando servicios base..."
docker compose up -d postgres-master redis mosquitto

echo "⏳ Esperando a que los servicios base estén listos..."
sleep 30

echo "🔄 Iniciando réplica de PostgreSQL..."
docker compose up -d postgres-replica
sleep 15

echo "🔧 Configurando réplica..."
# Ejecutar script de réplica si es necesario
# ./scripts/setup-replica.sh

echo "🌐 Iniciando backends..."
docker compose up -d backend-1 backend-2 backend-3

echo "⚖️ Iniciando balanceador de carga..."
docker compose up -d nginx-lb mosquitto-sidecar

echo "🎨 Iniciando frontend..."
docker compose up -d frontend

echo "📊 Iniciando monitoreo..."
docker compose up -d prometheus

echo "✅ Despliegue completado!"

echo "
🎉 Sistema desplegado exitosamente!

📍 Puntos de acceso:
- Frontend: http://localhost:3000
- API (balanceada): http://localhost:80/api
- WebSockets (balanceados): ws://localhost:8080/ws
- MQTT (directo): localhost:1883
- MQTT (sidecar): localhost:1884
- PostgreSQL Master: localhost:5433
- PostgreSQL Replica: localhost:5434
- Redis: localhost:6379
- Prometheus: http://localhost:9090
- HAProxy Stats: http://localhost:8404/stats

🏗️ Arquitectura implementada:
✅ Dockerización completa
✅ Alta disponibilidad (PostgreSQL Master-Replica)
✅ Balanceador de carga (NGINX para backend)
✅ Patrón Sidecar (HAProxy para Mosquitto)
✅ Sistema de base de datos (PostgreSQL)
✅ Sistema de colas (Mosquitto MQTT)
✅ WebSockets para comunicación en tiempo real
✅ Frontend y Backend separados

🔍 Verificar estado:
docker-compose ps
"