"""Local programming knowledge retrieval."""

from dataclasses import dataclass
from pathlib import Path
import re

from src.programming.classifier import normalize_text


STOPWORDS = {
    "como",
    "cual",
    "cuando",
    "dame",
    "de",
    "del",
    "el",
    "en",
    "es",
    "explica",
    "la",
    "las",
    "los",
    "para",
    "por",
    "que",
    "un",
    "una",
    "y",
}


@dataclass(frozen=True)
class KnowledgeEntry:
    """One searchable knowledge item loaded from notes.txt."""

    topic: str
    content: str


class KnowledgeBase:
    """Load and search local programming notes."""

    def __init__(self, notes_path: Path) -> None:
        self.notes_path = notes_path

    def load_entries(self) -> list[KnowledgeEntry]:
        """Load entries formatted as 'topic: content'."""

        notes = self.notes_path.read_text(encoding="utf-8")
        entries: list[KnowledgeEntry] = []
        for line in notes.splitlines():
            if ":" not in line:
                continue
            topic, content = line.split(":", maxsplit=1)
            if topic.strip() and content.strip():
                entries.append(
                    KnowledgeEntry(topic=topic.strip(), content=content.strip())
                )
        return entries

    def search(
        self,
        question: str,
        category: str,
        limit: int = 3,
    ) -> list[KnowledgeEntry]:
        """Return the most relevant entries for a question."""

        question_terms = tokenize(question)
        scored_entries: list[tuple[int, KnowledgeEntry]] = []
        normalized_question = normalize_text(question)

        for entry in self.load_entries():
            searchable = f"{entry.topic} {entry.content}"
            entry_terms = tokenize(searchable)
            score = len(question_terms.intersection(entry_terms))

            if normalize_text(entry.topic) in normalized_question:
                score += 4
            if category in normalize_text(entry.content):
                score += 1

            if score > 0:
                scored_entries.append((score, entry))

        scored_entries.sort(key=lambda item: item[0], reverse=True)
        return [entry for _, entry in scored_entries[:limit]]


def tokenize(text: str) -> set[str]:
    """Tokenize text into searchable words."""

    words = re.findall(r"[a-z0-9]+", normalize_text(text))
    return {word for word in words if len(word) > 2 and word not in STOPWORDS}
