"""HTTP routes for the StudyBot Agent API."""

import logging

from fastapi import APIRouter, HTTPException, status

from src.agent import StudyBotAgent
from src.api.schemas import AnswerResponse, HealthResponse, QuestionRequest
from src.config import settings
from src.validator import InputValidationError, sanitize_question, validate_question


router = APIRouter()
logger = logging.getLogger(__name__)
agent = StudyBotAgent()


@router.get("/health", response_model=HealthResponse, tags=["health"])
def health_check() -> HealthResponse:
    """Return service health status for deployment platforms."""

    return HealthResponse(status="ok", environment=settings.app_env)


@router.post("/ask", response_model=AnswerResponse, tags=["agent"])
def ask_question(payload: QuestionRequest) -> AnswerResponse:
    """Validate, sanitize, and answer a student question."""

    try:
        validate_question(payload.question)
        clean_question = sanitize_question(payload.question)
        result = agent.answer(clean_question)
        logger.info("Question answered successfully")
        return AnswerResponse(**result)
    except InputValidationError as exc:
        logger.warning("Rejected unsafe question: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except FileNotFoundError as exc:
        logger.exception("Knowledge source is unavailable")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Knowledge source is not available.",
        ) from exc
