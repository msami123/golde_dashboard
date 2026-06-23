from flask import Blueprint, render_template, session

from config import FORECAST_SCENARIOS
from services.portfolio_service import forecast_portfolio
from utils.formatting import format_money, format_percentage, format_weight
from utils.i18n import get_lang, t
from utils.privacy import is_privacy_mode
from web.auth import login_required
from web.dashboard_helpers import close_portfolio_context, load_portfolio_context

bp = Blueprint("forecast", __name__, url_prefix="/dashboard/forecast")


def _scenario_cards(summary, gram_price: float) -> list[dict]:
    lang = get_lang()
    specs = []
    if gram_price > 0:
        specs.append((t("sell_today"), gram_price, True))
    for price in FORECAST_SCENARIOS[3:6]:
        specs.append((f"{t('if_gold_reaches')} {int(price)}", price, False))

    cards = []
    for label, price, featured in specs:
        df = forecast_portfolio(summary.total_grams, summary.total_cost, [price])
        row = df.iloc[0].to_dict()
        profit = row["profit"]
        cards.append(
            {
                "title": label,
                "price_text": f"{t('at_price')} {format_money(row['target_price'], lang)}",
                "value_text": format_money(row["portfolio_value"], lang),
                "profit_text": format_money(profit, lang, signed=True),
                "return_text": format_percentage(row["return_percentage"]),
                "is_profit": profit >= 0,
                "featured": featured,
            }
        )
    return cards


@bp.route("/")
@login_required
def index():
    force_refresh = session.pop("force_price_refresh", False)
    ctx = load_portfolio_context(session["user_id"], force_refresh)
    try:
        summary = ctx["summary"]
        lang = get_lang()
        if summary.num_bars == 0:
            return render_template(
                "forecast.html",
                empty=True,
                price_ctx=ctx["price_ctx"],
                privacy_mode=is_privacy_mode(),
            )

        forecast_stats = [
            (t("total_gold"), format_weight(summary.total_grams, lang)),
            (t("total_invested"), format_money(summary.total_cost, lang)),
            (t("avg_cost_per_gram"), format_money(summary.avg_cost_per_gram, lang)),
            (
                t("current_price"),
                format_money(ctx["gram_price"], lang) if ctx["gram_price"] > 0 else "—",
            ),
        ]

        return render_template(
            "forecast.html",
            empty=False,
            summary=summary,
            forecast_stats=forecast_stats,
            forecast_cards=_scenario_cards(summary, ctx["gram_price"]),
            price_ctx=ctx["price_ctx"],
            privacy_mode=is_privacy_mode(),
        )
    finally:
        close_portfolio_context(ctx)
