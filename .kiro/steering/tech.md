---
inclusion: always
---

# Technology Stack & Code Conventions

## Stack

- **Backend**: FastAPI (Python 3.x) + PostgreSQL + SQLAlchemy (async)
- **AI**: Google Vertex AI - Gemini 2.0 Flash
- **Math/SVG**: svgwrite, shapely, numpy
- **Frontend**: Next.js 14+ + React 18+ + TypeScript

## Critical Backend Conventions

### Async-First (Non-Negotiable)
- ALL I/O operations MUST use `async`/`await` (database, AI calls, file operations)
- ALL service methods MUST be async
- Use `AsyncSession` from SQLAlchemy for database queries
- Never use blocking synchronous calls in async contexts

### Strict Layer Separation (Never Mix)
- **Routers** (`routers/`) - HTTP endpoints only, zero business logic
- **Services** (`service/`) - Business logic orchestration, error handling
- **Inference** (`inference/`) - AI model calls, prompt engineering
- **Engines** (`engine/`) - Pure math functions, deterministic, no I/O
- **Models** (`model/`) - Pydantic validation models

### Data Validation
- Use Pydantic models for ALL API inputs/outputs
- Engine configs MUST be Pydantic models in `engine/*/models.py`
- Leverage FastAPI's automatic validation

### Import Style
- Use absolute imports: `from app.service.pattern_service import PatternService`
- Never use relative imports across modules

### Engine Structure (Standard Template)
Every pattern engine under `engine/` MUST follow this structure:
- `engine.py` - Core algorithm implementation
- `processor.py` - SVG post-processing (tiling, wrapping)
- `models.py` - Pydantic config models
- `prompts.py` - LLM prompt templates

## Development Commands

```bash
# Backend (run from backend/ directory)
uvicorn app.main:app --reload

# API docs: http://localhost:8000/docs
# API prefix: /ts (e.g., /ts/pattern)
```

## Environment Setup

- `backend/.env` requires: `GCP_PROJECT_ID`, `GCP_REGION`
- `backend/gcp_creds.json` - GCP service account credentials
- Load env vars in `main.py` using `python-dotenv`
