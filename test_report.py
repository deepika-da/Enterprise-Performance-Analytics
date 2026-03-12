import pandas as pd

from analytics.kpi_engine import KPIEngine
from analytics.segmentation import CustomerSegmentation
from analytics.forecasting import SalesForecasting
from reporting.report_generator import ReportGenerator

fact = pd.read_csv("data/warehouse/fact_sales.csv")

kpi = KPIEngine()
seg = CustomerSegmentation()
forecast = SalesForecasting()

kpi= {"Total_Revenue": kpi.total_revenue(fact), 
    "Profit_Margin" : kpi.profit_margin(fact),
    "Average_Order_Value" : kpi.average_order_value(fact)}

rfm, _ = seg.segment_customers(fact)
rfm = seg.label_segments(rfm)

monthly_data = forecast.prepare_monthly_data(fact)
forecast = forecast.compare_forecast(monthly_data)

report = ReportGenerator(kpi, monthly_data, rfm, forecast)

print(report.generate_report())