import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gradio as gr
import pandas as pd
import mysql.connector
from scripts.forecast import forecast_demand
from scripts.replenish import check_replenishment
from scripts.allocate import allocate_inventory


# ✅ Path to your sales data
CSV_PATH = "C:/Users/srira/Desktop/GenAi2/Ecommerce_inventory_mvp/data/sales_data.csv"

# ✅ Connect to MySQL
def fetch_inventory():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Ecommerce_inventory"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory_tracking")
        rows = cursor.fetchall()
        columns = ["Product ID", "Product Name", "Warehouse", "Current Stock", "Last Updated"]
        df = pd.DataFrame(rows, columns=columns)
        cursor.close()
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})

# ✅ Forecast Function
def run_forecast():
    try:
        forecast = forecast_demand(CSV_PATH)
        return forecast
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})

# ✅ Replenishment Function
def run_replenishment():
    try:
        replenishment = check_replenishment(CSV_PATH)
        return replenishment
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})

# ✅ Allocation Function
def run_allocation():
    try:
        allocation = allocate_inventory(CSV_PATH)
        return allocation.round(1)
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})

# ✅ Build Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 📦 Ecommerce Inventory Dashboard (Gradio Version)")

    gr.Markdown("### 📋 View Current Inventory")
    inv_btn = gr.Button("🔄 Load Inventory")
    inv_output = gr.Dataframe()
    inv_btn.click(fetch_inventory, outputs=inv_output)

    gr.Markdown("### 📈 Demand Forecasting")
    forecast_btn = gr.Button("📊 Run Forecast")
    forecast_output = gr.Dataframe()
    forecast_btn.click(run_forecast, outputs=forecast_output)

    gr.Markdown("### 🚨 Replenishment Check")
    rep_btn = gr.Button("🛒 Check Replenishment")
    rep_output = gr.Dataframe()
    rep_btn.click(run_replenishment, outputs=rep_output)

    gr.Markdown("### 🔁 Inventory Allocation")
    alloc_btn = gr.Button("⚙️ Optimize Allocation")
    alloc_output = gr.Dataframe()
    alloc_btn.click(run_allocation, outputs=alloc_output)

# ✅ Launch App
demo.launch()
# Note: Ensure you have the necessary packages installed:
# pip install gradio pandas mysql-connector-python