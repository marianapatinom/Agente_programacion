"""Question classification for the programming tutor agent."""

from dataclasses import dataclass
import re
import unicodedata


CATEGORY_KEYWORDS = {
    "frontend": {
        "react",
        "useeffect",
        "html",
        "css",
        "dom",
        "componente",
        "frontend",
        "tailwind",
        "vite",
        "estado",
        "props",
    },
    "backend": {
        "backend",
        "fastapi",
        "django",
        "flask",
        "node",
        "express",
        "servidor",
        "endpoint",
        "controlador",
    },
    "databases": {
        "sql",
        "join",
        "tabla",
        "base",
        "datos",
        "postgres",
        "mysql",
        "mongodb",
        "consulta",
    },
    "algorithms": {
        "algoritmo",
        "ordenamiento",
        "busqueda",
        "recursion",
        "complejidad",
        "arbol",
        "grafo",
        "pila",
        "cola",
    },
    "debugging": {
        "error",
        "exception",
        "traceback",
        "undefined",
        "null",
        "fallo",
        "bug",
        "debug",
        "no funciona",
    },
    "apis": {
        "api",
        "rest",
        "http",
        "json",
        "request",
        "response",
        "status",
        "post",
        "get",
    },
    "python": {"python", "pip", "venv", "lista", "diccionario", "pytest"},
    "javascript": {
        "javascript",
        "js",
        "promise",
        "async",
        "await",
        "array",
        "npm",
        "node",
    },
    "java": {"java", "spring", "clase", "objeto", "public", "static", "jvm"},
    "security_devops": {
        "devops",
        "devsecops",
        "docker",
        "pipeline",
        "ci",
        "cd",
        "seguridad",
        "xss",
        "cors",
    },
}


@dataclass(frozen=True)
class QuestionIntent:
    """Detected programming category and response style."""

    category: str
    style: str
    topic: str


class QuestionClassifier:
    """Classify programming questions with deterministic lexical rules."""

    def classify(self, question: str) -> QuestionIntent:
        """Return category, style, and topic for a user question."""

        normalized = normalize_text(question)
        return QuestionIntent(
            category=self._detect_category(normalized),
            style=self._detect_style(normalized),
            topic=self._extract_topic(question),
        )

    def _detect_category(self, normalized: str) -> str:
        scores: dict[str, int] = {}
        for category, keywords in CATEGORY_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in normalized)
            if score:
                scores[category] = score
        if not scores:
            return "general_programming"
        return max(scores, key=scores.get)

    def _detect_style(self, normalized: str) -> str:
        if any(word in normalized for word in ("error", "traceback", "exception")):
            return "debugging"
        if any(word in normalized for word in ("ejemplo", "codigo", "hazme")):
            return "code_example"
        if any(word in normalized for word in ("diferencia", "comparar", " vs ")):
            return "comparison"
        if any(word in normalized for word in ("pasos", "como hago", "implementar")):
            return "steps"
        return "explanation"

    def _extract_topic(self, question: str) -> str:
        cleaned = re.sub(r"[?¿!¡]", "", question).strip()
        normalized = normalize_text(cleaned)
        patterns = [
            r"que es (?P<topic>.+)",
            r"explicame (?P<topic>.+)",
            r"explica (?P<topic>.+)",
            r"como funciona (?P<topic>.+)",
            r"por que (?P<topic>.+)",
            r"hazme (?P<topic>.+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, normalized)
            if match:
                return match.group("topic").strip()
        return cleaned[:90] or "programacion"


def normalize_text(text: str) -> str:
    """Lowercase text and remove accents for matching."""

    decomposed = unicodedata.normalize("NFKD", text.lower())
    return "".join(char for char in decomposed if not unicodedata.combining(char))
