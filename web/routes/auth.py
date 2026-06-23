from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from config import DEFAULT_LANGUAGE
from utils.context import set_lang, set_privacy_mode
from utils.i18n import t
from web.auth import login_required, login_user, logout_user, try_authenticate

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash(t("login_required"), "error")
        else:
            user = try_authenticate(username, password)
            if user:
                login_user(user)
                return redirect(url_for("overview.index"))
            flash(t("login_failed"), "error")
    return render_template("login.html")


@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@bp.before_app_request
def sync_request_context():
    if "lang" not in session:
        session["lang"] = DEFAULT_LANGUAGE
    lang = session.get("lang", DEFAULT_LANGUAGE)
    set_lang(lang)
    set_privacy_mode(session.get("privacy_mode", False))
