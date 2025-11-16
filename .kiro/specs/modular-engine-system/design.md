# Design Document

## Overview

This design implements a modular, scalable pattern engine system that supports multiple geometric generation engines. The key innovation is an intelligent engine classification layer that routes user prompts to the appropriate engine, combined with a modularized prompt system that prevents prompt bloat as new engines are added.

The system follows a two-phase AI inference approach:
1. **Engine Classification**: Analyze the user prompt and select the appropriate engine type
2. **Pattern Generation**: Use engine-specific prompts to generate pattern configuration

This design maintains the existing architectural patterns while adding two new engines (parametric and tessellation) alongside the existing l_system engine.

## Architecture

### High-Level Flow

```
User Prompt → Engine Router (AI Classification)
                    ↓
            Selected Engine Type
                    ↓
    Base Prompt + Engine-Specific Prompt
                    ↓
        Pattern Config Generation (AI)
                    ↓
            Selected Engine
                    ↓
            Pattern Processor
                    ↓
            Card Generator
                    ↓
            Final Card SVG
```

### Component Interaction

1. **Pattern Service** receives user prompt
2. **Engine Router** classifies prompt → engine_type
3. **Prompt Builder** concatenates base + engine-specific prompt
4. **Inference Service** generates pattern config using combined prompt
5. **Selected Engine** generates standalone pattern
6. **Selected Processor** creates repeating background
7. **Card Generator** adds content overlay
8. **Response** returns complete card SVG


### Design Principles

- **Modularity**: Each engine is self-contained with its own prompt, models, and logic
- **Scalability**: Adding new engines requires minimal changes to core system
- **Type Safety**: Pydantic models ensure validation throughout
- **Async/Await**: All I/O operations remain asynchronous
- **Backward Compatibility**: Existing l_system functionality remains unchanged
- **Single Responsibility**: Each component has a clear, focused purpose

## Components and Interfaces

### 1. Engine Type Enumeration (New)

**Location**: `backend/app/model/prompt.py` (new file)

```python
from pydantic import BaseModel, Field
from enum import Enum

class EngineTypeEnum(str, Enum):
    """Available pattern generation engines."""
    l_system = "l_system"
    parametric = "parametric"
    tessellation = "tessellation"

class EngineChoice(BaseModel):
    """Router output model for engine classification."""
    engine_type: EngineTypeEnum = Field(
        ...,
        description="The selected pattern generation engine based on user prompt analysis."
    )
```

### 2. Engine Router (New)

**Location**: `backend/app/inference/engine_router.py` (new file)

**Purpose**: Classify user prompts into appropriate engine types using AI

**Key Method**:
```python
async def classify_engine(user_prompt: str) -> EngineTypeEnum
```

**Responsibilities**:
- Build router prompt with classification instructions
- Call inference service with EngineChoice schema
- Return selected engine_type
- Default to l_system on failure


### 3. Prompt System Refactoring

**Base Prompt** (`backend/app/prompt/base_prompt.py` - already exists)
- Core instructions shared across all engines
- Explains the role as generative artist and mathematician
- Describes JSON output requirement

**Engine-Specific Prompts**:
- `backend/app/engine/l_system/prompts.py` - L-System instructions and examples
- `backend/app/engine/parametric_engine/prompts.py` - Parametric equations instructions
- `backend/app/engine/tessellation_engine/prompts.py` - Tessellation instructions

**Prompt Builder Function** (New in `backend/app/prompt/prompt_builder.py`):
```python
def build_engine_prompt(engine_type: EngineTypeEnum, user_prompt: str) -> str:
    """Concatenates base prompt + engine-specific prompt + user prompt."""
    base = BASE_PROMPT
    
    if engine_type == EngineTypeEnum.l_system:
        from app.engine.fractal_engine.prompts import L_SYSTEM_PROMPT
        engine_prompt = L_SYSTEM_PROMPT
    elif engine_type == EngineTypeEnum.parametric:
        from app.engine.parametric_engine.prompts import PARAMETRIC_PROMPT
        engine_prompt = PARAMETRIC_PROMPT
    elif engine_type == EngineTypeEnum.tessellation:
        from app.engine.tessellation_engine.prompts import TESSELLATION_PROMPT
        engine_prompt = TESSELLATION_PROMPT
    
    return f"{base}\n\n{engine_prompt}\n\n---\nUSER PROMPT:\n{user_prompt}"
```

