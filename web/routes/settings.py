from flask import Blueprint, render_template, session

from utils.i18n import t
from web.auth import login_required

bp = Blueprint("settings", __name__, url_prefix="/dashboard/settings")


@bp.route("/")
@login_required
def index():
    return render_template(
        "settings.html",
        username=session.get("username"),
        is_admin=session.get("is_admin", False),
    )
