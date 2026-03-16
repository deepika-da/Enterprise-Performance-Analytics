import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.drawing.image import Image

class ReportGenerator:

    def __init__(self, kpi, monthly_data, segmentation, forecast, output_path="data/reports/analytics_report.xlsx"):
        self.kpi = kpi
        self.monthly_data = monthly_data
        self.segmentation = segmentation
        self.forecast = forecast
        self.output_path = output_path


    def generate(self):

        # Format month column
        date_col = self.monthly_data.columns[0]
        self.monthly_data[date_col] = pd.to_datetime(
            self.monthly_data[date_col]
        ).dt.strftime('%b-%Y')

        date_col = self.forecast.columns[0]
        self.forecast[date_col] = pd.to_datetime(
            self.forecast[date_col]
        ).dt.strftime('%b-%Y')

        with pd.ExcelWriter(self.output_path, engine="xlsxwriter") as writer:

            # ---- KPI SUMMARY (only scalar KPIs) ----
            summary = {
                "total_revenue": self.kpi["total_revenue"],
                "profit_margin": self.kpi["profit_margin"],
                "average_order_value": self.kpi["average_order_value"]
            }

            summary_df = pd.DataFrame(summary.items(), columns=["KPI", "Value"])
            summary_df.to_excel(writer, sheet_name="KPI_Summary", index=False)


            # ---- CUSTOMER LIFETIME VALUE ----
            clv = self.kpi["customer_lifetime_value"].reset_index()
            clv.columns = ["customer_id", "revenue"]
            clv.to_excel(writer, sheet_name="Customer_Lifetime_Value", index=False)


            # ---- REGION PERFORMANCE ----
            region_perf = self.kpi["region_performance"].reset_index()
            region_perf.columns = ["region", "revenue"]
            region_perf.to_excel(writer, sheet_name="Region_Performance", index=False)


            # ---- PRODUCT PERFORMANCE ----
            product_perf = self.kpi["product_performance"].reset_index()
            product_perf.columns = ["product_name", "revenue"]
            product_perf.to_excel(writer, sheet_name="Product_Performance", index=False)


            # ---- REVENUE TREND ----
            self.monthly_data.to_excel(writer, sheet_name="Revenue_Trend", index=False)


            # ---- CUSTOMER SEGMENTATION ----
            self.segmentation.to_excel(writer, sheet_name="Customer_Segmentation", index=False)


            # ---- FORECAST ----
            self.forecast.to_excel(writer, sheet_name="Forecast_Analysis", index=False)

            # ---- CHARTS SHEET ----
            workbook = writer.book
            charts_sheet = workbook.add_worksheet("Charts")

            # Insert charts if they exist
            charts = [
                ("data/reports/revenue_trend.png", "B2"),
                ("data/reports/kpi_chart.png", "B35"),
                ("data/reports/segmentation_chart.png", "B68"),
                ("data/reports/forecast_chart.png", "B101"),
                ("data/reports/region_heatmap.png", "B134")
            ]
        
            for chart_path, position in charts:
                if os.path.exists(chart_path):
                    charts_sheet.insert_image(position, chart_path)

        print(f"Report Generated successfully at {self.output_path}")