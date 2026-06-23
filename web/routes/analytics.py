from flask import Blueprint, render_template, session

from services.chart_service import portfolio_value_chart, profit_distribution_chart
from services.portfolio_service import get_best_performing, get_worst_performing
from utils.i18n import t
from utils.privacy import is_privacy_mode
from web.auth import login_required
from web.dashboard_helpers import close_portfolio_context, load_portfolio_context
from web.helpers import plotly_to_html

bp = Blueprint("analytics", __name__, url_prefix="/dashboard/analytics")


@bp.route("/")
@login_required
def index():
    force_refresh = session.pop("force_price_refresh", False)
    ctx = load_portfolio_context(session["user_id"], force_refresh)
    try:
        metrics = ctx["metrics"]
        if not metrics:
            return render_template(
                "analytics.html",
                empty=True,
                price_ctx=ctx["price_ctx"],
                privacy_mode=is_privacy_mode(),
            )

        portfolio_chart = plotly_to_html(
            portfolio_value_chart(
                metrics,
                ctx["gram_price"],
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

        return render_template(
            "analytics.html",
            empty=False,
            metrics=metrics,
            portfolio_chart=portfolio_chart,
            profit_chart=profit_chart,
            best=best,
            worst=worst,
            summary=ctx["summary"],
            price_ctx=ctx["price_ctx"],
            privacy_mode=is_privacy_mode(),
        )
    finally:
        close_portfolio_context(ctx)
