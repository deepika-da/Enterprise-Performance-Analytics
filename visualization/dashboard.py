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
        plt.savefig("data/reports/revenue_trend.png")
        plt.close()

    def kpi_chart(self, kpi_dict):
        
        # Keep only numeric KPIs
        numeric_kpis = {}

        for key, value in kpi_dict.items():
            # accept only numbers
            if isinstance(value, (int, float, np.number)):
                numeric_kpis[key] = float(value)

        if len(numeric_kpis) == 0:
            print("No numeric KPIs found for chart.")
            return
        
        names=list(numeric_kpis.keys())
        values=list(numeric_kpis.values())

        plt.figure()
        plt.bar(names, values)
        plt.title('KPI Overview')
        plt.xticks(rotation = 45)
        plt.tight_layout()
        plt.savefig("data/reports/kpi_chart.png")
        plt.close()

    def segmentation_chart(self, rfm):
        segment_counts= rfm['segment'].value_counts()
        plt.figure()
        plt.pie(segment_counts.values, labels = segment_counts.index, autopct = '%1.1f%%')
        plt.title('Customer_Segemnetation')
        plt.tight_layout()
        plt.savefig("data/reports/segmentation_chart.png")
        plt.close()
        
    def region_heatmap(self, fact_data):

        region_summary = fact_data.groupby('region')['revenue'].sum().reset_index()

        pivot = region_summary.set_index('region')

        plt.figure()
        plt.imshow(pivot, aspect='auto')
        plt.colorbar(label='Revenue')
        plt.yticks(range(len(pivot.index)), pivot.index)
        plt.xticks([])
        plt.title('Revenue by Region')
        plt.tight_layout()

        plt.savefig("data/reports/region_heatmap.png")
        plt.close()

    def forecast_chart(self, forecast_data):
        plt.figure()
        plt.plot(forecast_data['year_month'], forecast_data['revenue'], label = 'Actual Revenue')
        plt.plot(forecast_data['year_month'], forecast_data['moving_avg'], label = 'Moving Average')
        plt.plot(forecast_data['year_month'], forecast_data['exp_smoothing'], label = 'Exp Smoothing')
        plt.legend()
        plt.title('Forecast vs Actual')
        plt.xlabel('Month')
        plt.ylabel('Revenue')
        plt.xticks(rotation = 45)
        plt.tight_layout()
        plt.savefig("data/reports/forecast_chart.png")
        plt.close()  

dashboard_engine = Dashboard()

def create_dashboard(fact, kpi=None, segmentation=None, forecast=None, region_data=None):

    print("Generating dashboard visualizations...")

    # Example revenue trend (monthly)
    fact = fact.copy()
    fact['order_date'] = pd.to_datetime(fact['order_date'])
    fact['year_month'] = fact['order_date'].dt.to_period('M')

    monthly = fact.groupby('year_month')['revenue'].sum().reset_index()
    monthly['year_month'] = monthly['year_month'].dt.to_timestamp()

    dashboard_engine.revenue_trend_chart(monthly)

    if kpi is not None:
        dashboard_engine.kpi_chart(kpi)

    if segmentation is not None:
        dashboard_engine.segmentation_chart(segmentation)

    if forecast is not None:
        dashboard_engine.forecast_chart(forecast)

    if region_data is not None:
        dashboard_engine.region_heatmap(region_data)

    print("Dashboard generated successfully!")        