### 4. Parametric Engine (New)

**Location**: `backend/app/engine/parametric_engine/`

**Structure**:
- `engine.py` - Core parametric equation implementation
- `processor.py` - Converts standalone pattern to repeating background
- `models.py` - ParametricConfig Pydantic model
- `prompts.py` - PARAMETRIC_PROMPT constant

**Models** (`models.py`):
```python
class EquationTypeEnum(str, Enum):
    rose = "rose"
    lissajous = "lissajous"
    epitrochoid = "epitrochoid"
    hypotrochoid = "hypotrochoid"

class ParametricParams(BaseModel):
    equation_type: EquationTypeEnum
    amplitude_a: float
    amplitude_b: float
    frequency_a: float
    frequency_b: float
    phase_shift: float = 0.0
    num_points: int = 1000

class ParametricConfig(BaseModel):
    engine_type: str = "parametric"
    parameters: ParametricParams
    style: StyleParams
```


**Engine Logic** (`engine.py`):
```python
def generate_parametric_components(config: ParametricConfig) -> Dict[str, Any]:
    """
    Generates parametric curve components using mathematical equations.
    Returns path_data, style, and viewBox.
    """
    params = config.parameters
    equation_type = params.equation_type
    
    # Generate points based on equation type
    if equation_type == EquationTypeEnum.rose:
        # r = a * cos(k * θ)
        points = generate_rose_curve(params)
    elif equation_type == EquationTypeEnum.lissajous:
        # x = A * sin(a*t + δ), y = B * sin(b*t)
        points = generate_lissajous_curve(params)
    # ... other equation types
    
    # Convert points to SVG path data
    path_data = points_to_path(points)
    
    return {
        "path_data": path_data,
        "style": config.style.dict(),
        "viewBox": "0 0 1000 1000"
    }
```

**Processor Logic** (`processor.py`):
```python
def process_parametric_request(config: ParametricConfig) -> str:
    """
    Orchestrates parametric pattern generation.
    Returns JSON with svg_string and config.
    """
    # Generate components
    components = generate_parametric_components(config)
    
    # Build repeating pattern SVG
    svg_string = build_parametric_pattern_svg(components)
    
    # Return response
    response = ParametricResponse(
        svg_string=svg_string,
        config=config
    )
    return response.model_dump_json(indent=2)
```

### 5. Tessellation Engine (New)

**Location**: `backend/app/engine/tessellation_engine/`

**Structure**: Same as parametric (engine.py, processor.py, models.py, prompts.py)

**Models** (`models.py`):
```python
class TileShapeEnum(str, Enum):
    square = "square"
    hexagon = "hexagon"
    triangle = "triangle"
    diamond = "diamond"

class TessellationParams(BaseModel):
    tile_shape: TileShapeEnum
    tile_size: float
    rotation: float = 0.0
    spacing: float = 0.0
    color_palette: List[str]

class TessellationConfig(BaseModel):
    engine_type: str = "tessellation"
    parameters: TessellationParams
    style: StyleParams
```


**Engine Logic** (`engine.py`):
```python
def generate_tessellation_components(config: TessellationConfig) -> Dict[str, Any]:
    """
    Generates tessellation pattern using geometric tiling.
    Returns tile definitions, style, and viewBox.
    """
    params = config.parameters
    tile_shape = params.tile_shape
    
    # Generate tile geometry based on shape
    if tile_shape == TileShapeEnum.square:
        tile_path = generate_square_tile(params)
    elif tile_shape == TileShapeEnum.hexagon:
        tile_path = generate_hexagon_tile(params)
    # ... other shapes
    
    return {
        "tile_path": tile_path,
        "tile_size": params.tile_size,
        "style": config.style.dict(),
        "viewBox": "0 0 1000 1000"
    }
```

