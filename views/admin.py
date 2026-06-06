import streamlit as st

from services.auth_service import change_password, create_user, delete_user, list_users
from utils.i18n import t


def render(session, current_user_id: int) -> None:
    st.subheader(t("nav_admin"))
    st.caption(t("admin_subtitle"))

    users = list_users(session)

    st.markdown(f"**{t('admin_users_list')}**")
    if not users:
        st.info(t("admin_no_users"))
    else:
        for user in users:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                role = t("admin_role_admin") if user.is_admin else t("admin_role_user")
                st.markdown(f"**{user.username}** — {role}")
            with col2:
                if user.id == current_user_id:
                    st.caption(t("admin_you"))
            with col3:
                if user.id != current_user_id:
                    if st.button(
                        t("delete"),
                        key=f"delete_user_{user.id}",
                        type="secondary",
                    ):
                        delete_user(session, user.id)
                        st.success(t("admin_user_deleted"))
                        st.rerun()

    st.divider()
    st.markdown(f"**{t('admin_add_user')}**")

    with st.form("add_user_form"):
        new_username = st.text_input(t("username"))
        new_password = st.text_input(t("password"), type="password")
        is_admin = st.checkbox(t("admin_is_admin"))
        submitted = st.form_submit_button(t("save"), type="primary")

    if submitted:
        try:
            create_user(session, new_username, new_password, is_admin=is_admin)
            st.success(t("admin_user_created"))
            st.rerun()
        except ValueError as exc:
            error_key = str(exc)
            if error_key == "username_taken":
                st.error(t("admin_username_taken"))
            elif error_key == "password_too_short":
                st.error(t("admin_password_short"))
            elif error_key == "username_required":
                st.error(t("login_required"))
            else:
                st.error(t("admin_create_failed"))

    st.divider()
    st.markdown(f"**{t('admin_change_password')}**")

    with st.form("change_password_form"):
        current_password = st.text_input(t("current_password"), type="password")
        new_password = st.text_input(t("new_password"), type="password")
        confirm_password = st.text_input(t("confirm_password"), type="password")
        pwd_submitted = st.form_submit_button(t("admin_update_password"))

    if pwd_submitted:
        from services.auth_service import authenticate

        user = authenticate(session, st.session_state.username, current_password)
        if not user:
            st.error(t("admin_wrong_password"))
        elif new_password != confirm_password:
            st.error(t("admin_password_mismatch"))
        else:
            try:
                change_password(session, current_user_id, new_password)
                st.success(t("admin_password_updated"))
            except ValueError:
                st.error(t("admin_password_short"))
