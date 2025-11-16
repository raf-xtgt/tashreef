"""Parametric engine prompt template for LLM."""

PARAMETRIC_PROMPT = """
---
ENGINE: "parametric"
---
This engine generates hypnotic, circular, and spirograph-like patterns using 
parametric equations. It creates flowing curves and complex geometric designs.

- Use this engine if the user asks for: "spirograph", "circular", "hypnotic", 
  "vortex", "cosmic", "flowing curves", "rose", "lissajous"

**Parameters:**
- `equation_type`: The type of parametric equation to use
  - "rose": Flower-like patterns with petals
  - "lissajous": Figure-8 and complex loops
  - "epitrochoid": Spirograph patterns (circle rolling outside)
  - "hypotrochoid": Star-like patterns (circle rolling inside)

- `amplitude_a`: Size/scale in x-direction (50-500)
- `amplitude_b`: Size/scale in y-direction (50-500)
- `frequency_a`: Number of cycles in x-direction (1-20)
- `frequency_b`: Number of cycles in y-direction (1-20)
- `phase_shift`: Phase offset in radians (0-6.28)
- `num_points`: Number of points to generate (500-2000)

- `style`: Set the `stroke` to a color that matches the user's request. 
  `fill` should almost always be "none".

---
EXAMPLES of PARAMETRIC PATTERNS
---

1. **Rose Curve (5 petals):**
   * `equation_type`: "rose"
   * `amplitude_a`: 200
   * `amplitude_b`: 200
   * `frequency_a`: 5
   * `frequency_b`: 1
   * `num_points`: 1000

2. **Lissajous Figure:**
   * `equation_type`: "lissajous"
   * `amplitude_a`: 300
   * `amplitude_b`: 300
   * `frequency_a`: 3
   * `frequency_b`: 2
   * `phase_shift`: 1.57
   * `num_points`: 1500

3. **Spirograph (Epitrochoid):**
   * `equation_type`: "epitrochoid"
   * `amplitude_a`: 250
   * `amplitude_b`: 250
   * `frequency_a`: 7
   * `frequency_b`: 3
   * `num_points`: 2000

4. **Star Pattern (Hypotrochoid):**
   * `equation_type`: "hypotrochoid"
   * `amplitude_a`: 200
   * `amplitude_b`: 200
   * `frequency_a`: 5
   * `frequency_b`: 2
   * `num_points`: 1000

---
YOUR TASK
---
Read the user's prompt. Select appropriate parametric equation type and parameters 
that match their creative description. Set the style to match their request.

Respond ONLY with the JSON object. Do not include any other text, markdown, 
or conversation.
"""
