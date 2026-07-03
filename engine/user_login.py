# engine/user_login.py
import streamlit as st
import os
from engine.rbac import get_user_access
from db.bigquery_client import get_bigquery_client

# BigQuery accessable?
BIGQUERY_AVAILABLE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") is not None


def login_screen():
    """
    login interface，verify user，return access info
    """
    # Sidebar login removed to avoid duplicate UI. Use central login page instead.
    return None


def get_current_access():
    return st.session_state.get("access", None)


def is_logged_in():
    access = get_current_access()
    return access is not None and access.get("is_active", False)


def get_user_tier():
    access = get_current_access()
    if access:
        return access.get("tier", "free")
    return "free"