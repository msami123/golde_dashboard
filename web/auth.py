"""Flask authentication helpers."""

from functools import wraps

from flask import flash, redirect, session, url_for

from db.database import get_session
from services.auth_service import authenticate, get_user_by_id
from utils.i18n import t


def login_user(user) -> None:
    session["user_id"] = user.id
    session["username"] = user.username
    session["is_admin"] = user.is_admin
    session.permanent = True


def logout_user() -> None:
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("is_admin", None)


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    db = get_session()
    try:
        return get_user_by_id(db, user_id)
    finally:
        db.close()


def is_logged_in() -> bool:
    return bool(session.get("user_id"))


def is_admin() -> bool:
    return bool(session.get("is_admin"))


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for("auth.login"))
        if not is_admin():
            flash(t("admin_forbidden"), "error")
            return redirect(url_for("overview.index"))
        return f(*args, **kwargs)

    return decorated


def try_authenticate(username: str, password: str):
    db = get_session()
    try:
        return authenticate(db, username, password)
    finally:
        db.close()
