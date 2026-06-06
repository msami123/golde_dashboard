from datetime import datetime

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    gold_bars: Mapped[list["GoldBar"]] = relationship(
        "GoldBar",
        back_populates="owner",
        cascade="all, delete-orphan",
    )


class GoldBar(Base):
    __tablename__ = "gold_bars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    purchase_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    purchase_price: Mapped[float] = mapped_column(Float, nullable=False)
    grams: Mapped[float] = mapped_column(Float, nullable=False)
    bar_type: Mapped[str] = mapped_column(String(100), nullable=False)
    ownership_percentage: Mapped[float] = mapped_column(Float, default=100.0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    owner: Mapped["User"] = relationship("User", back_populates="gold_bars")
    participants: Mapped[list["OwnershipParticipant"]] = relationship(
        "OwnershipParticipant",
        back_populates="gold_bar",
        cascade="all, delete-orphan",
    )


class OwnershipParticipant(Base):
    __tablename__ = "ownership_participants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    gold_bar_id: Mapped[int] = mapped_column(ForeignKey("gold_bars.id"), nullable=False)
    participant_name: Mapped[str] = mapped_column(String(100), nullable=False)
    ownership_percentage: Mapped[float] = mapped_column(Float, nullable=False)

    gold_bar: Mapped["GoldBar"] = relationship("GoldBar", back_populates="participants")
