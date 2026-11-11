from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.schemas import UserRegister
from app.core.security import hash_password, verify_password


def register_user(db: Session, data: UserRegister):
    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if existing_user:
        return None

    user = User(
        full_name=data.full_name,
        email=data.email,
        password_hash=hash_password(data.password),
        role="cliente",
        active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(db: Session, email: str, password: str):
    user = (
        db.query(User)
        .filter(
            User.email == email,
            User.active == True
        )
        .first()
    )

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user