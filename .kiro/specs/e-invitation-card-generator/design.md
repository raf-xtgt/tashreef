# Design Document

## Overview

The e-invitation card generator is a two-phase AI-powered system that transforms a geometric pattern SVG into a complete draft invitation card. The design follows the existing architectural patterns in Tashreef, using a service-layer orchestration approach with separate concerns for AI inference, content generation, and SVG composition.

The system integrates seamlessly into the current pattern generation flow: after the fractal processor generates the repeating pattern SVG, the card generator performs a second AI inference round to determine contextually appropriate content and styling, then composes the final card SVG.

## Architecture

### High-Level Flow

```
User Prompt → Pattern Service → Inference Service (Pattern Config)
                    ↓
            Fractal Processor (Pattern SVG)
                    ↓
            Card Generator ← Inference Service (Content Config)
                    ↓
            Final Card SVG → Response
```

### Component Interaction

1. **Pattern Service** orchestrates the entire flow
2. **Inference Service** handles both AI inference rounds (pattern config + content config)
3. **Fractal Processor** generates the pattern SVG (existing)
4. **Card Generator** composes the final card SVG with content overlay

### Design Principles

- **Separation of Concerns**: Card generator focuses solely on SVG composition, not AI logic
- **Reusability**: Inference service is extended to support multiple prompt types
- **Type Safety**: Pydantic models ensure data validation throughout
- **Async/Await**: All I/O operations remain asynchronous
- **Minimal Changes**: Integrate into existing flow without breaking current functionality

## Components and Interfaces

### 1. ContentConfig Model (New)

**Location**: `backend/app/engine/fractal_engine/models.py`

```python
class ContentConfig(BaseModel):
    """AI-generated content and styling for the e-invitation card."""
    event_title: str
    event_subtitle: str
    date_placeholder: str
    time_placeholder: str
    venue_placeholder: str
    rsvp_text: str
    color_scheme: ColorScheme

class ColorScheme(BaseModel):
    """Color palette for the invitation card."""
    primary_text_color: str  # Hex color for main text
    secondary_text_color: str  # Hex color for secondary text
    overlay_color: str  # Hex color for semi-transparent overlay
    overlay_opacity: float  # 0.0 to 1.0
```

### 2. CardResponse Model (New)

**Location**: `backend/app/engine/fractal_engine/models.py`

```python
class CardResponse(BaseModel):
    """Complete response containing the final card SVG."""
    card_svg: str
    pattern_config: LSystemConfig
    content_config: ContentConfig
```

### 3. Card Generator Function (Implementation)

**Location**: `backend/app/engine/fractal_engine/card_generator.py`

**Signature**:
```python
async def generate_card(
    pattern_svg: str,
    user_prompt: str,
    pattern_config: LSystemConfig,
    inference_service: InferenceService
) -> CardResponse
```

**Responsibilities**:
- Call inference service to generate ContentConfig
- Parse the pattern SVG to extract the pattern definition
- Compose final card SVG with content overlay
- Return CardResponse with all components

**Key Logic**:
1. Invoke `inference_service._generate_structured_content()` with content prompt
2. Extract pattern `<defs>` and `<rect>` from pattern_svg
3. Build text elements with proper positioning and styling
4. Add semi-transparent overlay for text readability
5. Compose final SVG with proper layering (pattern → overlay → text)

### 4. Inference Service Extension (Modification)

**Location**: `backend/app/inference/inference_service.py`

**New Method**:
```python
async def generate_content_config(
    self, 
    user_prompt: str, 
    event_context: str
) -> ContentConfig
```

**Responsibilities**:
- Build a specialized prompt for content generation
- Use existing `_generate_structured_content()` with ContentConfig schema
- Handle errors and provide default fallback

### 5. Pattern Service Integration (Modification)

**Location**: `backend/app/service/pattern_service.py`

**Changes to `generate_pattern()` method**:
```python
async def generate_pattern(self, user_prompt: str, db: AsyncSession):
    # Existing pattern generation...
    ai_config = await service._generate_structured_content(user_prompt, LSystemConfig)
    pattern_svg_json = process_fractal_request(ai_config)
    pattern_data = json.loads(pattern_svg_json)
    
    # NEW: Generate complete card
    from app.engine.fractal_engine.card_generator import generate_card
    card_response = await generate_card(
        pattern_svg=pattern_data['svg_string'],
        user_prompt=user_prompt,
        pattern_config=ai_config,
        inference_service=service
    )
    
    # Save final card SVG
    output_filename = "sample_patterns/temp_card_output.svg"
    with open(output_filename, "w") as f:
        f.write(card_response.card_svg)
    
    return card_response.model_dump_json(indent=2)
```

## Data Models

### ContentConfig Schema

```json
{
  "event_title": "You're Invited",
  "event_subtitle": "Join us for a celebration",
  "date_placeholder": "Saturday, December 25th, 2025",
  "time_placeholder": "6:00 PM onwards",
  "venue_placeholder": "The Grand Ballroom",
  "rsvp_text": "RSVP by December 15th",
  "color_scheme": {
    "primary_text_color": "#FFFFFF",
    "secondary_text_color": "#F0F0F0",
    "overlay_color": "#000000",
    "overlay_opacity": 0.4
  }
}
```

### CardResponse Schema

```json
{
  "card_svg": "<svg>...</svg>",
  "pattern_config": { /* LSystemConfig */ },
  "content_config": { /* ContentConfig */ }
}
```

## Error Handling

### AI Inference Failures

**Scenario**: Gemini API fails or returns invalid JSON

**Handling**:
1. Log the error with full context
2. Use default ContentConfig values:
   - Generic event text ("Your Event Here")
   - Standard date/time placeholders
   - Safe color scheme (white text, black overlay)
