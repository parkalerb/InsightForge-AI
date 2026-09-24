from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    """Represents a text chunk created from a document for vector indexing."""

    chunk_id: str = Field(..., description="Unique identifier for the chunk.")
    document_name: str = Field(..., description="Name of the source document.")
    document_type: str = Field(..., description="Type/extension of the document ('pdf' or 'txt').")
    source: str = Field(..., description="Original source or filename.")
    page_number: Optional[int] = Field(default=None, description="1-indexed page number if applicable.")
    chunk_index: int = Field(..., description="0-indexed sequence position of the chunk in the document.")
    text: str = Field(..., description="Clean text content of the chunk.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata key-value pairs.")


class IndexingResult(BaseModel):
    """Result summary returned after indexing a document into the vector store."""

    document_name: str = Field(..., description="Name of the indexed document.")
    chunks_created: int = Field(..., description="Total number of chunks generated.")
    chunks_indexed: int = Field(..., description="Total number of chunks successfully stored.")
    embedding_dimension: int = Field(..., description="Dimensionality of generated vector embeddings.")
    status: str = Field(..., description="Status of the indexing operation ('success' or 'failed').")
    message: str = Field(..., description="Informational message or detail summary.")
