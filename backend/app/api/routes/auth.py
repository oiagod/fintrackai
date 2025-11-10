from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
async def signup(name: str, email: str, password: str, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.signup(name, email, password)

@router.post("/login")
async def login(email: str, password: str, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.login(email, password)

@router.post("/token")
async def login_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    try:
        return await service.login(form_data.username, form_data.password)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")