3. Continue with card generation using defaults
4. Include error flag in response for client awareness

### Invalid Pattern SVG

**Scenario**: Pattern SVG is malformed or missing required elements

**Handling**:
1. Validate SVG structure before processing
2. If invalid, log error and return error response
3. Do not attempt card generation with invalid pattern

### Database Errors

**Scenario**: Database operations fail (future consideration)

**Handling**:
- Currently no database operations in card generator
- Future: Implement retry logic and transaction rollback

## Testing Strategy

### Unit Tests

**Test File**: `backend/tests/test_card_generator.py`

**Test Cases**:
1. `test_generate_card_with_valid_inputs()` - Happy path with mock inference
2. `test_generate_card_with_inference_failure()` - Verify default fallback
3. `test_content_config_validation()` - Test Pydantic model validation
4. `test_svg_composition()` - Verify SVG structure and layering
5. `test_color_scheme_application()` - Verify colors applied correctly

### Integration Tests

**Test File**: `backend/tests/test_pattern_service_integration.py`

**Test Cases**:
1. `test_end_to_end_card_generation()` - Full flow from prompt to card
2. `test_pattern_and_content_consistency()` - Verify both AI calls work together
3. `test_file_output()` - Verify SVG files are saved correctly

### Manual Testing

**Test Scenarios**:
1. Wedding invitation prompt → Verify formal content and elegant colors
2. Birthday party prompt → Verify casual content and playful colors
3. Corporate event prompt → Verify professional content and brand colors
4. Invalid prompt → Verify graceful degradation with defaults

## SVG Composition Details

### Layer Structure

```xml
<svg width="1080" height="1920" viewBox="0 0 1080 1920">
  <!-- Layer 1: Pattern Background -->
  <defs>
    <pattern id="fractal-pattern">...</pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#fractal-pattern)" />
  
  <!-- Layer 2: Semi-transparent Overlay -->
  <rect width="100%" height="100%" 
        fill="{overlay_color}" 
        opacity="{overlay_opacity}" />
  
  <!-- Layer 3: Content Text -->
  <text y="800" ...>{event_title}</text>
  <text y="900" ...>{event_subtitle}</text>
  <text y="1000" ...>{date_placeholder}</text>
  <text y="1080" ...>{time_placeholder}</text>
  <text y="1160" ...>{venue_placeholder}</text>
  <text y="1300" ...>{rsvp_text}</text>
</svg>
```

### Text Positioning

- **Vertical Center**: Primary content centered around y=960 (half of 1920)
- **Spacing**: 80-100px between text elements
- **Horizontal**: All text centered (x="50%", text-anchor="middle")
- **Font Sizes**: 
  - Title: 96px
  - Subtitle: 48px
  - Details: 36px
  - RSVP: 32px

### Responsive Considerations

- Fixed dimensions (1080x1920) for consistent output
- ViewBox ensures proper scaling on different displays
- Text sizes proportional to card dimensions

## Content Generation Prompt

### System Prompt for Content Config

```
You are an expert invitation designer. Given a user's request for an e-invitation card, 
generate appropriate placeholder content and a color scheme.

Analyze the user's prompt to determine:
1. Event type (wedding, birthday, corporate, casual, formal, etc.)
2. Tone (formal, casual, playful, elegant, professional)
3. Cultural context (if mentioned)

Generate:
- Event title and subtitle that match the tone
- Realistic date, time, and venue placeholders
- RSVP text appropriate for the event type
- Color scheme that enhances readability over the geometric pattern

Respond ONLY with valid JSON matching the ContentConfig schema.
```

### Example Prompts and Expected Outputs

**Input**: "Create a wedding invitation with elegant floral patterns"

**Output**:
```json
{
  "event_title": "Together with their families",
  "event_subtitle": "request the honor of your presence",
  "date_placeholder": "Saturday, the fifteenth of June",
  "time_placeholder": "at half past four in the afternoon",
  "venue_placeholder": "The Rose Garden Estate",
  "rsvp_text": "Kindly respond by May 30th",
  "color_scheme": {
    "primary_text_color": "#FFFFFF",
    "secondary_text_color": "#F5F5DC",
    "overlay_color": "#2C1810",
    "overlay_opacity": 0.5
  }
}
```

**Input**: "Birthday party invitation with fun geometric shapes"

**Output**:
```json
{
  "event_title": "You're Invited!",
  "event_subtitle": "Let's celebrate together",
  "date_placeholder": "Saturday, March 20th, 2025",
  "time_placeholder": "3:00 PM - 7:00 PM",
  "venue_placeholder": "123 Party Street",
  "rsvp_text": "Let us know if you can make it!",
  "color_scheme": {
    "primary_text_color": "#FFD700",
    "secondary_text_color": "#FFFFFF",
    "overlay_color": "#FF1493",
    "overlay_opacity": 0.3
  }
}
```

## Implementation Notes

### Code Organization

- Keep card generator logic in `card_generator.py` (single responsibility)
- Add models to existing `models.py` (maintain consistency)
- Extend inference service without breaking existing functionality
- Modify pattern service minimally (just add card generation call)

### Performance Considerations

- Second AI inference adds ~1-2 seconds to total generation time
- Acceptable for draft card generation use case
- Future optimization: Cache common content configs by event type

### Future Enhancements

1. **User Customization**: Allow users to override AI-generated content
2. **Template Library**: Pre-defined content templates for common events
3. **Multi-language Support**: Generate content in different languages
4. **Font Selection**: AI chooses appropriate fonts based on event type
5. **Image Upload**: Allow users to add photos to the card
6. **QR Code**: Generate QR code for RSVP or event details
