import io

import pandas as pd
import streamlit as st

from config import ENABLE_MONTHLY_SELL_PROJECTION, get_gold_api_key
from services.chart_service import (
    monthly_sell_chart,
    portfolio_value_chart,
    profit_distribution_chart,
)
from services.gold_price_service import get_projection_monthly_prices
from services.portfolio_service import (
    get_best_performing,
    get_portfolio_metrics,
    get_worst_performing,
    metrics_to_dataframe,
    monthly_sell_projection,
)
from utils.cards import render_bar_card, render_hero_balance, render_metric_card
from utils.formatting import (
    format_date_local,
    format_money,
    format_percentage,
    format_weight,
)
from utils.i18n import format_month_label, get_lang, render_empty_state, render_section_header, t
from views.forecasting import render_forecasting_section
from utils.privacy import format_profit_direction, is_privacy_mode, mask_count
from utils.responsive import BAR_CARDS_PER_ROW, SUMMARY_CARDS_PER_ROW


def _render_export(metrics) -> None:
    if is_privacy_mode() or not metrics:
        return

    df = metrics_to_dataframe(metrics)
    lang = get_lang()
    export_df = df.rename(
        columns={
            "purchase_date": t("purchase_date"),
            "bar_type": t("bar_type"),
            "grams": t("grams"),
            "my_grams": t("grams"),
            "purchase_price": t("purchase_price"),
            "my_cost": t("cost"),
            "cost_per_gram": t("cost_per_gram"),
            "current_value": t("current_value"),
            "profit_loss": t("profit_loss"),
            "return_percentage": t("return_pct"),
            "ownership_percentage": t("ownership_pct"),
            "notes": t("notes"),
        }
    )

    col1, col2 = st.columns(2)
    with col1:
        csv_data = export_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            t("export_csv"),
            data=csv_data,
            file_name="gold_portfolio.csv",
            mime="text/csv",
            width="stretch",
        )
    with col2:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            export_df.to_excel(writer, index=False, sheet_name="Portfolio")
        st.download_button(
            t("export_excel"),
            data=buffer.getvalue(),
            file_name="gold_portfolio.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width="stretch",
        )


def _render_summary_cards(summary) -> None:
    lang = get_lang()
    is_profit = summary.profit_loss >= 0
    badge_type = "profit" if is_profit else "loss"
    value_type = badge_type
    arrow = "↑" if is_profit else "↓"
    status_badge = "ربح" if is_profit else "خسارة"
    if lang == "en":
        status_badge = "Profit" if is_profit else "Loss"

    if is_privacy_mode():
        pl_value = format_profit_direction(summary.profit_loss, lang)
    else:
        pl_value = format_money(summary.profit_loss, lang, signed=True)

    cards = [
        (t("total_gold"), format_weight(summary.total_grams, lang), None, None, None),
        (t("total_cost"), format_money(summary.total_cost, lang), None, None, None),
        (
            t("return_pct"),
            format_percentage(summary.return_percentage),
            status_badge,
            badge_type,
            value_type,
        ),
        (t("num_bars"), mask_count() if is_privacy_mode() else str(summary.num_bars), None, None, None),
        (t("avg_cost_per_gram"), format_money(summary.avg_cost_per_gram, lang), None, None, None),
        (t("total_profit_loss"), pl_value, status_badge, badge_type, value_type),
    ]

    per_row = SUMMARY_CARDS_PER_ROW
    for start in range(0, len(cards), per_row):
        cols = st.columns(per_row)
        for col, (title, value, badge, btype, vtype) in zip(cols, cards[start : start + per_row]):
            with col:
                render_metric_card(
                    title,
                    value,
                    badge=badge,
                    badge_type=btype,
                    value_type=vtype,
                    summary=True,
                )


def _render_analytics_chart(metrics, gram_price: float) -> None:
    render_section_header(t("nav_analytics"))
    st.plotly_chart(
        portfolio_value_chart(
            metrics,
            gram_price,
            "",
            t("invested_capital"),
            t("portfolio_value"),
        ),
        width="stretch",
    )


def _render_profit_distribution(metrics) -> None:
    render_section_header(t("chart_profit_distribution"))
    st.plotly_chart(
        profit_distribution_chart(metrics, ""),
        width="stretch",
    )


