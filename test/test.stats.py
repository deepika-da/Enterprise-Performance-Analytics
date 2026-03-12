import pandas as pd
import analytics
from analytics.statistical_analysis import statistical_analysis

fact = pd.read_csv('data/warehouse/fact_sales.csv')
dim_customer = pd.read_csv('data/warehouse/dim_customer.csv')

analysis = statistical_analysis()

print("\nCorrelation Matrix:")
print(analysis.correlation(fact))

print("\nRevenue Trend:")
print(analysis.revenue_trend(fact))

print("\nCohort Analysis:")
print(analysis.cohort_analysis(fact))

print("\nDescriptive Statistics:")
print(analysis.descriptive_stats(fact))

print("\nRegional T-Test (South vs North):")
print(analysis.regional_ttest(fact, dim_customer, "South", "North"))