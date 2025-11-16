from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class TileShapeEnum(str, Enum):
    """Available tessellation tile shapes."""
    square = "square"
    hexagon = "hexagon"
    triangle = "triangle"
    diamond = "diamond"

class TessellationParams(BaseModel):
    """Parameters for tessellation pattern generation."""
    tile_shape: TileShapeEnum = Field(
        ...,
        description="The shape of the repeating tile (square, hexagon, triangle, diamond).",
        example="hexagon"
    )
    tile_size: float = Field(
        ...,
        description="Size of each tile in pixels (50-200).",
        ge=50.0,
        le=200.0,
        example=100.0
    )
    rotation: float = Field(
        default=0.0,
        description="Rotation angle in degrees (0-360).",
        ge=0.0,
        le=360.0,
        example=0.0
    )
    spacing: float = Field(
        default=0.0,
        description="Gap between tiles in pixels (0-10).",
        ge=0.0,
        le=10.0,
        example=2.0
    )
    color_palette: List[str] = Field(
        ...,
        description="Array of 2-5 hex colors for alternating tiles.",
        min_items=2,
        max_items=5,
        example=["#4682B4", "#87CEEB", "#B0E0E6"]
    )

class StyleParams(BaseModel):
    """Styling information for the final SVG."""
    fill: str = Field(
        default="#4682B4",
        description="Fill color (e.g., '#RRGGBB'). Not used for tessellations (color_palette is used instead).",
        example="#4682B4"
    )
    stroke: str = Field(
        default="#FFFFFF",
        description="Stroke color (e.g., '#FFFFFF', '#000000').",
        example="#FFFFFF"
    )
    stroke_width: float = Field(
        default=1.0,
        description="Stroke width in pixels.",
        ge=0.5,
        le=10.0,
        example=1.0
    )

class TessellationConfig(BaseModel):
    """
    The complete configuration for generating a tessellation pattern.
    This is the JSON object the AI must generate.
    """
    engine_type: str = Field(
        default="tessellation",
        description="The specific generative engine to use. Should be 'tessellation'."
    )
    parameters: TessellationParams = Field(
        ...,
        description="The mathematical parameters for the tessellation pattern."
    )
    style: StyleParams = Field(
        ...,
        description="The visual style for the resulting SVG."
    )

class TessellationResponse(BaseModel):
    """Response containing the generated tessellation pattern SVG and configuration."""
    svg_string: str = Field(
        ...,
        description="The complete SVG string for the tessellation pattern."
    )
    config: TessellationConfig = Field(
        ...,
        description="The tessellation configuration used to generate the pattern."
    )
