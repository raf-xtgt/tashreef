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

    async def generate_content_config(self, user_prompt: str):
        """
        Generates content configuration for e-invitation card based on user prompt.
        
        Args:
            user_prompt: The user's natural language request for the invitation
            
        Returns:
            ContentConfig object with event content and color scheme, or default fallback on error
        """
        from app.engine.fractal_engine.models import ContentConfig, ColorScheme
        from app.engine.fractal_engine.prompts import CONTENT_SYSTEM_PROMPT
        
        print(f"Generating content config for prompt: {user_prompt}")
        
        # Build the specialized prompt combining system prompt and user prompt
        full_prompt = f"{CONTENT_SYSTEM_PROMPT}\n\n---\nUSER PROMPT:\n{user_prompt}"
        
        try:
            # Use existing _generate_structured_content with ContentConfig schema
            content_config = await self._generate_structured_content(full_prompt, ContentConfig)
            
            if content_config:
                print("Successfully generated content config")
                return content_config
            else:
                print("AI returned None, using default content config")
                return self._get_default_content_config()
                
        except Exception as e:
            print(f"Error in generate_content_config: {e}")
            print("Falling back to default content config")
            return self._get_default_content_config()
    
    def _get_default_content_config(self):
        """Returns a default ContentConfig when AI inference fails."""
        from app.engine.fractal_engine.models import ContentConfig, ColorScheme
        
        return ContentConfig(
            event_title="Your Event Here",
            event_subtitle="Join us for a celebration",
            date_placeholder="Date to be announced",
            time_placeholder="Time to be announced",
            venue_placeholder="Venue to be announced",
            rsvp_text="Please RSVP",
            color_scheme=ColorScheme(
                primary_text_color="#FFFFFF",
                secondary_text_color="#F0F0F0",
                overlay_color="#000000",
                overlay_opacity=0.4
            )
        )
