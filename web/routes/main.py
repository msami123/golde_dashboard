from flask import Blueprint, redirect, request, session, url_for

from utils.context import set_lang, set_privacy_mode
from web.auth import login_required

bp = Blueprint("main", __name__)


@bp.route("/set-lang/<lang>")
@login_required
def set_language(lang: str):
    if lang in ("ar", "en"):
        session["lang"] = lang
        set_lang(lang)
    return redirect(request.referrer or url_for("overview.index"))


@bp.route("/toggle-privacy", methods=["POST"])
@login_required
def toggle_privacy():
    session["privacy_mode"] = not session.get("privacy_mode", False)
    set_privacy_mode(session["privacy_mode"])
    return redirect(request.referrer or url_for("overview.index"))


@bp.route("/refresh-price")
@login_required
def refresh_price():
    session["force_price_refresh"] = True
    return redirect(request.referrer or url_for("overview.index"))
