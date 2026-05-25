"""Generate the StudyBot Agent project presentation PDF."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "presentacion-studybot-agent.pdf"
PAGE_SIZE = landscape((13.333 * inch, 7.5 * inch))
WIDTH, HEIGHT = PAGE_SIZE


def draw_background(pdf: canvas.Canvas) -> None:
    """Draw a dark SaaS-style slide background."""

    pdf.setFillColor(colors.HexColor("#05070d"))
    pdf.rect(0, 0, WIDTH, HEIGHT, fill=True, stroke=False)

    pdf.setStrokeColor(colors.HexColor("#12355f"))
    pdf.setLineWidth(0.3)
    for x in range(0, int(WIDTH), 42):
        pdf.line(x, 0, x, HEIGHT)
    for y in range(0, int(HEIGHT), 42):
        pdf.line(0, y, WIDTH, y)

    pdf.setFillColor(colors.Color(0.05, 0.45, 0.95, alpha=0.16))
    pdf.circle(WIDTH * 0.86, HEIGHT * 0.88, 170, fill=True, stroke=False)
    pdf.setFillColor(colors.Color(0.0, 0.8, 0.7, alpha=0.12))
    pdf.circle(WIDTH * 0.12, HEIGHT * 0.12, 140, fill=True, stroke=False)


def draw_title(pdf: canvas.Canvas, kicker: str, title: str) -> None:
    """Draw slide kicker and title."""

    pdf.setFillColor(colors.HexColor("#22d3ee"))
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(0.7 * inch, HEIGHT - 0.85 * inch, kicker.upper())

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 34)
    pdf.drawString(0.7 * inch, HEIGHT - 1.45 * inch, title)


def draw_bullets(pdf: canvas.Canvas, bullets: list[str], x: float, y: float) -> None:
    """Draw bullet list with consistent spacing."""

    pdf.setFont("Helvetica", 17)
    for bullet in bullets:
        pdf.setFillColor(colors.HexColor("#10b981"))
        pdf.circle(x, y + 5, 4, fill=True, stroke=False)
        pdf.setFillColor(colors.HexColor("#dbeafe"))
        pdf.drawString(x + 18, y, bullet)
        y -= 34


def draw_card(
    pdf: canvas.Canvas,
    x: float,
    y: float,
    w: float,
    h: float,
    label: str,
    body: str,
) -> None:
    """Draw a translucent-looking card approximation for PDF."""

    pdf.setFillColor(colors.Color(1, 1, 1, alpha=0.06))
    pdf.setStrokeColor(colors.HexColor("#1e3a5f"))
    pdf.roundRect(x, y, w, h, 8, fill=True, stroke=True)
    pdf.setFillColor(colors.HexColor("#22d3ee"))
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(x + 18, y + h - 32, label)
    pdf.setFillColor(colors.HexColor("#dbeafe"))
    pdf.setFont("Helvetica", 12)
    text = pdf.beginText(x + 18, y + h - 58)
    text.setLeading(17)
    for line in body.split("|"):
        text.textLine(line.strip())
    pdf.drawText(text)


def add_slide(
    pdf: canvas.Canvas,
    kicker: str,
    title: str,
    bullets: list[str],
    cards: list[tuple[str, str]] | None = None,
) -> None:
    """Create one presentation page."""

    draw_background(pdf)
    draw_title(pdf, kicker, title)
    draw_bullets(pdf, bullets, 0.9 * inch, HEIGHT - 2.25 * inch)

    if cards:
        card_w = 3.65 * inch
        card_h = 1.25 * inch
        start_x = 0.9 * inch
        y = 0.75 * inch
        for index, (label, body) in enumerate(cards):
            draw_card(
                pdf,
                start_x + index * (card_w + 0.25 * inch),
                y,
                card_w,
                card_h,
                label,
                body,
            )

    pdf.setFillColor(colors.HexColor("#64748b"))
    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(WIDTH - 0.7 * inch, 0.35 * inch, "StudyBot Agent")
    pdf.showPage()


def main() -> None:
    """Build the PDF presentation."""

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=PAGE_SIZE)
    pdf.setTitle("StudyBot Agent - Presentacion")

    add_slide(
        pdf,
        "Vision",
        "StudyBot Agent Full Stack",
        [
            "Plataforma academica para consultas asistidas por IA.",
            "Frontend React moderno conectado con backend FastAPI.",
            "Proyecto orientado a ciclo de vida DevSecOps.",
        ],
        [
            ("Stack", "Python 3.11 | FastAPI | React + Vite"),
            ("UX", "Dark mode | Glassmorphism | Animaciones"),
            ("Entrega", "Docker | GitHub Actions | Render"),
        ],
    )

    add_slide(
        pdf,
        "Arquitectura",
        "Flujo web limpio y desacoplado",
        [
            "El navegador consume la API REST mediante Axios.",
            "FastAPI valida, sanitiza y registra cada solicitud.",
            "El agente consulta notes.txt como herramienta externa.",
        ],
        [
            ("Frontend", "Componentes reutilizables | TailwindCSS"),
            ("Backend", "Routers | Schemas | Config | Logging"),
            ("Knowledge", "notes.txt como fuente controlada"),
        ],
    )

    add_slide(
        pdf,
        "Agente",
        "Decision simple, explicable y testeable",
        [
            "La logica del agente se mantiene separada de la API.",
            "LangChain Core se usa para representar el documento local.",
            "Las respuestas se retornan en JSON con fuente visible.",
        ],
        [
            ("Entrada", "Pregunta academica validada"),
            ("Decision", "Reglas por palabras clave"),
            ("Salida", "question | answer | source"),
        ],
    )

    add_slide(
        pdf,
        "Seguridad",
        "Controles minimos antes del procesamiento",
        [
            "Limite maximo de 500 caracteres por pregunta.",
            "Bloqueo basico de etiquetas script y patrones SQL.",
            "Variables de entorno para configuracion y CORS.",
        ],
        [
            ("XSS", "Filtro de script + escape HTML"),
            ("SQLi", "Patrones DROP | SELECT | UNION"),
            ("Secrets", ".env fuera del repositorio"),
        ],
    )

    add_slide(
        pdf,
        "DevSecOps",
        "Calidad automatizada en el pipeline",
        [
            "GitHub Actions instala dependencias y ejecuta flake8.",
            "Pytest valida agente, endpoint y controles de seguridad.",
            "pip-audit revisa vulnerabilidades conocidas.",
        ],
        [
            ("CI", "Lint | Tests | Coverage"),
            ("Audit", "pip-audit en cada flujo"),
            ("Build", "Frontend Vite verificado"),
        ],
    )

    add_slide(
        pdf,
        "Despliegue",
        "Listo para Docker y Render",
        [
            "Dockerfile backend con usuario no root.",
            "Dockerfile frontend con build estatico servido por Nginx.",
            "docker-compose levanta backend y frontend localmente.",
        ],
        [
            ("Backend", "http://localhost:8000"),
            ("Frontend", "http://localhost:5173"),
            ("Docs API", "http://localhost:8000/docs"),
        ],
    )

    pdf.save()
    print(OUTPUT)


if __name__ == "__main__":
    main()
