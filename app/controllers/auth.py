from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import LoginRequest, TokenResponse
from app.services import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticación"])
service = AuthService()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    token = service.authenticate(db, payload.email, payload.password)
    return TokenResponse(access_token=token.token, expires_at=token.expires_at)
