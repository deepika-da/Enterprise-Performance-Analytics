import os

from ingestion.ingest import ingest_data
from cleaning.data_cleaner import DataCleaner
from warehouse.star_schema import star_schema

# analytics modules
from analytics.kpi_engine import calculate_kpis
from analytics.segmentation import segment_customers
from analytics.forecasting import forecast_sales
from analytics.statistical_analysis import sales_statistics

# visualization
from visualization.dashboard import create_dashboard

# reporting
from reporting.report_generator import ReportGenerator


def run_pipeline():

    print("===== Enterprise Performance Analytics Pipeline =====")

    # Step 1: Ingest
    df = ingest_data()

    # Step 2: Clean
    cleaner = DataCleaner()
    df = cleaner.handle_missings(df, strategy="median")
    df = cleaner.remove_duplicates(df)
    df = cleaner.convert_types(df)
    df = cleaner.text_columns(df)

    print("Cleaning completed successfully!")

    # Step 3: Star Schema
    fact_sales, dim_customer, dim_product, dim_time, dim_location = star_schema(df)

    print("Star schema created successfully!")

    # Step 4: Save to Warehouse
    output_path = "data/warehouse"
    os.makedirs(output_path, exist_ok=True)

    fact_sales.to_csv(os.path.join(output_path, "fact_sales.csv"), index=False)
    dim_customer.to_csv(os.path.join(output_path, "dim_customer.csv"), index=False)
    dim_product.to_csv(os.path.join(output_path, "dim_product.csv"), index=False)
    dim_time.to_csv(os.path.join(output_path, "dim_time.csv"), index=False)
    dim_location.to_csv(os.path.join(output_path, "dim_location.csv"), index=False)

    print("Fact and Dimension tables saved successfully!")

    # Step 5: Analytics
    kpi = calculate_kpis(fact_sales, dim_customer, dim_product)
    segmentation_df, centroids = segment_customers(fact_sales)
    stats = sales_statistics(fact_sales)

    print("Analytics modules executed!")

    # Step 6: Forecasting
    forecast_value, forecast_df = forecast_sales(fact_sales)
    monthly_data = forecast_df[['year_month','revenue']]
    print("Forecasting completed!")
    
    # Step 7: Visualization

    fact_with_region = fact_sales.merge(
        dim_customer[['customer_id', 'region']],
        on='customer_id',
        how='left'
    )

    create_dashboard(
        fact_sales,
        kpi=kpi,
        segmentation=segmentation_df,
        forecast=forecast_df,
        region_data=fact_with_region
    )

    
    print("Dashboard generated!")

    # Step 8: Reporting
    report = ReportGenerator(kpi, monthly_data, segmentation_df, forecast_df)
    report.generate()

    print("Report generated successfully!")

    print("Enterprise Analytics Pipeline Completed Successfully!")