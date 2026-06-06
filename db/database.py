from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config import get_database_url
from db.models import Base

_database_url = get_database_url()
_connect_args = {"check_same_thread": False} if _database_url.startswith("sqlite") else {}
engine = create_engine(_database_url, connect_args=_connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    from services.auth_service import seed_admin_user

    seed_admin_user()


def get_session() -> Session:
    return SessionLocal()
