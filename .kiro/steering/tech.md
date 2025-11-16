---
inclusion: always
---

# Technology Stack & Conventions

## Backend Stack

- **Framework**: FastAPI (Python 3.x)
- **Database**: PostgreSQL with asyncpg + SQLAlchemy (async ORM)
- **AI/ML**: Google Vertex AI - Gemini 2.0 Flash model
- **SVG/Math**: svgwrite, shapely, numpy

## Critical Libraries

- `fastapi` + `uvicorn` - Web framework and ASGI server
- `sqlalchemy` - Async database ORM
- `pydantic` - Data validation and JSON schema
- `vertexai` / `google-genai` - Google AI SDK
- `python-dotenv` - Environment configuration

## Development Commands

```bash
# Start backend dev server (from backend/ directory)
uvicorn app.main:app --reload

# API docs available at http://localhost:8000/docs
# API prefix: /ts (e.g., /ts/pattern)
```

## Environment Configuration

Required in `backend/.env`:
- `GCP_PROJECT_ID` - Google Cloud project ID
- `GCP_REGION` - GCP region for Vertex AI
- Service account credentials: `backend/gcp_creds.json`

## Code Style & Patterns

### Async-First
- **Always use async/await** for I/O operations (database, AI calls, file operations)
- All service methods should be async
- Database queries use SQLAlchemy async sessions

### Layered Architecture
- **Routers** (`routers/`) - HTTP endpoints, request/response handling only
- **Services** (`service/`) - Business logic orchestration, no HTTP concerns
- **Inference** (`inference/`) - AI model communication layer
- **Engines** (`engine/`) - Pure mathematical computation, no I/O
- **Models** (`model/`) - Pydantic models for validation

### Data Validation
- Use Pydantic models for all API inputs/outputs
- Engine configurations defined as Pydantic models in `engine/*/models.py`
- Leverage FastAPI's automatic validation and OpenAPI schema generation

### Import Conventions
- Absolute imports from app root: `from app.service.pattern_service import PatternService`
- Router registration in `main.py` with URL prefix
- Load environment variables in `main.py` using `python-dotenv`

### Engine Organization
- Each pattern type gets its own subdirectory under `engine/`
- Structure: `engine.py` (core algorithm), `processor.py` (post-processing), `models.py` (config), `prompts.py` (AI templates)
