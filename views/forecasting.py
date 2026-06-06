import streamlit as st

from services.portfolio_service import forecast_portfolio
from utils.cards import render_forecast_card, render_metric_card
from utils.formatting import format_money, format_percentage, format_weight
from utils.i18n import get_lang, render_section_header, t
from utils.responsive import FORECAST_STATS_PER_ROW


def _scenario_row(total_grams: float, total_cost: float, price: float) -> dict:
    df = forecast_portfolio(total_grams, total_cost, [price])
    return df.iloc[0].to_dict()


def _render_scenario(title: str, row: dict, lang: str, featured: bool = False) -> None:
    profit = row["profit"]
    render_forecast_card(
        title=title,
        price_text=f"{t('at_price')} {format_money(row['target_price'], lang)}",
        value_text=format_money(row["portfolio_value"], lang),
        profit_text=format_money(profit, lang, signed=True),
        return_text=format_percentage(row["return_percentage"]),
        is_profit=profit >= 0,
        featured=featured,
    )


def render_forecasting_section(summary, gram_price: float) -> None:
    render_section_header(t("forecast_title"))
    st.caption(t("forecast_subtitle"))

    lang = get_lang()

    forecast_cards = [
        (t("total_gold"), format_weight(summary.total_grams, lang)),
        (t("total_invested"), format_money(summary.total_cost, lang)),
        (t("avg_cost_per_gram"), format_money(summary.avg_cost_per_gram, lang)),
        (
            t("current_price"),
            format_money(gram_price, lang) if gram_price > 0 else "—",
        ),
    ]
    per_row = FORECAST_STATS_PER_ROW
    for start in range(0, len(forecast_cards), per_row):
        cols = st.columns(per_row)
        for col, (title, value) in zip(cols, forecast_cards[start : start + per_row]):
            with col:
                render_metric_card(title, value)

    key_specs: list[tuple[str, float, bool]] = []
    if gram_price > 0:
        key_specs.append((t("sell_today"), gram_price, True))
    key_specs.append((f"{t('if_gold_reaches')} 600", 600.0, False))
    key_specs.append((f"{t('if_gold_reaches')} 650", 650.0, False))

    scenario_cols = st.columns(3)
    for col, (label, price, featured) in zip(scenario_cols, key_specs):
        with col:
            row = _scenario_row(summary.total_grams, summary.total_cost, price)
            _render_scenario(label, row, lang, featured=featured)

    custom_price = st.number_input(
        t("custom_price"),
        min_value=0.0,
        value=float(gram_price) if gram_price > 0 else 550.0,
        step=10.0,
    )
    if custom_price > 0:
        custom_row = _scenario_row(summary.total_grams, summary.total_cost, custom_price)
        _render_scenario(t("forecast_custom_result"), custom_row, lang, featured=True)


def render(session, gram_price: float, user_id: int) -> None:
    from services.portfolio_service import get_portfolio_metrics

    _, summary = get_portfolio_metrics(session, gram_price, user_id)

    if summary.num_bars == 0:
        st.info(t("no_bars"))
        return

    render_forecasting_section(summary, gram_price)
