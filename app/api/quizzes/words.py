from enum import Enum

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api import deps
from app.api.tools import raise_400
from app.crud.quizzes import words
from app.models import User, Word, WordInApi, WordInDB, WordOut, responses

router = APIRouter()


class WordErrors(Enum):
    NoRightsForUser = "User doesn't have rights"
    CreationError = "An error occurred in creating an entity"


@router.post("/", response_model=WordOut, status_code=200, responses=responses)
def create_word(
    payload: WordInApi,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Word | None:
    """
    This endpoint allows for the creation of a new word entry in the database.
    It is restricted to users with admin privileges.
    """
    if not current_user.is_admin:
        raise_400(WordErrors.NoRightsForUser)

    word_in = WordInDB(**payload.dict())
    word = words.create(db, word_in)
    if not word:
        raise_400(WordErrors.CreationError)
    return word
