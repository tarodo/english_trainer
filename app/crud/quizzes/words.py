import logging

from sqlmodel import Session

from app.crud import common
from app.models import Word, WordInDB, WordSet, WordSetInDB, WordUpdate

logger = logging.getLogger(__name__)


def create(db: Session, payload: WordInDB) -> Word | None:
    """Create a word"""
    return common.create(db, Word, payload)


def read_by_id(db: Session, word_id: int) -> Word | None:
    """Read one word by id"""
    return common.read_by_id(db, Word, word_id)


def update(db: Session, db_obj: Word, payload: WordUpdate) -> Word:
    """Update word's data"""
    return common.update(db, db_obj, payload)


def remove(db: Session, db_obj: Word) -> Word:
    """Remove word from DB"""
    return common.remove(db, db_obj)


def create_set(db: Session, payload: WordSetInDB) -> WordSet | None:
    """Create a set for words"""
    return common.create(db, WordSet, payload)


def read_set_by_id(db: Session, word_set_id: int) -> WordSet | None:
    """Read one word set"""
    return common.read_by_id(db, WordSet, word_set_id)


def read_set_all(db: Session) -> list[WordSet] | None:
    """Read all word sets"""
    return common.read_all(db, WordSet)


def remove_set(db: Session, db_obj: WordSet) -> WordSet:
    """Remove word set from DB"""
    return common.remove(db, db_obj)
