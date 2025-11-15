from pydantic import BaseModel
from .models import LSystemConfig
from .engine import generate_l_system_components # Import the new function
import json

class FractalResponse(BaseModel):
    """
    A client-side-ready response containing the generated SVG string
    and the configuration parameters used to create it.
    """
    svg_string: str
    config: LSystemConfig

def build_e_card_svg(components: dict) -> str:
    """
    Builds the final e-invitation card SVG with a repeating pattern background.
    """
    
    # --- Configuration for the E-Invitation ---
    CARD_WIDTH = 1080
    CARD_HEIGHT = 1920
    # Size of the repeating tile. You can adjust this.
    TILE_SIZE = 300 
    
    # Extract components from the engine
    path_data = components['path_data']
    style = components['style']
    fractal_viewbox = components['viewBox']
    
    # Build the final SVG string using an f-string
    svg_string = f"""
<svg width="{CARD_WIDTH}" height="{CARD_HEIGHT}" viewBox="0 0 {CARD_WIDTH} {CARD_HEIGHT}" 
     xmlns="http://www.w3.org/2000/svg">
  
  <defs>
    <pattern id="fractal-pattern" 
             patternUnits="userSpaceOnUse"
             width="{TILE_SIZE}" 
             height="{TILE_SIZE}">
      
      <svg viewBox="{fractal_viewbox}" width="{TILE_SIZE}" height="{TILE_SIZE}">
        <path d="{path_data}" 
              fill="{style['fill']}" 
              stroke="{style['stroke']}" 
              stroke-width="{style['stroke_width']}" />
      </svg>
    </pattern>
  </defs>
  
  <rect width="100%" height="100%" fill="url(#fractal-pattern)" />
  
  <text x="50%" y="50%" 
        font-family="sans-serif" font-size="72" 
        fill="white" stroke="black" stroke-width="2"
        text-anchor="middle" dominant-baseline="middle">
    Your Event Here
  </text>
  
</svg>
"""
    return svg_string

def process_fractal_request(config: LSystemConfig) -> str:
    """
    Orchestrates the L-System generation and returns a
    client-side-ready JSON string.

    This is the "FractalProcessor" layer.
    """
    print(f"Processing L-System request for engine: {config.engine_type}")
    
    # 1. Call the "math engine" to get the raw components
    svg_components = generate_l_system_components(config)
    
    # 2. Call the "presentation" function to build the SVG string with the repeating pattern
    final_svg_string = build_e_card_svg(svg_components)
    
    # 3. Create the client-side-ready response object
    response_data = FractalResponse(
        svg_string=final_svg_string,
        config=config
    )
    
    # 4. Return as a JSON string
    print("Successfully generated repeating pattern SVG. Returning JSON payload.")
    return response_data.model_dump_json(indent=2)