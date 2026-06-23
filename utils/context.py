"""Request-scoped context for lang and privacy mode (works with Flask and Streamlit)."""

from contextvars import ContextVar

_lang: ContextVar[str] = ContextVar("lang", default="ar")
_privacy_mode: ContextVar[bool] = ContextVar("privacy_mode", default=False)


def get_lang() -> str:
    return _lang.get()


def set_lang(lang: str) -> None:
    _lang.set(lang if lang in ("ar", "en") else "ar")


def is_privacy_mode() -> bool:
    return _privacy_mode.get()


def set_privacy_mode(enabled: bool) -> None:
    _privacy_mode.set(bool(enabled))
