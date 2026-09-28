from typing import Annotated

from pydantic import AnyHttpUrl, Field, PositiveInt, StringConstraints

from asklearnly.schemas.base import ApiModel

NonEmptyText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class Citation(ApiModel):
    id: NonEmptyText
    source_id: PositiveInt
    title: NonEmptyText
    page_number: PositiveInt
    excerpt: NonEmptyText
    score: float = Field(ge=0, le=1)
    preview_url: AnyHttpUrl


class RetrievalEvent(ApiModel):
    citations: list[Citation] = Field(default_factory=list)


class TokenEvent(ApiModel):
    delta: str = Field(min_length=1)


class DoneEvent(ApiModel):
    finish_reason: NonEmptyText
    model: NonEmptyText


class ErrorEvent(ApiModel):
    code: str = Field(min_length=1, pattern=r"^[a-z][a-z0-9_]*$")
    message: NonEmptyText


class ApiErrorResponse(ApiModel):
    detail: NonEmptyText
    code: str = Field(
        min_length=1,
        pattern=r"^[a-z][a-z0-9_]*$",
    )
