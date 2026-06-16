from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

client = bigquery.Client()

table = client.get_table(
    "demografy.prod_tables.a_master_view"
)

for schema in table.schema:
    print(
        schema.name,
        schema.field_type
    )