import streamlit as st


def is_privacy_mode() -> bool:
    return bool(st.session_state.get("privacy_mode", False))


def mask_money(lang: str = "ar") -> str:
    return "•••••• ر.س" if lang == "ar" else "•••••• SAR"


def mask_weight(lang: str = "ar") -> str:
    return "•••• جرام" if lang == "ar" else "•••• g"


def mask_date() -> str:
    return "••/••/••••"


def mask_count() -> str:
    return "••"


def format_profit_direction(value: float, lang: str = "ar") -> str:
    is_profit = value >= 0
    arrow = "↑" if is_profit else "↓"
    if lang == "ar":
        label = "ربح" if is_profit else "خسارة"
    else:
        label = "Profit" if is_profit else "Loss"
    return f"{label} {arrow}"
