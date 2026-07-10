import os

import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account


def get_bigquery_client():
    if "gcp_service_account" in st.secrets:
        credentials = service_account.Credentials.from_service_account_info(
            dict(st.secrets["gcp_service_account"])
        )

        return bigquery.Client(
            credentials=credentials,
            project=credentials.project_id,
        )

    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if credentials_path:
        return bigquery.Client.from_service_account_json(
            credentials_path
        )

    raise RuntimeError(
        "BigQuery credentials are not configured."
    )