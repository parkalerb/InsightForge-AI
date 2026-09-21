import logging
from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.schemas.document import DocumentSchema
from app.services.document_ingestion import DocumentIngestionService

logger = logging.getLogger("insightforge.api.documents")

router = APIRouter(prefix="/documents", tags=["documents"])
ingestion_service = DocumentIngestionService()


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
