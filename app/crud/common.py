import logging
from typing import Annotated, Protocol, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import InstrumentedAttribute
from sqlmodel import Session, SQLModel, select

logger = logging.getLogger(__name__)


class HasId(Protocol):
    id: int


T = TypeVar("T", bound=SQLModel)
SQLModelWithId = TypeVar("SQLModelWithId", bound=Annotated[SQLModel, HasId])


def read_by_id(
    db: Session, model: Type[SQLModelWithId], elem_id: int
) -> SQLModelWithId | None:
    """Read one element by id"""
    logger.info(f"{type(model)=}")
    elem = select(model).where(model.id == elem_id)
    elem = db.exec(elem).one_or_none()
    return elem


def read_by_field(
    db: Session, field: InstrumentedAttribute, value: object
) -> SQLModel | None:
    """Read one element by field value"""
    elem = select(field.class_).where(field == value)
    elem = db.exec(elem).one_or_none()
    return elem


def read_by_field_many(
    db: Session, field: InstrumentedAttribute, value: object
) -> list[SQLModel] | None:
    """Read several elements by field value"""
    elem = select(field.class_).where(field == value)
    elem = db.exec(elem).all()
    return elem


def create(db: Session, model: Type[T], payload: SQLModel) -> T | None:
    """Create an element"""
    try:
        element = model(**payload.dict())
        db.add(element)
        db.commit()
        db.refresh(element)
        return element
    except IntegrityError:
        db.rollback()
        return None


def update(db: Session, db_obj: T, payload: SQLModel) -> T:
    """Update element's data"""
    obj_data = jsonable_encoder(db_obj)
    update_data = payload.dict(exclude_unset=True, exclude_none=True)
    for field in obj_data:
        if field in update_data:
            new_data = update_data[field]
            setattr(db_obj, field, new_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, db_obj: T) -> T:
    """Remove element from DB"""
    db.delete(db_obj)
    db.commit()
    return db_obj
