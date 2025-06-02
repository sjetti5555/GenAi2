import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from scripts.forecast import forecast_demand  # ✅ Now this works!

def check_replenishment(file_path):
    df = pd.read_csv(file_path)
    forecast_df = forecast_demand(file_path)

    latest_stock_df = (
        df.sort_values('date')
          .groupby(['product_id', 'product_id'], as_index=False)
          .last()[['product_id', 'product_id', 'stock']]
    )

    merged_df = pd.merge(forecast_df, latest_stock_df, on=['product_id', 'product_id'])
    merged_df['restock_needed'] = merged_df['poisson_forecast'] > merged_df['stock']
    merged_df['status'] = merged_df['restock_needed'].apply(
        lambda x: '🚨 Restock Needed' if x else '✅ Stock OK'
    )

    return merged_df

if __name__ == "__main__":
    path = "C:/Users/srira/Desktop/GenAi2/Ecommerce_inventory_mvp/data/sales_data.csv"
    df = check_replenishment(path)
    print(df)
    print("\n✅ Replenishment check completed.")