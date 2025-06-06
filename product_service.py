import sqlite3

DB_NAME = "stock.db"

def add_product(reference, name, type, category, quantity, price, image_path):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (reference, name, type, category, quantity, price, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (reference, name, type, category, quantity, price, image_path))
    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_product(product_id, reference, name, type, category, quantity, price, image_path):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products
        SET reference = ?, name = ?, type = ?, category = ?, quantity = ?, price = ?, image_path = ?
        WHERE id = ?
    """, (reference, name, type, category, quantity, price, image_path, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def search_products(keyword):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM products
        WHERE name LIKE ? OR category LIKE ? OR reference LIKE ? OR type LIKE ?
    """, (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    results = cursor.fetchall()
    conn.close()
    return results
