import bcrypt
from sqlalchemy.orm import Session

from config import get_admin_password, get_admin_username
from db.database import get_session
from db.models import User


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False


def get_user_by_id(session: Session, user_id: int) -> User | None:
    return session.query(User).filter(User.id == user_id).first()


def get_user_by_username(session: Session, username: str) -> User | None:
    return session.query(User).filter(User.username == username.strip().lower()).first()


def list_users(session: Session) -> list[User]:
    return session.query(User).order_by(User.username).all()


def authenticate(session: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(session, username)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def create_user(
    session: Session,
    username: str,
    password: str,
    *,
    is_admin: bool = False,
) -> User:
    normalized = username.strip().lower()
    if not normalized:
        raise ValueError("username_required")
    if get_user_by_username(session, normalized):
        raise ValueError("username_taken")
    if len(password) < 6:
        raise ValueError("password_too_short")

    user = User(
        username=normalized,
        password_hash=hash_password(password),
        is_admin=is_admin,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: int) -> bool:
    user = get_user_by_id(session, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True


def change_password(session: Session, user_id: int, new_password: str) -> bool:
    if len(new_password) < 6:
        raise ValueError("password_too_short")
    user = get_user_by_id(session, user_id)
    if not user:
        return False
    user.password_hash = hash_password(new_password)
    session.commit()
    return True


def seed_admin_user() -> None:
    session = get_session()
    try:
        if session.query(User).count() > 0:
            return
        username = get_admin_username()
        password = get_admin_password()
        create_user(session, username, password, is_admin=True)
    finally:
        session.close()
