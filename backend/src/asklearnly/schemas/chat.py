from enum import StrEnum
from typing import Annotated

from pydantic import Field, PositiveInt, StringConstraints, field_validator

from asklearnly.schemas.base import ApiModel

Question = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=4000)]

MessageContent = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50_000)
]


class RetrievalStrategy(StrEnum):
    SIMILARITY = "similarity"
    MMR = "mmr"
    HYBRID = "hybrid"
    ENSEMBLE = "ensemble"


class ChatRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(ApiModel):
    role: ChatRole
    content: MessageContent


class ChatRequest(ApiModel):
    question: Question
    source_ids: list[PositiveInt] = Field(default_factory=list)
    strategy: RetrievalStrategy = RetrievalStrategy.SIMILARITY
    top_k: int = Field(default=5, le=20, ge=1)
    score_threshold: float | None = Field(default=None, ge=0, le=1)
    history: list[ChatMessage] = Field(default_factory=list, max_length=20)

    @field_validator("source_ids")
    @classmethod
    def validate_unique_source_ids(cls, source_ids: list[int]) -> list[int]:
        if len(source_ids) != len(set(source_ids)):
            raise ValueError("source IDs must be unique")

        return source_ids
