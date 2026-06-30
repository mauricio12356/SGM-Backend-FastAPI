from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_token, hash_password, token_expiration, verify_password
from app.models import AuthToken, User
from app.repositories import TokenRepository, UserRepository


class AuthService:
    def __init__(self) -> None:
        self.users = UserRepository()
        self.tokens = TokenRepository()

    def authenticate(self, db: Session, email: str, password: str) -> AuthToken:
        user = self.users.by_email(db, email)
        if user is None or not user.active or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
        token = AuthToken(token=create_token(), expires_at=token_expiration(), user_id=user.id)
        db.add(token)
        db.commit()
        db.refresh(token)
        return token

    def ensure_default_admin(self, db: Session, email: str, password: str) -> User:
        existing = self.users.by_email(db, email)
        if existing:
            return existing
        user = User(
            first_name="Administrador",
            last_name="SGM",
            email=email,
            password_hash=hash_password(password),
            role="ADMIN",
            active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
