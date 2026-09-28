import pytest
from pydantic import ValidationError

from asklearnly.integrations.learnly.schemas import LearnlyPublishedDocument


def build_payload(**changes: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "id": 18,
        "slug": "attention-mechanisms",
        "originalFilename": "attention.pdf",
        "title": "Attention mechanisms",
        "topics": ["Deep learning"],
        "mimeType": "application/pdf",
        "checksumSha256": "A" * 64,
        "sizeBytes": 2048,
        "pageCount": 14,
        "previewUrl": "http://localhost:8000/documents/18/preview",
        "downloadUrl": "http://localhost:8000/documents/18/download",
        "updatedAt": "2026-09-19T08:30:00Z",
        "publishedAt": "2026-09-19T08:31:00Z",
        "description": "An additional field AskLearnly does not need.",
    }
    payload.update(changes)

    return payload


def test_learnly_document_parses_camel_case_response() -> None:
    document = LearnlyPublishedDocument.model_validate(build_payload())

    assert document.id == 18
    assert document.original_filename == "attention.pdf"
    assert document.page_count == 14


def test_checksum_is_normalized_to_lowercase() -> None:
    document = LearnlyPublishedDocument.model_validate(build_payload())

    assert document.checksum_sha256 == "a" * 64


def test_unneeded_learnly_fields_are_ignored() -> None:
    document = LearnlyPublishedDocument.model_validate(build_payload(viewCount=10, downloadCount=5))

    assert document.id == 18


def test_invalid_checksum_is_rejected() -> None:
    with pytest.raises(ValidationError):
        LearnlyPublishedDocument.model_validate(build_payload(checksumSha256="invalid"))


def test_zero_page_count_is_rejected() -> None:
    with pytest.raises(ValidationError):
        LearnlyPublishedDocument.model_validate(build_payload(pageCount=0))


def test_non_pdf_mime_type_is_rejected() -> None:
    with pytest.raises(ValidationError):
        LearnlyPublishedDocument.model_validate(build_payload(mimeType="text/plain"))


@pytest.mark.parametrize(
    "field",
    ["checksumSha256", "previewUrl", "downloadUrl"],
)
def test_required_sync_field_is_rejected_when_missing(field: str) -> None:
    payload = build_payload()
    payload.pop(field)

    with pytest.raises(ValidationError):
        LearnlyPublishedDocument.model_validate(payload)
