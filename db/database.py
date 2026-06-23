from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config import get_database_url
from db.models import Base

_database_url = get_database_url()
_connect_args = {"check_same_thread": False} if _database_url.startswith("sqlite") else {}
_engine_kwargs: dict = {
    "connect_args": _connect_args,
    "pool_pre_ping": True,
}
if not _database_url.startswith("sqlite"):
    _engine_kwargs["pool_recycle"] = 300
engine = create_engine(_database_url, **_engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

_db_initialized = False


def init_db() -> None:
    global _db_initialized
    if _db_initialized:
        return
    Base.metadata.create_all(bind=engine)
    from services.auth_service import seed_admin_user

    seed_admin_user()
    _db_initialized = True


def get_session() -> Session:
    return SessionLocal()
