"""Copy gold bars from local SQLite to the configured DATABASE_URL (e.g. Neon)."""

from __future__ import annotations

import sqlite3
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config import get_admin_username
from db.database import get_session
from services.auth_service import get_user_by_username
from services.portfolio_service import create_bar, get_all_bars

SQLITE_PATH = ROOT / "gold_portfolio.db"


def migrate() -> None:
    if not SQLITE_PATH.exists():
        print("No local gold_portfolio.db found.")
        return

    session = get_session()
    try:
        owner = get_user_by_username(session, get_admin_username())
        if not owner:
            raise RuntimeError(f"User '{get_admin_username()}' not found in target database.")

        existing = get_all_bars(session, owner.id)
        if existing:
            print(f"Target DB already has {len(existing)} bar(s) for {owner.username}. Skipping.")
            return

        conn = sqlite3.connect(SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        bars = conn.execute("SELECT * FROM gold_bars ORDER BY id").fetchall()
        participants_by_bar: dict[int, list[dict]] = {}
        for row in conn.execute("SELECT * FROM ownership_participants ORDER BY id"):
            participants_by_bar.setdefault(row["gold_bar_id"], []).append(
                {
                    "participant_name": row["participant_name"],
                    "ownership_percentage": row["ownership_percentage"],
                }
            )
        conn.close()

        for bar in bars:
            purchase_date = date.fromisoformat(bar["purchase_date"])
            create_bar(
                session,
                owner.id,
                purchase_date=purchase_date,
                purchase_price=bar["purchase_price"],
                grams=bar["grams"],
                bar_type=bar["bar_type"],
                ownership_percentage=bar["ownership_percentage"],
                notes=bar["notes"],
                participants=participants_by_bar.get(bar["id"], []),
            )

        print(f"Migrated {len(bars)} bar(s) to {owner.username} on remote database.")
    finally:
        session.close()


if __name__ == "__main__":
    migrate()
