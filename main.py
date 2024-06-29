import logging

import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.api import login, users
from app.api.quizzes import words

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(users.router, prefix="/users", tags=["users"])
    application.include_router(words.router, prefix="/words", tags=["words"])
    application.include_router(login.router, tags=["login"])
    add_pagination(application)
    logger.info("Start project")
    return application


app = create_application()


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
