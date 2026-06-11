import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

def get_bigquery_client():
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set in .env")

    return bigquery.Client()