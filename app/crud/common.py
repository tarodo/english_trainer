import logging
from typing import Type

from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql import Select
from sqlmodel import Session, SQLModel, select

logger = logging.getLogger(__name__)


def read_by_id(db: Session, Model: Type[SQLModel], elem_id: int) -> SQLModel | None:
    """Read one element by id"""
    logger.info(f"{type(Model)=}")
    elem = select(Model).where(Model.id == elem_id)
    elem = db.exec(elem).one_or_none()
    return elem


def read_by_field(
    db: Session, Field: InstrumentedAttribute, value: object
) -> SQLModel | None:
    """Read one element by field value"""
    elem = select(Field.class_).where(Field == value)
    elem = db.exec(elem).one_or_none()
    return elem


def read_by_field_many(
    db: Session, Field: InstrumentedAttribute, value: object
) -> list[SQLModel] | None:
    """Read several elements by field value"""
    elem = select(Field.class_).where(Field == value)
    elem = db.exec(elem).all()
    return elem


def create(db: Session, Model: Type[SQLModel], payload: SQLModel) -> SQLModel:
    """Create an element"""
    try:
        element = Model(**payload.dict())
        db.add(element)
        db.commit()
        db.refresh(element)
        return element
    except IntegrityError:
        db.rollback()


def update(db: Session, db_obj: SQLModel, payload: SQLModel) -> SQLModel:
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


def remove(db: Session, db_obj: SQLModel) -> SQLModel:
    """Remove element from DB"""
    db.delete(db_obj)
    db.commit()
    return db_obj


def read_all_select(Model: Type[SQLModel]) -> Select:
    return select(Model)
