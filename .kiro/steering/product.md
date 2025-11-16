---
inclusion: always
---

# Tashreef: AI-Powered Geometric Pattern Generation

## Product Purpose

Tashreef generates e-invitation cards with intricate mathematical patterns inspired by ancient architectural designs (mosques, churches, palaces). The system uses **mathematical equations**, not image generation AI, to create precise SVG-based geometric patterns.

## Core Architecture

**AI + Math Hybrid Approach**: LLM generates mathematical parameters → Mathematical engines compute patterns → SVG output

### Pattern Generation Engines

1. **Parametric Equations** - Spirograph-style curves
2. **L-Systems (Fractal)** - Recursive fractal patterns using turtle graphics
3. **Tessellations** - Islamic geometric tiling patterns

## Generation Pipeline

1. User submits natural language prompt for e-invitation design
2. Gemini 2.0 Flash LLM interprets prompt → outputs JSON configuration with mathematical parameters
3. Appropriate engine generates base pattern SVG from configuration
4. Pattern processor creates repeating/tiled backgrounds
5. Final SVG card rendered with pattern background + placeholder content

## Key Constraints

- Output format is always SVG (vector graphics)
- Patterns are mathematically generated, not AI-image-generated
- Client-side customization: dimensions, colors, text content
- No raster images - pure geometric computation
