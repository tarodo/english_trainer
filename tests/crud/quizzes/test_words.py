from sqlmodel import Session

from app.crud.quizzes import words
from app.models import WordInDB, WordSetInDB
from tests.utils.users import create_random_user
from tests.utils.utils import random_lower_string


def test_word_create(db: Session) -> None:
    new_word = random_lower_string()
    translate = random_lower_string()
    word_in = WordInDB(word=new_word, translate=translate)
    word = words.create(db, payload=word_in)
    assert word
    assert word.word == new_word
    assert word.translate == translate


def test_word_set_create(db: Session) -> None:
    new_set_title = random_lower_string()
    user = create_random_user(db)
    user_id = user.id
    set_in = WordSetInDB(title=new_set_title, owner_id=user_id)
    new_set = words.create_set(db, payload=set_in)
    assert new_set
    assert new_set.title == new_set_title
    assert new_set.owner_id == user_id
