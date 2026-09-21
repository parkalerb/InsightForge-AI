from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DocumentPage(BaseModel):
    """Represents a single page extracted from a document."""

    page_number: Optional[int] = Field(
        default=None,
        description="1-indexed page number if applicable to the document format."
    )
    text: str = Field(
        ...,
        description="Text content extracted from this page."
    )


class DocumentSchema(BaseModel):
    """Clean internal document representation for RAG pipeline ingestion."""

    document_name: str = Field(..., description="Original filename of the document.")
    document_type: str = Field(..., description="Document format ('pdf' or 'txt').")
    extracted_text: str = Field(..., description="Consolidated extracted text across all pages.")
    pages: List[DocumentPage] = Field(
        default_factory=list,
        description="Page-level structured content preserved during ingestion."
    )
    source: str = Field(..., description="Source reference identifier or filename.")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata payload containing character count, page count, file size, etc."
    )


class IngestionErrorResponse(BaseModel):
    """Structured error response for failed ingestion attempts."""

    detail: str = Field(..., description="Description of the ingestion error.")
