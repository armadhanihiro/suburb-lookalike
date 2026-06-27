import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv
import os

load_dotenv()

def get_bigquery_client():
    return bigquery.Client.from_service_account_json(
        r"E:\DAX\AI\Project AI\suburb-similarity\suburb-similarity-team\secrets\demografy-bigquery.json"
    )

def explore_dev_customers():
    client = get_bigquery_client()
    
    query = """
    SELECT *
    FROM `demografy.ref_tables.dev_customers`
    LIMIT 20
    """
    
    df = client.query(query).to_dataframe()
    
    print("=" * 60)
    print("dev_customers basic info")
    print("=" * 60)
    print(f"total rows: {len(df)}")
    print(f"Column names: {df.columns.tolist()}")
    
    print("\n" + "=" * 60)
    print("First 5 rows")
    print("=" * 60)
    print(df.head())
    
    print("\n" + "=" * 60)
    print("user_id unique values")
    print("=" * 60)
    print(df["user_id"].unique())
    
    print("\n" + "=" * 60)
    print("tier distribution")
    print("=" * 60)
    print(df["tier"].value_counts())
    
    print("\n" + "=" * 60)
    print("is_active distribution")
    print("=" * 60)
    print(df["is_active"].value_counts())
    
    print("\n" + "=" * 60)
    print("Specific user query example: user_017")
    print("=" * 60)
    sample = df[df["user_id"] == "user_017"]
    if not sample.empty:
        print(sample[["user_id", "email", "tier", "is_active"]].to_dict(orient="records"))
    else:
        print("user_017 does not exist in the table")

if __name__ == "__main__":
    explore_dev_customers()