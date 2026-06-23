"""Jinja2 template filters and globals."""

from utils.formatting import (
    format_date_local,
    format_datetime_local,
    format_money,
    format_ownership,
    format_percentage,
    format_weight,
    ltr_text,
)
from utils.i18n import format_month_label, get_lang, t


def register_filters(app) -> None:
    app.jinja_env.filters["money"] = format_money
    app.jinja_env.filters["weight"] = format_weight
    app.jinja_env.filters["pct"] = format_percentage
    app.jinja_env.filters["date_local"] = format_date_local
    app.jinja_env.filters["datetime_local"] = format_datetime_local
    app.jinja_env.filters["ownership"] = format_ownership
    app.jinja_env.filters["month_label"] = format_month_label
    app.jinja_env.filters["ltr"] = ltr_text

    app.jinja_env.globals.update(
        t=t,
        get_lang=get_lang,
        format_money=format_money,
        format_weight=format_weight,
        format_percentage=format_percentage,
        format_date_local=format_date_local,
        format_ownership=format_ownership,
        format_month_label=format_month_label,
        ltr_text=ltr_text,
    )
