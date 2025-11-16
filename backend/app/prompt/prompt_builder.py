"""
Prompt builder utility for constructing engine-specific prompts.

This module provides functionality to concatenate base prompts with
engine-specific prompts based on the selected engine type.
"""

from app.model.prompt import EngineTypeEnum
from app.prompt.base_prompt import BASE_PROMPT


def build_engine_prompt(engine_type: EngineTypeEnum, user_prompt: str) -> str:
    """
    Build a complete prompt by concatenating base prompt, engine-specific prompt, and user prompt.
    
    Args:
        engine_type: The type of pattern generation engine to use
        user_prompt: The user's natural language request
        
    Returns:
        A complete prompt string ready for LLM inference
        
    Example:
        >>> prompt = build_engine_prompt(EngineTypeEnum.l_system, "Create a fern pattern")
        >>> # Returns: BASE_PROMPT + L_SYSTEM_PROMPT + user_prompt
    """
    base = BASE_PROMPT
    
    # Import and select the appropriate engine-specific prompt
    if engine_type == EngineTypeEnum.l_system:
        from app.engine.fractal_engine.prompts import L_SYSTEM_PROMPT
        engine_prompt = L_SYSTEM_PROMPT
    elif engine_type == EngineTypeEnum.parametric:
        from app.engine.parametric_engine.prompts import PARAMETRIC_PROMPT
        engine_prompt = PARAMETRIC_PROMPT
    elif engine_type == EngineTypeEnum.tessellation:
        from app.engine.tessellation_engine.prompts import TESSELLATION_PROMPT
        engine_prompt = TESSELLATION_PROMPT
    else:
        # Default to l_system if unknown engine type
        from app.engine.fractal_engine.prompts import L_SYSTEM_PROMPT
        engine_prompt = L_SYSTEM_PROMPT
    
    # Concatenate all parts with clear separation
    return f"{base}\n\n{engine_prompt}\n\n---\nUSER PROMPT:\n{user_prompt}"
