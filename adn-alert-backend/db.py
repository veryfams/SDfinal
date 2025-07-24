import psycopg2
from psycopg2.extras import RealDictCursor

class Database:
    def __init__(self, dbname, user, password, host='postgres', port=5432):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        self._ensure_table()

    def _ensure_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS alerts (
            id SERIAL PRIMARY KEY,
            topic VARCHAR(255) NOT NULL,
            payload TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL
        );
        '''
        self.cur.execute(create_table_query)
        self.conn.commit()

    def insert_alert(self, topic, payload, timestamp):
        query = """
        INSERT INTO alerts (topic, payload, timestamp)
        VALUES (%s, %s, %s)
        """
        self.cur.execute(query, (topic, payload, timestamp))
        self.conn.commit()

    def get_alerts(self):
        self.cur.execute("SELECT * FROM alerts ORDER BY timestamp DESC")
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
