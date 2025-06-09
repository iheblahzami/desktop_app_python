import sqlite3

DB_NAME = "stock.db"

def add_product(reference, nom, quantite, prix, categorie, fournisseur, image):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (reference, nom, quantite, prix, categorie, fournisseur, image)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (reference, nom, quantite, prix, categorie, fournisseur, image))
    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_product(product_id, reference, nom, quantite, prix, categorie, fournisseur, image):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE products
        SET reference=?, nom=?, quantite=?, prix=?, categorie=?, fournisseur=?, image=?
        WHERE id=?
    ''', (reference, nom, quantite, prix, categorie, fournisseur, image, product_id))
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
        WHERE nom LIKE ? OR categorie LIKE ? OR reference LIKE ?
    """, (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    results = cursor.fetchall()
    conn.close()
    return results

def get_low_stock_products(threshold=5):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE quantite < ?', (threshold,))
    results = cursor.fetchall()
    conn.close()
    return results

def update_stock(product_id, delta_quantity):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT quantite FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    if row:
        current_qty = row[0]
        new_qty = max(0, current_qty + delta_quantity)  # Avoid negative quantity
        cursor.execute("UPDATE products SET quantite = ? WHERE id = ?", (new_qty, product_id))
        conn.commit()
    conn.close()
