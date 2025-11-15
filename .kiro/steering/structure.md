# Project Structure

## Root Layout

```
/backend          - Python FastAPI backend application
/frontend         - Frontend application (minimal/empty)
```

## Backend Organization

### Core Application (`backend/app/`)

```
app/
├── main.py                    - FastAPI application entry point, CORS, router registration
├── config/                    - Configuration modules
│   └── db_config.py          - Database connection configuration
├── routers/                   - API route controllers (like Flask Blueprints)
│   └── pattern/              - Pattern generation endpoints
├── service/                   - Business logic layer
│   └── pattern_service.py    - Pattern generation orchestration
├── inference/                 - AI/ML integration layer
│   └── inference_service.py  - Vertex AI and Gemini model interactions
├── engine/                    - Mathematical computation engines
│   └── fractal_engine/       - L-System fractal pattern generation
│       ├── engine.py         - Core L-System algorithm and turtle graphics
│       ├── processor.py      - SVG pattern processing and wrapping
│       ├── models.py         - Pydantic models for pattern configurations
│       └── prompts.py        - AI prompt templates
└── model/                     - Data models
    └── prompt.py             - Prompt-related models
```

### Supporting Files

- `backend/.env` - Environment variables (GCP credentials, region)
- `backend/requirements.txt` - Python dependencies
- `backend/gcp_creds.json` - Google Cloud Platform service account credentials
- `backend/sample_patterns/` - Generated SVG output samples
- `backend/webserviceVenv/` - Python virtual environment

## Architectural Layers

1. **Router Layer** (`routers/`) - HTTP endpoints and request handling
2. **Service Layer** (`service/`) - Business logic orchestration
3. **Inference Layer** (`inference/`) - AI model communication
4. **Engine Layer** (`engine/`) - Mathematical pattern generation
5. **Model Layer** (`model/`) - Data structures and validation

## Code Organization Conventions

- Use async/await for all I/O operations (database, AI calls)
- Pydantic models for data validation and JSON schema generation
- Separate concerns: routers handle HTTP, services handle logic, engines handle math
- Each engine type (fractal, parametric, tessellation) gets its own subdirectory
- Configuration and credentials isolated in `config/` and `.env`

## Import Patterns

- Relative imports within app: `from app.service.pattern_service import PatternService`
- Router registration in `main.py` with URL prefix
- Environment variables loaded via `python-dotenv` in `main.py`
