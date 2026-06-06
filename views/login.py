import streamlit as st

from db.database import get_session
from services.auth_service import authenticate
from utils.auth_session import set_logged_in
from utils.i18n import apply_rtl_css, t


def render() -> None:
    apply_rtl_css()

    st.markdown(
        f"""
        <div style="text-align:center; padding: 2rem 0 1rem;">
            <div style="font-size:3rem;">🥇</div>
            <h1 style="margin:0.5rem 0;">{t("app_title")}</h1>
            <p style="opacity:0.7;">{t("login_subtitle")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, col, _ = st.columns([1, 2, 1])
    with col:
        with st.form("login_form"):
            username = st.text_input(t("username"), autocomplete="username")
            password = st.text_input(
                t("password"),
                type="password",
                autocomplete="current-password",
            )
            submitted = st.form_submit_button(t("login"), type="primary", use_container_width=True)

        if submitted:
            if not username.strip() or not password:
                st.error(t("login_required"))
            else:
                session = get_session()
                try:
                    user = authenticate(session, username, password)
                finally:
                    session.close()

                if user:
                    set_logged_in(user)
                    st.rerun()
                else:
                    st.error(t("login_failed"))
