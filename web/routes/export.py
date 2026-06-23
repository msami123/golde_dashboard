import io

import pandas as pd
from flask import Blueprint, send_file, session

from db.database import get_session
from services.portfolio_service import get_portfolio_metrics, metrics_to_dataframe
from utils.i18n import get_lang, t
from web.auth import login_required
from web.helpers import get_price_context

bp = Blueprint("export", __name__, url_prefix="/export")


@bp.route("/csv")
@login_required
def export_csv():
    db = get_session()
    try:
        price_ctx = get_price_context(force_refresh=session.pop("force_price_refresh", False))
        metrics, _ = get_portfolio_metrics(db, price_ctx["gram_price"], session["user_id"])
        df = metrics_to_dataframe(metrics)
        lang = get_lang()
        export_df = df.rename(
            columns={
                "purchase_date": t("purchase_date"),
                "bar_type": t("bar_type"),
                "grams": t("grams"),
                "my_grams": t("grams"),
                "purchase_price": t("purchase_price"),
                "my_cost": t("cost"),
                "cost_per_gram": t("cost_per_gram"),
                "current_value": t("current_value"),
                "profit_loss": t("profit_loss"),
                "return_percentage": t("return_pct"),
                "ownership_percentage": t("ownership_pct"),
                "notes": t("notes"),
            }
        )
        csv_data = export_df.to_csv(index=False).encode("utf-8-sig")
        return send_file(
            io.BytesIO(csv_data),
            mimetype="text/csv",
            as_attachment=True,
            download_name="gold_portfolio.csv",
        )
    finally:
        db.close()


@bp.route("/excel")
@login_required
def export_excel():
    db = get_session()
    try:
        price_ctx = get_price_context(force_refresh=session.pop("force_price_refresh", False))
        metrics, _ = get_portfolio_metrics(db, price_ctx["gram_price"], session["user_id"])
        df = metrics_to_dataframe(metrics)
        lang = get_lang()
        export_df = df.rename(
            columns={
                "purchase_date": t("purchase_date"),
                "bar_type": t("bar_type"),
                "grams": t("grams"),
                "my_grams": t("grams"),
                "purchase_price": t("purchase_price"),
                "my_cost": t("cost"),
                "cost_per_gram": t("cost_per_gram"),
                "current_value": t("current_value"),
                "profit_loss": t("profit_loss"),
                "return_percentage": t("return_pct"),
                "ownership_percentage": t("ownership_pct"),
                "notes": t("notes"),
            }
        )
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            export_df.to_excel(writer, index=False, sheet_name="Portfolio")
        buffer.seek(0)
        return send_file(
            buffer,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name="gold_portfolio.xlsx",
        )
    finally:
        db.close()
