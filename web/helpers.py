"""Shared helpers for Flask routes."""

import plotly.graph_objects as go

from config import OUNCES_PER_GRAM, get_gold_api_key
from services.gold_price_service import get_api_usage_stats, get_gold_price
from utils.formatting import format_datetime_local, format_money, format_percentage
from utils.i18n import get_lang, t


def plotly_to_html(fig: go.Figure) -> str:
    return fig.to_html(full_html=False, include_plotlyjs="cdn", config={"displayModeBar": False})


def get_price_context(force_refresh: bool = False) -> dict:
    price_data = get_gold_price(force_refresh=force_refresh)
    lang = get_lang()
    gram_price = price_data.get("current_gram_price", 0.0)
    ounce_price = price_data.get("current_ounce_price", 0.0)
    change_pct = price_data.get("change_pct")
    gram_change = price_data.get("gram_change", 0.0)

    context = {
        "price_data": price_data,
        "gram_price": gram_price,
        "ounce_price": ounce_price,
        "change_pct": change_pct,
        "gram_change": gram_change,
        "grams_per_ounce": f"{OUNCES_PER_GRAM:.1f}",
        "api_usage": get_api_usage_stats() if get_gold_api_key() else None,
    }

    if gram_price > 0:
        context["gram_display"] = format_money(gram_price, lang)
        context["ounce_display"] = format_money(ounce_price, lang)
        if change_pct is not None and abs(change_pct) > 0:
            context["delta_display"] = format_percentage(change_pct)
        if price_data.get("fetched_at"):
            context["updated_at"] = format_datetime_local(price_data["fetched_at"], lang)

    return context


def price_error_message(error_code: str | None) -> str | None:
    if not error_code:
        return None
    mapping = {
        "quota_exceeded": t("api_quota_exceeded"),
        "invalid_key": t("api_invalid_key"),
        "missing_key": t("api_key_missing"),
        "network_error": t("api_network_error"),
    }
    if error_code in mapping:
        return mapping[error_code]
    if error_code.startswith("http_"):
        return t("api_fetch_failed")
    return t("api_fetch_failed")
