from datetime import timedelta
from enum import Enum
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.api import deps
from app.api.tools import raise_400
from app.core import security
from app.core.config import settings
from app.crud import users
from app.models import responses
from app.models.token import Token, BotLoginPayload
from app.models import User


class LoginErrors(Enum):
    IncorrectCredentials = "Incorrect email or password"
    UserIsNotBot = "User is not a bot"


router = APIRouter()


@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = users.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise_400(LoginErrors.IncorrectCredentials)
        return

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/access-token-bot", response_model=Token, responses=responses)
def login_access_token_by_bot(
    payload: BotLoginPayload,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Login user by bot.
    """
    if not current_user.is_bot:
        return raise_400(LoginErrors.UserIsNotBot)

    user = users.read_by_tg_id(db, payload.tg_id)
    if not user:
        return raise_400(LoginErrors.IncorrectCredentials)

    return {
        "access_token": security.create_access_token(user.id),
        "token_type": "bearer",
    }
