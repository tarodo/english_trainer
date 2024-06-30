from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models import User


class WordBase(SQLModel):
    word: str = Field(..., min_length=1)
    translate: str = Field(..., min_length=1)
    example: str | None = Field(None)


class Word(WordBase, table=True):  # type: ignore
    id: int = Field(primary_key=True)
    set_id: int = Field(foreign_key="word_set.id")

    set: "WordSet" = Relationship(back_populates="words")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Word):
            return self.id == other.id
        return False


class WordInApi(WordBase):
    pass


class WordInDB(WordBase):
    set_id: int


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


class WordSetOutComp(WordSetBase):
    id: int


class WordQuizz(SQLModel):
    word: str
    id: int
    translate: str
    wrong_words: list[Word]


class WordSetQuizz(SQLModel):
    title: str
    words: list[WordQuizz] | None
