"""Tessellation pattern processor for creating seamless tiling backgrounds."""
from .models import TessellationConfig, TessellationResponse, TileShapeEnum
from .engine import generate_tessellation_components
import json
import math

def build_tessellation_pattern_svg(components: dict) -> str:
    """
    Builds the final tessellation pattern SVG with seamless tiling.
    Ensures tiles connect properly without gaps or overlaps.
    """
    
    # --- Configuration for the Pattern Background ---
    CARD_WIDTH = 1080
    CARD_HEIGHT = 1920
    
    # Extract components from the engine
    tile_path = components['tile_path']
    tile_shape = components['tile_shape']
    tile_size = components['tile_size']
    rotation = components['rotation']
    spacing = components['spacing']
    color_palette = components['color_palette']
    style = components['style']
    
    # Calculate tile dimensions based on shape for proper tiling
    if tile_shape == "hexagon":
        # Hexagon tiling requires specific spacing
        tile_width = tile_size
        tile_height = tile_size * math.sqrt(3) / 2
        pattern_width = tile_width * 0.75 + spacing
        pattern_height = tile_height + spacing
    elif tile_shape == "triangle":
        # Triangle tiling
        tile_width = tile_size
        tile_height = tile_size * math.sqrt(3) / 2
        pattern_width = tile_width + spacing
        pattern_height = tile_height + spacing
    else:
        # Square and diamond use same dimensions
        pattern_width = tile_size + spacing
        pattern_height = tile_size + spacing
    
    # Build SVG with pattern definition
    svg_parts = []
    svg_parts.append(f'''<svg width="{CARD_WIDTH}" height="{CARD_HEIGHT}" viewBox="0 0 {CARD_WIDTH} {CARD_HEIGHT}" 
     xmlns="http://www.w3.org/2000/svg">''')
    
    svg_parts.append('  <defs>')
    svg_parts.append(f'''    <pattern id="tessellation-pattern" 
             patternUnits="userSpaceOnUse"
             width="{pattern_width}" 
             height="{pattern_height}">''')
    
    # Add tiles to pattern with color variations
    if tile_shape == "hexagon":
        # Hexagon tiling with offset rows
        svg_parts.append(_build_hexagon_pattern_tiles(
            tile_path, tile_size, spacing, color_palette, style, rotation
        ))
    elif tile_shape == "triangle":
        # Triangle tiling with alternating orientations
        svg_parts.append(_build_triangle_pattern_tiles(
            tile_path, tile_size, spacing, color_palette, style, rotation
        ))
    else:
        # Square and diamond use simple grid
        svg_parts.append(_build_grid_pattern_tiles(
            tile_path, tile_size, spacing, color_palette, style, rotation
        ))
    
    svg_parts.append('    </pattern>')
    svg_parts.append('  </defs>')
    
    # Apply pattern to full card
    svg_parts.append('  <rect width="100%" height="100%" fill="url(#tessellation-pattern)" />')
    
    # Add placeholder text
    svg_parts.append('''  <text x="50%" y="50%" 
        font-family="sans-serif" font-size="72" 
        fill="white" stroke="black" stroke-width="2"
        text-anchor="middle" dominant-baseline="middle">
    Your Event Here
  </text>''')
    
    svg_parts.append('</svg>')
    
    return '\n'.join(svg_parts)

def _build_grid_pattern_tiles(tile_path: str, tile_size: float, spacing: float, 
                               color_palette: list, style: dict, rotation: float) -> str:
    """Build tiles for square/diamond grid pattern."""
    tiles = []
    center = tile_size / 2 + spacing / 2
    
    # Single tile with color from palette
    color = color_palette[0]
    transform = f'translate({center}, {center})'
    if rotation != 0:
        transform += f' rotate({rotation})'
    
    tiles.append(f'''      <g transform="{transform}">
        <path d="{tile_path}" 
              fill="{color}" 
              stroke="{style['stroke']}" 
              stroke-width="{style['stroke_width']}" />
      </g>''')
    
    return '\n'.join(tiles)

def _build_hexagon_pattern_tiles(tile_path: str, tile_size: float, spacing: float,
                                  color_palette: list, style: dict, rotation: float) -> str:
    """Build tiles for hexagon honeycomb pattern with proper offset."""
    tiles = []
    
    # Hexagon dimensions
    width = tile_size
    height = tile_size * math.sqrt(3) / 2
    
    # Main hexagon
    color = color_palette[0]
    transform = f'translate({width * 0.375}, {height / 2})'
    if rotation != 0:
        transform += f' rotate({rotation})'
    
    tiles.append(f'''      <g transform="{transform}">
        <path d="{tile_path}" 
              fill="{color}" 
              stroke="{style['stroke']}" 
              stroke-width="{style['stroke_width']}" />
      </g>''')
    
    # Offset hexagon for seamless tiling (if multiple colors)
    if len(color_palette) > 1:
        color2 = color_palette[1]
        transform2 = f'translate({width * 0.375}, {height * 1.5})'
        if rotation != 0:
            transform2 += f' rotate({rotation})'
        
        tiles.append(f'''      <g transform="{transform2}">
        <path d="{tile_path}" 
              fill="{color2}" 
              stroke="{style['stroke']}" 
              stroke-width="{style['stroke_width']}" />
      </g>''')
    
    return '\n'.join(tiles)

def _build_triangle_pattern_tiles(tile_path: str, tile_size: float, spacing: float,
                                   color_palette: list, style: dict, rotation: float) -> str:
    """Build tiles for triangle pattern with alternating orientations."""
    tiles = []
    
    height = tile_size * math.sqrt(3) / 2
    center_x = tile_size / 2
    center_y = height / 2
    
    # Upward triangle
    color = color_palette[0]
    transform = f'translate({center_x}, {center_y})'
    if rotation != 0:
        transform += f' rotate({rotation})'
    
    tiles.append(f'''      <g transform="{transform}">
        <path d="{tile_path}" 
              fill="{color}" 
              stroke="{style['stroke']}" 
              stroke-width="{style['stroke_width']}" />
      </g>''')
    
    # Downward triangle (if multiple colors)
    if len(color_palette) > 1:
        color2 = color_palette[1]
        transform2 = f'translate({center_x}, {center_y}) rotate(180)'
        if rotation != 0:
            transform2 += f' rotate({rotation})'
        
        tiles.append(f'''      <g transform="{transform2}">
        <path d="{tile_path}" 
              fill="{color2}" 
              stroke="{style['stroke']}" 
              stroke-width="{style['stroke_width']}" />
      </g>''')
    
    return '\n'.join(tiles)

def process_tessellation_request(config: TessellationConfig) -> str:
    """
    Orchestrates the tessellation pattern generation and returns a
    client-side-ready JSON string.
    
    This is the "TessellationProcessor" layer.
    """
    print(f"Processing tessellation request for engine: {config.engine_type}")
    
    # 1. Call the "math engine" to get the raw components
    svg_components = generate_tessellation_components(config)
    
    # 2. Call the "presentation" function to build the SVG string with seamless tiling
    final_svg_string = build_tessellation_pattern_svg(svg_components)
    
    # 3. Create the client-side-ready response object
    response_data = TessellationResponse(
        svg_string=final_svg_string,
        config=config
    )
    
    # 4. Return as a JSON string
    print("Successfully generated tessellation pattern SVG. Returning JSON payload.")
    return response_data.model_dump_json(indent=2)
