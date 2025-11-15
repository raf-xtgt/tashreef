from pydantic import BaseModel, Field
from typing import Dict, Optional

class LSystemPatternParams(BaseModel):
    """Parameters for the L-System generation algorithm."""
    axiom: str = Field(
        ..., 
        description="The starting string (initiator) for the L-System.",
        example="X"
    )
    rules: Dict[str, str] = Field(
        ..., 
        description="The set of production rules to apply.",
        example={"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"}
    )
    angle: float = Field(
        ..., 
        description="The angle in degrees for turtle turns (+ or -).",
        example=25.0
    )
    iterations: int = Field(
        ..., 
        description="The number of times to apply the rules.",
        example=5
    )
    line_length: float = Field(
        default=5.0, 
        description="The length of a single 'F' (forward) segment. This will be scaled down for higher iterations."
    )
    start_x: float = Field(default=500.0, description="Starting X coordinate on the canvas.")
    start_y: float = Field(default=950.0, description="Starting Y coordinate on the canvas.")
    start_angle: float = Field(default=-90.0, description="Starting angle (in degrees). -90 is 'up'.")

class StyleParams(BaseModel):
    """Styling information for the final SVG."""
    fill: str = Field(default="none", description="Fill color (e.g., 'none', '#RRGGBB', 'PANTONE 15-0343').")
    stroke: str = Field(default="#000000", description="Stroke color (e.g., '#RRGGBB', 'PANTONE 15-0343').")
    stroke_width: float = Field(default=0.5, description="Stroke width in pixels.")

class LSystemConfig(BaseModel):
    """
    The complete configuration for generating an L-System pattern.
    This is the JSON object the AI must generate.
    """
    engine_type: str = Field(
        default="l_system",
        description="The specific generative engine to use. Should be 'l_system'."
    )
    parameters: LSystemPatternParams = Field(
        ...,
        description="The mathematical parameters for the L-System."
    )
    style: StyleParams = Field(
        ...,
        description="The visual style for the resulting SVG."
    )

class ColorScheme(BaseModel):
    """Color palette for the invitation card."""
    primary_text_color: str = Field(
        ...,
        description="Hex color code for main text elements (e.g., event title).",
        example="#FFFFFF"
    )
    secondary_text_color: str = Field(
        ...,
        description="Hex color code for secondary text elements (e.g., subtitle, details).",
        example="#F0F0F0"
    )
    overlay_color: str = Field(
        ...,
        description="Hex color code for the semi-transparent overlay behind text.",
        example="#000000"
    )
    overlay_opacity: float = Field(
        ...,
        description="Opacity value for the overlay (0.0 to 1.0).",
        ge=0.0,
        le=1.0,
        example=0.4
    )

class ContentConfig(BaseModel):
    """AI-generated content and styling for the e-invitation card."""
    event_title: str = Field(
        ...,
        description="The main title of the event (e.g., 'You're Invited', 'Together with their families').",
        example="You're Invited"
    )
    event_subtitle: str = Field(
        ...,
        description="A subtitle or secondary message for the event.",
        example="Join us for a celebration"
    )
    date_placeholder: str = Field(
        ...,
        description="Placeholder text for the event date.",
        example="Saturday, December 25th, 2025"
    )
    time_placeholder: str = Field(
        ...,
        description="Placeholder text for the event time.",
        example="6:00 PM onwards"
    )
    venue_placeholder: str = Field(
        ...,
        description="Placeholder text for the event venue.",
        example="The Grand Ballroom"
    )
    rsvp_text: str = Field(
        ...,
        description="Text for RSVP instructions.",
        example="RSVP by December 15th"
    )
    color_scheme: ColorScheme = Field(
        ...,
        description="The color palette for text and overlay elements."
    )

class CardResponse(BaseModel):
    """Complete response containing the final card SVG and all configuration data."""
    card_svg: str = Field(
        ...,
        description="The complete SVG string for the final e-invitation card."
    )
    pattern_config: LSystemConfig = Field(
        ...,
        description="The L-System configuration used to generate the pattern."
    )
    content_config: ContentConfig = Field(
        ...,
        description="The AI-generated content and styling configuration."
    )
