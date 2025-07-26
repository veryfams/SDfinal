#!/bin/bash

# Script para configurar la réplica de PostgreSQL
echo "Configurando réplica de PostgreSQL..."

# Esperar a que el master esté listo
echo "Esperando a que el master esté disponible..."
until PGPASSWORD=tu_password psql -h postgres-master -U postgres -d adn_alert_db -c '\q'; do
  echo "Master no disponible, esperando..."
  sleep 2
done

echo "Master disponible, configurando réplica..."

# Crear usuario de replicación en el master
PGPASSWORD=tu_password psql -h postgres-master -U postgres -d adn_alert_db <<EOF
CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replicator_password';
SELECT pg_create_physical_replication_slot('replica_slot');
EOF

# Configurar la réplica
docker exec postgres-replica bash -c "
rm -rf /var/lib/postgresql/data/*
PGPASSWORD=replicator_password pg_basebackup -h postgres-master -D /var/lib/postgresql/data -U replicator -v -P -W
echo \"standby_mode = 'on'\" >> /var/lib/postgresql/data/recovery.conf
echo \"primary_conninfo = 'host=postgres-master port=5432 user=replicator password=replicator_password'\" >> /var/lib/postgresql/data/recovery.conf
echo \"primary_slot_name = 'replica_slot'\" >> /var/lib/postgresql/data/recovery.conf
"

echo "Réplica configurada. Reiniciando servicio..."
docker restart postgres-replica

echo "Configuración completada!"