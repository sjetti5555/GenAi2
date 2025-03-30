import pandas as pd

def forecast_demand(file_path, window=3):
    # Load the sales data
    df = pd.read_csv(file_path, parse_dates=['date'])

    # Group by product and calculate moving average for units_sold
    forecast = (
        df.groupby(['product_id', 'product_name'])
          .apply(lambda x: x.sort_values('date')
                             .set_index('date')['units_sold']
                             .rolling(window=window)
                             .mean()
                             .iloc[-1])
          .reset_index(name='forecast_units')
    )

    return forecast

if __name__ == "__main__":
    file_path = "C:/Users/srira/Desktop/GenAi2/Ecommerce_inventory_mvp/data/sales_data.csv"  # Update the path as needed
    # Forecast demand using the moving average method
    forecast = forecast_demand(file_path)
    print("📈 Forecasted Demand (Moving Average):")
    print(forecast)
    print("✅ Forecasting Completed Successfully!")


# This script forecasts demand for products using a moving average method. It loads sales data from a CSV file, groups the data by product, and calculates the moving average of units sold over a specified window. The forecasted demand is then printed to the console.