from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models import User


class WordSetConnector(SQLModel, table=True):  # type: ignore
    __tablename__ = "word_set_connector"

    word_id: int = Field(foreign_key="word.id", primary_key=True)
    set_id: int = Field(foreign_key="word_set.id", primary_key=True)


class WordBase(SQLModel):
    word: str = Field(..., min_length=1)
    translate: str = Field(..., min_length=1)


class Word(WordBase, table=True):  # type: ignore
    id: int = Field(primary_key=True)
    sets: list["WordSet"] = Relationship(
        back_populates="words", link_model=WordSetConnector
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)


class WordInApi(WordBase):
    pass


class WordInDB(WordBase):
    pass


class WordUpdate(WordBase):
    pass


class WordOut(Word):
    pass


class WordSetBase(SQLModel):
    title: str
    owner_id: int = Field(foreign_key="et_user.id")


class WordSet(WordSetBase, table=True):  # type: ignore
    __tablename__ = "word_set"

    id: int = Field(primary_key=True)
    words: list[Word] = Relationship(back_populates="sets", link_model=WordSetConnector)

    owner: "User" = Relationship(back_populates="word_sets")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class WordSetInDB(WordSetBase):
    pass
