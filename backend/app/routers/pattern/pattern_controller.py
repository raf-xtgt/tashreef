from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from app.config.db_config import get_db
from app.service.pattern_service import PatternService
from app.model.prompt import TashreefPrompt

router = APIRouter(
    prefix="/pattern",  
    tags=["Pattern"]    
)
pattern_service = PatternService()

@router.post("/generate")
async def create_session(
    payload: TashreefPrompt,
    dbConn: AsyncSession = Depends(get_db)
):
    """
    Create a new session.
    """
    user_prompt = payload.text
    await pattern_service.generate_pattern(user_prompt, dbConn)
    print("generate session")

