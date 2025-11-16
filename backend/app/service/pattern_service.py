from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from app.inference.inference_service import InferenceService
from app.engine.fractal_engine.models import *
from app.engine.fractal_engine.processor import (process_fractal_request)
from app.engine.fractal_engine.card_generator import generate_card
import json
from app.prompt.system_prompt import SYSTEM_PROMPT

service = InferenceService()
class PatternService:
    async def generate_pattern(self, user_prompt:str ,  db: AsyncSession) -> CardResponse:
        full_prompt = f"{SYSTEM_PROMPT}\n\n---\nUSER PROMPT:\n{user_prompt}"

        ai_config = await service._generate_structured_content(full_prompt, LSystemConfig)
        if ai_config and isinstance(ai_config, LSystemConfig):
            print("\nSuccessfully parsed AI config.")
            
            # Pass the config to the FractalProcessor to generate pattern SVG
            client_ready_json = process_fractal_request(ai_config)
            
            # Parse the JSON to extract the pattern SVG
            pattern_data = json.loads(client_ready_json)
            pattern_svg = pattern_data['svg_string']
            
            # Generate complete card with content overlay
            print("\n--- Generating Complete Card ---")
            card_response = await generate_card(
                pattern_svg=pattern_svg,
                user_prompt=user_prompt,
                pattern_config=ai_config,
                inference_service=service
            )
            
            # Save the final card SVG
            output_filename = "sample_patterns/temp_card_output.svg"
            with open(output_filename, "w") as f:
                f.write(card_response.card_svg)
            print(f"\n✅  Saved final card SVG to: {output_filename}")
            
            # Return CardResponse
            return card_response
            
        elif ai_config:
            print(f"\nAI returned an unexpected object type: {type(ai_config)}")
        else:
            print("\nFailed to generate or parse AI config.")

        return ""

