import os
from ingestion.ingest import ingest_data
from cleaning.data_cleaner import DataCleaner
from warehouse.star_schema import star_schema


def run_pipeline():

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

    # Step 4: Save to CSV
    output_path = "data/warehouse"
    os.makedirs(output_path, exist_ok=True)

    fact_sales.to_csv(os.path.join(output_path, "fact_sales.csv"), index=False)
    dim_customer.to_csv(os.path.join(output_path, "dim_customer.csv"), index=False)
    dim_product.to_csv(os.path.join(output_path, "dim_product.csv"), index=False)
    dim_time.to_csv(os.path.join(output_path, "dim_time.csv"), index=False)
    dim_location.to_csv(os.path.join(output_path, "dim_location.csv"), index=False)

    print("Fact and Dimension tables saved successfully!")
    print("ETL Pipeline completed successfully!")
