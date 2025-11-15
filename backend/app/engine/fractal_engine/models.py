from pydantic import BaseModel, Field
from typing import Dict

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