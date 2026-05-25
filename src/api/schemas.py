"""Pydantic schemas used by the StudyBot API."""

from pydantic import BaseModel, Field

from src.validator import MAX_QUESTION_LENGTH


class QuestionRequest(BaseModel):
    """Request payload for student questions."""

    question: str = Field(
        ...,
        min_length=1,
        max_length=MAX_QUESTION_LENGTH,
        description="Academic question to be answered by the agent.",
        examples=["What is DevSecOps?"],
    )


class AnswerResponse(BaseModel):
    """Response payload returned by the agent."""

    question: str
    answer: str
    source: str


class HealthResponse(BaseModel):
    """Health response for runtime platforms."""

    status: str
    environment: str
