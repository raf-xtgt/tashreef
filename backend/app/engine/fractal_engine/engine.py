import math
from .models import LSystemConfig
from typing import Dict, Any

def apply_l_system_rules(axiom: str, rules: dict, iterations: int) -> str:
    """Recursively applies the L-System rules to the axiom."""
    result = axiom
    for _ in range(iterations):
        new_result = ""
        for char in result:
            new_result += rules.get(char, char)
        result = new_result
    return result

def generate_l_system_components(config: LSystemConfig) -> Dict[str, Any]:
    """
    Generates L-System components (path data, style, viewbox) 
    using a turtle graphics system.
    
    This function is a pure "math engine" component.
    """
    print(f"Generating L-System components...")
    
    # 1. Get parameters from the config
    params = config.parameters
    style = config.style
    
    # 2. Generate the final L-System string
    l_string = apply_l_system_rules(params.axiom, params.rules, params.iterations)
    
    # 3. Set up the canvas dimensions (for the viewbox)
    canvas_width = 1000
    canvas_height = 1000
    
    # 4. Turtle graphics implementation
    stack = []
    current_x = params.start_x
    current_y = params.start_y
    current_angle_deg = params.start_angle
    
    # Adjust line length heuristic
    line_length = params.line_length / (1.2**params.iterations)

    # We will build a single, highly efficient <path> element
    path_data = f"M {current_x} {current_y} "
    
    for char in l_string:
        if char in ('F', 'G'):
            rad = math.radians(current_angle_deg)
            next_x = current_x + line_length * math.cos(rad)
            next_y = current_y + line_length * math.sin(rad)
            path_data += f"L {next_x} {next_y} "
            current_x = next_x
            current_y = next_y
            
        elif char == '+':
            current_angle_deg -= params.angle
            
        elif char == '-':
            current_angle_deg += params.angle
            
        elif char == '[':
            stack.append((current_x, current_y, current_angle_deg))
            
        elif char == ']':
            if stack:
                pop_x, pop_y, pop_angle = stack.pop()
                current_x = pop_x
                current_y = pop_y
                current_angle_deg = pop_angle
                path_data += f"M {current_x} {current_y} "

    # 5. Return the raw components
    print("L-System components generated.")
    return {
        "path_data": path_data,
        "style": {
            "fill": style.fill,
            "stroke": style.stroke,
            "stroke_width": style.stroke_width
        },
        "viewBox": f"0 0 {canvas_width} {canvas_height}"
    }