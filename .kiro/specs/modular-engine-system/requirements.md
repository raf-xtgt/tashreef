# Requirements Document

## Introduction

This feature implements a modular, scalable pattern engine system that supports multiple geometric generation engines (L-System/Fractal, Parametric/Spirograph, and Tessellation). The system introduces an intelligent engine classification layer that routes user prompts to the appropriate engine, and modularizes the prompt system to prevent prompt bloat as new engines are added.

## Glossary

- **Engine Router**: An AI-powered classification layer that analyzes user prompts and selects the appropriate pattern generation engine
- **Engine Type**: One of the available pattern generation engines (l_system, parametric, tessellation)
- **Base Prompt**: The core system instructions shared across all engine types
- **Engine-Specific Prompt**: Specialized instructions and examples for a particular engine type
- **Parametric Engine**: A pattern generator that creates spirograph-like patterns using parametric equations
- **Tessellation Engine**: A pattern generator that creates tiled, mosaic-like patterns using geometric shapes
- **L-System Engine**: The existing fractal pattern generator using Lindenmayer systems
- **Inference Service**: The service that communicates with the Gemini LLM for AI-powered decisions
- **Pattern Processor**: Engine-specific module that converts standalone patterns into repeating backgrounds

## Requirements

### Requirement 1

**User Story:** As a developer, I want the prompt system to be modular, so that adding new engines doesn't create an overwhelmingly large prompt for the LLM.

#### Acceptance Criteria

1. THE System SHALL maintain a base prompt containing core instructions shared across all engines
2. THE System SHALL maintain separate engine-specific prompts for each pattern generation engine
3. WHEN generating a pattern, THE System SHALL concatenate the base prompt with the selected engine-specific prompt
4. THE Base Prompt SHALL be stored in `backend/app/prompt/base_prompt.py`
5. THE Engine-Specific Prompts SHALL be stored in their respective engine directories under `backend/app/engine/*/prompts.py`

### Requirement 2

**User Story:** As a user, I want the system to automatically select the right pattern engine based on my creative description, so that I don't need to understand technical engine types.

#### Acceptance Criteria

1. THE Engine Router SHALL analyze the user prompt using chain-of-thought reasoning
2. THE Engine Router SHALL classify the prompt into one of three engine types: l_system, parametric, or tessellation
3. WHEN the user requests organic, branching, or fractal patterns, THE Engine Router SHALL select "l_system"
4. WHEN the user requests circular, hypnotic, or spirograph-like patterns, THE Engine Router SHALL select "parametric"
5. WHEN the user requests tiled, geometric, or mosaic-like patterns, THE Engine Router SHALL select "tessellation"
6. IF the prompt is ambiguous, THEN THE Engine Router SHALL default to "l_system"

### Requirement 3

**User Story:** As a developer, I want the engine router to use structured output, so that the classification result is type-safe and validated.

#### Acceptance Criteria

1. THE System SHALL define an EngineTypeEnum with values: l_system, parametric, tessellation
2. THE System SHALL define an EngineChoice Pydantic model containing the selected engine_type
3. THE Inference Service SHALL use structured output to ensure valid EngineChoice response
4. THE Engine Router SHALL return only the engine_type without generating pattern parameters
5. IF the router fails to classify, THEN THE System SHALL default to "l_system"

### Requirement 4

**User Story:** As a user, I want to create spirograph-like patterns using natural language, so that I can generate hypnotic circular designs for my invitations.

#### Acceptance Criteria

1. THE Parametric Engine SHALL generate patterns using parametric equations
2. THE Parametric Engine SHALL support configuration parameters: equation_type, amplitude, frequency, phase_shift, num_points
3. THE Parametric Engine SHALL create standalone pattern SVGs with circular or flowing curves
4. THE Parametric Processor SHALL convert standalone patterns into repeating backgrounds
5. THE Parametric Processor SHALL support grid-based tiling of the circular patterns

### Requirement 5

**User Story:** As a user, I want to create tessellation patterns using natural language, so that I can generate architectural mosaic designs for my invitations.

#### Acceptance Criteria

1. THE Tessellation Engine SHALL generate patterns using geometric tiling
2. THE Tessellation Engine SHALL support configuration parameters: tile_shape, tile_size, rotation, color_palette
3. THE Tessellation Engine SHALL support tile shapes: square, hexagon, triangle, diamond
4. THE Tessellation Processor SHALL convert standalone patterns into seamless repeating backgrounds
5. THE Tessellation Processor SHALL ensure tiles connect properly without gaps or overlaps

### Requirement 6

**User Story:** As a developer, I want each engine to follow the same architectural pattern, so that the codebase remains consistent and maintainable.

#### Acceptance Criteria

1. EACH engine directory SHALL contain: engine.py, processor.py, models.py, prompts.py
2. THE engine.py file SHALL contain the core pattern generation algorithm
3. THE processor.py file SHALL contain the logic to create repeating backgrounds
4. THE models.py file SHALL contain Pydantic configuration models
5. THE prompts.py file SHALL contain engine-specific LLM prompt templates

### Requirement 7

**User Story:** As a developer, I want the pattern service to support all three engines, so that users can generate any type of pattern through a single API endpoint.

#### Acceptance Criteria

1. THE Pattern Service SHALL invoke the Engine Router before generating patterns
2. THE Pattern Service SHALL select the appropriate engine based on the router's classification
3. THE Pattern Service SHALL pass the user prompt to the selected engine's inference call
4. THE Pattern Service SHALL invoke the appropriate processor for the selected engine
5. THE Pattern Service SHALL maintain backward compatibility with existing l_system patterns

### Requirement 8

**User Story:** As a user, I want the parametric engine to support different equation types, so that I can create various spirograph-like patterns.

#### Acceptance Criteria

1. THE Parametric Engine SHALL support equation types: rose, lissajous, epitrochoid, hypotrochoid
2. WHEN equation_type is "rose", THE Engine SHALL use the rose curve formula: r = a * cos(k * θ)
3. WHEN equation_type is "lissajous", THE Engine SHALL use parametric equations: x = A * sin(a*t + δ), y = B * sin(b*t)
4. WHEN equation_type is "epitrochoid", THE Engine SHALL use the epitrochoid formula
5. WHEN equation_type is "hypotrochoid", THE Engine SHALL use the hypotrochoid formula

### Requirement 9

**User Story:** As a developer, I want comprehensive error handling for the engine router, so that classification failures don't break the pattern generation flow.

#### Acceptance Criteria

1. IF the Engine Router fails to classify, THEN THE System SHALL log the error and default to "l_system"
2. IF the selected engine fails to generate a pattern, THEN THE System SHALL log the error and return an error response
3. THE System SHALL NOT attempt to fall back to a different engine if pattern generation fails
4. THE System SHALL include the selected engine_type in the final response for debugging
5. THE System SHALL log all router decisions for monitoring and improvement
