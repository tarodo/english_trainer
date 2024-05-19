from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models import User


class QuestionAnswerBase(SQLModel):
    answer: str = Field(..., min_length=1)
    is_correct: bool = Field(...)
    question_id: int = Field(foreign_key="question.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class QuestionAnswer(QuestionAnswerBase, table=True):
    id: int = Field(primary_key=True)


class QuestionAnswerInApi(QuestionAnswerBase):
    pass


class QuestionAnswerInDB(QuestionAnswerBase):
    pass


class QuestionAnswerUpdate(QuestionAnswerBase):
    pass


class QuestionAnswerOut(QuestionAnswer):
    pass


class QuestionBase(SQLModel):
    question: str = Field(..., min_length=1)
    set_id: int = Field(foreign_key="question_set.id")


class Question(QuestionBase, table=True):  # type: ignore
    __tablename__ = "question"

    id: int = Field(primary_key=True)

    set: "QuestionSet" = Relationship(back_populates="questions")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class QuestionInApi(QuestionBase):
    pass


class QuestionInDB(QuestionBase):
    pass


class QuestionUpdate(QuestionBase):
    pass


class QuestionOut(Question):
    pass


class QuestionSetBase(SQLModel):
    title: str
    owner_id: int = Field(foreign_key="et_user.id")


class QuestionSet(QuestionSetBase, table=True):  # type: ignore
    __tablename__ = "question_set"

    id: int = Field(primary_key=True)
    questions: list[Question] | None = Relationship(
        back_populates="set", sa_relationship_kwargs={"cascade": "delete"}
    )

    owner: "User" = Relationship(back_populates="question_sets")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class QuestionSetInApi(QuestionSetBase):
    pass


class QuestionSetInDB(QuestionSetBase):
    pass


class QuestionSetUpdate(QuestionSetBase):
    pass


class QuestionSetOut(QuestionSetBase):
    id: int
    questions: list[Question] | None


class QuestionSetOutComp(QuestionSetBase):
    id: int


class QuestionSetQuizz(SQLModel):
    title: str
    questions: list[Question] | None
