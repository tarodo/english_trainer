from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models import User


class WordBase(SQLModel):
    word: str = Field(..., min_length=1)
    translate: str = Field(..., min_length=1)
    set_id: int = Field(foreign_key="word_set.id")


class Word(WordBase, table=True):  # type: ignore
    id: int = Field(primary_key=True)

    set: "WordSet" = Relationship(back_populates="words")
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
    words: list[Word] | None = Relationship(
        back_populates="set", sa_relationship_kwargs={"cascade": "delete"}
    )

    owner: "User" = Relationship(back_populates="word_sets")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class WordSetInApi(WordSetBase):
    pass


class WordSetInDB(WordSetBase):
    pass


class WordSetUpdate(WordSetBase):
    pass


class WordSetOut(WordSetBase):
    id: int
    words: list[Word] | None


class WordSetQuizz(SQLModel):
    title: str
    words: list[Word] | None
