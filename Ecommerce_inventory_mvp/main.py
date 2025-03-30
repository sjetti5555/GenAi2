from database.inventory_db import insert_inventory, read_inventory

if __name__ == "__main__":
    insert_inventory("P001", "Smartphone", "Hyderabad", 100)
    insert_inventory("P002", "Laptop", "Bangalore", 60)

    print("📦 Current Inventory from Database:")
    read_inventory()
