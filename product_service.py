import sqlite3

DB_NAME = "stock.db"

def add_product(reference, nom, categorie, quantite, fournisseur, image):
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (reference, nom, categorie, quantite, fournisseur, image)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (reference, nom, categorie, quantite, fournisseur, image))
    conn.commit()
    conn.close()


def get_all_products():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_product(product_id, reference, nom, categorie, quantite, fournisseur, image):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products
        SET reference = ?, nom = ?, categorie = ?, quantite = ?, fournisseur = ?, image = ?
        WHERE id = ?
    """, (reference, nom, categorie, quantite, fournisseur, image, product_id))
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
    cursor.execute('''
        SELECT reference, name, category, quantity, price, image_path
        FROM products WHERE quantity < ?
    ''', (threshold,))
    results = cursor.fetchall()
    conn.close()
    return results