**Processor Logic** (`processor.py`):
```python
def process_tessellation_request(config: TessellationConfig) -> str:
    """
    Orchestrates tessellation pattern generation.
    Returns JSON with svg_string and config.
    """
    # Generate components
    components = generate_tessellation_components(config)
    
    # Build seamless tiling pattern SVG
    svg_string = build_tessellation_pattern_svg(components)
    
    # Return response
    response = TessellationResponse(
        svg_string=svg_string,
        config=config
    )
    return response.model_dump_json(indent=2)
```

### 6. Pattern Service Refactoring

**Location**: `backend/app/service/pattern_service.py`

**Updated Flow**:
```python
async def generate_pattern(self, user_prompt: str, db: AsyncSession) -> CardResponse:
    # Step 1: Classify engine type
    from app.inference.engine_router import classify_engine
    engine_type = await classify_engine(user_prompt)
    print(f"Selected engine: {engine_type}")
    
    # Step 2: Build engine-specific prompt
    from app.prompt.prompt_builder import build_engine_prompt
    full_prompt = build_engine_prompt(engine_type, user_prompt)
    
    # Step 3: Generate pattern config based on engine type
    if engine_type == EngineTypeEnum.l_system:
        config_model = LSystemConfig
        processor_func = process_fractal_request
    elif engine_type == EngineTypeEnum.parametric:
        config_model = ParametricConfig
        processor_func = process_parametric_request
    elif engine_type == EngineTypeEnum.tessellation:
        config_model = TessellationConfig
        processor_func = process_tessellation_request
    
    # Step 4: Generate pattern config via AI
    ai_config = await service._generate_structured_content(full_prompt, config_model)
    
    # Step 5: Process pattern
    pattern_json = processor_func(ai_config)
    pattern_data = json.loads(pattern_json)
    pattern_svg = pattern_data['svg_string']
    
    # Step 6: Generate complete card (existing logic)
    card_response = await generate_card(
        pattern_svg=pattern_svg,
        user_prompt=user_prompt,
        pattern_config=ai_config,
        inference_service=service
    )
    
    return card_response
```


## Data Models

### Engine Classification

**Router Prompt Input**:
```
User prompt: "Create a hypnotic circular pattern for my birthday party"
```

**Router Output**:
```json
{
  "engine_type": "parametric"
}
```

### Parametric Pattern Config

```json
{
  "engine_type": "parametric",
  "parameters": {
    "equation_type": "rose",
    "amplitude_a": 200.0,
    "amplitude_b": 200.0,
    "frequency_a": 5.0,
    "frequency_b": 3.0,
    "phase_shift": 0.0,
    "num_points": 1000
  },
  "style": {
    "fill": "none",
    "stroke": "#FF1493",
    "stroke_width": 2.0
  }
}
```

### Tessellation Pattern Config

```json
{
  "engine_type": "tessellation",
  "parameters": {
    "tile_shape": "hexagon",
    "tile_size": 100.0,
    "rotation": 30.0,
    "spacing": 2.0,
    "color_palette": ["#4682B4", "#87CEEB", "#B0E0E6"]
  },
  "style": {
    "fill": "#4682B4",
    "stroke": "#FFFFFF",
    "stroke_width": 1.0
  }
}
```

## Error Handling

### Engine Classification Failures

**Scenario**: Router fails to classify or returns invalid engine type

**Handling**:
1. Log the error with full context
2. Default to "l_system" engine
3. Continue with pattern generation
4. Include warning in response metadata

### Pattern Generation Failures

**Scenario**: Selected engine fails to generate pattern

**Handling**:
1. Log the error with engine type and config
2. Return error response to client
3. Do NOT fall back to different engine (user intent may be lost)
4. Suggest user try different prompt

### Invalid Configuration

**Scenario**: AI returns invalid parameters for selected engine

