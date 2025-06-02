import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from scipy.stats import poisson
import warnings
warnings.filterwarnings("ignore")

def forecast_poisson(sales):
    # Mean of sales = lambda
    lam = sales['units_sold'].mean()
    return round(poisson.mean(mu=lam))

def forecast_arima(sales, steps=1):
    ts = sales.sort_values('date').set_index('date')['units_sold']
    model = ARIMA(ts, order=(1, 1, 1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=steps)
    return round(forecast.iloc[-1])

def forecast_demand(file_path, model_type='both'):
    df = pd.read_csv(file_path, parse_dates=['date'])

    results = []
    for (pid, pname), group in df.groupby(['product_id', 'product_id']):
        row = {'product_id': pid, 'product_id': pname}
        
        if model_type in ['poisson', 'both']:
            row['poisson_forecast'] = forecast_poisson(group)
        
        if model_type in ['arima', 'both']:
            row['arima_forecast'] = forecast_arima(group)
        
        results.append(row)

    return pd.DataFrame(results)

if __name__ == "__main__":
    file_path = "C:/Users/srira/Desktop/GenAi2/Ecommerce_inventory_mvp/data/sales_data.csv"
    forecast_df = forecast_demand(file_path, model_type='both')
    print(forecast_df)
    print("\n📈 Forecasted Demand:")