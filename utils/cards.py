import streamlit as st

from utils.formatting import (
    format_date_local,
    format_money,
    format_percentage,
    format_weight,
)
from utils.i18n import get_lang, t
from utils.privacy import is_privacy_mode


def render_metric_card(
    title: str,
    value: str,
    badge: str | None = None,
    badge_type: str | None = None,
    value_type: str | None = None,
    *,
    summary: bool = False,
) -> None:
    lang = get_lang()
    direction = "rtl" if lang == "ar" else "ltr"
    text_align = "right" if lang == "ar" else "left"

    value_class = "bar-card-price"
    if value_type in ("profit", "loss"):
        value_class += f" {value_type}"

    if badge:
        badge_class = badge_type or "neutral"
        badge_html = f'<span class="bar-card-badge {badge_class}">{badge}</span>'
    else:
        badge_html = '<span class="bar-card-badge-spacer"></span>'

    card_class = "bar-card summary-card" if summary else "bar-card"

    st.markdown(
        f"""
        <div class="{card_class}" style="direction:{direction}; text-align:{text_align};">
            <div class="bar-card-title">{title}</div>
            <div class="{value_class}">{value}</div>
            <div class="bar-card-badge-slot">{badge_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_forecast_card(
    title: str,
    price_text: str,
    value_text: str,
    profit_text: str,
    return_text: str,
    is_profit: bool,
    featured: bool = False,
) -> None:
    lang = get_lang()
    direction = "rtl" if lang == "ar" else "ltr"
    text_align = "right" if lang == "ar" else "left"
    value_type = "profit" if is_profit else "loss"

    card_class = "bar-card forecast-card"
    if featured:
        card_class += " featured"

    st.markdown(
        f"""
        <div class="{card_class}" style="direction:{direction}; text-align:{text_align};">
            <span class="forecast-card-tag">{price_text}</span>
            <div class="bar-card-title">{title}</div>
            <div class="bar-card-price">{value_text}</div>
            <div class="hero-balance-row">
                <span class="bar-card-badge {value_type}">{profit_text}</span>
                <span class="bar-card-badge neutral">{return_text}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_daily_price_change(gram_change: float, change_pct: float | None) -> None:
    if not gram_change or abs(gram_change) <= 0:
        return

    lang = get_lang()
    direction = "rtl" if lang == "ar" else "ltr"
    text_align = "right" if lang == "ar" else "left"
    is_up = gram_change >= 0
    pill_class = "gold-change-pill up" if is_up else "gold-change-pill down"
    arrow = "↑" if is_up else "↓"
    amount_text = format_money(gram_change, lang, signed=True)
    pill_text = amount_text
    if change_pct is not None and abs(change_pct) > 0:
        pill_text = f"{amount_text} · {format_percentage(change_pct)} {arrow}"
    else:
        pill_text = f"{amount_text} {arrow}"

    st.markdown(
        f"""
        <div class="gold-change-line" style="direction:{direction}; text-align:{text_align};">
            {t("price_change_today")}:
            <span class="{pill_class}">{pill_text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero_balance(summary, gram_price: float, price_data: dict | None = None) -> None:
    lang = get_lang()
    direction = "rtl" if lang == "ar" else "ltr"
    text_align = "right" if lang == "ar" else "left"
    is_profit = summary.profit_loss >= 0
    value_type = "profit" if is_profit else "loss"
    arrow = "↑" if is_profit else "↓"
    pl_badge_type = value_type

    balance_value = format_money(summary.current_value, lang)
    pl_text = format_money(summary.profit_loss, lang, signed=True)
    return_text = format_percentage(summary.return_percentage)
    pl_pill = f"{pl_text} · {return_text} {arrow}"

    gold_line = ""
    if gram_price > 0 and price_data:
        gram_label = format_money(gram_price, lang)
        change_pct = price_data.get("change_pct")
        gram_change = price_data.get("gram_change", 0.0)
        if change_pct is not None and not is_privacy_mode():
            change_class = "gold-up" if gram_change >= 0 else "gold-down"
            change_arrow = "↑" if gram_change >= 0 else "↓"
            change_sign = "+" if gram_change >= 0 else ""
            gold_line = (
                f'{t("gold_today")}: {gram_label} · '
                f'<span class="{change_class}">'
                f'{change_sign}{gram_change:,.1f} ({change_sign}{change_pct:,.1f}%) {change_arrow}'
                f"</span>"
            )
        else:
            gold_line = f'{t("gold_today")}: {gram_label}'

    st.markdown(
        f"""
        <div class="hero-balance" style="direction:{direction}; text-align:{text_align};">
            <div class="hero-balance-label">💎 {t("wallet_balance")}</div>
            <div class="hero-balance-value {value_type}">{balance_value}</div>
            <div class="hero-balance-row">
                <span class="bar-card-badge {pl_badge_type}">{pl_pill}</span>
            </div>
            <div class="hero-gold-line">{gold_line}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_bar_card(bar) -> None:
    lang = get_lang()
    is_profit = bar.profit_loss >= 0
    badge_type = "profit" if is_profit else "loss"
    arrow = "↑" if is_profit else "↓"
    pl_label = "ربح" if is_profit else "خسارة"
    if lang == "en":
        pl_label = "Profit" if is_profit else "Loss"

    if is_privacy_mode():
        badge = f"{format_percentage(bar.return_percentage)} {arrow}"
    else:
        badge = (
            f"{format_date_local(bar.purchase_date, lang)} · "
            f"{pl_label} {format_money(abs(bar.profit_loss), lang)} {arrow}"
        )
    title = f"{bar.bar_type} — {format_weight(bar.grams, lang)}"
    value = format_money(bar.my_cost, lang)
    render_metric_card(title, value, badge=badge, badge_type=badge_type)
