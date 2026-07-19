import sqlite3
from dataclasses import dataclass


@dataclass
class CreateDatabase:
    db_path: str

    def __post_init__(self):
        self.init_text_gen_db()
        self.init_sentiment_db()


    def init_text_gen_db(self):
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS text_generation (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt TEXT NOT NULL,
                    generated_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
        finally:
            conn.close()


    def init_sentiment_db(self):
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sentiment_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt TEXT NOT NULL,
                    sentiment TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
        finally:
            conn.close()


    def save_response_text_gen(self, prompt: str, generated_text: str):
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO text_generation (prompt, generated_text)
                VALUES (?, ?)
            ''', (prompt, generated_text))
            conn.commit()
        finally:
            conn.close()


    def save_response_sentiment(self, prompt: str, sentiment: str, confidence: float):
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sentiment_analysis (prompt, sentiment, confidence)
                VALUES (?, ?, ?)
            ''', (prompt, sentiment, confidence))
            conn.commit()
        finally:
            conn.close()
