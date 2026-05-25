"""FastAPI entrypoint for StudyBot Agent."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router
from src.config import settings
from src.core.logging import configure_logging


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""

    configure_logging(settings.log_level)

    fastapi_app = FastAPI(
        title="StudyBot Agent API",
        description=(
            "Academic AI agent backend with validation, local knowledge "
            "tools, CORS, logging, and DevSecOps-friendly structure."
        ),
        version="2.0.0",
    )

    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    fastapi_app.include_router(router)
    fastapi_app.include_router(router, prefix="/api")
    return fastapi_app


app = create_app()
