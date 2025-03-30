import pandas as pd
import numpy as np

def allocate_inventory(file_path):
    # Load sales data
    df = pd.read_csv(file_path)

    # Calculate regional demand per product
    demand_df = df.groupby(['product_id', 'warehouse'])['units_sold'].sum().reset_index()
    pivot = demand_df.pivot(index='warehouse', columns='product_id', values='units_sold').fillna(0)

    print("📊 Regional Demand Matrix (warehouses x products):")
    print(pivot)

    # Normalize demand (sum to 1 per product)
    demand_matrix = pivot.values
    column_sums = demand_matrix.sum(axis=0)
    normalized = demand_matrix / column_sums

    # Assume total stock available per product (mock for MVP)
    total_stock = {
        'P001': 100,   # Smartphone
        'P002': 60     # Laptop
    }

    stock_array = np.array([total_stock[pid] for pid in pivot.columns])
    allocation_matrix = normalized * stock_array

    # Convert back to DataFrame
    allocation_df = pd.DataFrame(allocation_matrix, index=pivot.index, columns=pivot.columns)
    print("\n📦 Recommended Inventory Allocation:")
    print(allocation_df.round(1))

    return allocation_df

if __name__ == "__main__":
    file_path = "C:/Users/srira/Desktop/GenAi2/Ecommerce_inventory_mvp/data/sales_data.csv"
    allocate_inventory(file_path)
