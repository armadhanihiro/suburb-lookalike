import streamlit as st

from db.bigquery_client import get_bigquery_client
from engine.rbac import get_user_access


def login_screen():
    if st.session_state.get("access"):
        access = st.session_state.access
        user_id = access.get("user_id", "")

        st.sidebar.write(f"👋 Welcome, **{user_id}**")

        if st.sidebar.button("Logout", use_container_width=True):
            st.session_state.access = None
            st.rerun()

        return access

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("# 🏘️ Demografy")
        st.title("🔐 Welcome to Demografy")
        st.markdown(
            "Please log in to access the Suburb Look-alike Finder."
        )

        with st.form("login_form"):
            login_id = st.text_input(
                "Email or User ID",
                placeholder="Enter your registered email or user ID",
            ).strip()

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
            )

            submitted = st.form_submit_button(
                "Login",
                use_container_width=True,
            )

        if submitted:
            if not login_id:
                st.error("Please enter your email or user ID.")
                return None

            if not password:
                st.error("Please enter your password.")
                return None

            try:
                client = get_bigquery_client()
                user_access = get_user_access(
                    login_id,
                    client=client,
                )
            except Exception as error:
                st.error(f"Database connection error: {error}")
                return None

            if user_access is None:
                st.warning(
                    "🔑 No account found with this email or user ID."
                )
                return None

            if not user_access.get("is_active", False):
                st.error(
                    "⛔ Your account is inactive. "
                    "Please contact support."
                )
                return None

            st.success(f"Welcome back, {login_id}!")
            return user_access

        st.caption(
            "New user? Contact your administrator to get access."
        )

    return None


def is_logged_in():
    access = st.session_state.get("access")
    return bool(access and access.get("is_active", False))


def get_current_access():
    return st.session_state.get("access")


def get_user_tier():
    access = get_current_access()

    if access:
        return access.get("tier", "free")

    return "free"