import pandas as pd
import numpy as np

def allocate_inventory(file_path):
    # Load sales data
    df = pd.read_csv(file_path)

    # Step 1: Compute demand matrix
    demand_df = df.groupby(['product_id', 'warehouse'])['units_sold'].sum().reset_index()
    pivot = demand_df.pivot(index='warehouse', columns='product_id', values='units_sold').fillna(0)

    print("📊 Regional Demand Matrix (warehouses x products):")
    print(pivot)

    demand_matrix = pivot.values
    warehouse_names = pivot.index.tolist()
    product_ids = pivot.columns.tolist()

    # Step 2: Total stock (mock)
    total_stock = {
        'P001': 100,
        'P002': 60
    }

    # Step 3: Add weight factors
    warehouse_capacity = {
        'Hyderabad': 200,
        'Bangalore': 150
    }

    supplier_lead_time = {
        'Hyderabad': 2,     # 2 days
        'Bangalore': 1      # 1 day
    }

    # Step 4: Normalize demand
    demand_weight = demand_matrix / demand_matrix.sum(axis=0)

    # Step 5: Apply capacity and lead time weights
    for i, warehouse in enumerate(warehouse_names):
        cap_weight = warehouse_capacity[warehouse] / sum(warehouse_capacity.values())
        lead_time_weight = 1 / supplier_lead_time[warehouse]  # Faster = higher weight
        demand_weight[i] *= cap_weight * lead_time_weight

    # Step 6: Final allocation
    stock_array = np.array([total_stock[pid] for pid in product_ids])
    final_alloc = demand_weight / demand_weight.sum(axis=0) * stock_array

    # Step 7: Create final DataFrame
    allocation_df = pd.DataFrame(final_alloc, index=warehouse_names, columns=product_ids)
    
    print("\n📦 Optimized Inventory Allocation with Weights:")
    print(allocation_df.round(1))

    return allocation_df

if __name__ == "__main__":
    file_path = "C:/Users/srira/Desktop/GenAi2/Ecommerce_inventory_mvp/data/sales_data.csv"
    allocate_inventory(file_path)
    print("\n✅ Inventory allocation completed.")
# This script allocates inventory based on sales data and warehouse capacities.