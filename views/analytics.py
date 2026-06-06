import streamlit as st

from services.chart_service import portfolio_value_chart, profit_distribution_chart
from services.portfolio_service import (
    get_portfolio_metrics,
    get_best_performing,
    get_worst_performing,
)
from utils.cards import render_metric_card
from utils.formatting import (
    format_date_local,
    format_money,
    format_percentage,
    format_weight,
)
from utils.i18n import get_lang, t


def _render_bar_card(bar) -> None:
    lang = get_lang()
    is_profit = bar.profit_loss >= 0
    badge_type = "profit" if is_profit else "loss"
    arrow = "↑" if is_profit else "↓"

    if lang == "ar":
        pl_label = "ربح" if is_profit else "خسارة"
        badge = (
            f"{format_date_local(bar.purchase_date, lang)} · "
            f"{pl_label} {format_money(abs(bar.profit_loss), lang)} {arrow}"
        )
    else:
        pl_label = "Profit" if is_profit else "Loss"
        badge = (
            f"{format_date_local(bar.purchase_date, lang)} · "
            f"{pl_label} {format_money(abs(bar.profit_loss), lang)} {arrow}"
        )

    title = f"{bar.bar_type} — {format_weight(bar.grams, lang)}"
    value = format_money(bar.my_cost, lang)
    render_metric_card(title, value, badge=badge, badge_type=badge_type)


def render(session, gram_price: float, user_id: int) -> None:
    st.subheader(t("nav_analytics"))

    metrics, _ = get_portfolio_metrics(session, gram_price, user_id)
    lang = get_lang()

    if not metrics:
        st.info(t("no_bars"))
        return

    best = get_best_performing(metrics)
    worst = get_worst_performing(metrics)

    table_rows = []
    if best:
        table_rows.append(
            {
                t("best_performing"): t("best_performing"),
                t("bar_type"): best.bar_type,
                t("purchase_date"): format_date_local(best.purchase_date, lang),
                t("grams"): format_weight(best.grams, lang),
                t("profit_loss"): format_money(best.profit_loss, lang, signed=True),
                t("return_pct"): format_percentage(best.return_percentage),
            }
        )
    if worst:
        table_rows.append(
            {
                t("best_performing"): t("worst_performing"),
                t("bar_type"): worst.bar_type,
                t("purchase_date"): format_date_local(worst.purchase_date, lang),
                t("grams"): format_weight(worst.grams, lang),
                t("profit_loss"): format_money(worst.profit_loss, lang, signed=True),
                t("return_pct"): format_percentage(worst.return_percentage),
            }
        )

    if table_rows:
        import pandas as pd

        st.dataframe(
            pd.DataFrame(table_rows),
            width="stretch",
            hide_index=True,
        )

    st.divider()

    st.markdown(f"### {t('nav_gold_bars')}")
    cols = st.columns(3)
    for idx, m in enumerate(metrics):
        with cols[idx % 3]:
            _render_bar_card(m)

    st.divider()

    st.plotly_chart(
        portfolio_value_chart(
            metrics,
            gram_price,
            t("chart_portfolio_value"),
            t("invested_capital"),
            t("portfolio_value"),
        ),
        width="stretch",
    )

    st.plotly_chart(
        profit_distribution_chart(metrics, t("chart_profit_distribution")),
        width="stretch",
    )
