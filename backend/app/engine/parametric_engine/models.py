from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class EquationTypeEnum(str, Enum):
    """Available parametric equation types."""
    rose = "rose"
    lissajous = "lissajous"
    epitrochoid = "epitrochoid"
    hypotrochoid = "hypotrochoid"

class ParametricParams(BaseModel):
    """Parameters for parametric equation generation."""
    equation_type: EquationTypeEnum = Field(
        ...,
        description="The type of parametric equation to use (rose, lissajous, epitrochoid, hypotrochoid).",
        example="rose"
    )
    amplitude_a: float = Field(
        ...,
        description="Size/scale in x-direction (50-500).",
        ge=50.0,
        le=500.0,
        example=200.0
    )
    amplitude_b: float = Field(
        ...,
        description="Size/scale in y-direction (50-500).",
        ge=50.0,
        le=500.0,
        example=200.0
    )
    frequency_a: float = Field(
        ...,
        description="Number of cycles in x-direction (1-20).",
        ge=1.0,
        le=20.0,
        example=5.0
    )
    frequency_b: float = Field(
        ...,
        description="Number of cycles in y-direction (1-20).",
        ge=1.0,
        le=20.0,
        example=3.0
    )
    phase_shift: float = Field(
        default=0.0,
        description="Phase offset in radians (0-6.28).",
        ge=0.0,
        le=6.28,
        example=0.0
    )
    num_points: int = Field(
        default=1000,
        description="Number of points to generate (500-2000).",
        ge=500,
        le=2000,
        example=1000
    )

class StyleParams(BaseModel):
    """Styling information for the final SVG."""
    fill: str = Field(
        default="none",
        description="Fill color (e.g., 'none', '#RRGGBB').",
        example="none"
    )
    stroke: str = Field(
        ...,
        description="Stroke color (e.g., '#RRGGBB').",
        example="#FF1493"
    )
    stroke_width: float = Field(
        default=2.0,
        description="Stroke width in pixels.",
        ge=0.5,
        le=10.0,
        example=2.0
    )

class ParametricConfig(BaseModel):
    """
    The complete configuration for generating a parametric pattern.
    This is the JSON object the AI must generate.
    """
    engine_type: str = Field(
        default="parametric",
        description="The specific generative engine to use. Should be 'parametric'."
    )
    parameters: ParametricParams = Field(
        ...,
        description="The mathematical parameters for the parametric equations."
    )
    style: StyleParams = Field(
        ...,
        description="The visual style for the resulting SVG."
    )

class ParametricResponse(BaseModel):
    """Response containing the generated parametric pattern SVG and configuration."""
    svg_string: str = Field(
        ...,
        description="The complete SVG string for the parametric pattern."
    )
    config: ParametricConfig = Field(
        ...,
        description="The parametric configuration used to generate the pattern."
    )
