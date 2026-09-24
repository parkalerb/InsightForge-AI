import logging
from typing import List, Union
from sentence_transformers import SentenceTransformer

logger = logging.getLogger("insightforge.services.embeddings")

DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingService:
    """Service responsible for generating local vector embeddings using sentence-transformers."""

    def __init__(self, model_name: str = DEFAULT_MODEL_NAME):
        self.model_name = model_name
        self._model: Union[SentenceTransformer, None] = None
        self._dimension: int = 384

    @property
    def model(self) -> SentenceTransformer:
        """Lazy-load sentence-transformer model."""
        if self._model is None:
            logger.info("Loading local embedding model '%s'...", self.model_name)
            self._model = SentenceTransformer(self.model_name)
            if hasattr(self._model, "get_embedding_dimension"):
                self._dimension = self._model.get_embedding_dimension() or 384
            else:
                self._dimension = getattr(self._model, "get_sentence_embedding_dimension")() or 384
        return self._model

    @property
    def embedding_dimension(self) -> int:
        """Return the vector dimension size of the current embedding model."""
        if self._model is not None:
            return self._dimension
        return 384

    def generate_embedding(self, text: str) -> List[float]:
        """Generate a single vector embedding for a text string.

        Args:
            text: Input text string.

        Returns:
            List of floats representing the embedding vector.

        Raises:
            ValueError: If input text is empty or invalid.
        """
        if not text or not text.strip():
            raise ValueError("Text content cannot be empty for embedding generation.")

        try:
            vec = self.model.encode(text, convert_to_numpy=True)
            return vec.tolist()
        except Exception as exc:
            logger.error("Error generating embedding: %s", exc, exc_info=True)
            raise ValueError("Failed to generate vector embedding.") from exc

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate vector embeddings for a list of text strings in batch.

        Args:
            texts: List of text strings.

        Returns:
            List of float lists representing vector embeddings for each input text.
        """
        if not texts:
            return []

        clean_texts = [t.strip() for t in texts if t and t.strip()]
        if not clean_texts:
            raise ValueError("Batch contains no non-empty text strings.")

        try:
            vectors = self.model.encode(clean_texts, convert_to_numpy=True)
            return [vec.tolist() for vec in vectors]
        except Exception as exc:
            logger.error("Error generating batch embeddings: %s", exc, exc_info=True)
            raise ValueError("Failed to generate batch vector embeddings.") from exc