**Handling**:
1. Pydantic validation will catch errors
2. Log validation errors
3. Return error response with details
4. Do not attempt generation with invalid config


## Testing Strategy

### Unit Tests

**Engine Router Tests** (`tests/test_engine_router.py`):
1. `test_classify_organic_prompt()` - Verify l_system selection
2. `test_classify_circular_prompt()` - Verify parametric selection
3. `test_classify_geometric_prompt()` - Verify tessellation selection
4. `test_classify_ambiguous_prompt()` - Verify default to l_system
5. `test_router_failure_handling()` - Verify graceful degradation

**Parametric Engine Tests** (`tests/test_parametric_engine.py`):
1. `test_generate_rose_curve()` - Verify rose equation implementation
2. `test_generate_lissajous_curve()` - Verify lissajous implementation
3. `test_parametric_config_validation()` - Test Pydantic validation
4. `test_parametric_processor()` - Verify SVG generation

**Tessellation Engine Tests** (`tests/test_tessellation_engine.py`):
1. `test_generate_square_tile()` - Verify square tiling
2. `test_generate_hexagon_tile()` - Verify hexagon tiling
3. `test_seamless_tiling()` - Verify no gaps/overlaps
4. `test_tessellation_config_validation()` - Test Pydantic validation

**Prompt Builder Tests** (`tests/test_prompt_builder.py`):
1. `test_build_l_system_prompt()` - Verify correct concatenation
2. `test_build_parametric_prompt()` - Verify correct concatenation
3. `test_build_tessellation_prompt()` - Verify correct concatenation

### Integration Tests

**End-to-End Tests** (`tests/test_pattern_service_integration.py`):
1. `test_e2e_l_system_generation()` - Full flow with organic prompt
2. `test_e2e_parametric_generation()` - Full flow with circular prompt
3. `test_e2e_tessellation_generation()` - Full flow with geometric prompt
4. `test_engine_switching()` - Verify different engines work in sequence

### Manual Testing

**Test Scenarios**:
1. **L-System**: "Create a delicate fern pattern for a garden wedding"
2. **Parametric**: "Generate a hypnotic spirograph design for a psychedelic party"
3. **Tessellation**: "Make an Islamic geometric mosaic for a formal event"
4. **Ambiguous**: "Create a beautiful pattern" → Should default to l_system

## Parametric Equations Reference

### Rose Curve
```
r = a * cos(k * θ)
x = r * cos(θ)
y = r * sin(θ)
```
- `a`: amplitude (size of petals)
- `k`: frequency (number of petals)
- Creates flower-like patterns

### Lissajous Curve
```
x = A * sin(a*t + δ)
y = B * sin(b*t)
```
- `A, B`: amplitudes
- `a, b`: frequencies
- `δ`: phase shift
- Creates figure-8 and complex loops

### Epitrochoid
```
x = (R + r) * cos(t) - d * cos((R + r) * t / r)
y = (R + r) * sin(t) - d * sin((R + r) * t / r)
```
- `R`: radius of fixed circle
- `r`: radius of rolling circle
- `d`: distance from center of rolling circle
- Creates spirograph-like patterns

### Hypotrochoid
```
x = (R - r) * cos(t) + d * cos((R - r) * t / r)
y = (R - r) * sin(t) - d * sin((R - r) * t / r)
```
- Similar to epitrochoid but circle rolls inside
- Creates star-like patterns


## Tessellation Patterns Reference

### Square Tiling
- Simplest tessellation
- Tiles arranged in grid pattern
- Can apply rotation for diamond effect

### Hexagon Tiling
- Honeycomb pattern
- Offset rows for seamless tiling
- Natural, organic appearance

### Triangle Tiling
- Can create complex patterns
- Combine with rotation for variety
- Sharp, angular aesthetic

### Diamond Tiling
- Rotated squares
- Creates dynamic visual flow
- Good for modern designs

## Prompt Examples

### Router Classification Prompt

