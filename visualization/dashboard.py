import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Dashboard:
    def revenue_trend_chart(self, monthly_data):
        plt.figure()
        plt.plot(monthly_data['year_month'], monthly_data['revenue'], label = 'Actual Revenue')
        plt.title('Monthly Revenue Trend')
        plt.xlabel('Month')
        plt.ylabel('Revenue')
        plt.xticks(rotation = 45)
        plt.tight_layout()
        plt.show()

    def kpi_chart(self, kpi_dict):
        plt.figure()
        names=list(kpi_dict.keys())
        values=list(kpi_dict.values())
        plt.bar(names, values)
        plt.title('KPI Overview')
        plt.xticks(rotation = 45)
        plt.tight_layout()
        plt.show()

    def segmentation_chart(self, rfm):
        segment_counts= rfm['segment'].value_counts()
        plt.figure()
        plt.pie(segment_counts.values, labels = segment_counts.index, autopct = '%1.1f%%')
        plt.title('Customer_Segemnetation')
        plt.tight_layout()
        plt.show()
        
    def region_heatmap(self, region_data):
        pivot= region_data.pivot_table(values= 'revenue', index='region',aggfunc='sum')
        plt.figure()
        plt.imshow(pivot, aspect = 'auto')
        plt.colorbar(label='Revenue')
        plt.yticks(range(len(pivot.index)), pivot.index)
        plt.xticks([])
        plt.title('Revenue by Region')
        plt.tight_layout()
        plt.show()

    def forecast_chart(self, forecast_data):
        plt.figure()
        plt.plot(forecast_data['year_month'], forecast_data['revenue'], label = 'Actual Revenue')
        plt.plot(forecast_data['year_month'], forecast_data['moving_average'], label = 'Moving Average')
        plt.plot(forecast_data['year_month'], forecast_data['Exp_smoothing'], label = 'Exp Smoothing')
        plt.legend()
        plt.title('Forecast vs Actual')
        plt.xlabel('Month')
        plt.ylabel('Revenue')
        plt.xticks(rotation = 45)
        plt.tight_layout()
        plt.show()  

        