import logging

import random
from sqlmodel import Session

from app.crud import common
from app.models import Word, WordInDB, WordSet, WordSetInDB, WordUpdate, WordQuizz

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


def collect_quizz(word_set: WordSet, words_cnt: int) -> list[WordQuizz]:
    result = []
    if word_set.words:
        logger.info(f"{words_cnt=} :: {len(word_set.words)=}")
        quizz_words: list[Word] = random.sample(
            word_set.words, min(words_cnt, len(word_set.words))
        )
        for one_word in quizz_words:
            wrong_words = random.sample(list(set(quizz_words) - {one_word}), 3)
            one_word_quiz = WordQuizz(
                word=one_word.word,
                id=one_word.id,
                translate=one_word.translate,
                wrong_words=wrong_words,
            )
            result.append(one_word_quiz)
    return result
