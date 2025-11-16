---
inclusion: always
---

# Project Structure & Organization

## Directory Layout

```
backend/app/              - FastAPI application
├── main.py              - App entry point, CORS, router registration
├── config/              - Configuration (database, credentials)
├── routers/             - HTTP endpoints (like Flask Blueprints)
├── service/             - Business logic orchestration
├── inference/           - AI/ML integration (Vertex AI)
├── engine/              - Mathematical pattern generators
│   └── fractal_engine/  - L-System fractal implementation
│       ├── engine.py    - Core algorithm (turtle graphics)
│       ├── processor.py - SVG post-processing (tiling, wrapping)
│       ├── models.py    - Pydantic configuration models
│       └── prompts.py   - LLM prompt templates
└── model/               - Shared data models

frontend/                - Frontend app (minimal/in development)
```

## Architectural Layers (Request Flow)

```
HTTP Request
    ↓
1. Router Layer (routers/) - Parse request, validate input
    ↓
2. Service Layer (service/) - Orchestrate business logic
    ↓
3. Inference Layer (inference/) - Call LLM for parameters
    ↓
4. Engine Layer (engine/) - Generate pattern via math
    ↓
5. Response - Return SVG
```

## Layer Responsibilities

### Routers (`routers/`)
- HTTP endpoint definitions
- Request/response serialization
- No business logic

### Services (`service/`)
- Coordinate between layers
- Business logic and workflow
- Error handling and validation

### Inference (`inference/`)
- Vertex AI / Gemini API calls
- Prompt engineering
- Response parsing

### Engines (`engine/`)
- Pure mathematical computation
- No I/O, no external calls
- Deterministic pattern generation

### Models (`model/`)
- Pydantic models for validation
- Shared data structures

## File Naming Conventions

- Services: `*_service.py` (e.g., `pattern_service.py`)
- Routers: Organized by domain in subdirectories
- Engines: Each type in own subdirectory with standard files (`engine.py`, `processor.py`, `models.py`, `prompts.py`)

## Configuration Files

- `backend/.env` - Environment variables (GCP_PROJECT_ID, GCP_REGION)
- `backend/gcp_creds.json` - Service account credentials
- `backend/requirements.txt` - Python dependencies
- `backend/sample_patterns/` - Generated SVG examples

## Adding New Pattern Engines

When creating a new pattern type:
1. Create subdirectory under `engine/` (e.g., `engine/parametric_engine/`)
2. Implement standard files:
   - `engine.py` - Core generation algorithm
   - `processor.py` - SVG post-processing
   - `models.py` - Pydantic config models
   - `prompts.py` - LLM prompt templates
3. Register in service layer
4. Add router endpoint if needed
