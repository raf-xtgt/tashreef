from .inference_service import *
from vertexai.generative_models import GenerativeModel, GenerationConfig
from pydantic import BaseModel
import json

class InferenceService:
    def __init__(self):
        self.generative_model = GenerativeModel(
             "gemini-2.0-flash", 
        )

    async def _generate_structured_content(self, prompt: str, response_model: BaseModel):
        """Calls the LLM with a prompt and a JSON schema, returns a Pydantic object."""
        print("Generating structured content...")
        response = None
        try:
            
            response = await self.generative_model.generate_content_async(
                prompt,
                generation_config=GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=response_model.model_json_schema()
                )
            )
            
            response_text = response.text
            print("--- AI JSON Response ---")
            print(response_text)
            print("------------------------")
            
            return response_model.model_validate_json(response_text)
        
        except Exception as e:
            print(f"Error generating structured content: {e}")
            if response and hasattr(response, 'prompt_feedback'):
                 print(f"Prompt Feedback: {response.prompt_feedback}")
            if response and hasattr(response, 'candidates') and response.candidates:
                 print(f"Finish Reason: {response.candidates[0].finish_reason}")
                 print(f"Safety Ratings: {response.candidates[0].safety_ratings}")
            return None
