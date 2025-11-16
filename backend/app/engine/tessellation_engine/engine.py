"""Tessellation engine for generating geometric tiling patterns."""
import math
from typing import List, Tuple, Dict, Any
from .models import TessellationConfig, TessellationParams

def generate_square_tile(params: TessellationParams) -> str:
    """
    Generate SVG path data for a square tile.
    Returns path data for a square centered at origin.
    """
    size = params.tile_size
    half = size / 2
    
    # Square vertices (centered at origin)
    path = f"M {-half} {-half} L {half} {-half} L {half} {half} L {-half} {half} Z"
    return path

def generate_hexagon_tile(params: TessellationParams) -> str:
    """
    Generate SVG path data for a regular hexagon tile.
    Returns path data for a hexagon centered at origin.
    """
    size = params.tile_size
    radius = size / 2
    
    # Regular hexagon vertices (flat-top orientation)
    points = []
    for i in range(6):
        angle = (math.pi / 3) * i  # 60 degrees between vertices
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append((x, y))
    
    # Build path
    path = f"M {points[0][0]} {points[0][1]} "
    for x, y in points[1:]:
        path += f"L {x} {y} "
    path += "Z"
    
    return path

def generate_triangle_tile(params: TessellationParams) -> str:
    """
    Generate SVG path data for an equilateral triangle tile.
    Returns path data for a triangle centered at origin.
    """
    size = params.tile_size
    height = size * math.sqrt(3) / 2
    
    # Equilateral triangle vertices (pointing up, centered)
    points = [
        (0, -height * 2/3),           # Top vertex
        (-size/2, height * 1/3),      # Bottom left
        (size/2, height * 1/3)        # Bottom right
    ]
    
    path = f"M {points[0][0]} {points[0][1]} "
    for x, y in points[1:]:
        path += f"L {x} {y} "
    path += "Z"
    
    return path

def generate_diamond_tile(params: TessellationParams) -> str:
    """
    Generate SVG path data for a diamond (rhombus) tile.
    Returns path data for a diamond centered at origin.
    """
    size = params.tile_size
    half = size / 2
    
    # Diamond vertices (rotated square)
    points = [
        (0, -half),      # Top
        (half, 0),       # Right
        (0, half),       # Bottom
        (-half, 0)       # Left
    ]
    
    path = f"M {points[0][0]} {points[0][1]} "
    for x, y in points[1:]:
        path += f"L {x} {y} "
    path += "Z"
    
    return path

def apply_rotation(path: str, rotation_degrees: float) -> str:
    """
    Apply rotation transform to a path.
    Returns the path with rotation applied via transform attribute.
    """
    if rotation_degrees == 0:
        return path
    return path  # Rotation will be applied at the group level in processor

def generate_tessellation_components(config: TessellationConfig) -> Dict[str, Any]:
    """
    Generates tessellation pattern components using geometric tiling.
    Returns tile path, tile size, style, and viewBox.
    
    This is a pure "math engine" component.
    """
    print(f"Generating tessellation components with tile shape: {config.parameters.tile_shape}")
    
    params = config.parameters
    style = config.style
    
    # Generate tile geometry based on shape
    if params.tile_shape == "square":
        tile_path = generate_square_tile(params)
    elif params.tile_shape == "hexagon":
        tile_path = generate_hexagon_tile(params)
    elif params.tile_shape == "triangle":
        tile_path = generate_triangle_tile(params)
    elif params.tile_shape == "diamond":
        tile_path = generate_diamond_tile(params)
    else:
        # Default to square
        tile_path = generate_square_tile(params)
    
    print("Tessellation components generated.")
    return {
        "tile_path": tile_path,
        "tile_shape": params.tile_shape,
        "tile_size": params.tile_size,
        "rotation": params.rotation,
        "spacing": params.spacing,
        "color_palette": params.color_palette,
        "style": {
            "fill": style.fill,
            "stroke": style.stroke,
            "stroke_width": style.stroke_width
        },
        "viewBox": "0 0 1000 1000"
    }
