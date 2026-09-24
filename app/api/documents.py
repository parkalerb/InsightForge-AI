import logging
from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.schemas.document import DocumentSchema
from app.schemas.indexing import IndexingResult
from app.services.document_ingestion import DocumentIngestionService
from app.services.indexing import IndexingService

logger = logging.getLogger("insightforge.api.documents")

router = APIRouter(prefix="/documents", tags=["documents"])
ingestion_service = DocumentIngestionService()
indexing_service = IndexingService()


@router.post(
    "/ingest",
    response_model=DocumentSchema,
    status_code=status.HTTP_200_OK,
    summary="Ingest PDF or TXT document",
    description="Validates and extracts clean text, page boundaries, and metadata from an uploaded PDF or TXT document."
)
async def ingest_document(file: UploadFile = File(...)) -> DocumentSchema:
    """Ingest an uploaded PDF or TXT document."""
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is missing from upload."
        )

    try:
        content = await file.read()
        return ingestion_service.ingest_document(filename=file.filename, content=content)
    except ValueError as exc:
        logger.warning("Document ingestion failed for %s: %s", file.filename, exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        ) from exc
    except Exception as exc:
        logger.error("Unexpected error during document ingestion for %s: %s", file.filename, exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during document ingestion."
        ) from exc


@router.post(
    "/index",
    response_model=IndexingResult,
    status_code=status.HTTP_200_OK,
    summary="Ingest and Index PDF or TXT document into Vector DB",
    description="Accepts a document upload, extracts content, generates chunks, builds embeddings, and stores vectors in local database."
)
async def index_document(file: UploadFile = File(...)) -> IndexingResult:
    """Ingest and vector-index an uploaded document."""
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is missing from upload."
        )

    try:
        content = await file.read()
        doc = ingestion_service.ingest_document(filename=file.filename, content=content)
        result = indexing_service.index_document(document=doc)
        if result.status == "failed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )
        return result
    except ValueError as exc:
        logger.warning("Document indexing failed for %s: %s", file.filename, exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        ) from exc
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Unexpected error during document indexing for %s: %s", file.filename, exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during document indexing."
        ) from exc


@router.post(
    "/index-payload",
    response_model=IndexingResult,
    status_code=status.HTTP_200_OK,
    summary="Index pre-ingested DocumentSchema payload into Vector DB",
    description="Accepts a clean DocumentSchema payload and indexes its content into the local vector database."
)
async def index_document_payload(document: DocumentSchema) -> IndexingResult:
    """Index a pre-ingested DocumentSchema payload."""
    try:
        result = indexing_service.index_document(document=document)
        if result.status == "failed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )
        return result
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        ) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during payload indexing."
        ) from exc
