"""Parametric equation engine for generating spirograph-like patterns."""
import math
from typing import List, Tuple, Dict, Any
from .models import ParametricConfig, ParametricParams

def generate_rose_curve(params: ParametricParams) -> List[Tuple[float, float]]:
    """
    Generate points for a rose curve pattern.
    Formula: r = a * cos(k * θ)
    where x = r * cos(θ), y = r * sin(θ)
    """
    points = []
    a = params.amplitude_a
    k = params.frequency_a / params.frequency_b if params.frequency_b != 0 else params.frequency_a
    
    # Generate points over full rotation(s)
    for i in range(params.num_points):
        theta = (2 * math.pi * i) / params.num_points
        r = a * math.cos(k * theta)
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        points.append((x, y))
    
    return points

def generate_lissajous_curve(params: ParametricParams) -> List[Tuple[float, float]]:
    """
    Generate points for a Lissajous curve pattern.
    Formula: x = A * sin(a*t + δ), y = B * sin(b*t)
    """
    points = []
    A = params.amplitude_a
    B = params.amplitude_b
    a = params.frequency_a
    b = params.frequency_b
    delta = params.phase_shift
    
    # Generate points over full period
    for i in range(params.num_points):
        t = (2 * math.pi * i) / params.num_points
        x = A * math.sin(a * t + delta)
        y = B * math.sin(b * t)
        points.append((x, y))
    
    return points

def generate_epitrochoid_curve(params: ParametricParams) -> List[Tuple[float, float]]:
    """
    Generate points for an epitrochoid pattern (spirograph with circle rolling outside).
    Formula:
    x = (R + r) * cos(t) - d * cos((R + r) * t / r)
    y = (R + r) * sin(t) - d * sin((R + r) * t / r)
    
    Using amplitude_a as R, frequency_a/frequency_b ratio to derive r, 
    and amplitude_b as d for tracing distance.
    """
    points = []
    R = params.amplitude_a
    r = R / params.frequency_a if params.frequency_a != 0 else R / 5
    d = params.amplitude_b * 0.7  # Distance from center of rolling circle
    
    # Generate points over multiple rotations
    num_rotations = int(params.frequency_a) + 1
    for i in range(params.num_points):
        t = (2 * math.pi * num_rotations * i) / params.num_points
        x = (R + r) * math.cos(t) - d * math.cos((R + r) * t / r)
        y = (R + r) * math.sin(t) - d * math.sin((R + r) * t / r)
        points.append((x, y))
    
    return points

def generate_hypotrochoid_curve(params: ParametricParams) -> List[Tuple[float, float]]:
    """
    Generate points for a hypotrochoid pattern (spirograph with circle rolling inside).
    Formula:
    x = (R - r) * cos(t) + d * cos((R - r) * t / r)
    y = (R - r) * sin(t) - d * sin((R - r) * t / r)
    
    Using amplitude_a as R, frequency_a/frequency_b ratio to derive r,
    and amplitude_b as d for tracing distance.
    """
    points = []
    R = params.amplitude_a
    r = R / params.frequency_a if params.frequency_a != 0 else R / 5
    d = params.amplitude_b * 0.7  # Distance from center of rolling circle
    
    # Generate points over multiple rotations
    num_rotations = int(params.frequency_a) + 1
    for i in range(params.num_points):
        t = (2 * math.pi * num_rotations * i) / params.num_points
        x = (R - r) * math.cos(t) + d * math.cos((R - r) * t / r)
        y = (R - r) * math.sin(t) - d * math.sin((R - r) * t / r)
        points.append((x, y))
    
    return points

def points_to_path(points: List[Tuple[float, float]], center_x: float = 500, center_y: float = 500) -> str:
    """
    Convert a list of (x, y) points to SVG path data.
    Centers the pattern at (center_x, center_y).
    """
    if not points:
        return ""
    
    # Start path at first point (centered)
    path_data = f"M {points[0][0] + center_x} {points[0][1] + center_y} "
    
    # Add line segments to all other points
    for x, y in points[1:]:
        path_data += f"L {x + center_x} {y + center_y} "
    
    # Close the path
    path_data += "Z"
    
    return path_data

def generate_parametric_components(config: ParametricConfig) -> Dict[str, Any]:
    """
    Generates parametric curve components using mathematical equations.
    Returns path_data, style, and viewBox.
    
    This is a pure "math engine" component.
    """
    print(f"Generating parametric components with equation type: {config.parameters.equation_type}")
    
    params = config.parameters
    style = config.style
    
    # Generate points based on equation type
    if params.equation_type == "rose":
        points = generate_rose_curve(params)
    elif params.equation_type == "lissajous":
        points = generate_lissajous_curve(params)
    elif params.equation_type == "epitrochoid":
        points = generate_epitrochoid_curve(params)
    elif params.equation_type == "hypotrochoid":
        points = generate_hypotrochoid_curve(params)
    else:
        # Default to rose curve
        points = generate_rose_curve(params)
    
    # Convert points to SVG path data
    path_data = points_to_path(points)
    
    print("Parametric components generated.")
    return {
        "path_data": path_data,
        "style": {
            "fill": style.fill,
            "stroke": style.stroke,
            "stroke_width": style.stroke_width
        },
        "viewBox": "0 0 1000 1000"
    }
