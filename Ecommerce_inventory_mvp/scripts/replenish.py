import pandas as pd
from scripts.forecast import forecast_demand


def check_replenishment(sales_file):
    # Load sales data
    sales_df = pd.read_csv(sales_file)

    # Get forecasted demand
    forecast_df = forecast_demand(sales_file)

    # Merge forecast with latest stock levels
    latest_stock_df = (
        sales_df.sort_values('date')
                .groupby(['product_id', 'product_name'], as_index=False)
                .last()[['product_id', 'product_name', 'current_stock']]
    )

    merged_df = pd.merge(forecast_df, latest_stock_df, on=['product_id', 'product_name'])

    # Check if restock is needed
    merged_df['restock_needed'] = merged_df['forecast_units'] > merged_df['current_stock']

    # Print restock alerts
    for _, row in merged_df.iterrows():
        if row['restock_needed']:
            print(f"🚨 Restock Alert: {row['product_name']} (Product ID: {row['product_id']}) "
                  f"→ Forecasted Demand = {row['forecast_units']}, Stock = {row['current_stock']}")
        else:
            print(f"✅ Stock OK: {row['product_name']} → Forecasted Demand = {row['forecast_units']}, Stock = {row['current_stock']}")

    return merged_df

if __name__ == "__main__":
    sales_file = "C:/Users/srira/Desktop/GenAi2/Ecommerce_inventory_mvp/data/sales_data.csv"
    check_replenishment(sales_file)
