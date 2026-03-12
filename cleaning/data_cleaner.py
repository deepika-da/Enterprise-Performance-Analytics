import pandas as pd
import numpy as np


class DataCleaner:

    def handle_missings(self, df, strategy="median"):
        for col in df.select_dtypes(include=np.number):
            if strategy == "mean":
                df[col] = df[col].fillna(df[col].mean())
            elif strategy == "median":
                df[col] = df[col].fillna(df[col].median())

        return df

    def remove_duplicates(self, df):
        before = df.shape[0]
        df = df.drop_duplicates()   # ✅ FIXED (you missed assignment)
        after = df.shape[0]

        print(f"Duplicates removed: {before - after}")
        return df

    def convert_types(self, df):
        if "order_date" in df.columns:
            df["order_date"] = pd.to_datetime(df["order_date"])

        return df

    def text_columns(self, df):
        text_cols = df.select_dtypes(include="object").columns

        for col in text_cols:
            df[col] = df[col].str.strip().str.title()

        return df
