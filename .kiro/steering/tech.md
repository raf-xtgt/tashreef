# Technology Stack

## Backend

- **Framework**: FastAPI (Python web framework)
- **Language**: Python 3.x
- **Database**: PostgreSQL with asyncpg and SQLAlchemy (async ORM)
- **AI/ML**: Google Vertex AI with Gemini 2.0 Flash model
- **SVG Generation**: svgwrite library
- **Geometry**: shapely, numpy for mathematical computations

## Key Libraries

- `fastapi` - Web framework with automatic API documentation
- `uvicorn` - ASGI server
- `sqlalchemy` - Async database ORM
- `pydantic` - Data validation and settings management
- `google-genai` / `vertexai` - Google AI integration
- `svgwrite` - SVG file generation
- `python-dotenv` - Environment variable management

## Frontend

- Located in `frontend/` directory (currently empty/minimal)

## Common Commands

### Development

```bash
# Run backend development server with auto-reload
uvicorn app.main:app --reload

# Run from backend directory
cd backend
uvicorn app.main:app --reload
```

### Environment Setup

- Backend requires `.env` file with `GCP_PROJECT_ID` and `GCP_REGION`
- Virtual environment: `backend/webserviceVenv/`

### API Documentation

- FastAPI auto-generates docs at `/docs` endpoint
- API prefix: `/ts` (e.g., `/ts/pattern`)

## Architecture Patterns

- **Service Layer Pattern**: Business logic in `service/` modules
- **Router Pattern**: API endpoints organized in `routers/` (similar to Flask Blueprints)
- **Engine Pattern**: Mathematical computation engines in `engine/` subdirectories
- **Async/Await**: All database operations and AI calls use async patterns
