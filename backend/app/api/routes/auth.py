from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
async def signup(name: str, email: str, password: str, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.signup(name, email, password)

@router.post("/login")
async def login(email: str, password: str, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.login(email, password)