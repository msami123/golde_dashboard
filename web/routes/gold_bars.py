from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from db.database import get_session
from services.portfolio_service import (
    create_bar,
    delete_bar,
    get_all_bars,
    get_bar_by_id,
    get_portfolio_metrics,
    update_bar,
)
from utils.formatting import (
    format_date_local,
    format_money,
    format_ownership,
    format_percentage,
    format_weight,
)
from utils.i18n import get_lang, t
from utils.privacy import is_privacy_mode
from web.auth import login_required
from web.helpers import get_price_context, price_error_message

bp = Blueprint("gold_bars", __name__, url_prefix="/gold-bars")

SORT_OPTIONS = {
    "sort_date": "purchase_date",
    "sort_profit": "profit_loss",
    "sort_value": "current_value",
    "sort_grams": "grams",
}


def _parse_participants(form) -> list[dict]:
    names = form.getlist("participant_name")
    pcts = form.getlist("participant_pct")
    participants = []
    for name, pct in zip(names, pcts):
        name = name.strip()
        if not name:
            continue
        try:
            pct_val = float(pct)
        except (TypeError, ValueError):
            pct_val = 0.0
        participants.append({"participant_name": name, "ownership_percentage": pct_val})
    return participants


def _validate_bar_form(
    purchase_date,
    purchase_price,
    grams,
    bar_type,
    ownership_percentage,
    participants,
    is_shared,
) -> str | None:
    if not purchase_date or not bar_type.strip() or purchase_price <= 0 or grams <= 0:
        return t("required_fields_error")
    if ownership_percentage < 1 or ownership_percentage > 100:
        return t("ownership_range_error")
    if is_shared and participants:
        total = sum(p["ownership_percentage"] for p in participants)
        if abs(total - 100.0) > 0.01:
            return t("participants_sum_error")
    return None


def _bar_form_data(form) -> dict | None:
    try:
        purchase_date = date.fromisoformat(form.get("purchase_date", ""))
    except ValueError:
        purchase_date = None
    try:
        purchase_price = float(form.get("purchase_price", 0))
        grams = float(form.get("grams", 0))
        ownership_percentage = float(form.get("ownership_percentage", 100))
    except (TypeError, ValueError):
        return None

    bar_type = form.get("bar_type", "").strip()
    notes = form.get("notes", "").strip() or None
    is_shared = form.get("is_shared") == "on"
    participants = _parse_participants(form) if is_shared else []

    error = _validate_bar_form(
        purchase_date,
        purchase_price,
        grams,
        bar_type,
        ownership_percentage,
        participants,
        is_shared,
    )
    if error:
        flash(error, "error")
        return None

    return {
        "purchase_date": purchase_date,
        "purchase_price": purchase_price,
        "grams": grams,
        "bar_type": bar_type,
        "ownership_percentage": ownership_percentage,
        "notes": notes,
        "participants": participants if is_shared else [],
    }


def _bar_cards(metrics, search: str, bar_type_filter: str, sort_key: str) -> list[dict]:
    lang = get_lang()
    filtered = list(metrics)

    sort_col = SORT_OPTIONS.get(sort_key, "purchase_date")
    reverse = sort_col != "purchase_date"
    filtered.sort(key=lambda m: getattr(m, sort_col), reverse=reverse)

    if search:
        q = search.lower()
        filtered = [
            m
            for m in filtered
            if q in m.bar_type.lower() or (m.notes and q in m.notes.lower())
        ]
    if bar_type_filter and bar_type_filter != t("all_types"):
        filtered = [m for m in filtered if m.bar_type == bar_type_filter]

    cards = []
    for m in filtered:
        pl_class = "profit" if m.profit_loss >= 0 else "loss"
        cards.append(
            {
                "title": f"{m.bar_type} — {format_weight(m.grams, lang)}",
                "rows": [
                    (t("purchase_date"), format_date_local(m.purchase_date, lang)),
                    (t("bar_type"), m.bar_type),
                    (t("grams"), format_weight(m.grams, lang)),
                    (t("purchase_price"), format_money(m.purchase_price, lang)),
                    (t("cost_per_gram"), format_money(m.cost_per_gram, lang)),
                    (t("current_value"), format_money(m.current_value, lang)),
                    (t("profit_loss"), format_money(m.profit_loss, lang, signed=True), pl_class),
                    (t("return_pct"), format_percentage(m.return_percentage)),
                    (t("ownership_pct"), format_ownership(m.ownership_percentage)),
                ],
            }
        )
    return cards


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    db = get_session()
    try:
        tab = request.args.get("tab", "list")
        price_ctx = get_price_context(force_refresh=session.pop("force_price_refresh", False))
        metrics, _ = get_portfolio_metrics(db, price_ctx["gram_price"], session["user_id"])

        if request.method == "POST":
            action = request.form.get("action")
            data = _bar_form_data(request.form)
            if action == "add" and data:
                create_bar(db, session["user_id"], **data)
                flash(t("bar_added"), "success")
                return redirect(url_for("gold_bars.index", tab="list"))
            if action == "edit" and data:
                bar_id = int(request.form.get("bar_id", 0))
                if update_bar(db, bar_id, session["user_id"], **data):
                    flash(t("bar_updated"), "success")
                return redirect(url_for("gold_bars.index", tab="list"))
            if action == "delete":
                bar_id = int(request.form.get("bar_id", 0))
                if delete_bar(db, bar_id, session["user_id"]):
                    flash(t("bar_deleted"), "success")
                return redirect(url_for("gold_bars.index", tab="list"))

        search = request.args.get("search", "")
        bar_type_filter = request.args.get("filter", t("all_types"))
        sort_key = request.args.get("sort", "sort_date")
        filtered_metrics = list(metrics)
        sort_col = SORT_OPTIONS.get(sort_key, "purchase_date")
        filtered_metrics.sort(key=lambda m: getattr(m, sort_col), reverse=sort_col != "purchase_date")
        if search:
            q = search.lower()
            filtered_metrics = [
                m for m in filtered_metrics
                if q in m.bar_type.lower() or (m.notes and q in m.notes.lower())
            ]
        if bar_type_filter != t("all_types"):
            filtered_metrics = [m for m in filtered_metrics if m.bar_type == bar_type_filter]

        bar_types = sorted({m.bar_type for m in metrics}) if metrics else []
        bars = get_all_bars(db, session["user_id"])
        lang = get_lang()

        edit_bar = None
        edit_id = request.args.get("edit")
        if edit_id:
            edit_bar = get_bar_by_id(db, int(edit_id), session["user_id"])

        return render_template(
            "gold_bars.html",
            tab=tab,
            metrics=filtered_metrics,
            bars=bars,
            bar_types=bar_types,
            search=search,
            bar_type_filter=bar_type_filter,
            sort_key=sort_key,
            sort_options=list(SORT_OPTIONS.keys()),
            edit_bar=edit_bar,
            today=date.today().isoformat(),
            price_ctx=price_ctx,
            price_error=price_error_message(price_ctx["price_data"].get("error")),
            privacy_mode=is_privacy_mode(),
        )
    finally:
        db.close()
