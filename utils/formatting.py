from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

from utils.privacy import (
    format_profit_direction,
    is_privacy_mode,
    mask_count,
    mask_date,
    mask_money,
    mask_weight,
)

SAUDI_TZ = ZoneInfo("Asia/Riyadh")


def round_num(value: float) -> float:
    return round(float(value), 1)


def format_currency(value: float, currency: str = "SAR", signed: bool = False) -> str:
    v = round_num(value)
    if signed:
        return f"{v:+,.1f} {currency}"
    return f"{v:,.1f} {currency}"


def format_currency_ar(value: float, signed: bool = False) -> str:
    v = round_num(value)
    if signed:
        return f"{v:+,.1f} ر.س"
    return f"{v:,.1f} ر.س"


def format_percentage(value: float, signed: bool = True) -> str:
    v = round_num(value)
    if signed:
        return f"{v:+,.1f}%"
    return f"{v:,.1f}%"


def format_ownership(value: float) -> str:
    if is_privacy_mode():
        return "••%"
    v = round_num(value)
    return f"{v:,.1f}%"


def format_grams(value: float) -> str:
    return f"{round_num(value):,.1f} g"


def format_grams_ar(value: float) -> str:
    v = round_num(value)
    grams = f"{v:.0f}" if v == int(v) else f"{v:.1f}"
    return f"{grams} جرام"


def format_date(value: date | datetime | str) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    return value.strftime("%Y-%m-%d")


def format_date_ar(value: date | datetime | str) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, datetime):
        return value.strftime("%d-%m-%Y")
    return value.strftime("%d-%m-%Y")


def format_money(value: float, lang: str = "ar", signed: bool = False) -> str:
    if is_privacy_mode():
        if signed:
            return format_profit_direction(value, lang)
        return mask_money(lang)
    if lang == "ar":
        return format_currency_ar(value, signed=signed)
    return format_currency(value, signed=signed)


def format_weight(value: float, lang: str = "ar") -> str:
    if is_privacy_mode():
        return mask_weight(lang)
    if lang == "ar":
        return format_grams_ar(value)
    return format_grams(value)


def format_date_local(value: date | datetime | str, lang: str = "ar") -> str:
    if is_privacy_mode():
        return mask_date()
    if lang == "ar":
        return format_date_ar(value)
    return format_date(value)


def _parse_datetime(value: str | datetime) -> datetime | None:
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def format_datetime_local(value: str | datetime, lang: str = "ar") -> str:
    if is_privacy_mode():
        return mask_date()
    dt = _parse_datetime(value)
    if not dt:
        return str(value)[:19].replace("T", " ")

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    saudi_dt = dt.astimezone(SAUDI_TZ)

    if lang == "ar":
        return saudi_dt.strftime("%d-%m-%Y %H:%M")
    return saudi_dt.strftime("%Y-%m-%d %H:%M")


def ltr_text(value: str) -> str:
    """Wrap text so numbers/dates display correctly in RTL layout."""
    return f"\u2066{value}\u2069"
