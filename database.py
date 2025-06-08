import sqlite3

def init_db():
    conn = sqlite3.connect("stock.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reference TEXT NOT NULL,
            nom TEXT NOT NULL,
            categorie TEXT,
            quantite INTEGER NOT NULL,
            fournisseur TEXT,
            image TEXT
        )
    """)
    
    conn.commit()
    conn.close()
