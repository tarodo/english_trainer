from typing import Any

from pydantic import BaseModel, Field


class Message(BaseModel):
    err: str = Field(..., description="Error code")
    message: str = Field(..., description="Full error message")


class ErrorMessage(BaseModel):
    detail: Message = Field(...)


responses: dict[int | str, dict[str, Any]] = {
    400: {"model": ErrorMessage, "description": "Bad Request"}
}
