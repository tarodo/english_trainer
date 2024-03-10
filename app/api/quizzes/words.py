import logging
import random
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
    WordSetQuizz,
    responses,
)

router = APIRouter()

logger = logging.getLogger(__name__)


class WordErrors(Enum):
    NoRightsForUser = "User doesn't have rights"
    CreationError = "An error occurred in creating an entity"
    NoUserID = "There is no user with ID"
    NoSetID = "There is no set with ID"
    NoWordID = "There is no word with ID"


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


@router.get("/{word_id}/", response_model=WordOut, status_code=200, responses=responses)
def get_word(
    word_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> WordOut | None:
    word = words.read_by_id(db, word_id)
    if not word:
        raise_400(WordErrors.NoWordID)
    return word


@router.delete("/{word_id}/", response_model=None, status_code=200, responses=responses)
def remove_word(
    word_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> None:
    word = words.read_by_id(db, word_id)
    if not word:
        if current_user.is_admin:
            raise_400(WordErrors.NoWordID)
        else:
            raise_400(WordErrors.NoRightsForUser)
    else:
        words.remove(db, word)


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


@router.get(
    "/sets/{set_id}/", response_model=WordSetOut, status_code=200, responses=responses
)
def get_word_set(
    set_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> WordSet | None:
    word_set = words.read_set_by_id(db, set_id)
    if not word_set:
        if current_user.is_admin:
            raise_400(WordErrors.NoSetID)
        else:
            raise_400(WordErrors.NoRightsForUser)
    else:
        owner_id = word_set.owner_id
        if current_user.id != owner_id:
            if not current_user.is_admin:
                raise_400(WordErrors.NoRightsForUser)

    return word_set


@router.delete(
    "/sets/{set_id}/", response_model=None, status_code=200, responses=responses
)
def remove_word_set(
    set_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> None:
    word_set = words.read_set_by_id(db, set_id)
    if not word_set:
        if current_user.is_admin:
            raise_400(WordErrors.NoWordID)
        else:
            raise_400(WordErrors.NoRightsForUser)
    else:
        words.remove_set(db, word_set)


@router.get(
    "/quizz/{set_id}/",
    response_model=WordSetQuizz,
    status_code=200,
    responses=responses,
)
def get_word_set_quizz(
    set_id: int,
    count: int = 5,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> WordSetQuizz | None:
    word_set = words.read_set_by_id(db, set_id)
    if not word_set:
        if current_user.is_admin:
            return raise_400(WordErrors.NoSetID)
        else:
            return raise_400(WordErrors.NoRightsForUser)
    quizz_words = []
    if word_set.words:
        quizz_words = random.sample(word_set.words, min(count, len(word_set.words)))
    title = word_set.title
    return WordSetQuizz(title=title, words=quizz_words)
