"""Migrate an existing single-tenant database to multi-user schema."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sqlalchemy import inspect, text

from config import get_admin_password, get_admin_username
from db.database import engine, init_db
from db.models import Base, GoldBar, User
from services.auth_service import create_user, get_user_by_username


def _table_exists(table_name: str) -> bool:
    return table_name in inspect(engine).get_table_names()


def _column_exists(table_name: str, column_name: str) -> bool:
    columns = [col["name"] for col in inspect(engine).get_columns(table_name)]
    return column_name in columns


def migrate() -> None:
    Base.metadata.create_all(bind=engine)

    if not _table_exists("users"):
        print("Created users table.")

    admin_username = get_admin_username()
    admin_password = get_admin_password()

    from db.database import get_session

    session = get_session()
    try:
        admin = get_user_by_username(session, admin_username)
        if not admin:
            admin = create_user(session, admin_username, admin_password, is_admin=True)
            print(f"Created admin user: {admin.username}")
        else:
            print(f"Admin user already exists: {admin.username}")

        if _table_exists("gold_bars") and not _column_exists("gold_bars", "owner_id"):
            with engine.begin() as conn:
                conn.execute(text("ALTER TABLE gold_bars ADD COLUMN owner_id INTEGER"))
            print("Added owner_id column to gold_bars.")

        if _table_exists("gold_bars") and _column_exists("gold_bars", "owner_id"):
            orphan_count = (
                session.query(GoldBar)
                .filter((GoldBar.owner_id.is_(None)) | (GoldBar.owner_id == 0))
                .count()
            )
            if orphan_count:
                session.query(GoldBar).filter(
                    (GoldBar.owner_id.is_(None)) | (GoldBar.owner_id == 0)
                ).update({GoldBar.owner_id: admin.id}, synchronize_session=False)
                session.commit()
                print(f"Assigned {orphan_count} gold bar(s) to admin user.")
            else:
                print("No orphan gold bars to migrate.")
    finally:
        session.close()

    init_db()
    print("Migration complete.")


if __name__ == "__main__":
    migrate()
