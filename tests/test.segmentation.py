import pandas as pd
from analytics.segmentation import CustomerSegmentation

df = pd.read_csv("data/warehouse/fact_sales.csv")

seg = CustomerSegmentation()

rfm, centroids = seg.segment_customers(df)

rfm_labeled = seg.label_segments(rfm)

print(rfm_labeled.head())