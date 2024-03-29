from sqlmodel import Session

from app.core.config import settings
from app.crud import users
from app.models import UserIn


def init_db(db: Session) -> None:
    user = users.read_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserIn(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_admin=True,
            is_bot=True,
        )
        user = users.create(db, payload=user_in)
