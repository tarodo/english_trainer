from enum import Enum

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api import deps
from app.api.tools import raise_400
from app.crud import users
from app.models import User, UserIn, UserOut, responses

router = APIRouter()


class UsersErrors(Enum):
    NoRightsForUser = "User doesn't have rights"
    UserWithEmailExists = "User with Email exists"


@router.post("/", response_model=UserOut, status_code=200, responses=responses)
def create_user(
    payload: UserIn,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> User:
    """Create One User"""
    if not current_user.is_admin:
        return raise_400(UsersErrors.NoRightsForUser)

    old_user = users.read_by_email(db, payload.email)
    if old_user:
        return raise_400(UsersErrors.UserWithEmailExists)

    user = users.create(db, payload)
    return user


@router.get("/me", response_model=UserOut, status_code=200, responses=responses)
def get_me(
    current_user: User = Depends(deps.get_current_user),
) -> User:
    """Get current user."""
    return current_user
