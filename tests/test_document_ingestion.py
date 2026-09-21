import os
from fastapi.testclient import TestClient

from app.main import app
from app.services.document_ingestion import DocumentIngestionService

client = TestClient(app)
ingestion_service = DocumentIngestionService()

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_documents")
SAMPLE_TXT_PATH = os.path.join(SAMPLE_DIR, "sample.txt")
SAMPLE_PDF_PATH = os.path.join(SAMPLE_DIR, "sample.pdf")


def test_txt_ingestion_api_success():
    """Verify that POST /documents/ingest succeeds for a valid TXT file."""
    assert os.path.exists(SAMPLE_TXT_PATH), "sample.txt file missing"
    with open(SAMPLE_TXT_PATH, "rb") as f:
        files = {"file": ("sample.txt", f, "text/plain")}
        response = client.post("/documents/ingest", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["document_name"] == "sample.txt"
    assert data["document_type"] == "txt"
    assert "Market Research & Strategy Analysis" in data["extracted_text"]
    assert len(data["pages"]) == 1
    assert data["pages"][0]["page_number"] is None
    assert data["metadata"]["total_pages"] == 1


def test_pdf_ingestion_api_success():
    """Verify that POST /documents/ingest succeeds for a valid PDF file and preserves page boundaries."""
    assert os.path.exists(SAMPLE_PDF_PATH), "sample.pdf file missing"
    with open(SAMPLE_PDF_PATH, "rb") as f:
        files = {"file": ("sample.pdf", f, "application/pdf")}
        response = client.post("/documents/ingest", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["document_name"] == "sample.pdf"
    assert data["document_type"] == "pdf"
    assert "Page 1" in data["extracted_text"]
    assert "Page 2" in data["extracted_text"]
    assert len(data["pages"]) == 2
    assert data["pages"][0]["page_number"] == 1
    assert data["pages"][1]["page_number"] == 2
    assert data["metadata"]["total_pages"] == 2


def test_empty_txt_ingestion_returns_400():
    """Verify that uploading an empty TXT file returns an HTTP 400 error."""
    files = {"file": ("empty.txt", b"", "text/plain")}
    response = client.post("/documents/ingest", files=files)

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "empty" in data["detail"].lower()


def test_unsupported_file_extension_returns_400():
    """Verify that uploading an unsupported file format (.docx) returns an HTTP 400 error."""
    files = {"file": ("report.docx", b"dummy content", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    response = client.post("/documents/ingest", files=files)

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "unsupported" in data["detail"].lower()


def test_corrupted_pdf_ingestion_returns_400():
    """Verify that uploading a corrupted PDF file returns an HTTP 400 error."""
    files = {"file": ("corrupt.pdf", b"not a valid pdf header", "application/pdf")}
    response = client.post("/documents/ingest", files=files)

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "corrupted" in data["detail"].lower() or "unreadable" in data["detail"].lower()


def test_service_direct_txt_extraction():
    """Direct service unit test verifying TXT text extraction and schema output."""
    sample_content = b"Direct Service Test Content\nLine 2"
    doc = ingestion_service.ingest_document("test.txt", sample_content)

    assert doc.document_name == "test.txt"
    assert doc.document_type == "txt"
    assert doc.extracted_text == "Direct Service Test Content\nLine 2"
    assert doc.metadata["character_count"] == len("Direct Service Test Content\nLine 2")
