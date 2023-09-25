from enum import Enum

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api import deps
from app.api.tools import raise_400
from app.crud import common, users
from app.crud.quizzes import words
from app.models import (
    User,
    WordInApi,
    WordInDB,
    WordOut,
    WordSet,
    WordSetInApi,
    WordSetInDB,
    WordSetOut,
    responses,
)

router = APIRouter()


class WordErrors(Enum):
    NoRightsForUser = "User doesn't have rights"
    CreationError = "An error occurred in creating an entity"
    NoUserID = "There is no user with ID"
    NoSetID = "There is no set with ID"


@router.post("/", response_model=WordOut, status_code=200, responses=responses)
def create_word(
    payload: WordInApi,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> WordOut | None:
    """
    This endpoint allows for the creation of a new word entry in the database.
    """
    word_set_id = payload.set_id
    word_set = words.read_set_by_id(db, word_set_id)
    if not word_set:
        raise_400(WordErrors.NoSetID)

    word_in = WordInDB(**payload.dict())
    word = words.create(db, word_in)
    if not word:
        raise_400(WordErrors.CreationError)
    return word


@router.post("/sets", response_model=WordSetOut, status_code=200, responses=responses)
def create_word_set(
    payload: WordSetInApi,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> WordSetOut | None:
    owner = users.read_by_id(db, payload.owner_id)

    if not current_user.is_admin:
        if not owner or owner.id != current_user.id:
            raise_400(WordErrors.NoRightsForUser)
    else:
        if not owner:
            raise_400(WordErrors.NoUserID)

    word_set_in = WordSetInDB(**payload.dict())
    word_set = common.create(db, WordSet, word_set_in)
    if not word_set:
        raise_400(WordErrors.CreationError)
    return word_set
