import pytest
from pydantic import ValidationError

from asklearnly.schemas.events import Citation, DoneEvent, ErrorEvent, RetrievalEvent, TokenEvent


def build_citation(**changes: object) -> Citation:
    data: dict[str, object] = {
        "id": "chunk-18-4",
        "source_id": 18,
        "title": "Attention mechanisms",
        "page_number": 6,
        "excerpt": "Scaled dot-product attention divides the scores.",
        "score": 0.86,
        "preview_url": ("http://localhost:8000/documents/18/preview#page=6"),
    }

    data.update(changes)

    return Citation.model_validate(data)


def test_citation_serializes_using_camel_case() -> None:
    payload = build_citation().model_dump(mode="json", by_alias=True)

    assert payload["sourceId"] == 18
    assert payload["pageNumber"] == 6
    assert "previewUrl" in payload


def test_retrieval_event_accepts_empty_citations() -> None:
    event = RetrievalEvent()

    assert event.citations == []


def test_citation_rejects_page_zero() -> None:
    with pytest.raises(ValidationError):
        build_citation(page_number=0)


@pytest.mark.parametrize("score", [-0.01, 1.01])
def test_citation_rejects_score_outside_range(score: float) -> None:
    with pytest.raises(ValidationError):
        build_citation(score=score)


def test_token_event_rejects_empty_delta() -> None:
    with pytest.raises(ValidationError):
        TokenEvent(delta="")


def test_token_event_preserves_whitespace_delta() -> None:
    event = TokenEvent(delta=" ")

    assert event.delta == " "


def test_done_event_serializes_finish_reason() -> None:
    event = DoneEvent(finish_reason="stop", model="configured-model")

    payload = event.model_dump(mode="json", by_alias=True)

    assert payload["finishReason"] == "stop"


def test_error_event_accepts_machine_code() -> None:
    event = ErrorEvent(
        code="generation_failed",
        message="The answer could not be completed.",
    )

    assert event.code == "generation_failed"


def test_error_event_rejects_invalid_machine_code() -> None:
    with pytest.raises(ValidationError):
        ErrorEvent(
            code="Generation Failed",
            message="The answer could not be completed.",
        )
