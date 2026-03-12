import pandas as pd
import numpy as np

class SalesForecasting:
    def prepare_monthly_data(self, fact):
        fact=fact.copy()
        fact['order_date'] = pd.to_datetime(fact['order_date'])
        fact['year_month'] =fact['order_date'].dt.to_period('M')
        monthly = fact.groupby('year_month')['revenue'].sum().reset_index()
        monthly['year_month'] = monthly['year_month'].dt.to_timestamp()
        return monthly
    
    def moving_average(self, series, window):
        return series.rolling(window=window).mean()
    
    def exponential_smoothing(self, series, alpha=0.3):
        result = [series.iloc[0]]
        for i in range(1,len(series)):
            value= alpha* series.iloc[i] + (1-alpha) * result[i-1]
            result.append(value)
        return pd.Series(result, index=series.index)
    
    def forecast_next(self, series, alpha=0.3):
        smoothed = self.exponential_smoothing(series, alpha)
        return smoothed.iloc[-1]
    
    def forecast_next(self, series, alpha=0.3):
        smoothed = self.exponential_smoothing(series, alpha)
        return smoothed.iloc[-1]
    
    def compare_forecast(self, monthly_data, window =3, alpha=0.3):
        monthly_data = monthly_data.copy()
        monthly_data['moving_avg'] = self.moving_average(monthly_data['revenue'], window)
        monthly_data['exp_smoothing'] = self.exponential_smoothing(monthly_data['revenue'],alpha)
        return monthly_data