import logging
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("insightforge")
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for application startup and shutdown."""
    logger.info("Starting %s in %s mode", settings.APP_NAME, settings.ENVIRONMENT)
    yield
    logger.info("Shutting down %s", settings.APP_NAME)


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Basic global exception handler for unexpected server errors."""
    logger.error("Unhandled error processing request %s: %s", request.url.path, exc, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": "error", "message": "An internal server error occurred."},
    )


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, Any]:
    """Health check endpoint indicating API status."""
    return {
        "status": "ok",
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
    }
