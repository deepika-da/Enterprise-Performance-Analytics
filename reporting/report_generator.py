import pandas as pd

class ReportGenerator:
    def __init__(self, kpi, monthly_data, segmentation, forecast, output_path = "data/reports/analytics_report.xlsx"):
        self.kpi = kpi
        self.monthly_data = monthly_data
        self.segmentation = segmentation
        self.forecast = forecast
        self.output_path = output_path

    def generate_report(self):

        self.monthly_data['year_month'] = pd.to_datetime(
            self.monthly_data['year_month']
        ).dt.strftime('%b-%Y')

        self.forecast['year_month'] = pd.to_datetime(
            self.forecast['year_month']
        ).dt.strftime('%b-%Y')

        with pd.ExcelWriter(self.output_path) as writer:
            #KPI_Summary
            kpi_df = pd.DataFrame(list(self.kpi.items()), columns = ['KPI', "Value"])
            kpi_df.to_excel(writer, sheet_name = 'KPI_Summary', index = False)
    
            #Revenue_Analysis
            self.monthly_data.to_excel(writer, sheet_name = "Revenue_trend_Analysis", index = False)

            #Customer_Segmentation
            self.segmentation.to_excel(writer, sheet_name = "Customer_Segmentation", index = False)

            #Forecast
            self.forecast.to_excel(writer, sheet_name = "Forecast_Analysis", index = False)

            return f"Report Generated successfully at {self.output_path}"

