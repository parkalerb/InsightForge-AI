import os
import shutil
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.document import DocumentPage, DocumentSchema
from app.services.chunking import ChunkingService
from app.services.embeddings import EmbeddingService
from app.services.indexing import IndexingService
from app.services.vector_store import VectorStoreService

client = TestClient(app)

TEST_VECTOR_DB_DIR = os.path.join("data", "test_vector_db")


@pytest.fixture(autouse=True)
def cleanup_test_db():
    """Cleanup test vector store directory after tests."""
    yield
    if os.path.exists(TEST_VECTOR_DB_DIR):
        try:
            shutil.rmtree(TEST_VECTOR_DB_DIR, ignore_errors=True)
        except Exception:
            pass


def test_chunking_normal_document():
    """Verify chunking service splits a normal document into chunks."""
    service = ChunkingService(default_chunk_size=100, default_chunk_overlap=20)
    doc = DocumentSchema(
        document_name="normal.txt",
        document_type="txt",
        extracted_text="A" * 250,
        pages=[DocumentPage(page_number=None, text="A" * 250)],
        source="normal.txt",
        metadata={"file_size_bytes": 250},
    )

    chunks = service.chunk_document(doc)
    assert len(chunks) > 1
    assert chunks[0].document_name == "normal.txt"
    assert chunks[0].chunk_index == 0
    assert chunks[1].chunk_index == 1


def test_chunking_overlap_behavior():
    """Verify that chunking overlap produces expected overlapping characters."""
    service = ChunkingService(default_chunk_size=50, default_chunk_overlap=10)
    text = "0123456789" * 10  # 100 chars
    doc = DocumentSchema(
        document_name="overlap.txt",
        document_type="txt",
        extracted_text=text,
        pages=[DocumentPage(page_number=None, text=text)],
        source="overlap.txt",
    )

    chunks = service.chunk_document(doc)
    assert len(chunks) >= 2
    # Second chunk start should overlap with first chunk end
    overlap_segment = chunks[0].text[-10:]
    assert chunks[1].text.startswith(overlap_segment[:5])


def test_chunking_no_empty_chunks():
    """Verify chunking service ignores empty pages and produces no empty chunks."""
    service = ChunkingService(default_chunk_size=100, default_chunk_overlap=10)
    doc = DocumentSchema(
        document_name="pdf_empty_pages.pdf",
        document_type="pdf",
        extracted_text="Valid page 1 text\n\nValid page 3 text",
        pages=[
            DocumentPage(page_number=1, text="Valid page 1 text"),
            DocumentPage(page_number=2, text="   "),  # Empty
            DocumentPage(page_number=3, text="Valid page 3 text"),
        ],
        source="pdf_empty_pages.pdf",
    )

    chunks = service.chunk_document(doc)
    assert len(chunks) == 2
    for c in chunks:
        assert len(c.text.strip()) > 0
    assert chunks[0].page_number == 1
    assert chunks[1].page_number == 3


def test_chunking_metadata_preservation():
    """Verify chunk metadata includes document_name, document_type, page_number, and source."""
    service = ChunkingService(default_chunk_size=200, default_chunk_overlap=20)
    doc = DocumentSchema(
        document_name="meta_doc.pdf",
        document_type="pdf",
        extracted_text="Page 1 text content here",
        pages=[DocumentPage(page_number=1, text="Page 1 text content here")],
        source="meta_doc.pdf",
    )

    chunks = service.chunk_document(doc)
    assert len(chunks) == 1
    chunk = chunks[0]
    assert chunk.document_name == "meta_doc.pdf"
    assert chunk.document_type == "pdf"
    assert chunk.page_number == 1
    assert chunk.source == "meta_doc.pdf"
    assert chunk.metadata["char_count"] == len(chunk.text)


def test_embedding_generation_and_dimension_consistency():
    """Verify local embedding generation and dimension consistency (384 for all-MiniLM-L6-v2)."""
    emb_service = EmbeddingService()
    vec1 = emb_service.generate_embedding("Test sentence for embedding.")
    vec2 = emb_service.generate_embedding("Another distinct sentence.")

    assert isinstance(vec1, list)
    assert len(vec1) == emb_service.embedding_dimension
    assert len(vec1) == len(vec2)
    assert len(vec1) == 384


def test_vector_store_initialization():
    """Verify VectorStoreService initializes persistent storage directory and ChromaDB client."""
    v_service = VectorStoreService(persist_directory=TEST_VECTOR_DB_DIR)
    assert os.path.exists(TEST_VECTOR_DB_DIR)
    count = v_service.get_collection_count("test_collection")
    assert count == 0


def test_successful_chunk_indexing_and_multiple_chunks():
    """Verify IndexingService chunks, embeds, and stores multiple document chunks in vector DB."""
    v_service = VectorStoreService(persist_directory=TEST_VECTOR_DB_DIR)
    idx_service = IndexingService(
        chunking_service=ChunkingService(default_chunk_size=50, default_chunk_overlap=10),
        vector_store_service=v_service,
    )

    doc = DocumentSchema(
        document_name="multi_chunk_doc.txt",
        document_type="txt",
        extracted_text="Paragraph 1 content. " * 5 + "\n\n" + "Paragraph 2 content. " * 5,
        pages=[DocumentPage(page_number=None, text="Paragraph 1 content. " * 5 + "\n\n" + "Paragraph 2 content. " * 5)],
        source="multi_chunk_doc.txt",
    )

    result = idx_service.index_document(doc, collection_name="test_multi_chunks")
    assert result.status == "success"
    assert result.chunks_created > 1
    assert result.chunks_indexed == result.chunks_created
    assert result.embedding_dimension == 384

    # Verify vector store collection count
    stored_count = v_service.get_collection_count("test_multi_chunks")
    assert stored_count == result.chunks_indexed


def test_api_index_endpoint_success():
    """Verify POST /documents/index API endpoint ingests and indexes sample.txt."""
    sample_txt_path = os.path.join("sample_documents", "sample.txt")
    assert os.path.exists(sample_txt_path)

    with open(sample_txt_path, "rb") as f:
        files = {"file": ("sample.txt", f, "text/plain")}
        response = client.post("/documents/index", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["document_name"] == "sample.txt"
    assert data["status"] == "success"
    assert data["chunks_indexed"] >= 1
    assert data["embedding_dimension"] == 384


def test_api_index_pdf_endpoint_success():
    """Verify POST /documents/index API endpoint ingests and indexes sample.pdf."""
    sample_pdf_path = os.path.join("sample_documents", "sample.pdf")
    assert os.path.exists(sample_pdf_path)

    with open(sample_pdf_path, "rb") as f:
        files = {"file": ("sample.pdf", f, "application/pdf")}
        response = client.post("/documents/index", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["document_name"] == "sample.pdf"
    assert data["status"] == "success"
    assert data["chunks_indexed"] >= 2
    assert data["embedding_dimension"] == 384
