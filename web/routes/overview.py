from flask import Blueprint, render_template, session, url_for

from db.database import get_session
from services.chart_service import portfolio_value_chart, profit_distribution_chart
from services.portfolio_service import (
    forecast_portfolio,
    get_best_performing,
    get_portfolio_metrics,
    get_worst_performing,
)
from utils.formatting import format_money, format_percentage, format_weight
from utils.i18n import get_lang, t
from utils.privacy import format_profit_direction, is_privacy_mode, mask_count
from web.auth import login_required
from web.helpers import get_price_context, plotly_to_html, price_error_message

bp = Blueprint("overview", __name__, url_prefix="/dashboard")


def _summary_cards(summary):
    lang = get_lang()
    is_profit = summary.profit_loss >= 0
    badge_type = "profit" if is_profit else "loss"
    status_badge = "ربح" if is_profit else "خسارة"
    if lang == "en":
        status_badge = "Profit" if is_profit else "Loss"

    if is_privacy_mode():
        pl_value = format_profit_direction(summary.profit_loss, lang)
    else:
        pl_value = format_money(summary.profit_loss, lang, signed=True)

    return [
        {"title": t("total_gold"), "value": format_weight(summary.total_grams, lang)},
        {"title": t("total_cost"), "value": format_money(summary.total_cost, lang)},
        {
            "title": t("return_pct"),
            "value": format_percentage(summary.return_percentage),
            "badge": status_badge,
            "badge_type": badge_type,
            "value_type": badge_type,
        },
        {
            "title": t("num_bars"),
            "value": mask_count() if is_privacy_mode() else str(summary.num_bars),
        },
        {
            "title": t("avg_cost_per_gram"),
            "value": format_money(summary.avg_cost_per_gram, lang),
        },
        {
            "title": t("total_profit_loss"),
            "value": pl_value,
            "badge": status_badge,
            "badge_type": badge_type,
            "value_type": badge_type,
        },
    ]


def _performance_card(bar, label: str) -> dict:
    lang = get_lang()
    is_profit = bar.profit_loss >= 0
    badge_type = "profit" if is_profit else "loss"
    arrow = "↑" if is_profit else "↓"
    from utils.formatting import format_date_local

    title = f"{label} — {bar.bar_type} — {format_weight(bar.grams, lang)}"
    value = format_money(bar.profit_loss, lang, signed=True)
    if is_privacy_mode():
        badge = f"{format_percentage(bar.return_percentage)} {arrow}"
    else:
        badge = (
            f"{format_date_local(bar.purchase_date, lang)} · "
            f"{format_percentage(bar.return_percentage)} {arrow}"
        )
    return {
        "title": title,
        "value": value,
        "badge": badge,
        "badge_type": badge_type,
        "value_type": badge_type,
    }


def _forecast_scenarios(summary, gram_price: float) -> list[dict]:
    lang = get_lang()
    specs = []
    if gram_price > 0:
        specs.append((t("sell_today"), gram_price, True))
    specs.append((f"{t('if_gold_reaches')} 600", 600.0, False))
    specs.append((f"{t('if_gold_reaches')} 650", 650.0, False))

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
    db = get_session()
    try:
        force_refresh = session.pop("force_price_refresh", False)
        price_ctx = get_price_context(force_refresh=force_refresh)
        metrics, summary = get_portfolio_metrics(
            db, price_ctx["gram_price"], session["user_id"]
        )

        if not metrics:
            return render_template(
                "overview.html",
                empty=True,
                price_ctx=price_ctx,
                price_error=price_error_message(price_ctx["price_data"].get("error")),
                add_bar_url=url_for("gold_bars.index", tab="add"),
            )

        portfolio_chart = plotly_to_html(
            portfolio_value_chart(
                metrics,
                price_ctx["gram_price"],
                "",
                t("invested_capital"),
                t("portfolio_value"),
            )
        )
        profit_chart = plotly_to_html(
            profit_distribution_chart(metrics, "")
        )

        best = get_best_performing(metrics)
        worst = get_worst_performing(metrics)
        best_card = _performance_card(best, t("best_performing")) if best else None
        worst_card = _performance_card(worst, t("worst_performing")) if worst else None

        forecast_stats = [
            (t("total_gold"), format_weight(summary.total_grams, get_lang())),
            (t("total_invested"), format_money(summary.total_cost, get_lang())),
            (t("avg_cost_per_gram"), format_money(summary.avg_cost_per_gram, get_lang())),
            (
                t("current_price"),
                format_money(price_ctx["gram_price"], get_lang())
                if price_ctx["gram_price"] > 0
                else "—",
            ),
        ]

        return render_template(
            "overview.html",
            empty=False,
            summary=summary,
            metrics=metrics,
            summary_cards=_summary_cards(summary),
            portfolio_chart=portfolio_chart,
            profit_chart=profit_chart,
            best_card=best_card,
            worst_card=worst_card,
            forecast_stats=forecast_stats,
            forecast_cards=_forecast_scenarios(summary, price_ctx["gram_price"]),
            price_ctx=price_ctx,
            price_error=price_error_message(price_ctx["price_data"].get("error")),
            privacy_mode=is_privacy_mode(),
        )
    finally:
        db.close()
