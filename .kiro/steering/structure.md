---
inclusion: always
---

# Project Structure & Architecture

## Request Flow (Strict Order - Never Skip Layers)

```
HTTP Request → Router → Service → Inference → Engine → SVG Response
```

## Layer Responsibilities (Enforce Separation)

### Routers (`routers/`)
- HTTP endpoints ONLY
- Request/response serialization
- ZERO business logic - delegate to services immediately

### Services (`service/`)
- Orchestrate workflow between layers
- Business logic and validation
- Error handling and logging
- Call inference layer for AI operations

### Inference (`inference/`)
- Vertex AI / Gemini API calls
- Prompt engineering and template rendering
- Parse and validate LLM JSON responses
- NO business logic

### Engines (`engine/`)
- Pure mathematical computation
- Deterministic algorithms (same input = same output)
- NO I/O operations (no database, no API calls, no file writes)
- Testable in isolation

### Models (`model/`)
- Pydantic validation models
- Shared data structures across layers

## Backend Directory Structure

```
backend/app/
├── main.py              - Entry point, CORS, router registration
├── config/              - Database config, credentials
├── routers/             - HTTP endpoints (FastAPI routers)
├── service/             - Business logic orchestration
├── inference/           - Vertex AI integration
├── engine/              - Mathematical pattern generators
│   ├── fractal_engine/
│   ├── parametric_engine/
│   └── tessellation_engine/
│       ├── engine.py    - Core algorithm
│       ├── processor.py - SVG post-processing
│       ├── models.py    - Pydantic configs
│       └── prompts.py   - LLM templates
└── model/               - Shared Pydantic models
```

## Frontend Directory Structure

```
frontend/tashreef-app/src/app/
├── page.tsx             - Root page (home)
├── layout.tsx           - Root layout
├── layoutClient.tsx     - Client-side layout wrapper
├── components/          - React components
│   ├── auth/            - Authentication UI
│   ├── eCardEditor/     - E-card editor components
│   │   ├── cardDisplay/ - Card preview/display
│   │   ├── cardPrompt/  - Prompt input interface
│   │   └── cardTools/   - Editor tools/controls
│   └── home/            - Home page components
├── context/             - React context providers
│   ├── stateController.tsx - Global state management
│   └── userContext.tsx     - User authentication state
├── eCardEditor/         - E-card editor page route
├── models/              - TypeScript data models
└── services/            - API service layer
    └── inferenceService.tsx - Backend API calls
```

## Naming Conventions

- Services: `*_service.py` (e.g., `pattern_service.py`)
- All service methods: async functions
- Engines: Subdirectory with 4 required files (`engine.py`, `processor.py`, `models.py`, `prompts.py`)
- Frontend components: PascalCase files with `.tsx` extension

## Adding New Pattern Engines (Checklist)

1. Create `backend/app/engine/<engine_name>/` directory
2. Implement 4 required files:
   - `engine.py` - Core algorithm (pure math, no I/O)
   - `processor.py` - SVG post-processing (tiling, wrapping)
   - `models.py` - Pydantic config models
   - `prompts.py` - LLM prompt templates
3. Register engine in `inference/engine_router.py`
4. Update service layer to handle new engine type
5. Add router endpoint if needed
