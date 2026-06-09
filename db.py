import sqlite3
from contextlib import contextmanager
from pathlib import Path
   
DB_PATH = Path(__file__).parent / "data" / "bot.db"

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    
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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        last_scraped_at TEXT,
        profile_url TEXT UNIQUE);
                    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads(
            id INTEGER PRIMARY KEY,
            organiser_id INTEGER,
            url TEXT NOT NULL,
            vendor TEXT,
            status TEXT,
            discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(organiser_id) REFERENCES organisers(id));
                   """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        location TEXT,
        starts_at TEXT,
        ends_at TEXT,
        categories TEXT,
        price_from REAL,
        url TEXT UNIQUE NOT NULL,
        organiser_id INTEGER,
        created_at TEXT,
        notified INTEGER DEFAULT 0,
        FOREIGN KEY (organiser_id) REFERENCES organisers(id)
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
        chat_id INTEGER PRIMARY KEY,
        cities TEXT,
        categories TEXT);
    """)
    
    conn.commit()
    
if __name__ == "__main__":
    with get_connection() as conn:
        init_db(conn)
    print("OK")