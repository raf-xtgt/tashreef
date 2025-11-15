# Implementation Plan

- [x] 1. Create data models for content configuration
  - Add ContentConfig and ColorScheme Pydantic models to `backend/app/engine/fractal_engine/models.py`
  - Add CardResponse Pydantic model to `backend/app/engine/fractal_engine/models.py`
  - Include proper field descriptions, examples, and validation rules
  - _Requirements: 1.2, 1.3, 5.1, 5.2, 5.5_

- [x] 2. Implement content generation prompt system
  - Create CONTENT_SYSTEM_PROMPT constant in `backend/app/engine/fractal_engine/prompts.py`
  - Include instructions for analyzing event type, tone, and cultural context
  - Define expected output format and examples for different event types
  - _Requirements: 1.1, 4.1, 4.2_

- [x] 3. Extend inference service for content generation
  - Add `generate_content_config()` method to `backend/app/inference/inference_service.py`
  - Build specialized prompt combining system prompt and user prompt
  - Use existing `_generate_structured_content()` with ContentConfig schema
  - Implement error handling with default ContentConfig fallback
  - _Requirements: 1.1, 1.4, 5.3, 5.4_

- [ ] 4. Implement core card generator function
  - [ ] 4.1 Create `generate_card()` async function in `backend/app/engine/fractal_engine/card_generator.py`
    - Accept pattern_svg, user_prompt, pattern_config, and inference_service as parameters
    - Return CardResponse object with complete card SVG
    - _Requirements: 2.1, 3.2_
  
  - [ ] 4.2 Implement content config generation logic
    - Call `inference_service.generate_content_config()` with user prompt
    - Handle inference failures with default ContentConfig
    - Log AI response and any errors
    - _Requirements: 1.1, 1.5_
  
  - [ ] 4.3 Implement SVG composition logic
    - Extract pattern defs and rect elements from pattern_svg
    - Build semi-transparent overlay rect with color scheme
    - Create text elements with proper positioning and styling
    - Compose final SVG with correct layer ordering
    - _Requirements: 2.2, 2.3, 2.4, 2.5_
  
  - [ ] 4.4 Apply color scheme to SVG elements
    - Apply primary_text_color to main text elements
    - Apply secondary_text_color to secondary text elements
    - Apply overlay_color and overlay_opacity to overlay rect
    - _Requirements: 2.4, 4.3, 4.4, 4.5_

- [ ] 5. Integrate card generator into pattern service
  - Import `generate_card` function in `backend/app/service/pattern_service.py`
  - Call `generate_card()` after `process_fractal_request()` completes
  - Pass pattern SVG, user prompt, pattern config, and inference service
  - Update file saving logic to save final card SVG
  - Update return value to include CardResponse JSON
  - _Requirements: 3.1, 3.2, 3.3, 3.5_

- [ ] 6. Update API response structure
  - Modify `generate_draft_card()` endpoint in `backend/app/routers/pattern/pattern_controller.py`
  - Return the CardResponse JSON from pattern service
  - Update endpoint documentation with new response structure
  - _Requirements: 3.4_

- [ ]* 7. Add error handling and logging
  - Add try-catch blocks for AI inference failures
  - Log all AI requests and responses for debugging
  - Log SVG composition steps and any validation errors
  - Add informative error messages for troubleshooting
  - _Requirements: 1.5, 3.5_

- [ ]* 8. Create default content config fallback
  - Define DEFAULT_CONTENT_CONFIG constant in `card_generator.py`
  - Include generic event text and safe color scheme
  - Use when AI inference fails or returns invalid data
  - _Requirements: 1.5_
