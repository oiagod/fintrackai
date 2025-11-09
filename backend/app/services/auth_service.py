from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.db.models.user import UserORM
from app.core.security import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def signup(self, name: str, email: str, password: str):
        res = await self.db.execute(select(UserORM).where(UserORM.email == email))
        if res.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        user = UserORM(name=name, email=email, password_hash=hash_password(password))
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
        
    async def login(self, email: str, password: str):
        res = await self.db.execute(select(UserORM).where(UserORM.email == email))
        user = res.scalar_one_or_none()
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}


