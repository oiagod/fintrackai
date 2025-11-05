from fastapi import FastAPI
from app.api.routes import transactions

app = FastAPI(title="Fintrack AI API")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(transactions.router)