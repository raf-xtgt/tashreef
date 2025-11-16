"""
Engine type models for pattern generation routing.

This module defines the engine types available in the system and the
structured output model for engine classification.
"""

from enum import Enum
from pydantic import BaseModel, Field


class EngineTypeEnum(str, Enum):
    """
    Available pattern generation engines.
    
    Each engine type represents a different mathematical approach to
    generating geometric patterns for e-invitation cards.
    """
    l_system = "l_system"
    parametric = "parametric"
    tessellation = "tessellation"


class EngineChoice(BaseModel):
    """
    Router output model for engine classification.
    
    This model is used as the structured output schema when the AI
    classifies user prompts to determine which pattern engine to use.
    """
    engine_type: EngineTypeEnum = Field(
        ...,
        description="The selected pattern generation engine based on user prompt analysis. "
                    "l_system for organic/fractal patterns, parametric for circular/spirograph patterns, "
                    "tessellation for geometric/mosaic patterns."
    )
