---
inclusion: always
---

# Project Structure & Architecture

## Directory Layout

```
backend/app/
├── main.py              - Entry point, CORS, router registration
├── config/              - Database, credentials
├── routers/             - HTTP endpoints
├── service/             - Business logic orchestration
├── inference/           - Vertex AI integration
├── engine/              - Mathematical pattern generators
│   └── fractal_engine/  - L-System implementation
│       ├── engine.py    - Core algorithm
│       ├── processor.py - SVG post-processing
│       ├── models.py    - Pydantic configs
│       └── prompts.py   - LLM templates
└── model/               - Shared Pydantic models

frontend/tashreef-app/   - Next.js app
├── src/app/
│   ├── page.tsx         - Root page (home)
│   ├── layout.tsx       - Root layout
│   ├── layoutClient.tsx - Client-side layout wrapper
│   ├── globals.css      - Global styles
│   ├── components/      - React components
│   │   ├── auth/        - Authentication components
│   │   ├── eCardEditor/ - E-card editor components
│   │   │   ├── cardDisplay/  - Card preview/display
│   │   │   ├── cardPrompt/   - Prompt input interface
│   │   │   └── cardTools/    - Editor tools/controls
│   │   └── home/        - Home page components
│   ├── context/         - React context providers
│   │   ├── stateController.tsx - Global state management
│   │   └── userContext.tsx     - User authentication state
│   ├── eCardEditor/     - E-card editor page
│   │   └── page.tsx     - Editor page route
│   ├── models/          - TypeScript data models
│   │   └── cardPromptModel.tsx
│   └── services/        - API service layer
│       └── inferenceService.tsx - Backend API calls
└── public/              - Static assets
```

## Request Flow (Strict Layer Order)

```
HTTP Request → Router → Service → Inference → Engine → SVG Response
```

## Layer Responsibilities (Do Not Mix)

**Routers** (`routers/`)
- HTTP endpoints only
- Request/response serialization
- Zero business logic

**Services** (`service/`)
- Orchestrate workflow
- Business logic
- Error handling

**Inference** (`inference/`)
- Vertex AI / Gemini calls
- Prompt engineering
- Parse LLM responses

**Engines** (`engine/`)
- Pure mathematical computation
- No I/O, no external calls
- Deterministic, testable

**Models** (`model/`)
- Pydantic validation models
- Shared data structures

## Naming Conventions

- Services: `*_service.py` (e.g., `pattern_service.py`)
- Routers: Domain-based subdirectories
- Engines: Subdirectory with `engine.py`, `processor.py`, `models.py`, `prompts.py`

## Key Files

- `backend/.env` - Environment variables
- `backend/gcp_creds.json` - Service account credentials
- `backend/requirements.txt` - Python dependencies
- `backend/sample_patterns/` - Generated SVG examples

## Adding New Pattern Engines

1. Create `engine/<engine_name>/` directory
2. Implement required files:
   - `engine.py` - Core algorithm
   - `processor.py` - SVG post-processing
   - `models.py` - Pydantic config models
   - `prompts.py` - LLM prompt templates
3. Register in service layer
4. Add router endpoint if needed
