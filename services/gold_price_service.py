import hashlib
import json
from datetime import date, datetime, timezone

import requests

from config import (
    API_USAGE_FILE,
    CACHE_FILE,
    CACHE_TTL_MINUTES,
    GOLD_API_URL,
    GOLD_PRICE_MANUAL_REFRESH_ONLY,
    HISTORY_CACHE_FILE,
    OUNCES_PER_GRAM,
    PROJECTION_START,
    get_gold_api_key,
)
from utils.formatting import round_num


def _read_cache() -> dict | None:
    if not CACHE_FILE.exists():
        return None
    try:
        with open(CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def _write_cache(data: dict) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _read_history_cache() -> dict:
    if not HISTORY_CACHE_FILE.exists():
        return {}
    try:
        with open(HISTORY_CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _write_history_cache(data: dict) -> None:
    HISTORY_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _read_usage_log() -> list[dict]:
    if not API_USAGE_FILE.exists():
        return []
    try:
        with open(API_USAGE_FILE, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return data.get("requests", [])
    except (json.JSONDecodeError, OSError, AttributeError):
        return []


def _write_usage_log(requests: list[dict]) -> None:
    API_USAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(API_USAGE_FILE, "w", encoding="utf-8") as f:
        json.dump({"requests": requests[-500:]}, f, ensure_ascii=False, indent=2)


def _log_api_request(endpoint: str, success: bool, error: str | None = None) -> None:
    requests = _read_usage_log()
    requests.append(
        {
            "at": datetime.now(timezone.utc).isoformat(),
            "endpoint": endpoint,
            "success": success,
            "error": error,
        }
    )
    _write_usage_log(requests)


def get_api_usage_stats() -> dict:
    requests = _read_usage_log()
    now = datetime.now(timezone.utc)
    month_prefix = now.strftime("%Y-%m")

    month_requests = [
        r for r in requests if str(r.get("at", "")).startswith(month_prefix)
    ]

    last = requests[-1] if requests else None
    return {
        "month_total": len(month_requests),
        "month_success": sum(1 for r in month_requests if r.get("success")),
        "month_failed": sum(1 for r in month_requests if not r.get("success")),
        "all_time": len(requests),
        "last": last,
    }


def _api_key_fingerprint(api_key: str) -> str:
    if not api_key:
        return ""
    return hashlib.sha256(api_key.encode()).hexdigest()[:12]


def _cache_is_fresh(cache: dict) -> bool:
    if GOLD_PRICE_MANUAL_REFRESH_ONLY and cache.get("fetched_at"):
        return True

    fetched_at = cache.get("fetched_at")
    if not fetched_at:
        return False
    try:
        cached_time = datetime.fromisoformat(fetched_at)
        if cached_time.tzinfo is None:
            cached_time = cached_time.replace(tzinfo=timezone.utc)
        age_minutes = (datetime.now(timezone.utc) - cached_time).total_seconds() / 60
        return age_minutes < CACHE_TTL_MINUTES
    except ValueError:
        return False


def _derive_change_pct(ounce_price: float, ounce_change: float, change_pct: float) -> float:
    if change_pct:
        return change_pct
    if ounce_change and ounce_price:
        previous_price = ounce_price - ounce_change
        if previous_price:
            return round_num((ounce_change / previous_price) * 100)
    return 0.0


def _api_error_code(exc: Exception) -> str:
    if isinstance(exc, requests.HTTPError) and exc.response is not None:
        status = exc.response.status_code
        if status == 403:
            return "quota_exceeded"
        if status == 401:
            return "invalid_key"
        return f"http_{status}"
    if isinstance(exc, requests.RequestException):
        return "network_error"
    if isinstance(exc, ValueError):
        return "missing_key"
    return "unknown"


def _fetch_from_api() -> dict:
    api_key = get_gold_api_key()
    if not api_key:
        raise ValueError("GOLD_API_KEY not configured")

    try:
        response = requests.get(
            GOLD_API_URL,
            headers={
                "x-access-token": api_key,
                "Content-Type": "application/json",
            },
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
        _log_api_request("current", success=True)
    except Exception as exc:
        _log_api_request("current", success=False, error=_api_error_code(exc))
        raise

    ounce_price = float(payload["price"])
    gram_price = float(payload["price_gram_24k"]) if payload.get("price_gram_24k") else (
        ounce_price / OUNCES_PER_GRAM
    )
    ounce_change = float(payload.get("ch") or 0.0)
    change_pct = _derive_change_pct(
        ounce_price,
        ounce_change,
        float(payload["chp"]) if payload.get("chp") is not None else 0.0,
    )
    gram_change = ounce_change / OUNCES_PER_GRAM

    return {
        "current_ounce_price": ounce_price,
        "current_gram_price": gram_price,
        "ounce_change": round_num(ounce_change),
        "gram_change": round_num(gram_change),
        "change_pct": round_num(change_pct),
        "currency": payload.get("currency", "SAR"),
        "metal": payload.get("metal", "XAU"),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": "api",
        "stale": False,
        "error": None,
        "api_key_fingerprint": _api_key_fingerprint(api_key),
    }


def get_gold_price(force_refresh: bool = False) -> dict:
    cache = _read_cache()
    api_key = get_gold_api_key()
    key_fingerprint = _api_key_fingerprint(api_key)

    if (
        cache
        and key_fingerprint
        and cache.get("api_key_fingerprint") not in (None, key_fingerprint)
    ):
        force_refresh = True

    if not force_refresh and cache and _cache_is_fresh(cache):
        result = dict(cache)
        result["change_pct"] = _derive_change_pct(
            float(result.get("current_ounce_price") or 0.0),
            float(result.get("ounce_change") or 0.0),
            float(result.get("change_pct") or 0.0),
        )
        result["stale"] = False
        result["error"] = None
        return result

    try:
        price_data = _fetch_from_api()
        _write_cache(price_data)
        return price_data
    except Exception as exc:
        error_code = _api_error_code(exc)
        if cache:
            result = dict(cache)
            result["stale"] = True
            result["error"] = error_code
            result["source"] = "cache"
            return result
        return {
            "current_ounce_price": 0.0,
            "current_gram_price": 0.0,
            "ounce_change": 0.0,
            "gram_change": 0.0,
            "change_pct": 0.0,
            "currency": "SAR",
            "metal": "XAU",
            "fetched_at": None,
            "source": "none",
            "stale": True,
            "error": error_code,
        }


def get_cached_gold_price(force_refresh: bool = False) -> dict:
    return get_gold_price(force_refresh=force_refresh)


def _month_starts(start: date, end: date) -> list[date]:
    months: list[date] = []
    year, month = start.year, start.month
    while date(year, month, 1) <= end:
        months.append(date(year, month, 1))
        month += 1
        if month > 12:
            month = 1
            year += 1
    return months


def get_historical_gram_price(target_date: date) -> float | None:
    date_key = target_date.strftime("%Y%m%d")
    history = _read_history_cache()

    if date_key in history:
        return round_num(float(history[date_key]))

    api_key = get_gold_api_key()
    if not api_key:
        return None

    try:
        url = f"{GOLD_API_URL}/{date_key}"
        response = requests.get(
            url,
            headers={
                "x-access-token": api_key,
                "Content-Type": "application/json",
            },
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
        _log_api_request(f"historical:{date_key}", success=True)
        ounce_price = float(payload["price"])
        gram_price = round_num(ounce_price / OUNCES_PER_GRAM)
        history[date_key] = gram_price
        _write_history_cache(history)
        return gram_price
    except Exception as exc:
        _log_api_request(f"historical:{date_key}", success=False, error=_api_error_code(exc))
        return None


def get_monthly_gram_prices(
    start: date,
    end: date,
    current_price: float,
) -> dict[str, float | None]:
    today = date.today()
    current_month_start = date(today.year, today.month, 1)
    prices: dict[str, float | None] = {}

    for month_start in _month_starts(start, end):
        key = month_start.isoformat()
        if month_start == current_month_start and current_price > 0:
            prices[key] = round_num(current_price)
        else:
            prices[key] = get_historical_gram_price(month_start)

    return prices


def get_projection_monthly_prices(current_price: float) -> dict[str, float | None]:
    end = date.today().replace(day=1)
    return get_monthly_gram_prices(PROJECTION_START, end, current_price)
