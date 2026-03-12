import pandas as pd
from analytics.kpi_engine import KPIEngine

fact = pd.read_csv("data/warehouse/fact_sales.csv")
dim_customer = pd.read_csv("data/warehouse/dim_customer.csv")
dim_product = pd.read_csv("data/warehouse/dim_product.csv")

kpi = KPIEngine()

print("Total Revenue:", kpi.total_revenue(fact))
print("Profit Margin:", kpi.profit_margin(fact))
print("Average Order Value:", kpi.average_order_value(fact))
print("Customer Lifetime Value:\n", kpi.customer_lifetime_value(fact, dim_customer))
print("Region Performance:\n", kpi.region_performance(fact, dim_customer))
print("Product Performance:\n", kpi.product_performance(fact, dim_product)) 