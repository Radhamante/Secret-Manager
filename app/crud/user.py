from sqlalchemy.orm import Session

from app.hash_manager import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        return None
    return db_user


def get_user_by_uuid(db: Session, user_uuid: str) -> User:
    db_user = db.query(User).filter(User.uuid == user_uuid).first()
    return db_user


def get_user_by_username_password(db: Session, username: str, password: str) -> User:
    db_user = (
        db.query(User)
        .filter(
            User.username == username,
        )
        .first()
    )
    if db_user is None or not verify_password(password, db_user.hashed_password):
        return None
    return db_user
