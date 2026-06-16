from google.cloud import bigquery
from dotenv import load_dotenv
import os

load_dotenv()

client = bigquery.Client()

query = """
SELECT
  sa2_code,
  sa2_name,
  state
FROM
  `demografy.prod_tables.a_master_view`
LIMIT 5
"""

df = client.query(query).to_dataframe()

print(df)