import psycopg2
import json
import time
from psycopg2.extras import RealDictCursor

class Database:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        for intento in range(1, 11):
            try:
                print(f"⏳ Intentando conexión a PostgreSQL... intento {intento}")
                self.conn = psycopg2.connect(
                    dbname=dbname,
                    user=user,
                    password=password,
                    host=host,
                    port=port
                )
                self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
                self._ensure_table()
                print("✅ Conexión a PostgreSQL establecida.")
                return
            except Exception as e:
                print(f"⚠️  Conexión fallida ({intento}/10): {e}")
                time.sleep(1)
        raise Exception("❌ No se pudo conectar a PostgreSQL después de varios intentos.")

    def _ensure_table(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id SERIAL PRIMARY KEY,
                topic VARCHAR(255) NOT NULL,
                payload TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL
            );
        ''')
        self.conn.commit()

    def insert_alert(self, topic, payload, timestamp):
        self.cur.execute(
            "INSERT INTO alerts (topic, payload, timestamp) VALUES (%s, %s, %s)",
            (topic, payload, timestamp)
        )
        self.conn.commit()

    def get_alerts(self):
        self.cur.execute("SELECT * FROM alerts ORDER BY timestamp DESC")
        rows = self.cur.fetchall()
        for row in rows:
            try:
                row["payload"] = json.loads(row["payload"])
            except json.JSONDecodeError:
                pass  # deja el string si no es JSON válido
        return rows

    def close(self):
        self.cur.close()
        self.conn.close()
