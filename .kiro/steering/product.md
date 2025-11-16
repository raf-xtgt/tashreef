---
inclusion: always
---

# Tashreef Product Context

## What This Application Does

Tashreef generates e-invitation cards with mathematical patterns inspired by ancient architectural designs. The system uses **mathematical computation**, not generative AI images, to create precise SVG geometric patterns.

## Core Approach: AI + Math Hybrid

LLM (Gemini 2.0 Flash) → JSON parameters → Mathematical engine → SVG pattern

## Pattern Engines Available

1. **Parametric Equations** - Spirograph-style curves
2. **L-Systems (Fractal)** - Recursive patterns via turtle graphics
3. **Tessellations** - Islamic geometric tiling

## Generation Flow

1. User provides natural language prompt describing desired e-invitation design
2. LLM interprets prompt and outputs JSON with mathematical parameters
3. Engine generates base pattern SVG from parameters
4. Processor creates tiled/repeating backgrounds
5. Final SVG card combines pattern background with content placeholders

## Critical Constraints

- **Output is always SVG** - vector graphics only, no raster images
- **Patterns are mathematically generated** - engines use equations, not AI image generation
- **Customization happens client-side** - dimensions, colors, text content
- **No external image assets** - pure geometric computation
