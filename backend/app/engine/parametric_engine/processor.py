"""Parametric pattern processor for creating repeating backgrounds."""
from .models import ParametricConfig, ParametricResponse
from .engine import generate_parametric_components
import json

def build_parametric_pattern_svg(components: dict) -> str:
    """
    Builds the final parametric pattern SVG with a repeating background.
    Creates a grid-based tiling of the circular/flowing patterns.
    """
    
    # --- Configuration for the Pattern Background ---
    CARD_WIDTH = 1080
    CARD_HEIGHT = 1920
    # Size of the repeating tile
    TILE_SIZE = 300
    
    # Extract components from the engine
    path_data = components['path_data']
    style = components['style']
    viewbox = components['viewBox']
    
    # Build the final SVG string with repeating pattern
    svg_string = f"""
<svg width="{CARD_WIDTH}" height="{CARD_HEIGHT}" viewBox="0 0 {CARD_WIDTH} {CARD_HEIGHT}" 
     xmlns="http://www.w3.org/2000/svg">
  
  <defs>
    <pattern id="parametric-pattern" 
             patternUnits="userSpaceOnUse"
             width="{TILE_SIZE}" 
             height="{TILE_SIZE}">
      
      <svg viewBox="{viewbox}" width="{TILE_SIZE}" height="{TILE_SIZE}">
        <path d="{path_data}" 
              fill="{style['fill']}" 
              stroke="{style['stroke']}" 
              stroke-width="{style['stroke_width']}" />
      </svg>
    </pattern>
  </defs>
  
  <rect width="100%" height="100%" fill="url(#parametric-pattern)" />
  
  <text x="50%" y="50%" 
        font-family="sans-serif" font-size="72" 
        fill="white" stroke="black" stroke-width="2"
        text-anchor="middle" dominant-baseline="middle">
    Your Event Here
  </text>
  
</svg>
"""
    return svg_string

def process_parametric_request(config: ParametricConfig) -> str:
    """
    Orchestrates the parametric pattern generation and returns a
    client-side-ready JSON string.
    
    This is the "ParametricProcessor" layer.
    """
    print(f"Processing parametric request for engine: {config.engine_type}")
    
    # 1. Call the "math engine" to get the raw components
    svg_components = generate_parametric_components(config)
    
    # 2. Call the "presentation" function to build the SVG string with the repeating pattern
    final_svg_string = build_parametric_pattern_svg(svg_components)
    
    # 3. Create the client-side-ready response object
    response_data = ParametricResponse(
        svg_string=final_svg_string,
        config=config
    )
    
    # 4. Return as a JSON string
    print("Successfully generated parametric pattern SVG. Returning JSON payload.")
    return response_data.model_dump_json(indent=2)
