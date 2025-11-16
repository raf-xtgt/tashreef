"""
Engine Router for Pattern Generation Classification.

This module provides AI-powered classification to route user prompts to the
appropriate pattern generation engine (l_system, parametric, or tessellation).
"""

from app.model.prompt import EngineTypeEnum, EngineChoice
from app.inference.inference_service import InferenceService


# Router system prompt with classification rules and examples
ROUTER_SYSTEM_PROMPT = """
You are a Pattern Engine Classifier. Your sole job is to interpret the user's 
creative request and classify it into one of the available geometric generation 
engine types.

--- CLASSIFICATION RULES ---

1. **l_system**: If the user asks for a pattern that is organic, branching, 
   fractal, plant-like, fern-like, snowflake-like, tree-like, or natural.
   
   Keywords: fractal, branching, organic, fern, plant, tree, snowflake, 
   recursive, natural, delicate, intricate branching

2. **parametric**: If the user asks for a pattern that is hypnotic, circular, 
   cosmic, vortex-like, gear-like, spirograph-like, or uses complex flowing curves.
   
   Keywords: spirograph, circular, hypnotic, vortex, cosmic, flowing, curved, 
   rose, lissajous, spiral, swirl, psychedelic

3. **tessellation**: If the user asks for a pattern that is rigid, symmetrical, 
   tiled, architectural, mosaic-like, geometric, or involves repeating shapes 
   (squares, hexagons, triangles).
   
   Keywords: tessellation, tiled, mosaic, geometric, architectural, Islamic, 
   symmetrical, grid, honeycomb, repeating shapes, structured

4. **Default**: If the request is ambiguous or doesn't clearly fit any category, 
   default to 'l_system'.

--- EXAMPLES ---

Input: "Create a delicate fern pattern"
Output: {"engine_type": "l_system"}

Input: "Generate a hypnotic spirograph design"
Output: {"engine_type": "parametric"}

Input: "Make an Islamic geometric mosaic"
Output: {"engine_type": "tessellation"}

Input: "Create a beautiful pattern"
Output: {"engine_type": "l_system"}

--- YOUR TASK ---

Analyze the user's prompt below. Use chain-of-thought reasoning to determine 
which engine best matches their creative intent. Respond ONLY with a JSON object 
containing the chosen 'engine_type'. Do not include any other text, markdown, 
or parameters.
"""


async def classify_engine(user_prompt: str) -> EngineTypeEnum:
    """
    Classifies user prompt to determine appropriate pattern generation engine.
    
    Uses AI-powered analysis to route the user's creative request to one of
    three available engines: l_system (organic/fractal), parametric (circular/
    spirograph), or tessellation (geometric/mosaic).
    
    Args:
        user_prompt: The user's natural language description of desired pattern
        
    Returns:
        EngineTypeEnum indicating which engine should generate the pattern
        
    Note:
        Defaults to l_system if classification fails or returns invalid result
    """
    print(f"[Engine Router] Classifying prompt: {user_prompt}")
    
    try:
        # Build full prompt combining system prompt and user prompt
        full_prompt = f"{ROUTER_SYSTEM_PROMPT}\n\n---\nUSER PROMPT:\n{user_prompt}"
        
        # Initialize inference service
        inference_service = InferenceService()
        
        # Call inference service with EngineChoice schema for structured output
        engine_choice = await inference_service._generate_structured_content(
            full_prompt, 
            EngineChoice
        )
        
        # Check if we got a valid response
        if engine_choice and engine_choice.engine_type:
            selected_engine = engine_choice.engine_type
            print(f"[Engine Router] Selected engine: {selected_engine}")
            return selected_engine
        else:
            # AI returned None or invalid response
            print("[Engine Router] AI returned None or invalid response, defaulting to l_system")
            return EngineTypeEnum.l_system
            
    except Exception as e:
        # Log error and default to l_system
        print(f"[Engine Router] Error during classification: {e}")
        print("[Engine Router] Defaulting to l_system due to error")
        return EngineTypeEnum.l_system