```
ROUTER_SYSTEM_PROMPT = """
You are a Pattern Engine Classifier. Your sole job is to interpret the user's 
creative request and classify it into one of the available geometric generation 
engine types.

--- CLASSIFICATION RULES ---

1. **l_system**: If the user asks for a pattern that is organic, branching, 
   fractal, plant-like, fern-like, snowflake-like, tree-like, or natural.
   
   Keywords: fractal, branching, organic, fern, plant, tree, snowflake, 
   recursive, natural, delicate, intricate branching

2. **parametric**: If the user asks for a pattern that is hypnotic, circular, 
   cosmic, vortex-like, gear-like, spirograph-like, or uses complex flowing curves.
   
   Keywords: spirograph, circular, hypnotic, vortex, cosmic, flowing, curved, 
   rose, lissajous, spiral, swirl, psychedelic

3. **tessellation**: If the user asks for a pattern that is rigid, symmetrical, 
   tiled, architectural, mosaic-like, geometric, or involves repeating shapes 
   (squares, hexagons, triangles).
   
   Keywords: tessellation, tiled, mosaic, geometric, architectural, Islamic, 
   symmetrical, grid, honeycomb, repeating shapes, structured

4. **Default**: If the request is ambiguous or doesn't clearly fit any category, 
   default to 'l_system'.

--- EXAMPLES ---

Input: "Create a delicate fern pattern"
Output: {"engine_type": "l_system"}

Input: "Generate a hypnotic spirograph design"
Output: {"engine_type": "parametric"}

Input: "Make an Islamic geometric mosaic"
Output: {"engine_type": "tessellation"}

Input: "Create a beautiful pattern"
Output: {"engine_type": "l_system"}

--- YOUR TASK ---

Analyze the user's prompt below. Use chain-of-thought reasoning to determine 
which engine best matches their creative intent. Respond ONLY with a JSON object 
containing the chosen 'engine_type'. Do not include any other text, markdown, 
or parameters.
"""
```


### Parametric Engine Prompt

```
PARAMETRIC_PROMPT = """
---
ENGINE: "parametric"
---
This engine generates hypnotic, circular, and spirograph-like patterns using 
parametric equations. It creates flowing curves and complex geometric designs.

- Use this engine if the user asks for: "spirograph", "circular", "hypnotic", 
  "vortex", "cosmic", "flowing curves", "rose", "lissajous"

**Parameters:**
- `equation_type`: The type of parametric equation to use
  - "rose": Flower-like patterns with petals
  - "lissajous": Figure-8 and complex loops
  - "epitrochoid": Spirograph patterns (circle rolling outside)
  - "hypotrochoid": Star-like patterns (circle rolling inside)

- `amplitude_a`: Size/scale in x-direction (50-500)
- `amplitude_b`: Size/scale in y-direction (50-500)
- `frequency_a`: Number of cycles in x-direction (1-20)
- `frequency_b`: Number of cycles in y-direction (1-20)
- `phase_shift`: Phase offset in radians (0-6.28)
- `num_points`: Number of points to generate (500-2000)

- `style`: Set the `stroke` to a color that matches the user's request. 
  `fill` should almost always be "none".

---
EXAMPLES of PARAMETRIC PATTERNS
---

1. **Rose Curve (5 petals):**
   * `equation_type`: "rose"
   * `amplitude_a`: 200
   * `amplitude_b`: 200
   * `frequency_a`: 5
   * `frequency_b`: 1
   * `num_points`: 1000

2. **Lissajous Figure:**
   * `equation_type`: "lissajous"
   * `amplitude_a`: 300
   * `amplitude_b`: 300
   * `frequency_a`: 3
   * `frequency_b`: 2
   * `phase_shift`: 1.57
   * `num_points`: 1500

3. **Spirograph (Epitrochoid):**
   * `equation_type`: "epitrochoid"
   * `amplitude_a`: 250
   * `amplitude_b`: 250
   * `frequency_a`: 7
   * `frequency_b`: 3
   * `num_points`: 2000

4. **Star Pattern (Hypotrochoid):**
   * `equation_type`: "hypotrochoid"
   * `amplitude_a`: 200
   * `amplitude_b`: 200
   * `frequency_a`: 5
   * `frequency_b`: 2
   * `num_points`: 1000

---
YOUR TASK
---
Read the user's prompt. Select appropriate parametric equation type and parameters 
that match their creative description. Set the style to match their request.

Respond ONLY with the JSON object. Do not include any other text, markdown, 
or conversation.
"""
```


