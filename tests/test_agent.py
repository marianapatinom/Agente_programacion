"""Unit and API tests for StudyBot Agent."""

from fastapi.testclient import TestClient

from src.agent import StudyBotAgent
from src.main import app
from src.validator import InputValidationError, sanitize_question, validate_question


client = TestClient(app)


def test_agent_answers_from_notes_for_devsecops() -> None:
    agent = StudyBotAgent()

    result = agent.answer("Que es un framework?")

    assert result["source"] == "programming-notes.txt"
    assert "framework" in result["answer"].lower()


def test_agent_returns_fallback_for_unknown_question() -> None:
    agent = StudyBotAgent()

    result = agent.answer("Que es literatura medieval?")

    assert "programación" in result["answer"]


def test_agent_answers_related_academic_topics() -> None:
    agent = StudyBotAgent()

    result = agent.answer("Explícame qué hace useEffect en React")

    assert "react" in result["answer"].lower()
    assert "efectos" in result["answer"].lower()


def test_agent_returns_code_example_for_fastapi() -> None:
    agent = StudyBotAgent()

    result = agent.answer("Hazme un ejemplo de API REST con FastAPI")

    assert "```python" in result["answer"]
    assert "FastAPI" in result["answer"]


def test_agent_answers_simple_greeting() -> None:
    agent = StudyBotAgent()

    result = agent.answer("Hola")

    assert "Hola" in result["answer"]
    assert "StudyBot" in result["answer"]


def test_validate_question_blocks_script_tag() -> None:
    try:
        validate_question("<script>alert('xss')</script>")
    except InputValidationError as exc:
        assert "script" in str(exc)
    else:
        raise AssertionError("Expected InputValidationError")


def test_validate_question_blocks_sql_injection() -> None:
    try:
        validate_question("DROP TABLE students;")
    except InputValidationError as exc:
        assert "SQL" in str(exc)
    else:
        raise AssertionError("Expected InputValidationError")


def test_validate_question_blocks_long_input() -> None:
    try:
        validate_question("a" * 501)
    except InputValidationError as exc:
        assert "500" in str(exc)
    else:
        raise AssertionError("Expected InputValidationError")


def test_sanitize_question_escapes_html() -> None:
    sanitized = sanitize_question("  Que es <b>FastAPI</b>?  ")

    assert sanitized == "Que es &lt;b&gt;FastAPI&lt;/b&gt;?"


def test_ask_endpoint_returns_answer() -> None:
    response = client.post("/ask", json={"question": "Que es FastAPI?"})

    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "programming-notes.txt"
    assert "FastAPI" in body["answer"]


def test_ask_endpoint_rejects_malicious_input() -> None:
    response = client.post("/ask", json={"question": "SELECT * FROM users"})

    assert response.status_code == 400
    assert "SQL" in response.json()["detail"]


def test_health_endpoint_returns_environment() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "environment" in response.json()


def test_api_prefixed_ask_endpoint_returns_answer() -> None:
    response = client.post("/api/ask", json={"question": "Que es SQL?"})

    assert response.status_code == 200
    assert response.json()["source"] == "programming-notes.txt"
