from flask import Blueprint, render_template, session

from utils.i18n import t
from web.auth import login_required
from web.dashboard_helpers import close_portfolio_context, load_portfolio_context

bp = Blueprint("alerts", __name__, url_prefix="/dashboard/alerts")


@bp.route("/")
@login_required
def index():
    ctx = load_portfolio_context(session["user_id"])
    try:
        return render_template(
            "alerts.html",
            price_ctx=ctx["price_ctx"],
            gram_price=ctx["gram_price"],
        )
    finally:
        close_portfolio_context(ctx)
