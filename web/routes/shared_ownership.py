from flask import Blueprint, render_template, session

from db.database import get_session
from services.portfolio_service import get_portfolio_metrics, get_shared_bars
from utils.formatting import (
    format_date_local,
    format_money,
    format_ownership,
    format_weight,
)
from utils.i18n import get_lang, t
from utils.privacy import is_privacy_mode
from web.auth import login_required
from web.helpers import get_price_context, price_error_message

bp = Blueprint("shared_ownership", __name__, url_prefix="/shared-ownership")


@bp.route("/")
@login_required
def index():
    db = get_session()
    try:
        price_ctx = get_price_context()
        metrics, _ = get_portfolio_metrics(db, price_ctx["gram_price"], session["user_id"])
        shared = get_shared_bars(metrics)
        lang = get_lang()

        bars_data = []
        for bar in shared:
            value_type = "profit" if bar.profit_loss >= 0 else "loss"
            bars_data.append(
                {
                    "title": (
                        f"{bar.bar_type} — {format_date_local(bar.purchase_date, lang)} "
                        f"({t('my_share')}: {format_ownership(bar.ownership_percentage)})"
                    ),
                    "grams": format_weight(bar.grams, lang),
                    "my_share": format_ownership(bar.ownership_percentage),
                    "current_value": format_money(bar.current_value, lang),
                    "value_type": value_type,
                    "participants": [
                        {
                            "name": p["participant_name"],
                            "ownership": format_ownership(p["ownership_percentage"]),
                            "grams": format_weight(p["grams"], lang),
                            "cost": format_money(p["cost"], lang),
                            "current_value": format_money(p["current_value"], lang),
                            "profit": format_money(p["profit_loss"], lang, signed=True),
                            "is_profit": p["profit_loss"] >= 0,
                        }
                        for p in bar.participants
                    ] if bar.participants else [],
                }
            )

        return render_template(
            "shared_ownership.html",
            shared=bars_data,
            empty=not shared,
            price_ctx=price_ctx,
            price_error=price_error_message(price_ctx["price_data"].get("error")),
            privacy_mode=is_privacy_mode(),
        )
    finally:
        db.close()