def _render_performance_card(bar, label: str) -> None:
    lang = get_lang()
    is_profit = bar.profit_loss >= 0
    badge_type = "profit" if is_profit else "loss"
    arrow = "↑" if is_profit else "↓"

    title = f"{label} — {bar.bar_type} — {format_weight(bar.grams, lang)}"
    value = format_money(bar.profit_loss, lang, signed=True)
    if is_privacy_mode():
        badge = f"{format_percentage(bar.return_percentage)} {arrow}"
    else:
        badge = (
            f"{format_date_local(bar.purchase_date, lang)} · "
            f"{format_percentage(bar.return_percentage)} {arrow}"
        )
    render_metric_card(
        title,
        value,
        badge=badge,
        badge_type=badge_type,
        value_type=badge_type,
    )


def _render_best_worst_table(metrics) -> None:
    best = get_best_performing(metrics)
    worst = get_worst_performing(metrics)

    if not best and not worst:
        return

    render_section_header(f"{t('best_performing')} / {t('worst_performing')}")
    col1, col2 = st.columns(2)
    with col1:
        if best:
            _render_performance_card(best, t("best_performing"))
    with col2:
        if worst:
            _render_performance_card(worst, t("worst_performing"))


def _render_bar_cards(metrics) -> None:
    render_section_header(t("nav_gold_bars"))
    per_row = BAR_CARDS_PER_ROW
    for start in range(0, len(metrics), per_row):
        cols = st.columns(per_row)
        for col, m in zip(cols, metrics[start : start + per_row]):
            with col:
                render_bar_card(m)


def _render_monthly_sell(metrics, gram_price: float) -> None:
    render_section_header(t("monthly_sell_title"))
    st.caption(t("monthly_sell_subtitle"))

    if not get_gold_api_key():
        st.info(t("api_key_missing"))
        return

    lang = get_lang()
    monthly_prices = get_projection_monthly_prices(gram_price)
    missing_prices = [k for k, v in monthly_prices.items() if v is None]

    if missing_prices:
        st.warning(t("monthly_sell_price_missing"))

    rows = monthly_sell_projection(metrics, monthly_prices)
    if not rows:
        st.info(t("monthly_sell_no_data"))
        return

    st.plotly_chart(
        monthly_sell_chart(rows, t("monthly_sell_title")),
        width="stretch",
    )

    table_rows = [
        {
            t("monthly_sell_month"): format_month_label(r.month_start, lang),
            t("monthly_sell_grams"): format_weight(r.grams_owned, lang),
            t("monthly_sell_price"): format_money(r.price_per_gram, lang),
            t("monthly_sell_value"): format_money(r.sell_value, lang),
            t("profit_loss"): format_money(r.profit_loss, lang, signed=True),
            t("return_pct"): format_percentage(r.return_percentage),
        }
        for r in rows
    ]
    st.dataframe(pd.DataFrame(table_rows), width="stretch", hide_index=True)


def render(session, gram_price: float, user_id: int, price_data: dict | None = None) -> None:
    metrics, summary = get_portfolio_metrics(session, gram_price, user_id)

    if is_privacy_mode():
        st.info(t("privacy_active"))

    if not metrics:
        render_empty_state(t("no_bars_title"), t("no_bars_hint"))
        if st.button(t("add_first_bar"), type="primary", use_container_width=True):
            st.session_state.page = "gold_bars"
            st.session_state.open_add_bar = True
            st.rerun()
        return

    render_hero_balance(summary, gram_price, price_data)

    _render_summary_cards(summary)

    if not is_privacy_mode():
        render_section_header(t("export_portfolio"))
        _render_export(metrics)

    st.divider()

    _render_analytics_chart(metrics, gram_price)
    st.divider()

    _render_bar_cards(metrics)
    st.divider()

    _render_profit_distribution(metrics)
    st.divider()

    _render_best_worst_table(metrics)
    st.divider()

    render_forecasting_section(summary, gram_price)

    if ENABLE_MONTHLY_SELL_PROJECTION:
        st.divider()
        _render_monthly_sell(metrics, gram_price)
