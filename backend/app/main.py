from fastapi import FastAPI
from app.api.routes import transactions, auth
from app.db.session import engine, Base

import app.db.models.user
import app.db.models.transaction

app = FastAPI(title="Fintrack AI API")

app.include_router(auth.router)
app.include_router(transactions.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
def health():
    return {"status": "ok"}
