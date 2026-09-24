import logging
from typing import Optional

from app.schemas.document import DocumentSchema
from app.schemas.indexing import IndexingResult
from app.services.chunking import ChunkingService
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStoreService

logger = logging.getLogger("insightforge.services.indexing")


class IndexingService:
    """Orchestrates document chunking, embedding generation, and vector store indexing."""

    def __init__(
        self,
        chunking_service: Optional[ChunkingService] = None,
        embedding_service: Optional[EmbeddingService] = None,
        vector_store_service: Optional[VectorStoreService] = None,
    ):
        self.chunking_service = chunking_service or ChunkingService()
        self.embedding_service = embedding_service or EmbeddingService()
        self.vector_store_service = vector_store_service or VectorStoreService()

    def index_document(
        self,
        document: DocumentSchema,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        collection_name: Optional[str] = None,
    ) -> IndexingResult:
        """Run complete indexing workflow for a DocumentSchema.

        Args:
            document: Clean DocumentSchema produced by ingestion.
            chunk_size: Optional custom maximum chunk size in characters.
            chunk_overlap: Optional custom overlap in characters.
            collection_name: Optional custom target vector store collection name.

        Returns:
            IndexingResult detailing chunks created, chunks indexed, and embedding dimension.
        """
        try:
            # 1. Create chunks from clean document
            chunks = self.chunking_service.chunk_document(
                document=document,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )

            if not chunks:
                return IndexingResult(
                    document_name=document.document_name,
                    chunks_created=0,
                    chunks_indexed=0,
                    embedding_dimension=self.embedding_service.embedding_dimension,
                    status="failed",
                    message="Document contained no non-empty text chunks to index.",
                )

            # 2. Extract chunk texts and generate embeddings
            chunk_texts = [c.text for c in chunks]
            embeddings = self.embedding_service.generate_embeddings_batch(chunk_texts)

            # 3. Store in vector database
            target_collection = collection_name or "insightforge_documents"
            indexed_count = self.vector_store_service.add_chunks(
                chunks=chunks,
                embeddings=embeddings,
                collection_name=target_collection,
            )

            dim = self.embedding_service.embedding_dimension

            logger.info(
                "Successfully indexed document '%s': %d chunks indexed into collection '%s'.",
                document.document_name,
                indexed_count,
                target_collection,
            )

            return IndexingResult(
                document_name=document.document_name,
                chunks_created=len(chunks),
                chunks_indexed=indexed_count,
                embedding_dimension=dim,
                status="success",
                message=f"Successfully created and vector-indexed {indexed_count} chunks.",
            )

        except Exception as exc:
            logger.error(
                "Indexing failed for document '%s': %s", document.document_name, exc, exc_info=True
            )
            return IndexingResult(
                document_name=document.document_name,
                chunks_created=0,
                chunks_indexed=0,
                embedding_dimension=self.embedding_service.embedding_dimension,
                status="failed",
                message=f"Indexing failed: {str(exc)}",
            )
