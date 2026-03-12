import pandas as pd
import numpy as np
import os

class statistical_analysis:
    def correlation(self, df):
       numeric_cols = df.select_dtypes(include=[np.number])
       return numeric_cols.corr()
    
    def revenue_trend(self,fact):
        fact = fact.copy()
        fact['order_date']= pd.to_datetime(fact['order_date'])
        fact['year_month'] = fact['order_date'].dt.to_period('M')

        trend = fact.groupby('year_month')['revenue'].sum().reset_index()
        return trend

    def cohort_analysis(self, fact):
        fact =fact.copy()
        fact['order_date'] = pd.to_datetime(fact['order_date'])
        fact['cohort_month'] = fact.groupby('customer_id')['order_date'].transform('min').dt.to_period('M')
        fact['order_month']=fact['order_date'].dt.to_period('M')

        fact['cohort_index'] = (fact['order_month'].dt.year - fact['cohort_month'].dt.year) * 12 + (fact['order_month'].dt.month - fact['cohort_month'].dt.month)

        cohort = fact.groupby(['cohort_month', 'cohort_index'])['customer_id'].nunique().reset_index()
        cohort_pivot = cohort.pivot(index = 'cohort_month', columns = 'cohort_index', values = 'customer_id')
        return cohort_pivot
    
    def t_test(self, group1, group2):
        group1=np.array(group1)
        group2=np.array(group2)

        mean1=np.mean(group1)
        mean2 = np.mean(group2)
        mean2 = np.array(mean2)

        var1=np.var(group1,ddof=1)
        var2=np.var(group2,ddof=1)

        n1=len(group1)
        n2=len(group2)
         
        t_stat = (mean1 - mean2) / np.sqrt((var1 / n1) + (var2 / n2))
        return t_stat
    
    def regional_ttest(self, fact, dim_customer, region1, region2):
        merged = fact.merge(dim_customer, on='customer_id')
        group1 = merged[merged['region']==region1]['revenue']
        group2= merged[merged['region']==region2]['revenue']

        return self.t_test(group1,group2)
    
    def descriptive_stats(self,fact):
        return fact.describe()
    

    def save_report(self, fact, output_path="data/reports/statistical_report.csv"):
        stats = fact.describe()
        stats.to_csv(output_path)
        return f"Report saved to {output_path}"