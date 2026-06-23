from web.routes.alerts import bp as alerts_bp
from web.routes.analytics import bp as analytics_bp
from web.routes.forecast import bp as forecast_bp
from web.routes.landing import bp as landing_bp
from web.routes.reports import bp as reports_bp
from web.routes.settings import bp as settings_bp
from web.routes.admin import bp as admin_bp
from web.routes.auth import bp as auth_bp
from web.routes.export import bp as export_bp
from web.routes.gold_bars import bp as gold_bars_bp
from web.routes.main import bp as main_bp
from web.routes.overview import bp as overview_bp
from web.routes.shared_ownership import bp as shared_ownership_bp

__all__ = [
    "landing_bp",
    "auth_bp",
    "main_bp",
    "overview_bp",
    "gold_bars_bp",
    "shared_ownership_bp",
    "analytics_bp",
    "forecast_bp",
    "reports_bp",
    "alerts_bp",
    "settings_bp",
    "admin_bp",
    "export_bp",
]
