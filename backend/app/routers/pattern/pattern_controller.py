from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from app.config.db_config import get_db



router = APIRouter(
    prefix="/pattern",  
    tags=["Pattern"]    
)


@router.get("/generate")
async def create_session(
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new session.
    """
    print("generate session")

