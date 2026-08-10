import psycopg2

from dataclasses import dataclass


@dataclass
class CreatePostgresDatabase:
    host: str
    password: str
    port: str = "5432"
    dbname: str = "postgres"
    user: str = "postgres"

    def __post_init__(self):
        self.init_text_gen_db()
        self.init_sentiment_db()

    def _connect(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            sslmode="require",
        )

    def init_text_gen_db(self):
        conn = self._connect()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS text_generation (
                    id SERIAL PRIMARY KEY,
                    prompt TEXT NOT NULL,
                    generated_text TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            ''')
            conn.commit()
        finally:
            conn.close()

    def init_sentiment_db(self):
        conn = self._connect()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sentiment_analysis (
                    id SERIAL PRIMARY KEY,
                    prompt TEXT NOT NULL,
                    sentiment TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            ''')
            conn.commit()
        finally:
            conn.close()

    def save_response_text_gen(self, prompt: str, generated_text: str):
        conn = self._connect()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO text_generation (prompt, generated_text)
                VALUES (%s, %s)
            ''', (prompt, generated_text))
            conn.commit()
        finally:
            conn.close()

    def save_response_sentiment(self, prompt: str, sentiment: str, confidence: float):
        conn = self._connect()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sentiment_analysis (prompt, sentiment, confidence)
                VALUES (%s, %s, %s)
            ''', (prompt, sentiment, confidence))
            conn.commit()
        finally:
            conn.close()
