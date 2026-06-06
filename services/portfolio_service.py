from dataclasses import dataclass
from datetime import date
from types import SimpleNamespace

import pandas as pd
import streamlit as st
from sqlalchemy.orm import Session, joinedload

from db.models import GoldBar, OwnershipParticipant
from utils.formatting import round_num


@dataclass
class BarMetrics:
    id: int
    purchase_date: date
    bar_type: str
    grams: float
    purchase_price: float
    ownership_percentage: float
    notes: str | None
    my_grams: float
    my_cost: float
    cost_per_gram: float
    current_value: float
    profit_loss: float
    return_percentage: float
    participants: list[dict]


@dataclass
class MonthlySellRow:
    month_start: date
    grams_owned: float
    cost_owned: float
    price_per_gram: float
    sell_value: float
    profit_loss: float
    return_percentage: float


@dataclass
class PortfolioSummary:
    total_grams: float
    total_cost: float
    current_value: float
    profit_loss: float
    return_percentage: float
    num_bars: int
    avg_cost_per_gram: float


def _ownership_factor(ownership_percentage: float) -> float:
    return ownership_percentage / 100.0


def _bar_record_from_orm(bar: GoldBar) -> dict:
    return {
        "id": bar.id,
        "purchase_date": bar.purchase_date,
        "bar_type": bar.bar_type,
        "grams": bar.grams,
        "purchase_price": bar.purchase_price,
        "ownership_percentage": bar.ownership_percentage,
        "notes": bar.notes,
        "participants": [
            {
                "participant_name": p.participant_name,
                "ownership_percentage": p.ownership_percentage,
            }
            for p in bar.participants
        ],
    }


def _bar_from_record(record: dict) -> SimpleNamespace:
    return SimpleNamespace(
        id=record["id"],
        purchase_date=record["purchase_date"],
        bar_type=record["bar_type"],
        grams=record["grams"],
        purchase_price=record["purchase_price"],
        ownership_percentage=record["ownership_percentage"],
        notes=record["notes"],
        participants=[
            SimpleNamespace(
                participant_name=p["participant_name"],
                ownership_percentage=p["ownership_percentage"],
            )
            for p in record["participants"]
        ],
    )


@st.cache_data(show_spinner=False)
def _fetch_bar_records(_session: Session, user_id: int) -> tuple[dict, ...]:
    bars = (
        _session.query(GoldBar)
        .options(joinedload(GoldBar.participants))
        .filter(GoldBar.owner_id == user_id)
        .order_by(GoldBar.purchase_date.desc())
        .all()
    )
    return tuple(_bar_record_from_orm(bar) for bar in bars)


def _invalidate_user_bar_cache(user_id: int) -> None:
    _fetch_bar_records.clear()


def calculate_bar_metrics(bar: GoldBar, gram_price: float) -> BarMetrics:
    factor = _ownership_factor(bar.ownership_percentage)
    my_grams = bar.grams * factor
    my_cost = bar.purchase_price * factor
    cost_per_gram = bar.purchase_price / bar.grams if bar.grams else 0.0
    current_value = my_grams * gram_price
    profit_loss = current_value - my_cost
    return_percentage = (profit_loss / my_cost * 100) if my_cost else 0.0

    participants = [
        {
            "participant_name": p.participant_name,
            "ownership_percentage": p.ownership_percentage,
            "grams": bar.grams * _ownership_factor(p.ownership_percentage),
            "cost": bar.purchase_price * _ownership_factor(p.ownership_percentage),
            "current_value": bar.grams
            * _ownership_factor(p.ownership_percentage)
            * gram_price,
            "profit_loss": (
                bar.grams * _ownership_factor(p.ownership_percentage) * gram_price
            )
            - (bar.purchase_price * _ownership_factor(p.ownership_percentage)),
        }
        for p in bar.participants
    ]

    return BarMetrics(
        id=bar.id,
        purchase_date=bar.purchase_date,
        bar_type=bar.bar_type,
        grams=round_num(bar.grams),
        purchase_price=round_num(bar.purchase_price),
        ownership_percentage=round_num(bar.ownership_percentage),
        notes=bar.notes,
        my_grams=round_num(my_grams),
        my_cost=round_num(my_cost),
        cost_per_gram=round_num(cost_per_gram),
        current_value=round_num(current_value),
        profit_loss=round_num(profit_loss),
        return_percentage=round_num(return_percentage),
        participants=participants,
    )


def get_all_bars(session: Session, user_id: int) -> list[GoldBar]:
    return (
        session.query(GoldBar)
        .options(joinedload(GoldBar.participants))
        .filter(GoldBar.owner_id == user_id)
        .order_by(GoldBar.purchase_date.desc())
        .all()
    )


def get_bar_by_id(session: Session, bar_id: int, user_id: int) -> GoldBar | None:
    return (
        session.query(GoldBar)
        .options(joinedload(GoldBar.participants))
        .filter(GoldBar.id == bar_id, GoldBar.owner_id == user_id)
        .first()
    )


def get_portfolio_metrics(
    session: Session, gram_price: float, user_id: int
) -> tuple[list[BarMetrics], PortfolioSummary]:
    records = _fetch_bar_records(session, user_id)
    bars = [_bar_from_record(record) for record in records]
    metrics = [calculate_bar_metrics(bar, gram_price) for bar in bars]

    total_grams = sum(m.my_grams for m in metrics)
    total_cost = sum(m.my_cost for m in metrics)
    current_value = sum(m.current_value for m in metrics)
    profit_loss = current_value - total_cost
    return_percentage = (profit_loss / total_cost * 100) if total_cost else 0.0
    avg_cost_per_gram = (total_cost / total_grams) if total_grams else 0.0

    summary = PortfolioSummary(
        total_grams=round_num(total_grams),
        total_cost=round_num(total_cost),
        current_value=round_num(current_value),
        profit_loss=round_num(profit_loss),
        return_percentage=round_num(return_percentage),
        num_bars=len(metrics),
        avg_cost_per_gram=round_num(avg_cost_per_gram),
    )

    return metrics, summary


