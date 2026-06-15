from dotenv import load_dotenv
load_dotenv()
import psycopg2
from contextlib import contextmanager
import os

DB_URL = os.environ.get("DATABASE_URL")

@contextmanager
def get_connection():
    conn = psycopg2.connect(DB_URL)
    
    try:
        yield conn
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS organisers(
        id SERIAL PRIMARY KEY,
        name TEXT,
        last_scraped_at TEXT,
        profile_url TEXT UNIQUE);
                    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads(
            id SERIAL PRIMARY KEY,
            organiser_id INTEGER,
            url TEXT NOT NULL,
            vendor TEXT,
            status TEXT,
            discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(organiser_id) REFERENCES organisers(id));
                   """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events(
        id SERIAL PRIMARY KEY,
        title TEXT,
        location TEXT,
        starts_at TEXT,
        ends_at TEXT,
        categories TEXT,
        price_from TEXT,
        url TEXT UNIQUE NOT NULL,
        organiser_id INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        notified INTEGER DEFAULT 0,
        FOREIGN KEY (organiser_id) REFERENCES organisers(id)
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
        chat_id BIGINT PRIMARY KEY,
        cities TEXT,
        categories TEXT);
    """)
    
    cursor.execute("""
        CREATE TABLE notifications (
        event_id INTEGER,
        chat_id INTEGER,
        PRIMARY KEY (event_id, chat_id));
                   """)
    
    conn.commit()
    
if __name__ == "__main__":
    with get_connection() as conn:
        init_db(conn)
    print("OK")