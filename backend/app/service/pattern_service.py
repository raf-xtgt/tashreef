from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from app.inference.inference_service import InferenceService
from app.engine.fractal_engine.models import *
from app.engine.fractal_engine.processor import (process_fractal_request)
import json

service = InferenceService()
class PatternService:
    async def generate_pattern(self, user_prompt:str ,  db: AsyncSession) :

        ai_config = await service._generate_structured_content(user_prompt, LSystemConfig)
        if ai_config and isinstance(ai_config, LSystemConfig):
            print("\nSuccessfully parsed AI config.")
            
            # 6. Pass the config to the FractalProcessor
            client_ready_json = process_fractal_request(ai_config)
            
            # 7. Print the result (in a real app, you'd return this)
            print("\n--- Client-Ready JSON Output ---")
            print(client_ready_json)
            print("--------------------------------")
            
            # --- TEMPORARY CODE TO SAVE SVG ---
            # This parses the JSON string back into a dict to get the SVG
            svg_data = json.loads(client_ready_json)
            output_filename = "sample_patterns/temp_fractal_output.svg"
            with open(output_filename, "w") as f:
                f.write(svg_data['svg_string'])
            print(f"\n✅  Temporarily saved SVG to: {output_filename}")
            # --- END TEMPORARY CODE ---
            
        elif ai_config:
            print(f"\nAI returned an unexpected object type: {type(ai_config)}")
        else:
            print("\nFailed to generate or parse AI config.")

        return ""

