from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from db.database import get_session
from services.auth_service import change_password, create_user, delete_user, list_users
from utils.i18n import t
from web.auth import admin_required, try_authenticate
from web.helpers import get_price_context, price_error_message

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/", methods=["GET", "POST"])
@admin_required
def index():
    db = get_session()
    try:
        if request.method == "POST":
            action = request.form.get("action")
            if action == "add_user":
                username = request.form.get("username", "").strip()
                password = request.form.get("password", "")
                is_admin = request.form.get("is_admin") == "on"
                try:
                    create_user(db, username, password, is_admin=is_admin)
                    flash(t("admin_user_created"), "success")
                except ValueError as exc:
                    error_key = str(exc)
                    error_map = {
                        "username_taken": t("admin_username_taken"),
                        "password_too_short": t("admin_password_short"),
                        "username_required": t("login_required"),
                    }
                    flash(error_map.get(error_key, t("admin_create_failed")), "error")
                return redirect(url_for("admin.index"))

            if action == "delete_user":
                user_id = int(request.form.get("user_id", 0))
                if user_id != session["user_id"]:
                    delete_user(db, user_id)
                    flash(t("admin_user_deleted"), "success")
                return redirect(url_for("admin.index"))

            if action == "change_password":
                current_password = request.form.get("current_password", "")
                new_password = request.form.get("new_password", "")
                confirm_password = request.form.get("confirm_password", "")
                user = try_authenticate(session["username"], current_password)
                if not user:
                    flash(t("admin_wrong_password"), "error")
                elif new_password != confirm_password:
                    flash(t("admin_password_mismatch"), "error")
                else:
                    try:
                        change_password(db, session["user_id"], new_password)
                        flash(t("admin_password_updated"), "success")
                    except ValueError:
                        flash(t("admin_password_short"), "error")
                return redirect(url_for("admin.index"))

        users = list_users(db)
        price_ctx = get_price_context()
        return render_template(
            "admin.html",
            users=users,
            current_user_id=session["user_id"],
            price_ctx=price_ctx,
            price_error=price_error_message(price_ctx["price_data"].get("error")),
        )
    finally:
        db.close()
