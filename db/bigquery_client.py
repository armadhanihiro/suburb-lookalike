import os

import streamlit as st
from dotenv import load_dotenv
from google.cloud import bigquery
from google.oauth2 import service_account


load_dotenv()


def get_bigquery_client():
    """
    Create a BigQuery client.

    Local development:
    - Uses GOOGLE_APPLICATION_CREDENTIALS from .env.

    Streamlit Cloud:
    - Uses the gcp_service_account section from st.secrets.
    """

    credentials_path = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS"
    )

    # Local development
    if credentials_path:
        return bigquery.Client.from_service_account_json(
            credentials_path
        )

    # Streamlit Community Cloud
    try:
        service_account_info = dict(
            st.secrets["gcp_service_account"]
        )
    except (FileNotFoundError, KeyError):
        service_account_info = None
    except Exception:
        service_account_info = None

    if service_account_info:
        credentials = (
            service_account.Credentials
            .from_service_account_info(
                service_account_info
            )
        )

        return bigquery.Client(
            credentials=credentials,
            project=credentials.project_id,
        )

    raise RuntimeError(
        "BigQuery credentials are not configured. "
        "For local development, set "
        "GOOGLE_APPLICATION_CREDENTIALS in .env. "
        "For Streamlit Cloud, configure "
        "[gcp_service_account] in app secrets."
    )