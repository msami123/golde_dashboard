import streamlit as st

from services.portfolio_service import get_portfolio_metrics, get_shared_bars
from utils.cards import render_data_card_grid, render_metric_card
from utils.formatting import (
    format_date_local,
    format_money,
    format_ownership,
    format_percentage,
    format_weight,
)
from utils.privacy import is_privacy_mode
from utils.i18n import get_lang, render_empty_state, t


def render(session, gram_price: float, user_id: int) -> None:
    st.subheader(t("shared_title"))
    st.caption(t("shared_subtitle"))

    if is_privacy_mode():
        st.info(t("privacy_active"))

    metrics, _ = get_portfolio_metrics(session, gram_price, user_id)
    shared = get_shared_bars(metrics)
    lang = get_lang()

    if not shared:
        render_empty_state(t("no_shared_bars"), t("shared_subtitle"))
        return

    for bar in shared:
        with st.expander(
            f"{bar.bar_type} — {format_date_local(bar.purchase_date, lang)} "
            f"({t('my_share')}: {format_ownership(bar.ownership_percentage)})",
            expanded=True,
        ):
            col1, col2, col3 = st.columns(3)
            with col1:
                render_metric_card(t("grams"), format_weight(bar.grams, lang))
            with col2:
                render_metric_card(t("my_share"), format_ownership(bar.ownership_percentage))
            with col3:
                value_type = "profit" if bar.profit_loss >= 0 else "loss"
                render_metric_card(
                    t("current_value"),
                    format_money(bar.current_value, lang),
                    value_type=value_type,
                )

            if bar.participants:
                participant_cards = []
                for p in bar.participants:
                    profit = p["current_value"] - p["cost"]
                    return_pct = (profit / p["cost"] * 100) if p["cost"] else 0.0
                    pl_class = "profit" if profit >= 0 else "loss"
                    participant_cards.append(
                        {
                            "title": p["participant_name"],
                            "rows": [
                                (
                                    t("ownership_pct"),
                                    format_ownership(p["ownership_percentage"]),
                                ),
                                (t("grams"), format_weight(p["grams"], lang)),
                                (t("cost"), format_money(p["cost"], lang)),
                                (
                                    t("current_value"),
                                    format_money(p["current_value"], lang),
                                ),
                                (
                                    t("profit_loss"),
                                    format_money(profit, lang, signed=True),
                                    pl_class,
                                ),
                                (t("return_pct"), format_percentage(return_pct)),
                            ],
                        }
                    )
                render_data_card_grid(participant_cards, lang)
            else:
                st.caption(t("full_bar"))
