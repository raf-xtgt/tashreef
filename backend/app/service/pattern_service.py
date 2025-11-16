from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from app.inference.inference_service import InferenceService
from app.inference.engine_router import classify_engine
from app.prompt.prompt_builder import build_engine_prompt
from app.model.prompt import EngineTypeEnum
from app.engine.fractal_engine.models import *
from app.engine.fractal_engine.processor import process_fractal_request
from app.engine.parametric_engine.models import ParametricConfig
from app.engine.parametric_engine.processor import process_parametric_request
from app.engine.tessellation_engine.models import TessellationConfig
from app.engine.tessellation_engine.processor import process_tessellation_request
from app.engine.fractal_engine.card_generator import generate_card
import json
from app.prompt.system_prompt import SYSTEM_PROMPT

service = InferenceService()
class PatternService:
    async def generate_pattern(self, user_prompt:str ,  db: AsyncSession) -> CardResponse:
        try:
            # Step 1: Classify engine type using router
            try:
                engine_type = await classify_engine(user_prompt)
                print(f"🎯 Selected engine: {engine_type}")
            except Exception as e:
                print(f"⚠️  Router classification failed: {str(e)}")
                print(f"⚠️  Defaulting to l_system engine")
                engine_type = EngineTypeEnum.l_system
            
            # Step 2: Build engine-specific prompt
            full_prompt = build_engine_prompt(engine_type, user_prompt)
            
            # Step 3: Select appropriate config model and processor based on engine type
            if engine_type == EngineTypeEnum.l_system:
                config_model = LSystemConfig
                processor_func = process_fractal_request
            elif engine_type == EngineTypeEnum.parametric:
                config_model = ParametricConfig
                processor_func = process_parametric_request
            elif engine_type == EngineTypeEnum.tessellation:
                config_model = TessellationConfig
                processor_func = process_tessellation_request
            else:
                # Default to l_system if unknown engine type
                config_model = LSystemConfig
                processor_func = process_fractal_request
            
            print(f"📋 Using config model: {config_model.__name__}")

            # Step 4: Generate pattern config via AI
            
            ai_config = await service._generate_structured_content(full_prompt, config_model)
            if not ai_config:
                print("\n❌ Failed to generate AI config.")
                raise ValueError("AI failed to generate valid configuration")
                
            print("\n✅ Successfully parsed AI config.")
           
            # Step 5: Process pattern using selected processor function
            try:
                client_ready_json = processor_func(ai_config)
                
                # Step 6: Extract pattern SVG from processor response
                pattern_data = json.loads(client_ready_json)
                pattern_svg = pattern_data['svg_string']
            except Exception as e:
                print(f"❌ Pattern generation failed for engine '{engine_type}': {str(e)}")
                print(f"   Config: {ai_config.model_dump_json(indent=2) if ai_config else 'None'}")
                raise ValueError(f"Failed to generate pattern with {engine_type} engine: {str(e)}")
            
            # Step 7: Generate complete card with content overlay (existing logic)
            try:
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
                
                # Return CardResponse (maintains backward compatibility)
                return card_response
            except Exception as e:
                print(f"❌ Card generation failed: {str(e)}")
                raise ValueError(f"Failed to generate complete card: {str(e)}")
                
        except Exception as e:
            print(f"\n❌ Pattern generation failed: {str(e)}")
            # Return error response without falling back to different engine
            raise

