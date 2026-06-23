from pathlib import Path

from flask import Blueprint, redirect, send_from_directory, url_for

from web.auth import is_logged_in

bp = Blueprint("landing", __name__)

LANDING_DIST = Path(__file__).resolve().parent.parent.parent / "landing" / "dist"


def _landing_available() -> bool:
    return (LANDING_DIST / "index.html").exists()


@bp.route("/")
def home():
    if is_logged_in():
        return redirect(url_for("overview.index"))
    if _landing_available():
        return send_from_directory(LANDING_DIST, "index.html")
    return redirect(url_for("auth.login"))


@bp.route("/assets/<path:filename>")
def assets(filename: str):
    assets_dir = LANDING_DIST / "assets"
    if assets_dir.exists():
        return send_from_directory(assets_dir, filename)
    return ("", 404)


@bp.route("/fonts/<path:filename>")
def fonts(filename: str):
    fonts_dir = LANDING_DIST / "fonts"
    if fonts_dir.exists():
        return send_from_directory(fonts_dir, filename)
    return ("", 404)


@bp.route("/favicon.svg")
def favicon():
    if (LANDING_DIST / "favicon.svg").exists():
        return send_from_directory(LANDING_DIST, "favicon.svg")
    return ("", 404)
