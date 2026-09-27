import pytest
from pydantic import ValidationError

from asklearnly.schemas.chat import ChatRequest, RetrievalStrategy


def build_request(**changes: object) -> ChatRequest:
    data: dict[str, object] = {
        "question": "Why does self-attention use scaling?",
        "source_ids": [18, 22],
        "strategy": "hybrid",
        "top_k": 5,
        "score_threshold": 0.25,
        "history": [
            {"role": "user", "content": "What is self-attention?"},
            {"role": "assistant", "content": "It relates tokens in a sequence."},
        ],
    }
    data.update(changes)

    return ChatRequest.model_validate(data)


def test_chat_request_accepts_valid_data() -> None:
    request = build_request()

    assert request.strategy is RetrievalStrategy.HYBRID
    assert request.source_ids == [18, 22]


def test_chat_request_serializes_using_camel_case() -> None:
    payload = build_request().model_dump(mode="json", by_alias=True)

    assert payload["sourceIds"] == [18, 22]
    assert payload["topK"] == 5
    assert payload["scoreThreshold"] == 0.25


def test_empty_source_ids_means_entire_library() -> None:
    request = build_request(source_ids=[])

    assert request.source_ids == []


def test_question_whitespace_is_removed() -> None:
    request = build_request(question="  What is RAG?  ")

    assert request.question == "What is RAG?"


def test_blank_question_is_rejected() -> None:
    with pytest.raises(ValidationError):
        build_request(question="   ")


def test_unknown_strategy_is_rejected() -> None:
    with pytest.raises(ValidationError):
        build_request(strategy="unknown")


@pytest.mark.parametrize("top_k", [0, 21])
def test_top_k_outside_limits_is_rejected(top_k: int) -> None:
    with pytest.raises(ValidationError):
        build_request(top_k=top_k)


def test_duplicate_source_ids_are_rejected() -> None:
    with pytest.raises(ValidationError):
        build_request(source_ids=[18, 18])


def test_more_than_twenty_history_messages_are_rejected() -> None:
    history = [{"role": "user", "content": f"Message {index}"} for index in range(21)]
    with pytest.raises(ValidationError):
        build_request(history=history)
