from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models import WordSet


class UserBase(SQLModel):
    email: EmailStr = Field(index=True, sa_column_kwargs={"unique": True})
    is_admin: bool = Field(default=False, nullable=False)
    is_bot: bool = Field(default=False, nullable=False)


class User(UserBase, table=True):  # type: ignore
    __tablename__ = "et_user"

    id: int = Field(primary_key=True)
    password: str = Field(...)

    word_sets: list["WordSet"] = Relationship(back_populates="owner")


class UserIn(UserBase):
    password: str = Field(...)


class UserOut(UserBase):
    id: int = Field(...)


class UserUpdate(SQLModel):
    email: EmailStr | None = None
    is_admin: bool | None = None
    is_bot: bool | None = None
    password: str | None = None
