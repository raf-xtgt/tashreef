from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import json
from app.config.db_config import get_db
from app.service.pattern_service import PatternService
from app.model.api_dto import TashreefPrompt

router = APIRouter(
    prefix="/pattern",  
    tags=["Pattern"]    
)
pattern_service = PatternService()

@router.post("/generate")
async def generate_draft_card(
    payload: TashreefPrompt,
    dbConn: AsyncSession = Depends(get_db)
):
    """
    Generate a complete draft e-invitation card with AI-powered geometric pattern and content.
    
    This endpoint orchestrates the full card generation process:
    1. Uses AI to generate mathematical parameters for a geometric pattern
    2. Generates the pattern SVG using L-System fractal algorithms
    3. Uses AI to generate contextually appropriate invitation content and color scheme
    4. Composes the final card SVG with pattern background and text overlay
    
    Args:
        payload: TashreefPrompt containing the user's text description of the desired card
        dbConn: Database session (injected dependency)
    
    Returns:
        CardResponse JSON containing:
        - card_svg: Complete SVG string for the final e-invitation card
        - pattern_config: L-System configuration used to generate the pattern
        - content_config: AI-generated content (titles, dates, venue) and color scheme
    
    Example Response:
        {
            "card_svg": "<svg width='1080' height='1920'>...</svg>",
            "pattern_config": {
                "engine_type": "l_system",
                "parameters": {...},
                "style": {...}
            },
            "content_config": {
                "event_title": "You're Invited",
                "event_subtitle": "Join us for a celebration",
                "date_placeholder": "Saturday, December 25th, 2025",
                "time_placeholder": "6:00 PM onwards",
                "venue_placeholder": "The Grand Ballroom",
                "rsvp_text": "RSVP by December 15th",
                "color_scheme": {
                    "primary_text_color": "#FFFFFF",
                    "secondary_text_color": "#F0F0F0",
                    "overlay_color": "#000000",
                    "overlay_opacity": 0.4
                }
            }
        }
    """
    user_prompt = payload.text
    card_response = await pattern_service.generate_pattern(user_prompt, dbConn)
    card_response_json = card_response.model_dump_json(indent=2)
    # Parse and return as JSON response
    if card_response_json:
        return JSONResponse(content=json.loads(card_response_json))
    else:
        return JSONResponse(
            content={"error": "Failed to generate card"},
            status_code=500
        )

