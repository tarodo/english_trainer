from sqlmodel import Session

from app.crud.quizzes import words
from app.models import WordInDB
from tests.utils.utils import random_lower_string


def test_user_create(db: Session) -> None:
    new_word = random_lower_string()
    translate = random_lower_string()
    word_in = WordInDB(word=new_word, translate=translate)
    word = words.create(db, payload=word_in)
    assert word
    assert word.word == new_word
    assert word.translate == translate
