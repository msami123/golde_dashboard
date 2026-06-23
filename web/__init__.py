from datetime import timedelta

from flask import Flask

from config import DEFAULT_LANGUAGE, get_cookie_secret
from db.database import init_db
from web.filters import register_filters
from web.routes import (
    admin_bp,
    alerts_bp,
    analytics_bp,
    auth_bp,
    export_bp,
    forecast_bp,
    gold_bars_bp,
    landing_bp,
    main_bp,
    overview_bp,
    reports_bp,
    settings_bp,
    shared_ownership_bp,
)


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = get_cookie_secret()
    app.permanent_session_lifetime = timedelta(days=30)

    init_db()
    register_filters(app)

    app.register_blueprint(landing_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(overview_bp)
    app.register_blueprint(gold_bars_bp)
    app.register_blueprint(shared_ownership_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(forecast_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(export_bp)

    @app.context_processor
    def inject_globals():
        from flask import session

        from config import GOLD_API_MONTHLY_LIMIT, get_gold_api_key
        from utils.context import get_lang, is_privacy_mode

        return {
            "lang": get_lang(),
            "privacy_mode": is_privacy_mode(),
            "username": session.get("username"),
            "is_admin": session.get("is_admin", False),
            "has_api_key": bool(get_gold_api_key()),
            "api_monthly_limit": GOLD_API_MONTHLY_LIMIT,
            "default_lang": DEFAULT_LANGUAGE,
        }

    return app