### Tessellation Engine Prompt

```
TESSELLATION_PROMPT = """
---
ENGINE: "tessellation"
---
This engine generates tiled, mosaic-like patterns using geometric shapes. 
It creates architectural, Islamic-inspired, and structured designs.

- Use this engine if the user asks for: "tessellation", "tiled", "mosaic", 
  "geometric", "architectural", "Islamic", "honeycomb", "grid"

**Parameters:**
- `tile_shape`: The shape of the repeating tile
  - "square": Simple grid pattern
  - "hexagon": Honeycomb pattern
  - "triangle": Angular, dynamic pattern
  - "diamond": Rotated squares

- `tile_size`: Size of each tile in pixels (50-200)
- `rotation`: Rotation angle in degrees (0-360)
- `spacing`: Gap between tiles in pixels (0-10)
- `color_palette`: Array of 2-5 hex colors for alternating tiles

- `style`: Set the `fill` and `stroke` colors. For tessellations, 
  `fill` is usually a color, and `stroke` is often white or black.

---
EXAMPLES of TESSELLATION PATTERNS
---

1. **Islamic Geometric (Hexagons):**
   * `tile_shape`: "hexagon"
   * `tile_size`: 100
   * `rotation`: 0
   * `spacing`: 2
   * `color_palette`: ["#4682B4", "#87CEEB", "#B0E0E6"]

2. **Modern Grid (Squares):**
   * `tile_shape`: "square"
   * `tile_size`: 80
   * `rotation`: 0
   * `spacing`: 5
   * `color_palette`: ["#FF6B6B", "#4ECDC4"]

3. **Dynamic Diamonds:**
   * `tile_shape`: "diamond"
   * `tile_size`: 120
   * `rotation`: 45
   * `spacing`: 0
   * `color_palette`: ["#FFD700", "#FFA500", "#FF8C00"]

4. **Angular Triangles:**
   * `tile_shape`: "triangle"
   * `tile_size`: 90
   * `rotation`: 30
   * `spacing`: 1
   * `color_palette`: ["#9B59B6", "#8E44AD"]

---
YOUR TASK
---
Read the user's prompt. Select appropriate tile shape, size, and colors that 
match their creative description. Ensure the color palette complements the 
event type.

Respond ONLY with the JSON object. Do not include any other text, markdown, 
or conversation.
"""
```

## Implementation Notes

### Code Organization

- **New Files**:
  - `backend/app/model/prompt.py` - Engine type enums
  - `backend/app/inference/engine_router.py` - Classification logic
  - `backend/app/prompt/prompt_builder.py` - Prompt concatenation
  - `backend/app/engine/parametric_engine/` - Complete engine directory
  - `backend/app/engine/tessellation_engine/` - Complete engine directory

- **Modified Files**:
  - `backend/app/service/pattern_service.py` - Add router and engine selection
  - `backend/app/engine/fractal_engine/prompts.py` - Extract L_SYSTEM_PROMPT

- **Unchanged Files**:
  - Existing l_system engine logic remains the same
  - Card generator remains the same
  - Content generation remains the same

### Performance Considerations

- Router adds ~0.5-1 second for classification (acceptable)
- Total generation time: ~2-4 seconds (router + pattern + content)
- Classification can be cached for repeated similar prompts (future optimization)

### Future Enhancements

1. **More Engines**: Voronoi diagrams, Penrose tiling, Celtic knots
2. **Hybrid Patterns**: Combine multiple engines in one card
3. **Style Transfer**: Apply artistic styles to generated patterns
4. **Pattern Library**: Save and reuse successful configurations
5. **User Feedback Loop**: Learn from user preferences to improve routing

