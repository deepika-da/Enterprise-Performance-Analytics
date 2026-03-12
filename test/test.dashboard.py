import pandas as pd
from visualization.dashboard import Dashboard
from analytics.forecasting import SalesForecasting
from analytics.segmentation import CustomerSegmentation
from analytics.kpi_engine import KPIEngine

fact = pd.read_csv("data/warehouse/fact_sales.csv")
dim_customer = pd.read_csv("data/warehouse/dim_customer.csv")

# Initialize modules
dashboard = Dashboard()
forecast = SalesForecasting()
seg = CustomerSegmentation()
kpi = KPIEngine()

# Monthly data
monthly = forecast.prepare_monthly_data(fact)
forecast_data = forecast.compare_forecast(monthly)

# KPI data
kpi_data = {
    "Total Revenue": kpi.total_revenue(fact),
    "Profit Margin": kpi.profit_margin(fact),
    "AOV": kpi.average_order_value(fact)
}

# Segmentation
rfm, _ = seg.segment_customers(fact)
rfm = seg.label_segments(rfm)

# Region data
region_data = fact.merge(dim_customer, on='customer_id')

# Generate charts
dashboard.revenue_trend_chart(monthly)
dashboard.kpi_chart(kpi_data)
dashboard.segmentation_chart(rfm)
dashboard.region_heatmap(region_data)
dashboard.forecast_chart(forecast_data)