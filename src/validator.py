"""Input validation and sanitization utilities."""

import html
import re


MAX_QUESTION_LENGTH = 500


class InputValidationError(ValueError):
    """Raised when user input violates security or quality rules."""


SCRIPT_PATTERN = re.compile(r"<\s*/?\s*script\b", re.IGNORECASE)
SQL_INJECTION_PATTERN = re.compile(
    r"(\bunion\b\s+\bselect\b|\bselect\b.+\bfrom\b|\binsert\b\s+\binto\b|"
    r"\bdelete\b\s+\bfrom\b|\bdrop\b\s+\btable\b|--|/\*|\*/|;)",
    re.IGNORECASE,
)


def validate_question(question: str) -> None:
    """Validate a question before it reaches the agent decision logic."""

    if not isinstance(question, str):
        raise InputValidationError("Question must be a string.")

    stripped_question = question.strip()
    if not stripped_question:
        raise InputValidationError("Question cannot be empty.")

    if len(stripped_question) > MAX_QUESTION_LENGTH:
        raise InputValidationError(
            f"Question exceeds the {MAX_QUESTION_LENGTH} character limit."
        )

    if SCRIPT_PATTERN.search(stripped_question):
        raise InputValidationError("Question contains a blocked script pattern.")

    if SQL_INJECTION_PATTERN.search(stripped_question):
        raise InputValidationError("Question contains a blocked SQL pattern.")


def sanitize_question(question: str) -> str:
    """Normalize whitespace and escape HTML-sensitive characters."""

    normalized = " ".join(question.strip().split())
    return html.escape(normalized, quote=True)
