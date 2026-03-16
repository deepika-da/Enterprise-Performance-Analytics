import pandas as pd
import numpy as np

class CustomerSegmentation:

    def create_rfm(self,fact):
        fact=fact.copy()
        fact['order_date']=pd.to_datetime(fact['order_date'])
        ref_date = fact['order_date'].max()  #ref_date is latest order date

        rfm = fact.groupby('customer_id').agg({
            'order_date' : lambda x:(ref_date - x.max()).days, #recency
            'order_id' : 'nunique', #frequency
            'revenue': 'sum' #monetary
        }).reset_index()

        rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
        return rfm
    
    def normalize(self, df):
        df_norm=df.copy()

        for col in ['recency', 'frequency', 'monetary']:
            df_norm[col] = (df_norm[col] - df_norm[col].min()) / (df_norm[col].max() -df_norm[col].min())
        return df_norm
    
    def initialize_centroids(self, data, k):
        np.random.seed(42)
        random_idx = np.random.choice(len(data), k, replace=False)

        return data[random_idx]
    
    def assign_clusters(self, data, centroids):
        distances = np.sqrt(((data[:,np.newaxis] - centroids)**2).sum(axis=2))
        return np.argmin(distances, axis = 1)
      
    def update_centroids(self, data, labels, k):
        new_centroids = np.array([data[labels == i].mean(axis=0) for i in range(k)])
        return new_centroids
    
    def kmeans(self, data, k=3, max_iters=100):
        centroids = self.initialize_centroids(data, k)

        for _ in range(max_iters):
            labels = self.assign_clusters(data, centroids)
            new_centroids = self.update_centroids(data, labels, k)
            if np.all(centroids == new_centroids):
                break
            centroids = new_centroids
        return labels, centroids
    
    def segment_customers(self,fact, k=3):
        rfm = self.create_rfm(fact)
        rfm_norm = self.normalize(rfm[['recency', 'frequency', 'monetary']])
        data = rfm_norm.values
        labels, centroids = self.kmeans(data,k)
        rfm['segment'] = labels
        return rfm, centroids
    
    def label_segments(self, rfm):
        segment_summary = rfm.groupby('segment')['monetary'].mean().sort_values(ascending=False)
        labels = {}
        labels[segment_summary.index[0]] = "High Value"
        labels[segment_summary.index[1]] = "Medium Value"
        labels[segment_summary.index[2]] = "Low Value"
        rfm['segment_label'] = rfm['segment'].map(labels)
        return rfm
    

segmentation_engine = CustomerSegmentation()

def segment_customers(fact):
    
    rfm, centroids = segmentation_engine.segment_customers(fact)
    rfm = segmentation_engine.label_segments(rfm)

    print("Customer segmentation completed!")

    return rfm, centroids
        

