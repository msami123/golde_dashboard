import streamlit as st
from config import GOLD_API_MONTHLY_LIMIT, OUNCES_PER_GRAM, get_gold_api_key
from db.database import get_session, init_db
from views import admin, gold_bars, login, overview, shared_ownership
from services.gold_price_service import get_api_usage_stats, get_gold_price
from utils.auth_session import is_logged_in, logout, restore_session_from_cookie
from utils.cards import render_daily_price_change
from utils.formatting import format_datetime_local, format_money, format_percentage, ltr_text
from utils.i18n import apply_rtl_css, get_lang, t

st.set_page_config(
    page_title="لوحة ذهب ذكية | Smart Gold",
    page_icon="🥇",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_db()

if "lang" not in st.session_state:
    st.session_state.lang = "ar"

if "page" not in st.session_state:
    st.session_state.page = "overview"

if "privacy_mode" not in st.session_state:
    st.session_state.privacy_mode = False

apply_rtl_css()

if not is_logged_in() and not restore_session_from_cookie():
    st.stop()

if not is_logged_in():
    login.render()
    st.stop()

user_id = st.session_state.user_id
username = st.session_state.username
is_admin = st.session_state.is_admin

with st.sidebar:
    st.markdown(f"## 🥇 {t('app_title')}")
    st.caption(t("app_subtitle"))
    st.caption(f"**{t('logged_in_as')}:** {username}")

    if st.button(t("logout"), width="stretch"):
        logout()
        st.rerun()

    st.divider()

    lang_choice = st.radio(
        t("language"),
        options=["ar", "en"],
        format_func=lambda x: "العربية" if x == "ar" else "English",
        index=0 if get_lang() == "ar" else 1,
        horizontal=True,
    )
    if lang_choice != st.session_state.lang:
        st.session_state.lang = lang_choice
        st.rerun()

    st.divider()

    refresh_clicked = st.button(t("refresh_price"))
    price_data = get_gold_price(force_refresh=refresh_clicked)

    gram_price = price_data.get("current_gram_price", 0.0)
    ounce_price = price_data.get("current_ounce_price", 0.0)
    change_pct = price_data.get("change_pct")
    gram_change = price_data.get("gram_change", 0.0)

    st.markdown(f"### {t('current_gold_price')}")
    if gram_price > 0:
        delta = None
        if change_pct is not None and abs(change_pct) > 0:
            delta = format_percentage(change_pct)
        st.metric(t("per_gram"), format_money(gram_price, get_lang()), delta=delta)
        if "gram_change" in price_data:
            render_daily_price_change(gram_change, change_pct)
        grams_per_ounce = f"{OUNCES_PER_GRAM:.1f}"
        if get_lang() == "ar":
            ounce_grams_text = f"الأونصة = {grams_per_ounce} جرام"
        else:
            ounce_grams_text = f"1 oz = {grams_per_ounce} g"
        lang = get_lang()
        st.caption(
            f"{t('per_ounce')}: {ltr_text(format_money(ounce_price, lang))} — {ounce_grams_text}"
        )
        if price_data.get("fetched_at"):
            updated_at = format_datetime_local(price_data["fetched_at"], lang)
            st.caption(
                f"{t('last_updated')}: {ltr_text(updated_at)} — {t('saudi_time')}"
            )
        if price_data.get("stale"):
            st.warning(t("price_stale"))
        error_code = price_data.get("error")
        if error_code == "quota_exceeded":
            st.error(t("api_quota_exceeded"))
        elif error_code == "invalid_key":
            st.error(t("api_invalid_key"))
        elif error_code == "missing_key":
            st.info(t("api_key_missing"))
        elif error_code == "network_error":
            st.error(t("api_network_error"))
        elif error_code and error_code.startswith("http_"):
            st.error(t("api_fetch_failed"))
    else:
        st.warning(t("price_unavailable"))
        error_code = price_data.get("error")
        if not get_gold_api_key() or error_code == "missing_key":
            st.info(t("api_key_missing"))
        elif error_code == "quota_exceeded":
            st.error(t("api_quota_exceeded"))
        elif error_code:
            st.error(t("api_fetch_failed"))

    if get_gold_api_key():
        usage = get_api_usage_stats()
        st.caption(f"**{t('api_usage_title')}**")
        st.caption(f"{t('api_usage_month')}: {usage['month_total']}")
        st.caption(f"{t('api_usage_total')}: {usage['all_time']}")
        if usage["last"]:
            last_label = (
                t("api_usage_last_ok")
                if usage["last"].get("success")
                else t("api_usage_last_fail")
            )
            st.caption(last_label)
        st.caption(t("api_usage_limit_hint").format(limit=GOLD_API_MONTHLY_LIMIT))

    st.divider()

    pages = {
        "overview": t("nav_overview"),
        "gold_bars": t("nav_gold_bars"),
        "shared_ownership": t("nav_shared_ownership"),
    }
    if is_admin:
        pages["admin"] = t("nav_admin")

    for page_key, label in pages.items():
        is_active = st.session_state.page == page_key
        if st.button(
            label,
            type="primary" if is_active else "secondary",
            width="stretch",
            key=f"nav_{page_key}",
        ):
            st.session_state.page = page_key
            st.rerun()

session = get_session()
try:
    eye_icon = "🔒" if st.session_state.privacy_mode else "👁️"
    st.markdown('<div class="privacy-eye-top-spacer"></div>', unsafe_allow_html=True)
    _, eye_col, _ = st.columns([9, 1, 0.6])
    with eye_col:
        if st.button(eye_icon, key="privacy_eye", help=t("privacy_mode_hint")):
            st.session_state.privacy_mode = not st.session_state.privacy_mode
            st.rerun()

    current_page = st.session_state.page

    if current_page in ("overview", "analytics", "forecasting"):
        overview.render(session, gram_price, user_id, price_data)
    elif current_page == "gold_bars":
        gold_bars.render(session, gram_price, user_id)
    elif current_page == "shared_ownership":
        shared_ownership.render(session, gram_price, user_id)
    elif current_page == "admin" and is_admin:
        admin.render(session, user_id)
    elif current_page == "admin":
        st.error(t("admin_forbidden"))
        st.session_state.page = "overview"
        st.rerun()
finally:
    session.close()
