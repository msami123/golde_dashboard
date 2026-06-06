from datetime import date

import plotly.graph_objects as go

from services.portfolio_service import BarMetrics, MonthlySellRow
from utils.formatting import format_money, format_percentage, format_weight, round_num
from utils.i18n import format_month_label, get_lang, t
from utils.privacy import format_profit_direction, is_privacy_mode


def _arabic_font() -> str:
    return "Cairo, Tajawal, Noto Sans Arabic, sans-serif"


def _bar_label(bar_type: str, grams: float) -> str:
    lang = get_lang()
    if is_privacy_mode():
        return bar_type
    grams_text = f"{grams:.0f}g" if grams == int(grams) else f"{grams:.1f}g"
    return f"{bar_type} — {grams_text}"


def _pl_text(value: float, lang: str) -> str:
    if is_privacy_mode():
        return format_profit_direction(value, lang)
    return format_money(value, lang, signed=True)


def _amount_axis_config(currency_label: str) -> dict:
    config = dict(
        title=currency_label,
        tickformat=",.1f",
        gridcolor="rgba(255,255,255,0.08)",
        zerolinecolor="rgba(255,255,255,0.2)",
    )
    if is_privacy_mode():
        config["showticklabels"] = False
        config["title"] = ""
    return config


def _base_layout(title: str) -> dict:
    # نجعل عنوان الرسم يبدأ من اليمين ليتناسب مع العربية
    return dict(
        title=dict(text=title, x=1.0, xanchor="right"),
        font_family=_arabic_font(),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )


def portfolio_value_chart(
    metrics: list[BarMetrics],
    gram_price: float,
    title: str,
    invested_label: str,
    value_label: str,
) -> go.Figure:
    if not metrics:
        fig = go.Figure()
        fig.update_layout(title=title)
        return fig

    sorted_metrics = sorted(metrics, key=lambda x: x.purchase_date)
    dates: list[date] = []
    invested_series: list[float] = []
    value_series: list[float] = []
    cum_invested = 0.0
    cum_grams = 0.0

    for m in sorted_metrics:
        cum_invested += m.my_cost
        cum_grams += m.my_grams
        dates.append(m.purchase_date)
        invested_series.append(round_num(cum_invested))
        value_series.append(
            round_num(cum_grams * gram_price) if gram_price > 0 else round_num(cum_invested)
        )

    today = date.today()
    if not dates or dates[-1] != today:
        dates.append(today)
        invested_series.append(round_num(cum_invested))
        value_series.append(
            round_num(cum_grams * gram_price) if gram_price > 0 else round_num(cum_invested)
        )

    lang = get_lang()
    currency_label = "ر.س" if lang == "ar" else "SAR"
    hover_amount = "••••••" if is_privacy_mode() else f"%{{y:,.1f}} {currency_label}"

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=invested_series,
            mode="lines+markers",
            name=invested_label,
            line=dict(color="#d4af37", width=3),
            hovertemplate=f"%{{x}}<br>{invested_label}: {hover_amount}<extra></extra>",
        )
    )
    # اختر لون قيمة المحفظة حسب الربح/الخسارة الحالية
    final_invested = invested_series[-1]
    final_value = value_series[-1]
    value_color = "#2ecc71" if final_value >= final_invested else "#e74c3c"

    fig.add_trace(
        go.Scatter(
            x=dates,
            y=value_series,
            mode="lines+markers",
            name=value_label,
            line=dict(color=value_color, width=3),
            hovertemplate=f"%{{x}}<br>{value_label}: {hover_amount}<extra></extra>",
        )
    )
    fig.update_layout(
        **_base_layout(title),
        hovermode="x unified",
        margin=dict(l=20, r=20, t=60, b=40),
        yaxis=_amount_axis_config(currency_label),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.05)",
            showticklabels=not is_privacy_mode(),
        ),
    )
    return fig


def profit_distribution_chart(metrics: list[BarMetrics], title: str) -> go.Figure:
    if not metrics:
        fig = go.Figure()
        fig.update_layout(title=title)
        return fig

    sorted_metrics = sorted(metrics, key=lambda x: x.profit_loss, reverse=True)
    labels = [_bar_label(m.bar_type, m.grams) for m in sorted_metrics]
    lang = get_lang()
    currency_label = "ر.س" if lang == "ar" else "SAR"
    values = [round_num(m.profit_loss) for m in sorted_metrics]
    colors = ["#2ecc71" if v >= 0 else "#e74c3c" for v in values]
    text_labels = [_pl_text(v, lang) for v in values]

    fig = go.Figure(
        data=[
            go.Bar(
                y=labels,
                x=values,
                orientation="h",
                marker_color=colors,
                text=text_labels,
                textposition="outside",
                textfont=dict(size=12, family=_arabic_font()),
                hovertemplate="%{y}<br>%{text}<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        **_base_layout(title),
        margin=dict(l=20, r=100, t=60, b=20),
        yaxis=dict(autorange="reversed"),
        xaxis=_amount_axis_config(currency_label),
        uniformtext_minsize=10,
        uniformtext_mode="hide",
    )
    return fig


def monthly_sell_chart(rows: list[MonthlySellRow], title: str) -> go.Figure:
    if not rows:
        fig = go.Figure()
        fig.update_layout(title=title)
        return fig

    lang = get_lang()
    currency_label = "ر.س" if lang == "ar" else "SAR"
    labels = [format_month_label(r.month_start, lang) for r in rows]
    values = [r.profit_loss for r in rows]
    colors = ["#2ecc71" if v >= 0 else "#e74c3c" for v in values]
    text_labels = [_pl_text(v, lang) for v in values]
    if is_privacy_mode():
        customdata = [[format_percentage(r.return_percentage)] for r in rows]
        hovertemplate = (
            f"%{{x}}<br>"
            f"{t('profit_loss')}: %{{text}}<br>"
            f"{t('return_pct')}: %{{customdata[0]}}"
            f"<extra></extra>"
        )
    else:
        customdata = [
            [format_weight(r.grams_owned, lang), format_percentage(r.return_percentage)]
            for r in rows
        ]
        hovertemplate = (
            f"%{{x}}<br>"
            f"{t('monthly_sell_grams')}: %{{customdata[0]}}<br>"
            f"{t('profit_loss')}: %{{text}}<br>"
            f"{t('return_pct')}: %{{customdata[1]}}"
            f"<extra></extra>"
        )

    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                marker_color=colors,
                text=text_labels,
                textposition="outside",
                textfont=dict(size=11, family=_arabic_font()),
                customdata=customdata,
                hovertemplate=hovertemplate,
            )
        ]
    )
    fig.update_layout(
        **_base_layout(title),
        margin=dict(l=20, r=20, t=60, b=80),
        xaxis=dict(tickangle=-25),
        yaxis=_amount_axis_config(currency_label),
        uniformtext_minsize=10,
        uniformtext_mode="hide",
    )
    return fig
