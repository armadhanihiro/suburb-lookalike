import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv
import os

load_dotenv()

client = bigquery.Client.from_service_account_json(
    r"E:\DAX\AI\Project AI\suburb-similarity\suburb-similarity-team\secrets\demografy-bigquery.json"
)

# project name
sql = """
SELECT *
FROM `demografy.prod_tables.a_master_view`
"""

df = client.query(sql).to_dataframe()

print("=" * 50)
print("1. basic info about the dataset")
print("=" * 50)
print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Column names: {list(df.columns)}")

print("\n" + "=" * 50)
print("2. KPI columns summary")
print("=" * 50)
numeric_cols = df.select_dtypes(include=['number']).columns
for col in numeric_cols:
    print(f"{col}: min={df[col].min():.2f}, max={df[col].max():.2f}, mean={df[col].mean():.2f}")

print("\n" + "=" * 50)
print("3. null value statistics")
print("=" * 50)
missing = df.isnull().sum()
missing_pct = 100 * missing / len(df)
missing_df = pd.DataFrame({'null value count': missing, 'null value percentage': missing_pct})
print(missing_df[missing_df['null value count'] > 0])

print("\n" + "=" * 50)
print("4. sa2_name repeat statistics")
print("=" * 50)
duplicate_sa2 = df[df.duplicated(['sa2_name'], keep=False)]
print(f"Duplicate sa2_name rows: {len(duplicate_sa2)}")
if len(duplicate_sa2) > 0:
    print("\nDuplicate examples:")
    print(duplicate_sa2[['sa2_name']].head(10))

print("\n" + "=" * 50)
print("5. Valid suburb count (unique sa2_name values)")
print("=" * 50)
print(f"Unique suburb count: {df['sa2_name'].nunique()}")

# 新增 state 分析
print("\n" + "=" * 50)
print("STATE COLUMN ANALYSIS")
print("=" * 50)
print("unique count state：")
print(df["state"].value_counts())
print("\n unique count state：")
print(df["state"].unique())