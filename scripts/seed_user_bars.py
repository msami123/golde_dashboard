"""Replace database contents with the user's gold bars."""

from datetime import date

from config import get_admin_username
from db.database import get_session, init_db
from db.models import GoldBar, OwnershipParticipant
from services.auth_service import get_user_by_username
from services.portfolio_service import create_bar

USER_BARS = [
    {
        "purchase_date": date(2026, 1, 10),
        "purchase_price": 5530.0,
        "grams": 10.0,
        "bar_type": "ساعة",
        "ownership_percentage": 50.0,
        "notes": "املك فقط 50% من السبيكة",
        "participants": [
            {"participant_name": "محمد", "ownership_percentage": 50.0},
            {"participant_name": "حسين", "ownership_percentage": 50.0},
        ],
    },
    {
        "purchase_date": date(2026, 2, 10),
        "purchase_price": 6220.0,
        "grams": 10.0,
        "bar_type": "الكعبة",
        "ownership_percentage": 100.0,
        "notes": None,
        "participants": [],
    },
    {
        "purchase_date": date(2026, 3, 14),
        "purchase_price": 3325.0,
        "grams": 5.0,
        "bar_type": "الكعبة",
        "ownership_percentage": 100.0,
        "notes": None,
        "participants": [],
    },
    {
        "purchase_date": date(2026, 4, 1),
        "purchase_price": 2975.0,
        "grams": 5.0,
        "bar_type": "وطن",
        "ownership_percentage": 100.0,
        "notes": None,
        "participants": [],
    },
    {
        "purchase_date": date(2026, 4, 30),
        "purchase_price": 2850.0,
        "grams": 5.0,
        "bar_type": "حصان",
        "ownership_percentage": 100.0,
        "notes": None,
        "participants": [],
    },
    {
        "purchase_date": date(2026, 6, 3),
        "purchase_price": 2760.0,
        "grams": 5.0,
        "bar_type": "سبيكة",
        "ownership_percentage": 100.0,
        "notes": None,
        "participants": [],
    },
]


def main() -> None:
    init_db()
    session = get_session()
    try:
        session.query(OwnershipParticipant).delete()
        session.query(GoldBar).delete()
        session.commit()

        admin = get_user_by_username(session, get_admin_username())
        if not admin:
            raise RuntimeError("Admin user not found. Run init_db() or migrate_add_users.py first.")

        for bar_data in USER_BARS:
            create_bar(session, admin.id, **bar_data)

        print(f"Seeded {len(USER_BARS)} gold bars.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
