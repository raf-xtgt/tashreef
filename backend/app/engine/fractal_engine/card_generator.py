import re
from .models import LSystemConfig, ContentConfig, CardResponse, ColorScheme
from typing import Optional

# Default content config to use when AI inference fails
DEFAULT_CONTENT_CONFIG = ContentConfig(
    event_title="Your Event Here",
    event_subtitle="Join us for a celebration",
    date_placeholder="Date to be announced",
    time_placeholder="Time to be announced",
    venue_placeholder="Venue to be announced",
    rsvp_text="Please RSVP",
    color_scheme=ColorScheme(
        primary_text_color="#FFFFFF",
        secondary_text_color="#F0F0F0",
        overlay_color="#000000",
        overlay_opacity=0.4
    )
)


async def generate_card(
    pattern_svg: str,
    user_prompt: str,
    pattern_config: LSystemConfig,
    inference_service
) -> CardResponse:
    """
    Generate a complete e-invitation card by combining pattern SVG with AI-generated content.
    
    Args:
        pattern_svg: The SVG string containing the repeating pattern background
        user_prompt: The user's original prompt describing the invitation
        pattern_config: The L-System configuration used to generate the pattern
        inference_service: The InferenceService instance for AI content generation
        
    Returns:
        CardResponse object containing the complete card SVG and all configurations
    """
    print("=== Starting Card Generation ===")
    print(f"User prompt: {user_prompt}")
    
    # Subtask 4.2: Implement content config generation logic
    content_config = await _generate_content_config(inference_service, user_prompt)
    
    # Subtask 4.3 & 4.4: Implement SVG composition and apply color scheme
    card_svg = _compose_card_svg(pattern_svg, content_config)
    
    print("=== Card Generation Complete ===")
    
    # Return CardResponse object
    return CardResponse(
        card_svg=card_svg,
        pattern_config=pattern_config,
        content_config=content_config
    )


async def _generate_content_config(
    inference_service,
    user_prompt: str
) -> ContentConfig:
    """
    Generate content configuration using AI inference with fallback to defaults.
    
    Subtask 4.2: Implement content config generation logic
    - Call inference_service.generate_content_config() with user prompt
    - Handle inference failures with default ContentConfig
    - Log AI response and any errors
    """
    print("--- Generating Content Config ---")
    
    try:
        # Call the inference service to generate content config
        content_config = await inference_service.generate_content_config(user_prompt)
        
        if content_config:
            print("✓ Successfully generated content config from AI")
            print(f"  Event: {content_config.event_title}")
            print(f"  Colors: {content_config.color_scheme.primary_text_color}")
            return content_config
        else:
            print("⚠ AI returned None, using default content config")
            return DEFAULT_CONTENT_CONFIG
            
    except Exception as e:
        print(f"✗ Error generating content config: {e}")
        print("  Falling back to default content config")
        return DEFAULT_CONTENT_CONFIG


def _compose_card_svg(pattern_svg: str, content_config: ContentConfig) -> str:
    """
    Compose the final card SVG by combining pattern, overlay, and text elements.
    
    Subtask 4.3: Implement SVG composition logic
    - Extract pattern defs and rect elements from pattern_svg
    - Build semi-transparent overlay rect with color scheme
    - Create text elements with proper positioning and styling
    - Compose final SVG with correct layer ordering
    
    Subtask 4.4: Apply color scheme to SVG elements
    - Apply primary_text_color to main text elements
    - Apply secondary_text_color to secondary text elements
    - Apply overlay_color and overlay_opacity to overlay rect
    """
    print("--- Composing Card SVG ---")
    
    # Extract pattern defs and rect from the pattern_svg
    defs_match = re.search(r'<defs>(.*?)</defs>', pattern_svg, re.DOTALL)
    pattern_rect_match = re.search(r'<rect[^>]*fill="url\(#fractal-pattern\)"[^>]*/>', pattern_svg)
    
    if not defs_match or not pattern_rect_match:
        print("⚠ Warning: Could not extract pattern elements from SVG")
        defs_content = ""
        pattern_rect = '<rect width="100%" height="100%" fill="#CCCCCC" />'
    else:
        defs_content = defs_match.group(1)
        pattern_rect = pattern_rect_match.group(0)
        print("✓ Extracted pattern defs and rect")
    
    # Extract color scheme
    color_scheme = content_config.color_scheme
    print(f"✓ Applying color scheme:")
    print(f"  Primary text: {color_scheme.primary_text_color}")
    print(f"  Secondary text: {color_scheme.secondary_text_color}")
    print(f"  Overlay: {color_scheme.overlay_color} @ {color_scheme.overlay_opacity}")
    
    # Card dimensions
    CARD_WIDTH = 1080
    CARD_HEIGHT = 1920
    
    # Build the final SVG with proper layer ordering
    # Layer 1: Pattern background
    # Layer 2: Semi-transparent overlay
    # Layer 3: Text content
    
    card_svg = f"""<svg width="{CARD_WIDTH}" height="{CARD_HEIGHT}" viewBox="0 0 {CARD_WIDTH} {CARD_HEIGHT}" 
     xmlns="http://www.w3.org/2000/svg">
  
  <!-- Layer 1: Pattern Background -->
  <defs>
{defs_content}
  </defs>
  
  {pattern_rect}
  
  <!-- Layer 2: Semi-transparent Overlay for Text Readability -->
  <rect width="100%" height="100%" 
        fill="{color_scheme.overlay_color}" 
        opacity="{color_scheme.overlay_opacity}" />
  
  <!-- Layer 3: Content Text -->
  <!-- Event Title (Primary Text) -->
  <text x="50%" y="800" 
        font-family="serif" font-size="96" font-weight="bold"
        fill="{color_scheme.primary_text_color}" 
        text-anchor="middle" dominant-baseline="middle">
    {_escape_xml(content_config.event_title)}
  </text>
  
  <!-- Event Subtitle (Secondary Text) -->
  <text x="50%" y="900" 
        font-family="serif" font-size="48" font-style="italic"
        fill="{color_scheme.secondary_text_color}" 
        text-anchor="middle" dominant-baseline="middle">
    {_escape_xml(content_config.event_subtitle)}
  </text>
  
  <!-- Date Placeholder (Secondary Text) -->
  <text x="50%" y="1000" 
        font-family="sans-serif" font-size="36"
        fill="{color_scheme.secondary_text_color}" 
        text-anchor="middle" dominant-baseline="middle">
    {_escape_xml(content_config.date_placeholder)}
  </text>
  
  <!-- Time Placeholder (Secondary Text) -->
  <text x="50%" y="1080" 
        font-family="sans-serif" font-size="36"
        fill="{color_scheme.secondary_text_color}" 
        text-anchor="middle" dominant-baseline="middle">
    {_escape_xml(content_config.time_placeholder)}
  </text>
  
  <!-- Venue Placeholder (Secondary Text) -->
  <text x="50%" y="1160" 
        font-family="sans-serif" font-size="36"
        fill="{color_scheme.secondary_text_color}" 
        text-anchor="middle" dominant-baseline="middle">
    {_escape_xml(content_config.venue_placeholder)}
  </text>
  
  <!-- RSVP Text (Secondary Text) -->
  <text x="50%" y="1300" 
        font-family="sans-serif" font-size="32"
        fill="{color_scheme.secondary_text_color}" 
        text-anchor="middle" dominant-baseline="middle">
    {_escape_xml(content_config.rsvp_text)}
  </text>
  
</svg>"""
    
    print("✓ Card SVG composition complete")
    return card_svg


def _escape_xml(text: str) -> str:
    """Escape special XML characters in text content."""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")) 