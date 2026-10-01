from dataclasses import FrozenInstanceError

import pytest

from asklearnly.loaders.base import DocumentLoader, DocumentPayload, LoadedPage


def build_payload() -> DocumentPayload:
    return DocumentPayload(
        source_id=18,
        filename="attention.pdf",
        mime_type="application/pdf",
        checksum_sha256="a" * 64,
        content=b"%PDF-1.7 example",
    )


class FakeLoader:
    def load(self, document: DocumentPayload) -> tuple[LoadedPage, ...]:
        return (
            LoadedPage(
                source_id=document.source_id,
                page_number=1,
                text="Extracted Page Text.",
                checksum_sha256=document.checksum_sha256,
            ),
        )


def test_document_payload_accepts_valid_data() -> None:
    payload = build_payload()

    assert payload.source_id == 18
    assert isinstance(payload.content, bytes)


def test_document_payload_rejects_empty_content() -> None:
    with pytest.raises(ValueError, match="content"):
        DocumentPayload(
            source_id=18,
            filename="attention.pdf",
            mime_type="application/pdf",
            checksum_sha256="a" * 64,
            content=b"",
        )


def test_document_payload_rejects_non_positive_source_id() -> None:
    with pytest.raises(ValueError, match="source ID"):
        DocumentPayload(
            source_id=0,
            filename="attention.pdf",
            mime_type="application/pdf",
            checksum_sha256="a" * 64,
            content=b"%PDF",
        )


def test_loaded_page_rejects_non_positive_page_number() -> None:
    with pytest.raises(ValueError, match="page number"):
        LoadedPage(source_id=18, page_number=0, text="text", checksum_sha256="a" * 64)


def test_domain_values_are_immutable() -> None:
    payload = build_payload()

    with pytest.raises(FrozenInstanceError):
        payload.filename = "changed.pdf"


def test_fake_loader_satisfies_protocol() -> None:
    loader = FakeLoader()

    assert isinstance(loader, DocumentLoader)


def test_loader_preserves_page_lineage() -> None:
    payload = build_payload()
    pages = FakeLoader().load(payload)

    assert len(pages) == 1
    assert pages[0].source_id == payload.source_id
    assert pages[0].page_number == 1
    assert pages[0].checksum_sha256 == payload.checksum_sha256
