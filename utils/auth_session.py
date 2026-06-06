import hashlib
import hmac
import time

import streamlit as st
from extra_streamlit_components import CookieManager

from config import get_cookie_secret
from db.database import get_session
from services.auth_service import get_user_by_id

COOKIE_NAME = "gold_session"
COOKIE_MAX_AGE_DAYS = 30


def get_cookie_manager() -> CookieManager:
    if "cookie_manager" not in st.session_state:
        st.session_state.cookie_manager = CookieManager()
    return st.session_state.cookie_manager


def _sign_payload(payload: str) -> str:
    secret = get_cookie_secret()
    sig = hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{payload}:{sig}"


def _verify_signed_token(token: str) -> str | None:
    if not token or ":" not in token:
        return None
    payload, sig = token.rsplit(":", 1)
    expected = hmac.new(
        get_cookie_secret().encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(sig, expected):
        return None
    return payload


def create_session_token(user_id: int) -> str:
    expiry = int(time.time()) + COOKIE_MAX_AGE_DAYS * 86400
    return _sign_payload(f"{user_id}:{expiry}")


def parse_session_token(token: str) -> int | None:
    payload = _verify_signed_token(token)
    if not payload:
        return None
    try:
        user_id_str, expiry_str = payload.split(":", 1)
        if int(expiry_str) < int(time.time()):
            return None
        return int(user_id_str)
    except (TypeError, ValueError):
        return None


def set_logged_in(user: object) -> None:
    st.session_state.user_id = user.id
    st.session_state.username = user.username
    st.session_state.is_admin = user.is_admin
    token = create_session_token(user.id)
    get_cookie_manager().set(
        COOKIE_NAME,
        token,
        max_age=COOKIE_MAX_AGE_DAYS * 86400,
    )


def clear_logged_in() -> None:
    for key in ("user_id", "username", "is_admin"):
        st.session_state.pop(key, None)
    get_cookie_manager().delete(COOKIE_NAME)


def is_logged_in() -> bool:
    return bool(st.session_state.get("user_id"))


def restore_session_from_cookie() -> bool:
    """Restore login from cookie. Returns False while cookies are still loading."""
    if is_logged_in():
        return True

    cookies = get_cookie_manager().get_all()
    if cookies is None:
        return False

    token = cookies.get(COOKIE_NAME)
    if not token:
        return True

    user_id = parse_session_token(token)
    if not user_id:
        return True

    session = get_session()
    try:
        user = get_user_by_id(session, user_id)
        if user:
            st.session_state.user_id = user.id
            st.session_state.username = user.username
            st.session_state.is_admin = user.is_admin
    finally:
        session.close()

    return True


def logout() -> None:
    clear_logged_in()
