import os
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)

load_dotenv(BASE_DIR / ".env", override=True)


def _secret_or_env(name: str, default: str = "") -> str:
    value = os.getenv(name, "").strip()
    if value:
        return value
    try:
        import streamlit as st

        if hasattr(st, "secrets") and name in st.secrets:
            return str(st.secrets[name]).strip()
    except Exception:
        pass
    return default


def get_database_url() -> str:
    url = _secret_or_env("DATABASE_URL")
    if not url:
        return f"sqlite:///{BASE_DIR / 'gold_portfolio.db'}"
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


DATABASE_URL = get_database_url()


def get_gold_api_key() -> str:
    return _secret_or_env("GOLD_API_KEY")


def get_admin_username() -> str:
    return _secret_or_env("ADMIN_USERNAME", "admin")


def get_admin_password() -> str:
    return _secret_or_env("ADMIN_PASSWORD", "changeme")


def get_cookie_secret() -> str:
    return _secret_or_env("COOKIE_SECRET", "dev-change-me-in-production")


GOLD_API_KEY = get_gold_api_key()
GOLD_API_URL = "https://www.goldapi.io/api/XAU/SAR"
CURRENCY = "SAR"
OUNCES_PER_GRAM = 31.1034768
CACHE_FILE = CACHE_DIR / "gold_price_cache.json"
HISTORY_CACHE_FILE = CACHE_DIR / "gold_price_history.json"
API_USAGE_FILE = CACHE_DIR / "api_usage.json"
GOLD_API_MONTHLY_LIMIT = 100
# Use cached price until the user clicks "Refresh" (saves GoldAPI requests).
GOLD_PRICE_MANUAL_REFRESH_ONLY = True
CACHE_TTL_MINUTES = 60 * 24 * 30
ENABLE_MONTHLY_SELL_PROJECTION = False
PROJECTION_START = date(2026, 1, 1)
DEFAULT_LANGUAGE = "ar"
FORECAST_SCENARIOS = [400, 450, 500, 550, 600, 650, 700]
GRAM_BUCKETS = [5, 10, 25, 50, 100]
