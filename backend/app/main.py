from fastapi import FastAPI

app = FastAPI(title="Fintrack AI API")

@app.get("/health")
def health():
    """
    Endpoint de verificação do sistema.
    Retorna um JSON simples para indicar que API está online
    """
    return {"status": "ok"}