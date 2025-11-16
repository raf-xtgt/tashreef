# Implementation Plan

- [x] 1. Create engine type models and enums
  - Create `backend/app/model/prompt.py` with EngineTypeEnum and EngineChoice Pydantic models
  - Define three engine types: l_system, parametric, tessellation
  - Add proper field descriptions and validation
  - _Requirements: 3.1, 3.2_

- [x] 2. Implement engine router for classification
  - [x] 2.1 Create router module and classification function
    - Create `backend/app/inference/engine_router.py`
    - Implement `classify_engine(user_prompt: str) -> EngineTypeEnum` async function
    - Define ROUTER_SYSTEM_PROMPT with classification rules and examples
    - _Requirements: 2.1, 2.2, 3.3_
  
  - [x] 2.2 Implement router logic with error handling
    - Build full prompt combining ROUTER_SYSTEM_PROMPT and user prompt
    - Call inference service with EngineChoice schema for structured output
    - Return selected engine_type from EngineChoice response
    - Default to "l_system" on classification failure or error
    - Add logging for router decisions and errors
    - _Requirements: 2.3, 2.4, 2.5, 2.6, 3.4, 3.5, 9.1, 9.5_

- [x] 3. Refactor prompt system for modularity
  - [x] 3.1 Extract L-System prompt from system_prompt.py
    - Create `backend/app/engine/fractal_engine/prompts.py` if it doesn't exist
    - Move L-System specific instructions to L_SYSTEM_PROMPT constant
    - Keep BASE_PROMPT in `backend/app/prompt/base_prompt.py`
    - _Requirements: 1.1, 1.2, 1.4, 1.5_
  
  - [x] 3.2 Create prompt builder utility
    - Create `backend/app/prompt/prompt_builder.py`
    - Implement `build_engine_prompt(engine_type, user_prompt)` function
    - Concatenate base prompt + engine-specific prompt + user prompt
    - Import appropriate engine prompt based on engine_type
    - _Requirements: 1.3_

- [x] 4. Implement parametric engine
  - [x] 4.1 Create parametric engine models
    - Create `backend/app/engine/parametric_engine/models.py`
    - Define EquationTypeEnum (rose, lissajous, epitrochoid, hypotrochoid)
    - Define ParametricParams Pydantic model with all parameters
    - Define ParametricConfig Pydantic model
    - Define ParametricResponse Pydantic model
    - _Requirements: 4.1, 4.2, 8.1_
  
  - [x] 4.2 Create parametric engine prompt
    - Create `backend/app/engine/parametric_engine/prompts.py`
    - Define PARAMETRIC_PROMPT with instructions and examples
    - Include all four equation types with parameter examples
    - _Requirements: 4.1_
  
  - [x] 4.3 Implement parametric equation generators
    - Create `backend/app/engine/parametric_engine/engine.py`
    - Implement `generate_rose_curve()` function
    - Implement `generate_lissajous_curve()` function
    - Implement `generate_epitrochoid_curve()` function
    - Implement `generate_hypotrochoid_curve()` function
    - Implement `generate_parametric_components()` main function
    - Convert generated points to SVG path data
    - _Requirements: 4.1, 4.3, 8.2, 8.3, 8.4, 8.5_
  
  - [x] 4.4 Implement parametric pattern processor
    - Create `backend/app/engine/parametric_engine/processor.py`
    - Implement `build_parametric_pattern_svg()` function for repeating background
    - Implement `process_parametric_request()` orchestration function
    - Return ParametricResponse with svg_string and config
    - _Requirements: 4.4, 4.5_

- [x] 5. Implement tessellation engine
  - [x] 5.1 Create tessellation engine models
    - Create `backend/app/engine/tessellation_engine/models.py`
    - Define TileShapeEnum (square, hexagon, triangle, diamond)
    - Define TessellationParams Pydantic model with all parameters
    - Define TessellationConfig Pydantic model
    - Define TessellationResponse Pydantic model
    - _Requirements: 5.1, 5.2, 5.3_
  
  - [x] 5.2 Create tessellation engine prompt
    - Create `backend/app/engine/tessellation_engine/prompts.py`
    - Define TESSELLATION_PROMPT with instructions and examples
    - Include all four tile shapes with parameter examples
    - _Requirements: 5.1_
  
  - [x] 5.3 Implement tessellation tile generators
    - Create `backend/app/engine/tessellation_engine/engine.py`
    - Implement `generate_square_tile()` function
    - Implement `generate_hexagon_tile()` function
    - Implement `generate_triangle_tile()` function
    - Implement `generate_diamond_tile()` function
    - Implement `generate_tessellation_components()` main function
    - _Requirements: 5.1, 5.3_
  
  - [x] 5.4 Implement tessellation pattern processor
    - Create `backend/app/engine/tessellation_engine/processor.py`
    - Implement `build_tessellation_pattern_svg()` function for seamless tiling
    - Ensure tiles connect properly without gaps or overlaps
    - Implement `process_tessellation_request()` orchestration function
    - Return TessellationResponse with svg_string and config
    - _Requirements: 5.4, 5.5_

- [x] 6. Integrate router and engines into pattern service
  - [x] 6.1 Add router classification to pattern service
    - Import `classify_engine` in `backend/app/service/pattern_service.py`
    - Call router at the start of `generate_pattern()` method
    - Log selected engine_type for debugging
    - _Requirements: 7.1, 9.5_
  
  - [x] 6.2 Add engine selection logic
    - Import prompt_builder and all engine processors
    - Build engine-specific prompt using `build_engine_prompt()`
    - Select appropriate config model based on engine_type
    - Select appropriate processor function based on engine_type
    - _Requirements: 7.2, 7.3_
  
  - [x] 6.3 Update pattern generation flow
    - Generate pattern config using selected config model
    - Process pattern using selected processor function
    - Extract pattern SVG from processor response
    - Pass pattern SVG to card generator (existing logic)
    - Maintain backward compatibility with existing l_system flow
    - _Requirements: 7.4, 7.5_
  
  - [x] 6.4 Add error handling for engine failures
    - Add try-catch for router classification failures
    - Add try-catch for pattern generation failures
    - Log errors with engine type and configuration details
    - Return appropriate error responses without falling back to different engines
    - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [ ]* 7. Add comprehensive logging and monitoring
  - Add detailed logging for router decisions
  - Log selected engine type and reasoning
  - Log pattern generation progress for each engine
  - Log any validation errors or failures
  - Add performance timing logs for optimization
  - _Requirements: 9.5_

- [ ]* 8. Update API response to include engine metadata
  - Modify CardResponse to include selected engine_type
  - Add router decision metadata to response
  - Update API documentation with new response structure
  - _Requirements: 9.4_
