# 📦 Demand Forecasting & Inventory Optimization System 

This project is a Minimum Viable Product (MVP) implementation of the **Demand Forecasting & Inventory Optimization System**. It focuses on forecasting product demand, automating stock replenishment, optimizing inventory distribution, and improving warehouse efficiency using Python, MySQL, and data analytics tools.

---

## 🔍 Project Overview

Inventory management is a critical function in e-commerce operations. The goal of this system is to:
- Accurately forecast demand for each product.
- Automatically trigger restocking based on real-time inventory levels.
- Optimize inventory allocation across multiple fulfillment centers.
- Provide actionable insights via an interactive dashboard.

---

## 🚀 Key Features

### 📈 1. Demand Forecasting
- **Poisson Distribution**: Used to model random demand spikes.
- **ARIMA**: Time series forecasting to capture trends and seasonality.
- Built using `statsmodels` and `scipy`.

### 🛒 2. Automated Replenishment
- Python script checks if forecasted demand exceeds current stock.
- Triggers restocking alerts when stock drops below forecast.
- Integrated with MySQL for live inventory monitoring.

### 📦 3. Inventory Allocation
- Uses matrix operations and linear equations to distribute stock.
- Factors in warehouse capacity and regional demand.
- Ensures optimal distribution with minimal overstock/understock.

### 🗄️ 4. Inventory Tracking System
- MySQL-based database (`inventory_tracking` table).
- Tracks product ID, warehouse, current stock, and last updated timestamp.
- Automatically updated based on sales and restocking logic.

### 🎛️ 5. Interactive Dashboard (Gradio)
- Web-based UI built with Gradio.
- Clickable buttons to run forecasting, replenishment, and allocation.
- Displays results in real time as DataFrames.

---

## 🛠️ Tech Stack

| Layer         | Tools/Technologies                         |
|---------------|---------------------------------------------|
| Language      | Python 3.10                                 |
| Database      | MySQL (via XAMPP + phpMyAdmin)              |
| UI            | Gradio                                      |
| Forecasting   | statsmodels, scipy                          |
| Data Handling | pandas, numpy                               |
| DB Connector  | mysql-connector-python                      |
| Visualization | Gradio frontend (expandable to Tableau/BI)  |

---

## 📂 Project Structure

## 📂 Project Structure

```
inventory_mvp/
│
├── data/                  # Historical sales CSV
│   └── sales_data.csv
│
├── scripts/               # Core logic
│   ├── forecast.py        # Poisson & ARIMA forecasting
│   ├── replenish.py       # Replenishment logic
│   └── allocate.py        # Allocation logic
│
├── db/                    # Database utility
│   └── inventory_db.py
│
├── dashboard/             # Gradio UI
│   └── gradio_app.py
│
├── main.py                # Optional script runner
├── README.md              # Project documentation
└── requirements.txt       # Dependencies



