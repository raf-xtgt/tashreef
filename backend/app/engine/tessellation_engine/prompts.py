"""
Tessellation Engine Prompt Template

This prompt guides the LLM to generate tessellation pattern configurations
based on user descriptions.
"""

TESSELLATION_PROMPT = """
---
ENGINE: "tessellation"
---
This engine generates tiled, mosaic-like patterns using geometric shapes. 
It creates architectural, Islamic-inspired, and structured designs.

- Use this engine if the user asks for: "tessellation", "tiled", "mosaic", 
  "geometric", "architectural", "Islamic", "honeycomb", "grid"

**Parameters:**
- `tile_shape`: The shape of the repeating tile
  - "square": Simple grid pattern
  - "hexagon": Honeycomb pattern
  - "triangle": Angular, dynamic pattern
  - "diamond": Rotated squares

- `tile_size`: Size of each tile in pixels (50-200)
- `rotation`: Rotation angle in degrees (0-360)
- `spacing`: Gap between tiles in pixels (0-10)
- `color_palette`: Array of 2-5 hex colors for alternating tiles

- `style`: Set the `fill` and `stroke` colors. For tessellations, 
  `fill` is usually a color, and `stroke` is often white or black.

---
EXAMPLES of TESSELLATION PATTERNS
---

1. **Islamic Geometric (Hexagons):**
   * `tile_shape`: "hexagon"
   * `tile_size`: 100
   * `rotation`: 0
   * `spacing`: 2
   * `color_palette`: ["#4682B4", "#87CEEB", "#B0E0E6"]

2. **Modern Grid (Squares):**
   * `tile_shape`: "square"
   * `tile_size`: 80
   * `rotation`: 0
   * `spacing`: 5
   * `color_palette`: ["#FF6B6B", "#4ECDC4"]

3. **Dynamic Diamonds:**
   * `tile_shape`: "diamond"
   * `tile_size`: 120
   * `rotation`: 45
   * `spacing`: 0
   * `color_palette`: ["#FFD700", "#FFA500", "#FF8C00"]

4. **Angular Triangles:**
   * `tile_shape`: "triangle"
   * `tile_size`: 90
   * `rotation`: 30
   * `spacing`: 1
   * `color_palette`: ["#9B59B6", "#8E44AD"]

---
YOUR TASK
---
Read the user's prompt. Select appropriate tile shape, size, and colors that 
match their creative description. Ensure the color palette complements the 
event type.

Respond ONLY with the JSON object. Do not include any other text, markdown, 
or conversation.
"""
