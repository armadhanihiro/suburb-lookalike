# engine/user_login.py
import streamlit as st
import os
from engine.rbac import get_user_access
from db.bigquery_client import get_bigquery_client

BIGQUERY_AVAILABLE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") is not None


def login_screen():
    """显示登录界面，返回用户 access 信息（不触发重载）"""
    print("  -> 进入 login_screen")
    
    # 如果已经登录，只显示欢迎信息和登出按钮，直接返回 access
    if "access" in st.session_state and st.session_state.access:
        print("  -> 用户已登录，显示欢迎信息")
        access = st.session_state.access
        user_id = access.get("user_id", "")
        st.sidebar.write(f"👋 Welcome, **{user_id}**")
        if st.sidebar.button("Logout", use_container_width=True):
            st.session_state.access = None
            # 注意：这里不调用 st.rerun()
            return None
        return access

    # 未登录：显示登录表单
    print("  -> 用户未登录，显示登录表单")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("# 🏘️ Demografy")
        st.title("🔐 Welcome to Demografy")
        st.markdown("Please log in to access the Suburb Look-alike Finder.")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your registered email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                if not email:
                    st.error("Please enter your email")
                    return None
                
                try:
                    client = get_bigquery_client()
                    user_access = get_user_access(email, client=client)
                except Exception as e:
                    st.error(f"Database connection error: {e}")
                    return None
                
                if user_access is None:
                    st.warning("🔑 No account found with this email. Please register first.")
                    st.caption("Contact your administrator to create an account.")
                    return None
                
                if user_access.get("is_active", False):
                    st.success(f"Welcome back, {email}!")
                    return user_access
                else:
                    st.error("⛔ Your account is inactive. Please contact support.")
                    return None
        
        st.caption("New user? Contact your administrator to get access.")
    
    return None


def is_logged_in():
    access = st.session_state.get("access", None)
    return access is not None and access.get("is_active", False)


def get_current_access():
    return st.session_state.get("access", None)


def get_user_tier():
    access = get_current_access()
    if access:
        return access.get("tier", "free")
    return "free"