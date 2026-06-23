from flask import Blueprint, render_template, session

from utils.i18n import t
from utils.privacy import is_privacy_mode
from web.auth import login_required
from web.dashboard_helpers import close_portfolio_context, load_portfolio_context

bp = Blueprint("reports", __name__, url_prefix="/dashboard/reports")


@bp.route("/")
@login_required
def index():
    force_refresh = session.pop("force_price_refresh", False)
    ctx = load_portfolio_context(session["user_id"], force_refresh)
    try:
        return render_template(
            "reports.html",
            summary=ctx["summary"],
            has_data=bool(ctx["metrics"]),
            price_ctx=ctx["price_ctx"],
            privacy_mode=is_privacy_mode(),
        )
    finally:
        close_portfolio_context(ctx)