def metrics_to_dataframe(metrics: list[BarMetrics]) -> pd.DataFrame:
    if not metrics:
        return pd.DataFrame()

    return pd.DataFrame(
        [
            {
                "id": m.id,
                "purchase_date": m.purchase_date,
                "bar_type": m.bar_type,
                "grams": m.grams,
                "my_grams": m.my_grams,
                "purchase_price": m.purchase_price,
                "my_cost": m.my_cost,
                "cost_per_gram": m.cost_per_gram,
                "current_value": m.current_value,
                "profit_loss": m.profit_loss,
                "return_percentage": m.return_percentage,
                "ownership_percentage": m.ownership_percentage,
                "notes": m.notes or "",
            }
            for m in metrics
        ]
    )


def get_best_performing(metrics: list[BarMetrics]) -> BarMetrics | None:
    if not metrics:
        return None
    return max(metrics, key=lambda m: m.profit_loss)


def get_worst_performing(metrics: list[BarMetrics]) -> BarMetrics | None:
    if not metrics:
        return None
    return min(metrics, key=lambda m: m.profit_loss)


def get_most_expensive(metrics: list[BarMetrics]) -> BarMetrics | None:
    if not metrics:
        return None
    return max(metrics, key=lambda m: m.my_cost)


def get_cheapest(metrics: list[BarMetrics]) -> BarMetrics | None:
    if not metrics:
        return None
    return min(metrics, key=lambda m: m.my_cost)


def get_shared_bars(metrics: list[BarMetrics]) -> list[BarMetrics]:
    return [m for m in metrics if m.ownership_percentage < 100 or m.participants]


def create_bar(
    session: Session,
    user_id: int,
    purchase_date: date,
    purchase_price: float,
    grams: float,
    bar_type: str,
    ownership_percentage: float,
    notes: str | None,
    participants: list[dict] | None = None,
) -> GoldBar:
    bar = GoldBar(
        owner_id=user_id,
        purchase_date=purchase_date,
        purchase_price=purchase_price,
        grams=grams,
        bar_type=bar_type,
        ownership_percentage=ownership_percentage,
        notes=notes,
    )
    session.add(bar)
    session.flush()

    if participants:
        for p in participants:
            session.add(
                OwnershipParticipant(
                    gold_bar_id=bar.id,
                    participant_name=p["participant_name"],
                    ownership_percentage=p["ownership_percentage"],
                )
            )

    session.commit()
    session.refresh(bar)
    _invalidate_user_bar_cache(user_id)
    return bar


def update_bar(
    session: Session,
    bar_id: int,
    user_id: int,
    purchase_date: date,
    purchase_price: float,
    grams: float,
    bar_type: str,
    ownership_percentage: float,
    notes: str | None,
    participants: list[dict] | None = None,
) -> GoldBar | None:
    bar = get_bar_by_id(session, bar_id, user_id)
    if not bar:
        return None

    bar.purchase_date = purchase_date
    bar.purchase_price = purchase_price
    bar.grams = grams
    bar.bar_type = bar_type
    bar.ownership_percentage = ownership_percentage
    bar.notes = notes

    for participant in bar.participants:
        session.delete(participant)
    session.flush()

    if participants:
        for p in participants:
            session.add(
                OwnershipParticipant(
                    gold_bar_id=bar.id,
                    participant_name=p["participant_name"],
                    ownership_percentage=p["ownership_percentage"],
                )
            )

    session.commit()
    session.refresh(bar)
    _invalidate_user_bar_cache(user_id)
    return bar


def delete_bar(session: Session, bar_id: int, user_id: int) -> bool:
    bar = get_bar_by_id(session, bar_id, user_id)
    if not bar:
        return False
    session.delete(bar)
    session.commit()
    _invalidate_user_bar_cache(user_id)
    return True


def monthly_sell_projection(
    metrics: list[BarMetrics],
    monthly_prices: dict[str, float | None],
) -> list[MonthlySellRow]:
    rows: list[MonthlySellRow] = []

    for month_key in sorted(monthly_prices.keys()):
        month_start = date.fromisoformat(month_key)
        price = monthly_prices[month_key]
        if price is None:
            continue

        owned = [m for m in metrics if m.purchase_date < month_start]
        grams_owned = sum(m.my_grams for m in owned)
        cost_owned = sum(m.my_cost for m in owned)

        if grams_owned <= 0:
            continue

        sell_value = round_num(grams_owned * price)
        profit_loss = round_num(sell_value - cost_owned)
        return_percentage = round_num(
            (profit_loss / cost_owned * 100) if cost_owned else 0.0
        )

        rows.append(
            MonthlySellRow(
                month_start=month_start,
                grams_owned=round_num(grams_owned),
                cost_owned=round_num(cost_owned),
                price_per_gram=round_num(price),
                sell_value=sell_value,
                profit_loss=profit_loss,
                return_percentage=return_percentage,
            )
        )

    return rows


def forecast_portfolio(total_grams: float, total_cost: float, target_prices: list[float]) -> pd.DataFrame:
    rows = []
    for price in target_prices:
        value = round_num(total_grams * price)
        profit = round_num(value - total_cost)
        return_pct = round_num((profit / total_cost * 100) if total_cost else 0.0)
        rows.append(
            {
                "target_price": round_num(price),
                "portfolio_value": value,
                "profit": profit,
                "return_percentage": return_pct,
            }
        )
    return pd.DataFrame(rows)
