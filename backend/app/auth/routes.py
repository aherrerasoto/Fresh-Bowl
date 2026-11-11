from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.core.dependencies import get_current_user

from app.auth import service
from app.auth.models import User
from app.auth.schemas import (
    UserRegister,
    UserLogin,
    UserResponse
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    data: UserRegister,
    db: Session = Depends(get_db)
):
    user = service.register_user(db, data)

    if not user:
        raise HTTPException(
            status_code=409,
            detail="Ya existe una cuenta con ese correo"
        )

    return user


@router.post("/login")
def login(
    data: UserLogin,
    response: Response,
    db: Session = Depends(get_db)
):
    user = service.authenticate_user(
        db,
        data.email,
        data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos"
        )

    token = create_access_token(user.id, user.role)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/"
    )

    return {
        "message": "Inicio de sesión exitoso",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role
        }
    }


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        path="/"
    )

    return {"message": "Sesión cerrada correctamente"}


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user