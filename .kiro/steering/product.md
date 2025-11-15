# Product Overview

Tashreef is an AI-powered geometric pattern generation engine for creating e-invitation cards with intricate mathematical designs inspired by ancient architectural patterns found in mosques, churches, and palaces.

## Core Concept

Unlike traditional AI image generation that iterates on training data, Tashreef uses mathematical equations and geometric concepts to generate patterns. The system bridges AI reasoning with mathematical engines to create SVG-based patterns.

## Key Features

- AI-powered pattern generation using mathematical equations (not image generation)
- Three pattern generation engines: Parametric Equations (Spirograph), L-Systems (Fractal), and Tessellations (Islamic Pattern)
- Client-side customizable SVG outputs with dynamic dimensions and color schemes
- E-invitation card generation with placeholder content

## User Flow

1. User provides a prompt describing their desired e-invitation card
2. LLM (Gemini 2.0 Flash) generates a pattern configuration JSON with mathematical parameters
3. Mathematical engine generates the pattern SVG using the configuration
4. Pattern processor creates repeating background patterns
5. Final SVG is rendered as a draft e-invitation card ready for user customization
