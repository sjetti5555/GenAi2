import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",              # Default user for XAMPP
        password="",              # Leave blank for default XAMPP
        database="ecommerce_inventory"
    )

def insert_inventory(product_id, product_name, warehouse, stock):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    INSERT INTO inventory_tracking (product_id, product_name, warehouse, current_stock)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE current_stock = VALUES(current_stock);
    """
    try:
        cursor.execute(query, (product_id, product_name, warehouse, stock))
        conn.commit()
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()

def read_inventory():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory_tracking")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    conn.close()
