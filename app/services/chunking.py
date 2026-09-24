import logging
import re
from typing import List, Optional

from app.schemas.document import DocumentSchema
from app.schemas.indexing import DocumentChunk

logger = logging.getLogger("insightforge.services.chunking")


class ChunkingService:
    """Service responsible for splitting clean documents into character-bounded chunks with overlap."""

    def __init__(self, default_chunk_size: int = 1000, default_chunk_overlap: int = 150):
        self.default_chunk_size = default_chunk_size
        self.default_chunk_overlap = default_chunk_overlap

    def chunk_document(
        self,
        document: DocumentSchema,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
    ) -> List[DocumentChunk]:
        """Splits a DocumentSchema into a list of DocumentChunks while preserving page and source metadata.

        Args:
            document: Clean document representation produced by ingestion.
            chunk_size: Target maximum characters per chunk.
            chunk_overlap: Number of overlapping characters between consecutive chunks.

        Returns:
            List of DocumentChunk instances.

        Raises:
            ValueError: If overlap is greater than or equal to chunk size or if parameters are invalid.
        """
        size = chunk_size if chunk_size is not None else self.default_chunk_size
        overlap = chunk_overlap if chunk_overlap is not None else self.default_chunk_overlap

        if size <= 0:
            raise ValueError("chunk_size must be a positive integer.")
        if overlap < 0:
            raise ValueError("chunk_overlap cannot be negative.")
        if overlap >= size:
            raise ValueError("chunk_overlap must be strictly less than chunk_size.")

        chunks: List[DocumentChunk] = []
        global_chunk_index = 0

        # Clean document name for safe chunk IDs
        clean_doc_name = re.sub(r"[^\w\-]", "_", document.document_name)

        if document.document_type == "pdf" and document.pages:
            # Preserve page boundaries for multi-page documents
            for page in document.pages:
                page_text = page.text.strip()
                if not page_text:
                    continue

                page_chunks_text = self._split_text(page_text, size, overlap)
                for text_segment in page_chunks_text:
                    chunk_id = f"{clean_doc_name}_p{page.page_number or 0}_c{global_chunk_index}"
                    chunks.append(
                        DocumentChunk(
                            chunk_id=chunk_id,
                            document_name=document.document_name,
                            document_type=document.document_type,
                            source=document.source,
                            page_number=page.page_number,
                            chunk_index=global_chunk_index,
                            text=text_segment,
                            metadata={
                                "char_count": len(text_segment),
                                "source": document.source,
                                "document_type": document.document_type,
                            },
                        )
                    )
                    global_chunk_index += 1
        else:
            # Single text document or TXT file
            full_text = document.extracted_text.strip()
            if full_text:
                text_segments = self._split_text(full_text, size, overlap)
                for text_segment in text_segments:
                    chunk_id = f"{clean_doc_name}_c{global_chunk_index}"
                    chunks.append(
                        DocumentChunk(
                            chunk_id=chunk_id,
                            document_name=document.document_name,
                            document_type=document.document_type,
                            source=document.source,
                            page_number=None,
                            chunk_index=global_chunk_index,
                            text=text_segment,
                            metadata={
                                "char_count": len(text_segment),
                                "source": document.source,
                                "document_type": document.document_type,
                            },
                        )
                    )
                    global_chunk_index += 1

        logger.info(
            "Chunked document '%s' (%s) into %d chunks (size=%d, overlap=%d).",
            document.document_name,
            document.document_type,
            len(chunks),
            size,
            overlap,
        )
        return chunks

    @staticmethod
    def _split_text(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
        """Splits a single text string into character segments with defined overlap."""
        if len(text) <= chunk_size:
            return [text]

        segments: List[str] = []
        step = chunk_size - chunk_overlap
        start = 0

        while start < len(text):
            end = start + chunk_size
            segment = text[start:end].strip()
            if segment:
                segments.append(segment)
            start += step

        return segments
