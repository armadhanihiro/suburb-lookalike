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
    st.image("assets/demografy-logo.png", width=200)
    st.sidebar.title("🔐 Login")
    
    email = st.sidebar.text_input("Email", placeholder="Enter your email")
    password = st.sidebar.text_input("Password", type="password", placeholder="Enter your password (demo: any)")
    
    login_btn = st.sidebar.button("Login", use_container_width=True)
    
    if login_btn:
        if not email:
            st.sidebar.error("Please enter your email")
            return None
        
        # query dev_customers table
        if BIGQUERY_AVAILABLE:
            try:
                client = get_bigquery_client()
                user_access = get_user_access(email, client=client)
            except Exception as e:
                st.sidebar.error(f"Database error: {e}")
                return None
            
            if user_access and user_access.get("is_active", False):
                st.sidebar.success(f"Welcome, {email}!")
                return user_access
            else:
                st.sidebar.error("Invalid email or inactive account. Please contact your administrator.")
                return None
        # 显示当前用户信息（如果已登录）
    if "access" in st.session_state and st.session_state.access:
        access = st.session_state.access
        st.sidebar.info(f"✅ Logged in as: {access.get('user_id', '')}")
        st.sidebar.caption(f"Tier: {access.get('tier', 'free')}")
        remaining = access.get('lookup_limit', 0) - access.get('lookups_used', 0)
        st.sidebar.caption(f"Remaining lookups: {remaining}")
        
        if st.sidebar.button("Logout", use_container_width=True):
            st.session_state.access = None
            st.rerun()
    
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