import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ecommerce_inventory"
    )

def insert_inventory(product_id, warehouse, stock):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    INSERT INTO inventory_tracking (product_id, warehouse, stock)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE stock = VALUES(stock);
    """
    try:
        cursor.execute(query, (product_id, warehouse, stock))
        conn.commit()
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()

def read_inventory(warehouse=None):
    conn = connect_db()
    cursor = conn.cursor()

    if warehouse:
        cursor.execute("SELECT * FROM inventory_tracking WHERE warehouse = %s", (warehouse,))
    else:
        cursor.execute("SELECT * FROM inventory_tracking")

    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.close()
    conn.close()
