import pandas as pd
from analytics.forecasting import SalesForecasting

fact = pd.read_csv("data/warehouse/fact_sales.csv")

forecast = SalesForecasting()

monthly = forecast.prepare_monthly_data(fact)

result = forecast.compare_forecast(monthly)

print(result.tail())