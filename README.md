# StudyBot Agent

StudyBot Agent es una plataforma web full stack para asistencia tecnica de
programacion. Combina un backend FastAPI con validaciones de seguridad y un
frontend React moderno para que estudiantes hagan preguntas sobre codigo,
errores, APIs, algoritmos, bases de datos y desarrollo web.

## Integrantes

- Mariana Patiño Munera
- Mariana Gutierrez Restrepo

## Vista del Producto

La aplicacion ofrece:

- Chat web responsive con historial simple de conversacion.
- Loader animado mientras el agente responde.
- Manejo visual de errores de API y validacion.
- UI dark mode sobria con Markdown, tablas y bloques de codigo resaltados.
- API REST documentada con FastAPI.
- Pipeline DevSecOps con lint, pruebas, cobertura y auditoria de dependencias.

## Screenshots

Coloca capturas del producto en `docs/screenshots/` cuando ejecutes la app:

```text
docs/screenshots/home-desktop.png
docs/screenshots/chat-mobile.png
docs/screenshots/api-docs.png
```

## Presentacion PDF

La presentacion ejecutiva del proyecto esta disponible en:

```text
docs/presentacion-studybot-agent.pdf
```

## Arquitectura Web

```text
Browser
  |
  | React + Vite + TailwindCSS + Axios
  v
Frontend Web
  |
  | POST /api/ask
  v
FastAPI Backend
  |
  | validation + sanitization + decision logic
  v
Programming Tutor Agent
  |
  v
src/tools/notes.txt
```

## Estructura

```text
studybot-agent/
├── frontend/                 # React + Vite + TailwindCSS
├── src/                      # Backend FastAPI
│   ├── api/                  # Rutas y schemas Pydantic
│   ├── core/                 # Logging y utilidades runtime
│   ├── tools/notes.txt       # Fuente externa del agente
│   ├── agent.py              # Logica del agente
│   ├── config.py             # Variables de entorno
│   ├── main.py               # App FastAPI
│   └── validator.py          # Validacion y sanitizacion
├── tests/                    # Pruebas Pytest
├── docs/                     # Requisitos y arquitectura
├── .github/workflows/ci.yml  # Pipeline DevSecOps
├── Dockerfile.backend        # Imagen backend
├── Dockerfile                # Imagen backend compatible con version inicial
├── docker-compose.yml        # Orquestacion local full stack
└── requirements.txt
```

## Archivos Principales

- `src/main.py`: construye la aplicacion FastAPI, configura CORS e incluye las
  rutas.
- `src/api/routes.py`: contiene `/ask` y `/health`, logging y errores HTTP.
- `src/api/schemas.py`: centraliza modelos Pydantic de request y response.
- `src/validator.py`: bloquea entradas vacias, enormes, XSS basico y patrones
  SQL peligrosos.
- `src/agent.py`: orquesta clasificacion, recuperacion local y respuesta.
- `src/programming/classifier.py`: detecta categoria y estilo de pregunta.
- `src/programming/knowledge.py`: busca conocimiento tecnico en `notes.txt`.
- `src/programming/responses.py`: genera respuestas Markdown contextualizadas.
- `frontend/src/components/ChatBox.jsx`: experiencia principal de chat tecnico.
- `frontend/src/components/MessageBubble.jsx`: render Markdown y codigo.
- `frontend/src/services/api.js`: cliente Axios para comunicarse con FastAPI.
- `frontend/src/index.css`: TailwindCSS y ajustes globales de scroll/tema.
- `.github/workflows/ci.yml`: lint, pruebas, cobertura, `pip-audit` y build web.
- `docker-compose.yml`: levanta backend y frontend juntos.

## Variables de Entorno

Backend, desde `.env.example`:

```env
APP_ENV=development
LOG_LEVEL=INFO
PORT=8000
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Frontend, desde `frontend/.env.example`:

```env
VITE_API_URL=http://localhost:8000
```

No se usan API keys. Si se agrega un proveedor LLM en el futuro, sus secretos
deben cargarse por variables de entorno o secretos del proveedor CI/CD.

## Instalacion Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

Ejecutar backend:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

En Windows tambien puedes usar el script incluido:

```powershell
cd C:\Users\Catherine\Desktop\Seguimiento3IS\studybot-agent
.\scripts\start-backend.ps1
```

## Instalacion Frontend

```bash
cd frontend
npm install
npm run dev
```

La aplicacion quedara disponible en:

```text
http://localhost:5173
```

Si el puerto `5173` esta ocupado, Vite usara otro puerto como `5174`. Abre la
URL `Local` que aparezca en la consola.

En Windows tambien puedes usar:

```powershell
cd C:\Users\Catherine\Desktop\Seguimiento3IS\studybot-agent
.\scripts\start-frontend.ps1
```

## Ejecucion Full Stack con Docker

Ejecutar:

```bash
docker compose up --build
```

Servicios:

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

## Pruebas y Calidad

Backend:

```bash
black src tests
flake8 src tests
pytest --cov=src --cov-fail-under=70
pip-audit
```

Frontend:

```bash
cd frontend
npm run lint
npm run build
```

## API

### `GET /health` o `GET /api/health`

```json
{
  "status": "ok",
  "environment": "development"
}
```

### `POST /ask` o `POST /api/ask`

Request:

```json
{
  "question": "Explícame qué hace useEffect en React"
}
```

Response:

```json
{
  "question": "Explícame qué hace useEffect en React",
  "answer": "## UseEffect en React...",
  "source": "programming-notes.txt"
}
```

## Despliegue en Render

Backend:

1. Crear un Web Service.
2. Seleccionar Docker.
3. Usar `Dockerfile.backend`.
4. Configurar `PORT`, `APP_ENV`, `LOG_LEVEL` y `CORS_ORIGINS`.
5. Validar `/health`.

Frontend:

1. Crear Static Site o Web Service.
2. Definir `VITE_API_URL` con la URL publica del backend.
3. Ejecutar `npm install && npm run build`.
4. Publicar `frontend/dist`.

## DevSecOps

El proyecto aplica buenas practicas reales:

- Validacion y sanitizacion antes de ejecutar logica de agente.
- Separacion de rutas, schemas, configuracion, logging y logica de dominio.
- CORS restringido por variables de entorno.
- Secretos fuera del codigo fuente.
- Pipeline con `flake8`, `pytest`, cobertura minima y `pip-audit`.
- Build frontend automatizado en GitHub Actions.
- Docker con usuario no root para backend.
- Despliegue reproducible con Docker Compose y Render.
