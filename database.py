import sqlite3

def init_db():
    conn = sqlite3.connect("stock.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reference TEXT,
        name TEXT NOT NULL,
        type TEXT,
        category TEXT,
        quantity INTEGER,
        price REAL,
        image_path TEXT               
    )
    """)

    conn.commit()
    conn.close()
