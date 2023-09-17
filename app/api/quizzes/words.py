from enum import Enum

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api import deps
from app.crud.quizzes import words
from app.models import Word, WordInApi, WordInDB, WordOut, responses

router = APIRouter()


class SentenceErrors(Enum):
    NoRightsForUser = "User doesn't have rights"


@router.post("/", response_model=WordOut, status_code=200, responses=responses)
def create_word(
    payload: WordInApi,
    # current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Word | None:
    """Create one sentence"""

    word_in = WordInDB(**payload.dict())
    word = words.create(db, word_in)
    return word
