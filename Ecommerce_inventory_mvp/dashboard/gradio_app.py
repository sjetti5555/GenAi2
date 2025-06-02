import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gradio as gr
import pandas as pd
import tempfile
import mysql.connector
import matplotlib.pyplot as plt
import plotly.express as px
import json

from scripts.forecast import forecast_demand
from scripts.replenish import check_replenishment
from scripts.allocate import allocate_inventory

DEFAULT_CSV_PATH = "C:/Users/srira/Desktop/GenAi2/Ecommerce_inventory_mvp/data/sales_data.csv"

# ✅ Audit log for all modules
def log_to_mysql(module_name, df):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Ecommerce_inventory"
        )
        cursor = conn.cursor()
        query = "INSERT INTO audit_logs (module, data) VALUES (%s, %s)"
        cursor.execute(query, (module_name, json.dumps(df.to_dict(orient="records"))))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Audit log failed for {module_name}: {str(e)}")

# ✅ Log forecast history (Poisson + ARIMA)
def log_forecast_history(df):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Ecommerce_inventory"
        )
        cursor = conn.cursor()
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO forecast_history (product_id, product_name, poisson_forecast, arima_forecast)
                VALUES (%s, %s, %s, %s)
            """, (
                row["product_id"],
                row["product_name"],
                row["poisson_forecast"],
                row["arima_forecast"]
            ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Forecast history log failed: {str(e)}")

# ✅ Fetch inventory from MySQL
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

# ✅ Forecast
def run_forecast(uploaded_file):
    try:
        path = uploaded_file.name if uploaded_file else DEFAULT_CSV_PATH
        forecast = forecast_demand(path)
        log_to_mysql("forecast", forecast)
        log_forecast_history(forecast)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", encoding="utf-8", newline='') as tmp:
            forecast.to_csv(tmp.name, index=False)
            return forecast, tmp.name
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]}), ""

# ✅ Forecast Chart
def generate_forecast_chart(uploaded_file):
    try:
        path = uploaded_file.name if uploaded_file else DEFAULT_CSV_PATH
        df = forecast_demand(path)
        fig, ax = plt.subplots()
        ax.bar(df["product_name"], df["poisson_forecast"], label="Poisson", alpha=0.6)
        ax.bar(df["product_name"], df["arima_forecast"], bottom=df["poisson_forecast"], label="ARIMA", alpha=0.6)
        ax.set_title("📈 Forecasted Demand (Poisson + ARIMA)")
        ax.set_ylabel("Units")
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig
    except Exception as e:
        print("Chart error:", e)
        return plt.figure()

# ✅ Replenishment
def run_replenishment(uploaded_file):
    try:
        path = uploaded_file.name if uploaded_file else DEFAULT_CSV_PATH
        result = check_replenishment(path)
        log_to_mysql("replenishment", result)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", encoding="utf-8", newline='') as tmp:
            result.to_csv(tmp.name, index=False)
            return result, tmp.name
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]}), ""

# ✅ Allocation
def run_allocation(uploaded_file):
    try:
        path = uploaded_file.name if uploaded_file else DEFAULT_CSV_PATH
        result = allocate_inventory(path)
        log_to_mysql("allocation", result)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", encoding="utf-8", newline='') as tmp:
            result.round(1).to_csv(tmp.name, index=False)
            return result.round(1), tmp.name
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]}), ""

# ✅ Low stock checker
def check_low_stock():
    try:
        df = fetch_inventory()
        return df[df["Current Stock"] < 50]
    except:
        return pd.DataFrame({"Error": ["Could not check low stock"]})

# ✅ Plotly historical chart
def plot_forecast_history():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Ecommerce_inventory"
        )
        df = pd.read_sql("SELECT * FROM forecast_history ORDER BY created_at DESC LIMIT 100", conn)
        conn.close()

        # Ensure the data is sorted and clean
        df["created_at"] = pd.to_datetime(df["created_at"])
        df = df.sort_values(by="created_at")

        # Create the Plotly figure
        fig = px.line(
            df,
            x="created_at",
            y=["poisson_forecast", "arima_forecast"],
            color="product_name",
            title="📊 Historical Forecast Trends (Bar Chart)",
            labels={
                "created_at": "Date",
                "value": "Forecasted Units",
                "variable": "Forecast Type",
                "product_name": "Product Name"
            },
            template="plotly_white"
        )

        # Customize the layout for better clarity
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Forecasted Units",            
            legend_title="Product Name",
            hovermode="x unified",
            font=dict(size=12),
            title=dict(font=dict(size=16)),
            margin=dict(l=40, r=40, t=40, b=40)
        )

        # Add gridlines for better readability
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor="lightgray")
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor="lightgray")

        return fig
    except Exception as e:
        print("Plotly Error:", e)
        return px.scatter(title="❌ Failed to load chart")

# ✅ Gradio App UI
with gr.Blocks() as demo:
    gr.Markdown("# 📦 Ecommerce Inventory Dashboard")

    # 👥 Role selection
    role = gr.Dropdown(
        choices=["Admin", "Warehouse"],
        value="Admin",
        label="Select Role"
    )

    # 🧑‍🏭 Warehouse Section
    with gr.Group(visible=True) as warehouse_section:
        gr.Markdown("### 📋 View Live Inventory")
        with gr.Row():
            inv_btn = gr.Button("🔄 Load Inventory")
            inv_output = gr.Dataframe()
            inv_btn.click(fetch_inventory, outputs=inv_output)

        gr.Markdown("### 📉 Low Stock Alerts")
        with gr.Row():
            low_btn = gr.Button("⚠️ Show Low Stock")
            low_output = gr.Dataframe()
            low_btn.click(check_low_stock, outputs=low_output)

    # 👨‍💼 Admin Section
    with gr.Group(visible=True) as admin_section:
        gr.Markdown("### 📁 Upload CSV to Run Analysis (Optional)")
        csv_input = gr.File(label="Upload sales_data.csv", file_types=[".csv"], file_count="single")

        gr.Markdown("### 📈 Forecast Demand")
        forecast_btn = gr.Button("📊 Run Forecast")
        forecast_output = gr.Dataframe()
        forecast_download = gr.File(label="Download Forecast CSV")
        forecast_btn.click(run_forecast, inputs=csv_input, outputs=[forecast_output, forecast_download])

        gr.Markdown("### 📊 Forecast Chart")
        chart_btn = gr.Button("📉 Show Forecast Chart")
        chart_output = gr.Plot()
        chart_btn.click(generate_forecast_chart, inputs=csv_input, outputs=chart_output)

        gr.Markdown("### 🚨 Replenishment Check")
        rep_btn = gr.Button("🛒 Run Replenishment")
        rep_output = gr.Dataframe()
        rep_download = gr.File(label="Download Replenishment CSV")
        rep_btn.click(run_replenishment, inputs=csv_input, outputs=[rep_output, rep_download])

        gr.Markdown("### 🔁 Optimize Inventory Allocation")
        alloc_btn = gr.Button("⚙️ Run Allocation")
        alloc_output = gr.Dataframe()
        alloc_download = gr.File(label="Download Allocation CSV")
        alloc_btn.click(run_allocation, inputs=csv_input, outputs=[alloc_output, alloc_download])

        gr.Markdown("### 📈 Historical Forecast Dashboard (Plotly)")
        history_btn = gr.Button("📜 View Forecast History")
        history_plot = gr.Plot()
        history_btn.click(plot_forecast_history, outputs=history_plot)

    # 🔄 Toggle visibility based on role
    def toggle_sections(selected_role):
        return (
            gr.update(visible=(selected_role == "Admin")),
        gr.update(visible=(selected_role in ["Admin", "Warehouse"]))
        )

    role.change(
        toggle_sections,
        inputs=role,
        outputs=[admin_section, warehouse_section]
    )

# ✅ Launch it
demo.launch()
# demo.queue().launch()  # For async processing