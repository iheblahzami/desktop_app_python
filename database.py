import sqlite3

def init_db():
    conn = sqlite3.connect("stock.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reference TEXT,
            nom TEXT,
            quantite INTEGER,
            prix REAL,
            categorie TEXT,
            fournisseur TEXT,
            image TEXT
        )
    """)

    
    conn.commit()
    conn.close()
