import io
import logging
from typing import List

import pypdf
from pypdf.errors import PdfReadError, PyPdfError

from app.schemas.document import DocumentPage, DocumentSchema

logger = logging.getLogger("insightforge.services.document_ingestion")

SUPPORTED_EXTENSIONS = {".pdf", ".txt"}


class DocumentIngestionService:
    """Service responsible for validating, parsing, and extracting text from PDF and TXT files."""

    def ingest_document(self, filename: str, content: bytes) -> DocumentSchema:
        """Main entry point to validate and process an uploaded document.

        Args:
            filename: Name of the uploaded file.
            content: Raw byte content of the file.

        Returns:
            DocumentSchema containing extracted text, page structures, and metadata.

        Raises:
            ValueError: If file extension is unsupported, file is empty, or PDF is unreadable.
        """
        if not content or len(content.strip()) == 0:
            raise ValueError("Uploaded file is empty.")

        ext = self._get_file_extension(filename)
        if ext not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type '{ext}'. Supported formats are: {', '.join(sorted(SUPPORTED_EXTENSIONS))}."
            )

        if ext == ".txt":
            return self._process_txt(filename, content)
        elif ext == ".pdf":
            return self._process_pdf(filename, content)
        else:
            raise ValueError(f"Unsupported file type '{ext}'.")

    @staticmethod
    def _get_file_extension(filename: str) -> str:
        """Extract lowercase file extension from filename."""
        if "." not in filename:
            return ""
        return "." + filename.rsplit(".", 1)[-1].lower()

    def _process_txt(self, filename: str, content: bytes) -> DocumentSchema:
        """Process plain text (.txt) files."""
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            try:
                text = content.decode("latin-1")
            except Exception as exc:
                raise ValueError("Failed to decode text file. Ensure valid UTF-8 encoding.") from exc

        clean_text = text.strip()
        if not clean_text:
            raise ValueError("TXT file contains no readable text.")

        page = DocumentPage(page_number=None, text=clean_text)

        return DocumentSchema(
            document_name=filename,
            document_type="txt",
            extracted_text=clean_text,
            pages=[page],
            source=filename,
            metadata={
                "file_size_bytes": len(content),
                "total_pages": 1,
                "character_count": len(clean_text),
            },
        )

    def _process_pdf(self, filename: str, content: bytes) -> DocumentSchema:
        """Process PDF (.pdf) files using pypdf."""
        try:
            pdf_reader = pypdf.PdfReader(io.BytesIO(content))
        except (PyPdfError, PdfReadError) as exc:
            logger.error("PyPdfError parsing %s: %s", filename, exc)
            raise ValueError("Corrupted or unreadable PDF file.") from exc
        except Exception as exc:
            logger.error("Unexpected error parsing PDF %s: %s", filename, exc)
            raise ValueError("Failed to process PDF document.") from exc

        if len(pdf_reader.pages) == 0:
            raise ValueError("PDF file contains no pages.")

        pages: List[DocumentPage] = []
        page_texts: List[str] = []

        for index, pdf_page in enumerate(pdf_reader.pages, start=1):
            try:
                extracted = pdf_page.extract_text() or ""
            except Exception as exc:
                logger.warning("Failed to extract text from page %d of %s: %s", index, filename, exc)
                extracted = ""

            clean_page_text = extracted.strip()
            if clean_page_text:
                pages.append(DocumentPage(page_number=index, text=clean_page_text))
                page_texts.append(clean_page_text)

        consolidated_text = "\n\n".join(page_texts).strip()

        if not consolidated_text:
            raise ValueError("PDF file contains no readable text.")

        return DocumentSchema(
            document_name=filename,
            document_type="pdf",
            extracted_text=consolidated_text,
            pages=pages,
            source=filename,
            metadata={
                "file_size_bytes": len(content),
                "total_pages": len(pdf_reader.pages),
                "non_empty_pages": len(pages),
                "character_count": len(consolidated_text),
            },
        )
