import pandas as pd
import numpy as np
import os

class KPIEngine:

    def total_revenue(self, fact):
        return fact['revenue'].sum()
    
    def profit_margin(self, fact):
        total_revenue = fact['revenue'].sum()
        total_profit = fact['profit'].sum()

        if total_revenue ==0:
            return 0
        return total_profit/total_revenue
    
    def average_order_value(self, fact):
        return fact['revenue'].sum()/fact['order_id'].nunique()
    
    def customer_lifetime_value(self, fact, dim_customer):
        return fact.groupby('customer_id')['revenue'].sum()

    def region_performance(self, fact, dim_customer):
        merged = fact.merge(dim_customer, on = 'customer_id')
        return merged.groupby('region')['revenue'].sum()
    
    def product_performance(self, fact, dim_product):
        merged = fact.merge(dim_product, on = 'product_id')
        return merged.groupby('product_name')['revenue'].sum()
    
kpi = KPIEngine()
