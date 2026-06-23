"""Shared dashboard context builders — presentation layer only."""

from db.database import get_session
from services.portfolio_service import get_portfolio_metrics
from web.helpers import get_price_context, plotly_to_html, price_error_message


def load_portfolio_context(user_id: int, force_refresh: bool = False) -> dict:
    db = get_session()
    try:
        price_ctx = get_price_context(force_refresh=force_refresh)
        metrics, summary = get_portfolio_metrics(
            db, price_ctx["gram_price"], user_id
        )
        return {
            "db": db,
            "metrics": metrics,
            "summary": summary,
            "price_ctx": price_ctx,
            "price_error": price_error_message(price_ctx["price_data"].get("error")),
            "gram_price": price_ctx["gram_price"],
        }
    except Exception:
        db.close()
        raise


def close_portfolio_context(ctx: dict) -> None:
    db = ctx.get("db")
    if db:
        db.close()
