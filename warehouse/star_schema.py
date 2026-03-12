import pandas as pd
import numpy as np
import os

def star_schema(df):
    fact_sales = df[['order_id','customer_id', 'product_id','quantity', 'revenue', 'profit','order_date']]

    dim_customer = df[['customer_id', 'customer_name', 'region', 'country']].drop_duplicates()
    dim_product = df[['product_id', 'product_name', 'category']].drop_duplicates()
    dim_time = df[['order_date']].drop_duplicates()
    
    dim_time['year']=df['order_date'].dt.year
    dim_time['month']=df['order_date'].dt.month
    dim_time['quarter']=df['order_date'].dt.quarter
    dim_time['day']=df['order_date'].dt.day

    dim_location = df[['region', 'country']].drop_duplicates()

    return fact_sales, dim_customer,dim_product, dim_time, dim_location

    fact_sales, dim_customer, dim_product, dim_time, dim_location = star_schema(df)