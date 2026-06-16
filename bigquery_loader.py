from google.cloud import bigquery

client = bigquery.Client.from_service_account_json(
    r"E:\DAX\AI\Project AI\suburb-similarity\suburb-similarity-team\secrets\demografy-bigquery.json"
)

sql = """
SELECT *
FROM `demografy.prod_tables.a_master_view`
LIMIT 10
"""

df = client.query(sql).to_dataframe()
print(df.head())
print(f"\n总列数: {len(df.columns)}")
print(f"列名: {list(df.columns)}")