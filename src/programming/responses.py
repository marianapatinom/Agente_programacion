"""Response generation templates for the programming tutor."""

from src.programming.classifier import QuestionIntent, normalize_text
from src.programming.knowledge import KnowledgeEntry


class ProgrammingResponder:
    """Generate natural, technical Markdown answers."""

    def respond(
        self,
        question: str,
        intent: QuestionIntent,
        entries: list[KnowledgeEntry],
    ) -> str:
        """Build a response adapted to the detected intent."""

        conversational = self._conversation(question)
        if conversational:
            return conversational

        if intent.style == "debugging":
            return self._debugging_response(entries)
        if intent.style == "code_example":
            return self._code_example_response(intent, entries)
        if intent.style == "comparison":
            return self._comparison_response(intent, entries)
        if intent.style == "steps":
            return self._steps_response(intent, entries)
        return self._explanation_response(intent, entries)

    def _conversation(self, question: str) -> str | None:
        normalized = normalize_text(question).strip()
        if normalized in {"hola", "buenas", "hey", "saludos"}:
            return (
                "Hola. Soy StudyBot, tu asistente de programación. "
                "Puedo ayudarte con errores, conceptos, algoritmos, APIs, "
                "Python, JavaScript, Java, SQL, HTML, CSS y desarrollo web."
            )
        if normalized in {"gracias", "muchas gracias", "thanks"}:
            return "Con gusto. Pásame otra duda o un fragmento de código."
        if normalized in {"ayuda", "help", "que puedes hacer"}:
            return (
                "Puedo ayudarte a:\n\n"
                "- Entender conceptos de programación.\n"
                "- Revisar errores de código.\n"
                "- Crear ejemplos en Python, JavaScript, Java o SQL.\n"
                "- Explicar algoritmos y estructuras de datos.\n"
                "- Diseñar APIs y componentes web."
            )
        return None

    def _explanation_response(
        self,
        intent: QuestionIntent,
        entries: list[KnowledgeEntry],
    ) -> str:
        return (
            f"## {self._title(intent.topic)}\n\n"
            f"{self._lead(intent, entries)}\n\n"
            "### Idea principal\n"
            "Piensa en el concepto por tres capas: qué problema resuelve, "
            "cómo se usa en código y qué errores comunes debes evitar.\n\n"
            "### Cómo estudiarlo\n"
            "1. Identifica la definición corta.\n"
            "2. Mira un ejemplo pequeño.\n"
            "3. Cambia una parte del ejemplo y observa el resultado.\n"
            "4. Explica con tus palabras cuándo lo usarías.\n\n"
            f"{self._related(entries)}"
        )

    def _steps_response(
        self,
        intent: QuestionIntent,
        entries: list[KnowledgeEntry],
    ) -> str:
        return (
            f"## Pasos para {intent.topic}\n\n"
            f"{self._lead(intent, entries)}\n\n"
            "1. Define la entrada y la salida esperada.\n"
            "2. Escribe una versión mínima que funcione.\n"
            "3. Valida casos normales y casos límite.\n"
            "4. Agrega manejo de errores.\n"
            "5. Refactoriza nombres, funciones y responsabilidades.\n"
            "6. Prueba el comportamiento con datos reales.\n\n"
            "Si me compartes tu código actual, puedo decirte qué cambiar."
        )

    def _comparison_response(
        self,
        intent: QuestionIntent,
        entries: list[KnowledgeEntry],
    ) -> str:
        return (
            f"## Comparación: {intent.topic}\n\n"
            "| Criterio | Qué mirar |\n"
            "| --- | --- |\n"
            "| Propósito | Qué problema resuelve cada opción |\n"
            "| Uso | En qué parte del sistema aparece |\n"
            "| Complejidad | Qué tanto código o configuración requiere |\n"
            "| Riesgos | Qué errores suelen aparecer |\n\n"
            f"{self._related(entries)}"
        )

    def _debugging_response(self, entries: list[KnowledgeEntry]) -> str:
        return (
            "## Revisemos el error\n\n"
            "Primero separa **síntoma**, **causa probable** y "
            "**prueba de verificación**.\n\n"
            "### Checklist rápido\n"
            "1. Lee la última línea del error.\n"
            "2. Ubica archivo y número de línea.\n"
            "3. Revisa variables, tipos de datos y dependencias.\n"
            "4. Ejecuta un caso mínimo para reproducirlo.\n\n"
            "```python\n"
            "try:\n"
            "    resultado = funcion_riesgosa()\n"
            "except Exception as exc:\n"
            "    print(type(exc).__name__, exc)\n"
            "```\n\n"
            "Pégame el traceback o el fragmento de código y lo revisamos "
            "línea por línea.\n\n"
            f"{self._related(entries)}"
        )

    def _code_example_response(
        self,
        intent: QuestionIntent,
        entries: list[KnowledgeEntry],
    ) -> str:
        if intent.category in {"backend", "apis", "python"}:
            return (
                "## Ejemplo de API REST con FastAPI\n\n"
                "```python\n"
                "from fastapi import FastAPI\n"
                "from pydantic import BaseModel\n\n"
                "app = FastAPI()\n\n"
                "class Item(BaseModel):\n"
                "    name: str\n"
                "    price: float\n\n"
                "@app.post('/items')\n"
                "def create_item(item: Item):\n"
                "    return {'message': 'Item creado', 'item': item}\n"
                "```\n\n"
                "```bash\n"
                "uvicorn main:app --reload\n"
                "```\n\n"
                "FastAPI valida el JSON antes de ejecutar la función.\n\n"
                f"{self._related(entries)}"
            )

        if intent.category in {"frontend", "javascript"}:
            return (
                "## Ejemplo en React\n\n"
                "```jsx\n"
                "import { useEffect, useState } from 'react';\n\n"
                "export default function Users() {\n"
                "  const [users, setUsers] = useState([]);\n\n"
                "  useEffect(() => {\n"
                "    fetch('/api/users')\n"
                "      .then((response) => response.json())\n"
                "      .then(setUsers);\n"
                "  }, []);\n\n"
                "  return users.map((user) => <p key={user.id}>{user.name}</p>);\n"
                "}\n"
                "```\n\n"
                "El arreglo vacío `[]` hace que el efecto corra una vez al montar."
            )

        return (
            f"## Ejemplo para {intent.topic}\n\n"
            "```text\n"
            "entrada -> validación -> procesamiento -> salida\n"
            "```\n\n"
            f"{self._related(entries)}"
        )

    def _lead(self, intent: QuestionIntent, entries: list[KnowledgeEntry]) -> str:
        if entries:
            return entries[0].content
        return (
            f"Te explico {intent.topic} desde programación: conviene verlo con "
            "definición, ejemplo y errores comunes."
        )

    def _related(self, entries: list[KnowledgeEntry]) -> str:
        if len(entries) <= 1:
            return ""
        lines = ["### Relacionado"]
        for entry in entries[1:3]:
            lines.append(f"- **{entry.topic}**: {entry.content}")
        return "\n".join(lines)

    def _title(self, topic: str) -> str:
        clean = topic.strip().capitalize()
        return clean if clean else "Concepto de programación"
