# Requisitos del Proyecto

## Proposito

StudyBot Agent es una plataforma web full stack para asistencia academica y
tecnica de programacion. Su objetivo es ayudar a estudiantes a entender
conceptos, depurar errores y generar ejemplos claros de codigo.

## Requisitos Funcionales

- Permitir que el estudiante escriba preguntas de programacion.
- Mostrar historial simple de conversacion.
- Mostrar loader mientras el backend procesa la respuesta.
- Manejar errores de validacion y conexion de forma clara.
- Consumir el endpoint `POST /api/ask` con Axios.
- Mantener `GET /health` para monitoreo.
- Clasificar categorias como frontend, backend, SQL, debugging y algoritmos.
- Leer conocimiento tecnico desde `src/tools/notes.txt`.
- Renderizar Markdown, listas, tablas simples y bloques de codigo.
- Retornar JSON con pregunta, respuesta y fuente.

## Requisitos de Frontend

- React + Vite.
- TailwindCSS para estilos.
- Axios para comunicacion con API.
- React Icons para iconografia.
- Framer Motion para animaciones suaves.
- Diseno responsive desktop, tablet y mobile.
- Estetica dark mode profesional con gradientes, glassmorphism, sombras y
  transiciones.

## Rendimiento

- El backend no depende de llamadas externas para responder.
- El frontend se compila como sitio estatico optimizado.
- La API debe responder con baja latencia para escenarios academicos.
- Docker Compose debe permitir levantar todo el sistema de forma reproducible.

## Seguridad

- No hardcodear secretos ni API keys.
- Usar `.env` y variables de entorno.
- Excluir `.env`, `node_modules`, caches y builds generados del repositorio.
- Validar longitud maxima de 500 caracteres.
- Bloquear `<script>` y patrones SQL injection comunes.
- Sanitizar texto antes de la logica del agente.
- Configurar CORS desde entorno.
- Ejecutar `pip-audit` en CI.
- Ejecutar backend con usuario no root en Docker.

## Mantenibilidad

- Backend dividido en `api/`, `core/`, agente, config y validacion.
- Frontend dividido en componentes reutilizables, paginas y servicios.
- Pruebas Pytest para agente, validacion y endpoint.
- Configuracion de Black, flake8, ESLint y Tailwind.
- README y documentos de arquitectura actualizados.
- Dockerfiles separados para backend y frontend.
- `docker-compose.yml` para ejecucion full stack.
