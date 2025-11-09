from fastapi import FastAPI
from app.api.routes import transactions, auth
from app.db.session import engine, Base

app = FastAPI(title="Fintrack AI API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router)
app.include_router(transactions.router)

@app.get("/health")
def health():
    return {"status": "ok"}
