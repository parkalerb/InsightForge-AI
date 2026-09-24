import logging
import os
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.schemas.indexing import DocumentChunk

logger = logging.getLogger("insightforge.services.vector_store")

DEFAULT_VECTOR_DB_DIR = os.path.join("data", "vector_db")
DEFAULT_COLLECTION_NAME = "insightforge_documents"


class VectorStoreService:
    """Service encapsulating local persistent vector database storage using ChromaDB."""

    def __init__(self, persist_directory: str = DEFAULT_VECTOR_DB_DIR):
        self.persist_directory = persist_directory
        os.makedirs(self.persist_directory, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=ChromaSettings(anonymized_telemetry=False),
        )

    def get_or_create_collection(self, collection_name: str = DEFAULT_COLLECTION_NAME):
        """Retrieve or create a named ChromaDB collection."""
        return self.client.get_or_create_collection(name=collection_name)

    def add_chunks(
        self,
        chunks: List[DocumentChunk],
        embeddings: List[List[float]],
        collection_name: str = DEFAULT_COLLECTION_NAME,
    ) -> int:
        """Store chunk text, vector embeddings, and metadata payload in the vector database.

        Args:
            chunks: List of DocumentChunk instances.
            embeddings: List of embedding vectors corresponding to chunks.
            collection_name: Name of target collection.

        Returns:
            Number of chunks stored.

        Raises:
            ValueError: If chunk count does not match embedding count or if lists are empty.
        """
        if not chunks or not embeddings:
            raise ValueError("Chunks and embeddings lists cannot be empty.")
        if len(chunks) != len(embeddings):
            raise ValueError(
                f"Mismatch: received {len(chunks)} chunks but {len(embeddings)} embeddings."
            )

        collection = self.get_or_create_collection(collection_name)

        ids: List[str] = []
        documents: List[str] = []
        metadatas: List[Dict[str, Any]] = []

        for chunk in chunks:
            ids.append(chunk.chunk_id)
            documents.append(chunk.text)

            # ChromaDB requires primitive metadata values (str, int, float, bool)
            meta: Dict[str, Any] = {
                "chunk_id": str(chunk.chunk_id),
                "document_name": str(chunk.document_name),
                "document_type": str(chunk.document_type),
                "source": str(chunk.source),
                "chunk_index": int(chunk.chunk_index),
            }
            if chunk.page_number is not None:
                meta["page_number"] = int(chunk.page_number)
            else:
                meta["page_number"] = -1

            metadatas.append(meta)

        try:
            collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
            )
            logger.info(
                "Indexed %d chunks into collection '%s' at '%s'.",
                len(chunks),
                collection_name,
                self.persist_directory,
            )
            return len(chunks)
        except Exception as exc:
            logger.error("Error storing chunks in ChromaDB: %s", exc, exc_info=True)
            raise ValueError("Failed to store chunks in vector database.") from exc

    def get_collection_count(self, collection_name: str = DEFAULT_COLLECTION_NAME) -> int:
        """Return total document count in the specified collection."""
        try:
            collection = self.get_or_create_collection(collection_name)
            return collection.count()
        except Exception as exc:
            logger.error("Error querying collection count: %s", exc)
            return 0

    def delete_collection(self, collection_name: str = DEFAULT_COLLECTION_NAME) -> None:
        """Delete a collection from the vector database (useful for test resets)."""
        try:
            self.client.delete_collection(name=collection_name)
            logger.info("Deleted collection '%s'.", collection_name)
        except Exception:
            pass
