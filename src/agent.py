"""Core orchestration for the StudyBot programming assistant."""

from pathlib import Path

from langchain_core.documents import Document

from src.programming.classifier import QuestionClassifier
from src.programming.knowledge import KnowledgeBase
from src.programming.responses import ProgrammingResponder


class StudyBotAgent:
    """Programming tutor agent backed by local technical knowledge."""

    def __init__(self, notes_path: Path | None = None) -> None:
        default_notes = Path(__file__).parent / "tools" / "notes.txt"
        self.notes_path = notes_path or default_notes
        self.classifier = QuestionClassifier()
        self.responder = ProgrammingResponder()

    def answer(self, question: str) -> dict[str, str]:
        """Return a JSON-serializable technical answer."""

        document = Document(
            page_content=self.notes_path.read_text(encoding="utf-8"),
            metadata={"source": "programming-notes.txt"},
        )
        intent = self.classifier.classify(question)
        entries = KnowledgeBase(self.notes_path).search(question, intent.category)
        answer = self.responder.respond(question, intent, entries)

        return {
            "question": question,
            "answer": answer,
            "source": str(document.metadata["source"]),
        }
