---
inclusion: always
---

# Technology Stack & Code Conventions

## Stack

**Backend**: FastAPI (Python 3.x) + PostgreSQL + SQLAlchemy (async)
**AI**: Google Vertex AI - Gemini 2.0 Flash
**Math/SVG**: svgwrite, shapely, numpy
**Frontend**: Next.js + React + TypeScript

## Key Libraries

- `fastapi` + `uvicorn` - ASGI web framework
- `sqlalchemy` - Async ORM
- `pydantic` - Data validation
- `vertexai` / `google-genai` - Google AI SDK
- `python-dotenv` - Environment config

## Development

```bash
# Backend (from backend/ directory)
uvicorn app.main:app --reload

# API docs: http://localhost:8000/docs
# API prefix: /ts (e.g., /ts/pattern)
```

**Environment**: `backend/.env` requires `GCP_PROJECT_ID`, `GCP_REGION`, and `backend/gcp_creds.json`

## Code Conventions

### Async-First (Critical)
- **Always use async/await** for I/O operations (database, AI, file operations)
- All service methods must be async
- Use SQLAlchemy async sessions for database queries

### Strict Layer Separation
- **Routers** (`routers/`) - HTTP only, no business logic
- **Services** (`service/`) - Business logic, orchestration
- **Inference** (`inference/`) - AI model calls
- **Engines** (`engine/`) - Pure math, no I/O, deterministic
- **Models** (`model/`) - Pydantic validation models

### Data Validation
- Use Pydantic models for all API inputs/outputs
- Engine configs are Pydantic models in `engine/*/models.py`
- Leverage FastAPI automatic validation

### Imports & Organization
- Use absolute imports: `from app.service.pattern_service import PatternService`
- Register routers in `main.py` with URL prefix
- Load env vars in `main.py` via `python-dotenv`

### Engine Structure (Standard)
Each pattern engine under `engine/` follows this structure:
- `engine.py` - Core algorithm
- `processor.py` - Post-processing (tiling, wrapping)
- `models.py` - Pydantic config models
- `prompts.py` - LLM prompt templates
